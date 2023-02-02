package clustering;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.jgrapht.Graph;
import org.jgrapht.graph.DefaultEdge;
import org.jgrapht.graph.SimpleGraph;
import org.jgrapht.traverse.DepthFirstIterator;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.databind.ObjectMapper;

public abstract class Clusterer {

	protected Clusterer() {
		// Nothing to do here.
	}
	
	protected abstract void cluster(Graph<Integer, DefaultEdge> graph);
	
	protected abstract void cluster(Graph<Integer, DefaultEdge> graph, int nClusters);

	protected void printGraph(Graph<Integer, DefaultEdge> g) {
		Iterator<Integer> iter = new DepthFirstIterator<>(g);
		while (iter.hasNext()) {
			int v = iter.next();
			logger.info("Vertex = {}, neighbours = {}", v, g.edgesOf(v));
		}
	}
	
	protected Graph<Integer, DefaultEdge> buildGraph(final String filename) {
		ObjectMapper mapper = new ObjectMapper();
		Graph<Integer, DefaultEdge> floor = new SimpleGraph<>(DefaultEdge.class);

		try {
			@SuppressWarnings("unchecked")
			Map<String, List<Map<String, Object>>> map = mapper.readValue(Paths.get(filename).toFile(), Map.class);
			List<Map<String, Object>> cleaningAreas = map.get("cleaningAreas");
			for (Map<String, Object> m : cleaningAreas) {
				int id = (int) m.get("id");
				floor.addVertex(id);
				List<?> neighbours = (List<?>) m.get("neighbourCleaningAreaIds");
				for (Object n : neighbours) {
					floor.addVertex((int) n);
					floor.addEdge(id, (int) n);
				}
			}
		} catch (IOException e) {
			logger.error(e.getMessage());
		}
		
		return floor;
	}
	
	protected static final Logger logger = LoggerFactory.getLogger(Clusterer.class.getName());
	protected static final String[] GRAPHS = {"graph_1.json", "graph_2.json"};
}
