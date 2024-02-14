import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

filename = 'crows/all_data_for_clustering.csv'
X = pd.read_csv(filename)
sse = {}
for k in range(1, 12):
    kmeans = KMeans(n_clusters=k, max_iter=1000).fit(X)
    sse[k] = kmeans.inertia_

plt.plot(list(sse.keys()), list(sse.values()))
plt.xlabel('# clusters')
plt.ylabel('SSE')
plt.show()
