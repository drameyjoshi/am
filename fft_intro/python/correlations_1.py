import sys
import os.path
import scipy.signal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from typing import List

# To calculate correlations between aum_{i}.csv with sam_{i}.csv where i
# ranges from 0 to 19.

def get_csv_list(dir: str) -> None:
    return [f for f in os.listdir(dir) 
            if os.path.isfile(os.path.join(dir, f)) 
            and os.path.splitext(f)[1] == '.csv']


def normalise(X: np.array) -> np.array:
    return X/np.max(abs(X))

def standardise(X: np.array) -> np.array:
    return (X - np.mean(X))/(np.std(X) * np.sqrt(len(X)))

def calculate(dir1: str, dir2: str, create_plot: bool=False) -> List[float]:
    minmax = []  
    if os.path.isdir(dir1) and os.path.isdir(dir2):
        csv1 = get_csv_list(dir1)
        csv2 = get_csv_list(dir2)

        assert len(csv1) == len(csv2)
        for i in range(0, len(csv1)):
            df1 = pd.read_csv(os.path.join(dir1, csv1[i]))
            df2 = pd.read_csv(os.path.join(dir2, csv2[i]))
            X1 = df1.to_numpy()
            X2 = df2.to_numpy()
            L = min(len(df1), len(df2))
            c = scipy.signal.correlate(standardise(X1[0:L]), standardise(X2[0:L]))
            if create_plot:
                plt.plot(range(0, len(c)), c)
                plt.savefig(f'corr_aum_sam_{i}.png')    
                plt.close()
            minmax.append(np.max(abs(c)))

    return minmax


def main(argv: List[str]) -> None:
    if len(argv) >= 3:
        person1 = argv[1]
        person2 = argv[2]
        results = calculate(person1, person2)
        for i in range(0, len(results)):
            #print(f'{round(results[i][0], 3)}, {round(results[i][1], 3)}, {round(results[i][2], 3)}')
            print(results[i])

        sys.exit(0)
    else:
        print('Need two arguments.')
        sys.exit(-1)

if __name__ == '__main__':
    main(sys.argv)