package clustering;

import java.util.List;
import java.util.Set;

import org.jgrapht.Graph;
import org.jgrapht.alg.clustering.GirvanNewmanClustering;
import org.jgrapht.alg.interfaces.ClusteringAlgorithm;
import org.jgrapht.graph.DefaultEdge;

public class GMClusterer extends Clusterer {

	public GMClusterer() {
		// Nothing to do here.
	}

	public static void main(String[] args) {
		GMClusterer clusterer = new GMClusterer();
		for (String filename : GRAPHS) {
			logger.info("Analysing clusters in {}.", filename);
			Graph<Integer, DefaultEdge> floor = clusterer.buildGraph(filename);
			clusterer.printGraph(floor);
			clusterer.cluster(floor, 3);
		}
	}

	@Override
	protected void cluster(Graph<Integer, DefaultEdge> graph) {
		cluster(graph, NUM_CLUSTERS);
	}

	@Override
	protected void cluster(Graph<Integer, DefaultEdge> graph, int nClusters) {
		GirvanNewmanClustering<Integer, DefaultEdge> algo = new GirvanNewmanClustering<>(graph, nClusters);
		ClusteringAlgorithm.Clustering<Integer> clusters = algo.getClustering();

		logger.info("The {} clusters are:", clusters.getNumberClusters());
		List<Set<Integer>> clusterSets = clusters.getClusters();

		int n = 1;
		for (Set<Integer> set : clusterSets) {
			StringBuilder sb = new StringBuilder();
			sb.append("[");
			for (Integer i : set) {
				sb.append(i);
				sb.append(", ");
			}
			sb.append("]");
			logger.info("Cluster {}: {}", n, sb);
			n++;
		}
	}

	private static final int NUM_CLUSTERS = 2;
}
