package clustering;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

import org.jgrapht.Graph;
import org.jgrapht.alg.interfaces.MatchingAlgorithm;
import org.jgrapht.alg.matching.DenseEdmondsMaximumCardinalityMatching;
import org.jgrapht.graph.DefaultEdge;
import org.jgrapht.graph.SimpleGraph;
import org.jgrapht.traverse.DepthFirstIterator;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.databind.ObjectMapper;

public class Clusterer {

	public Clusterer() {
		// Nothing to be done.
	}

	public static void main(String[] args) {
		ObjectMapper mapper = new ObjectMapper();
		Graph<Integer, DefaultEdge> floor = new SimpleGraph<>(DefaultEdge.class);

		try {
			@SuppressWarnings("unchecked")
			Map<String, List<Map<String, Object>>> map = mapper.readValue(Paths.get(GRAPH_FILE).toFile(), Map.class);
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

		printGraph(floor);
		DenseEdmondsMaximumCardinalityMatching<Integer, DefaultEdge> algo = new DenseEdmondsMaximumCardinalityMatching<>(
				floor);
		MatchingAlgorithm.Matching<Integer, DefaultEdge> matching = algo.getMatching();
		Set<Integer> tour1 = new TreeSet<>();
		Set<Integer> tour2 = new TreeSet<>();

		if (matching.isPerfect()) {
			logger.info("Found a perfect matching");
		} else {
			logger.info("Could not find a perfect matching.");
		}
		int mSize = matching.getEdges().size();
		logger.info("There are {} edges in the matching.", mSize);
		boolean flag = true;
		for (DefaultEdge e : matching.getEdges()) {
			if (flag) {
				tour1.add(floor.getEdgeSource(e));
				tour1.add(floor.getEdgeTarget(e));
			} else {
				tour2.add(floor.getEdgeSource(e));
				tour2.add(floor.getEdgeTarget(e));
			}
			flag = !flag;
		}

		logger.info("Cleaning areas in tour 1: {}", tour1);
		logger.info("Cleaning areas in tour 2: {}", tour2);
	}

	private static void printGraph(Graph<Integer, DefaultEdge> g) {
		Iterator<Integer> iter = new DepthFirstIterator<>(g);
		while (iter.hasNext()) {
			int v = iter.next();
			logger.info("Vertex = {}, neighbours = {}", v, g.edgesOf(v));
		}
	}

	private static final String GRAPH_FILE = "graph_2.json";
	private static final Logger logger = LoggerFactory.getLogger(Clusterer.class.getName());
}
