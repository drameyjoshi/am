import sys
import os.path
import scipy.signal
import pandas as pd
import matplotlib.pyplot as plt

from typing import List

def get_csv_list(dir: str) -> None:
    return [f for f in os.listdir(dir) 
            if os.path.isfile(os.path.join(dir, f)) 
            and os.path.splitext(f)[1] == '.csv']


def calculate(dir: str, name: str) -> None:    
    if os.path.isdir(dir):
        csv = get_csv_list(dir)        
        
        for i in range(0, len(csv)):
            for j in range(i + 1, len(csv)):
                df1 = pd.read_csv(os.path.join(dir, csv[i]))
                df2 = pd.read_csv(os.path.join(dir, csv[j]))
                X1 = df1.to_numpy()
                X2 = df2.to_numpy()
                L = min(len(df1), len(df2))
                c = scipy.signal.correlate(X1[0:L], X2[0:L])
                plt.plot(range(0, len(c)), c)
                plt.savefig(f'corr_{name}_{i}_{j}.png')    
                plt.close()


def main(argv: List[str]) -> None:
    if len(argv) >= 3:
        calculate(dir=argv[1], name=argv[2])
        sys.exit(0)
    else:
        print('Need two arguments.')
        sys.exit(-1)

if __name__ == '__main__':
    main(sys.argv)