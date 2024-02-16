import sys
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from typing import List


def cluster(filename: str, pngname: str=None) -> None:
    X = pd.read_csv(filename)
    sse = {}
    for k in range(1, 12):
        kmeans = KMeans(n_clusters=k, max_iter=1000).fit(X)
        sse[k] = kmeans.inertia_

    plt.plot(list(sse.keys()), list(sse.values()))
    plt.xlabel('# clusters')
    plt.ylabel('SSE')

    if pngname is None:
        plt.show()
    else:
        plt.savefig(pngname)


def main(argv: List[str]) -> None:
    if len(argv) >= 3:
        cluster(argv[1], argv[2])
        sys.exit(0)    
    elif len(argv) >= 2:
        cluster(argv[1])        
        sys.exit(0)
    else:
        print("Need filename as the argument.")
        sys.exit(-1)


if __name__ == '__main__':
    main(sys.argv)
