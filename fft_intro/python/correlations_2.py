import sys
import os.path
import scipy.signal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from typing import List, Tuple

# To calculate correlations between aum_{i}.csv with aum_{j}.csv where i and j
# range from 0 to 19.

def get_csv_list(dir: str) -> None:
    return [f for f in os.listdir(dir) 
            if os.path.isfile(os.path.join(dir, f)) 
            and os.path.splitext(f)[1] == '.csv']


def calculate(dir: str, name: str, create_plot: bool=False) -> List[Tuple[int, int, float]]:   
    minmax = []
    if os.path.isdir(dir):
        csv = get_csv_list(dir)        
        
        for i in range(0, len(csv)):
            for j in range(i + 1, len(csv)):
                df1 = pd.read_csv(os.path.join(dir, csv[i]))
                df2 = pd.read_csv(os.path.join(dir, csv[j]))
                X1 = df1.to_numpy()
                X2 = df2.to_numpy()
                L = min(len(df1), len(df2))
                Y1 = (X1[0:L] - np.mean(X1[0:L]))/(np.std(X1[0:L]) * L)
                Y2 = (X2[0:L] - np.mean(X2[0:L]))/(np.std(X2[0:L]) * 1)
                c = scipy.signal.correlate(Y1, Y2)  
                if create_plot:              
                    plt.plot(range(0, len(c)), c)
                    plt.savefig(f'corr_{name}_{i}_{j}.png')    
                    plt.close()
                minmax.append((i, j, np.max(abs(c))))

    return minmax


def main(argv: List[str]) -> None:
    if len(argv) >= 3:
        results = calculate(dir=argv[1], name=argv[2])
        for i in range(0, len(results)):
            print(results[i])
        sys.exit(0)
    else:
        print('Need two arguments.')
        sys.exit(-1)

if __name__ == '__main__':
    main(sys.argv)