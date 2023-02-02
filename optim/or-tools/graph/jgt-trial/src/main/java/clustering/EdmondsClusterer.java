package clustering;

import java.util.Set;
import java.util.TreeSet;

import org.jgrapht.Graph;
import org.jgrapht.alg.interfaces.MatchingAlgorithm;
import org.jgrapht.alg.matching.DenseEdmondsMaximumCardinalityMatching;
import org.jgrapht.graph.DefaultEdge;

public class EdmondsClusterer extends Clusterer {

	public EdmondsClusterer() {
		// Nothing to be done.
	}

	public static void main(String[] args) {
		EdmondsClusterer clusterer = new EdmondsClusterer();
		for (String filename : GRAPHS) {
			logger.info("Analysing clusters in {}.", filename);
			Graph<Integer, DefaultEdge> floor = clusterer.buildGraph(filename);
			clusterer.printGraph(floor);
			clusterer.cluster(floor, 2);
		}
	}

	@Override
	protected void cluster(Graph<Integer, DefaultEdge> graph) {
		DenseEdmondsMaximumCardinalityMatching<Integer, DefaultEdge> algo = new DenseEdmondsMaximumCardinalityMatching<>(
				graph);
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
				tour1.add(graph.getEdgeSource(e));
				tour1.add(graph.getEdgeTarget(e));
			} else {
				tour2.add(graph.getEdgeSource(e));
				tour2.add(graph.getEdgeTarget(e));
			}
			flag = !flag;
		}

		logger.info("Cleaning areas in tour 1: {}", tour1);
		logger.info("Cleaning areas in tour 2: {}", tour2);
	}

	@Override
	protected void cluster(Graph<Integer, DefaultEdge> graph, int nClusters) {
		if (nClusters != 2) {
			logger.warn("Edmonds Maximal Clusterer can produce only two clusters.");
		}
		cluster(graph);
	}
}
