import sys
import os.path
import scipy.signal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from typing import List

# To calculate correlations between aum_{i}.csv with sam_{i}.csv where i
# ranges from 0 to 19.

def normalise(X: np.array) -> np.array:
    return X/np.max(abs(X))

def standardise(X: np.array) -> np.array:
    return (X - np.mean(X))/(np.std(X) * np.sqrt(len(X)))

def calculate(file1: str, file2: str, create_plot: bool=False) -> List[float]:
    minmax = []  
    if os.path.isfile(file1) and os.path.isfile(file2):
        df1 = pd.read_csv(file1, header=None)
        df2 = pd.read_csv(file2, header=None)
        X1 = df1[0].to_numpy()
        X2 = df2[0].to_numpy()
        L = min(len(df1), len(df2))
        c = scipy.signal.correlate(standardise(X1[0:L]), standardise(X2[0:L]), method='direct')
        if create_plot:
            plt.plot(range(0, len(c)), c)
            plt.savefig(f'corr_aum_sam.png')    
            plt.close()
        minmax.append(np.max(abs(c)))

    return minmax


def main(argv: List[str]) -> None:
    if len(argv) >= 3:
        file1 = argv[1]
        file2 = argv[2]
        results = calculate(file1=file1, file2=file2)
        print(results)

        sys.exit(0)
    else:
        print('Need two arguments.')
        sys.exit(-1)

if __name__ == '__main__':
    main(sys.argv)