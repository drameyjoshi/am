package clustering;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import org.jgrapht.Graph;
import org.jgrapht.graph.DefaultEdge;
import org.jgrapht.graph.SimpleGraph;
import org.jgrapht.traverse.BreadthFirstIterator;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.databind.ObjectMapper;

public class AJClusterer {

	public AJClusterer() {
		nClusters = 2;
		cleaningAreas = new HashMap<>();
	}

	public static void main(String[] args) {
		AJClusterer clusterer = new AJClusterer();
		Graph<CleaningArea, DefaultEdge> cleaningGraph = clusterer.createGraph(GRAPHS[0]);
		clusterer.cluster(cleaningGraph);

		BreadthFirstIterator<CleaningArea, DefaultEdge> bfs = new BreadthFirstIterator<>(cleaningGraph);
		while (bfs.hasNext()) {
			CleaningArea v = bfs.next();
			if (logger.isInfoEnabled()) {
				logger.info("{}", v.showClusterInfo());
			}
		}
	}

	protected void cluster(Graph<CleaningArea, DefaultEdge> graph) {
		int timePerCluster = (int) Math.round(1.1 * totalTime / nClusters);
		logger.info("Time per cluster = {}", timePerCluster);
		int clusterId = 1;
		BreadthFirstIterator<CleaningArea, DefaultEdge> bfs = new BreadthFirstIterator<>(graph);
		Map<Integer, List<CleaningArea>> clusterMap = new HashMap<>();

		logger.info("Total time = {}, time per cluster = {}, # clusters = {}", totalTime, timePerCluster, nClusters);

		List<CleaningArea> clusterList = new LinkedList<>();
		while (bfs.hasNext()) {
			CleaningArea v = bfs.next();
			if (timePerCluster > v.getTimeToClean()) {
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
			int[] currentAllocations = new int[nClusters];

			for (int cid = 1; cid <= nClusters; cid++) {
				List<CleaningArea> cleaningAreasInCluster = clusterMap.get(cid);
				int clusterAllocation = 0;
				for (CleaningArea ca : cleaningAreasInCluster) {
					clusterAllocation += ca.getTimeToClean();
				}
				currentAllocations[cid - 1] = clusterAllocation;
			}

			List<CleaningArea> lastCluster = clusterMap.get(clusterId);

			timePerCluster = (int) Math.round(1.1 * totalTime / nClusters);
			for (CleaningArea ca : lastCluster) {
				for (int i = 0; i < nClusters; i++) {
					if (ca.getTimeToClean() < timePerCluster - currentAllocations[i]) {
						ca.setClusterId(i + 1);
						currentAllocations[i] += ca.getTimeToClean();
					}
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
	private int nClusters;
	private Map<Integer, CleaningArea> cleaningAreas;
	private static final String[] GRAPHS = { "graph_3.json" };
	protected static final Logger logger = LoggerFactory.getLogger(AJClusterer.class.getName());
}
