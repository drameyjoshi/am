package clustering;

import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.Collection;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import javax.imageio.ImageIO;

import org.jgrapht.Graph;
import org.jgrapht.ext.JGraphXAdapter;
import org.jgrapht.graph.DefaultEdge;
import org.jgrapht.graph.SimpleGraph;
import org.jgrapht.traverse.BreadthFirstIterator;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.mxgraph.layout.mxCircleLayout;
import com.mxgraph.layout.mxIGraphLayout;
import com.mxgraph.model.mxGraphModel;
import com.mxgraph.swing.mxGraphComponent;
import com.mxgraph.util.mxCellRenderer;
import com.mxgraph.util.mxConstants;
import com.mxgraph.util.mxUtils;

public class AJClusterer {

	public AJClusterer(int nClusters) {
		this.nClusters = nClusters;
		cleaningAreas = new HashMap<>();
	}

	public static void main(String[] args) {
		AJClusterer clusterer = new AJClusterer(3);
		Graph<CleaningArea, DefaultEdge> cleaningGraph = clusterer.createGraph(GRAPHS[0]);
		clusterer.cluster(cleaningGraph);

		BreadthFirstIterator<CleaningArea, DefaultEdge> bfs = new BreadthFirstIterator<>(cleaningGraph);
		while (bfs.hasNext()) {
			CleaningArea v = bfs.next();
			if (logger.isInfoEnabled()) {
				logger.info("{}", v.showClusterInfo());
			}
		}
		
		clusterer.exportImage(cleaningGraph, GRAPHS[0]);
	}

	@SuppressWarnings("deprecation")
	protected void exportImage(final Graph<CleaningArea, DefaultEdge> cleaningGraph, final String graphJSON) {
		JGraphXAdapter<CleaningArea, DefaultEdge> ga = new JGraphXAdapter<>(cleaningGraph);
		mxGraphComponent graphComponent = new mxGraphComponent(ga);
		mxGraphModel graphModel = (mxGraphModel) graphComponent.getGraph().getModel();
		Collection<Object> cells = graphModel.getCells().values();
		ga.getEdgeToCellMap().forEach((edge, cell) -> cell.setValue(null));
		mxUtils.setCellStyles(graphComponent.getGraph().getModel(),
				cells.toArray(), mxConstants.STYLE_ENDARROW, mxConstants.NONE);
		
		mxIGraphLayout layout = new mxCircleLayout(ga);		
		layout.execute(ga.getDefaultParent());

		BufferedImage image = mxCellRenderer.createBufferedImage(ga, null, 2, Color.white, true, null);
		String imgFileName = graphJSON.replace(".json", ".jpg");
		File imgFile = new File(imgFileName);

		try {
			ImageIO.write(image, "JPG", imgFile);
		} catch (IOException e) {
			logger.error(e.getMessage());
		}
	}

	protected void cluster(Graph<CleaningArea, DefaultEdge> graph) {
		int timePerCluster = (int) Math.round((1 + MARGIN) * totalTime / nClusters);
		logger.info("Time per cluster = {}", timePerCluster);
		int clusterId = 1;
		BreadthFirstIterator<CleaningArea, DefaultEdge> bfs = new BreadthFirstIterator<>(graph);
		Map<Integer, List<CleaningArea>> clusterMap = new HashMap<>();

		logger.info("Total time = {}, time per cluster = {}, # clusters = {}", totalTime, timePerCluster, nClusters);

		List<CleaningArea> clusterList = new LinkedList<>();
		while (bfs.hasNext()) {
			CleaningArea v = bfs.next();
			if (timePerCluster > v.getTimeToClean() && (clusterList.isEmpty() || v.isNeighbourOf(clusterList))) {
				timePerCluster -= v.getTimeToClean();
				v.setClusterId(clusterId);
				clusterList.add(v);
			} else {
				clusterMap.put(clusterId, clusterList);
				clusterId++;
				clusterList = new LinkedList<>();
				clusterList.add(v);
				v.setClusterId(clusterId);
			}
		}
		clusterMap.put(clusterId, clusterList);

		if (clusterId > nClusters) {
			logger.info("First pass created {} clusters when {} were needed.", clusterId, nClusters);
			rebalance(clusterMap, clusterId);
		}
	}

	private void rebalance(Map<Integer, List<CleaningArea>> clusterMap, int lastClusterId) {
		int[] currentAllocations = new int[nClusters];

		for (int cid = 1; cid <= nClusters; cid++) {
			List<CleaningArea> cleaningAreasInCluster = clusterMap.get(cid);
			int clusterAllocation = 0;
			for (CleaningArea ca : cleaningAreasInCluster) {
				clusterAllocation += ca.getTimeToClean();
			}
			currentAllocations[cid - 1] = clusterAllocation;
		}

		List<CleaningArea> lastCluster = clusterMap.get(lastClusterId);

		int timePerCluster = (int) Math.round((1 + MARGIN) * totalTime / nClusters);
		for (CleaningArea ca : lastCluster) {
			for (int i = 0; i < nClusters; i++) {
				if (ca.isNeighbourOf(clusterMap.get(i + 1))
						&& ca.getTimeToClean() < timePerCluster - currentAllocations[i]) {
					ca.setClusterId(i + 1);
					currentAllocations[i] += ca.getTimeToClean();
				}
			}
		}
	}

	private Graph<CleaningArea, DefaultEdge> createGraph(final String filename) {
		ObjectMapper mapper = new ObjectMapper();
		Graph<CleaningArea, DefaultEdge> cleaningGraph = new SimpleGraph<>(DefaultEdge.class);

		try {
			@SuppressWarnings("unchecked")
			Map<String, List<Map<String, Object>>> map = mapper.readValue(Paths.get(filename).toFile(), Map.class);
			List<Map<String, Object>> cleaningAreaList = map.get("cleaningAreas");
			for (Map<String, Object> m : cleaningAreaList) {
				CleaningArea cleaningArea = new CleaningArea();
				cleaningArea.setId((int) m.get("id"));
				cleaningArea.setFloorId((int) m.get("floorId"));
				cleaningArea.setTimeToClean((int) m.get("timeToClean"));
				cleaningArea.setName((String) m.get("name"));
				List<?> neighbours = (List<?>) m.get("neighbourCleaningAreaIds");
				int[] neighbourIds = new int[neighbours.size()];
				for (int i = 0; i < neighbours.size(); i++) {
					neighbourIds[i] = (int) neighbours.get(i);
				}
				cleaningArea.setNeighbours(neighbourIds);

				cleaningAreas.put(cleaningArea.getId(), cleaningArea);
				totalTime += cleaningArea.getTimeToClean();
			}
		} catch (IOException e) {
			logger.error(e.getMessage());
		}

		for (Entry<Integer, CleaningArea> entry : cleaningAreas.entrySet()) {
			CleaningArea v = entry.getValue();
			cleaningGraph.addVertex(v);
			for (int nid : v.getNeighbours()) {
				CleaningArea n = cleaningAreas.get(nid);
				cleaningGraph.addVertex(n);
				cleaningGraph.addEdge(v, n);
			}
		}

		return cleaningGraph;
	}

	private int totalTime;
	private final int nClusters;
	private final Map<Integer, CleaningArea> cleaningAreas;
	private static final String[] GRAPHS = { "graph_3.json" };
	protected static final Logger logger = LoggerFactory.getLogger(AJClusterer.class.getName());
	private static final double MARGIN = 0.1; // 10%
}
