package clustering;

public class CleaningArea {

	public CleaningArea() {
		// Nothing to be done here.
	}
	
	public String showClusterInfo() {
		return String.format("id = %d, time to clean = %d, cluster = %d", id, timeToClean, clusterId);
	}

	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public int getFloorId() {
		return floorId;
	}

	public void setFloorId(int floorId) {
		this.floorId = floorId;
	}

	public int getTimeToClean() {
		return timeToClean;
	}

	public void setTimeToClean(int timeToClean) {
		this.timeToClean = timeToClean;
	}

	public int[] getNeighbours() {
		return neighbours;
	}

	public void setNeighbours(int[] neighbours) {
		this.neighbours = neighbours;
	}

	public int getClusterId() {
		return clusterId;
	}

	public void setClusterId(int clusterId) {
		this.clusterId = clusterId;
	}

	private int id;
	private String name;
	private int floorId;
	private int timeToClean;
	private int[] neighbours;
	private int clusterId;
}
