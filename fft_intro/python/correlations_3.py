import sys
import os.path
import scipy.stats
import pandas as pd
import matplotlib.pyplot as plt

from typing import List, Tuple

def get_csv_list(dir: str) -> None:
    return [f for f in os.listdir(dir) 
            if os.path.isfile(os.path.join(dir, f)) 
            and os.path.splitext(f)[1] == '.csv']


def calculate(dir1: str, dir2: str) -> List[Tuple[float, float]]:
    correlations = []
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
            z = scipy.stats.pearsonr(X1[0:L, 0], X2[0:L, 0]) # Coefficient and p-value
            correlations.append(z)
            
    return correlations


def main(argv: List[str]) -> None:
    if len(argv) >= 3:
        person1 = argv[1]
        person2 = argv[2]
        correlations = calculate(person1, person2)
        for i in range(0, len(correlations)):
            print(correlations[i])

        sys.exit(0)
    else:
        print('Need two arguments.')
        sys.exit(-1)


if __name__ == '__main__':
    main(sys.argv)