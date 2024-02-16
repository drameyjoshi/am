import os.path
import sys

import pandas as pd

from typing import List, Tuple

def get_stats(filename: str) -> Tuple[float, float, float]:
    if os.path.isfile(filename):
        with open(filename, 'r') as fpr:
            lowest = 0
            highest = 0
            total = 0
            n = 0
            for line in fpr:
                x = float(line.strip().strip(','))
                if x < lowest:
                    lowest = x
                if x > highest:
                    highest = x

                total += x
                n += 1

            return (lowest, highest, total/n)
    else:
        return (None, None, None)


def describe(filename: str) -> None:
    if os.path.isfile(filename):
        df = pd.read_csv(filename)
        print(df.describe())


def get_limits(lowest: float,
               highest: float,
               pct_margin: float=0.05) -> float:
    assert pct_margin > 0 and pct_margin < 1    
    return max(abs(lowest), abs(highest)) * pct_margin


def transform(filename: str, abslimit: float) -> None:
    basename = os.path.basename(filename)
    dirname = os.path.dirname(filename)
    transformed_file = f'transformed_{basename}'
    transformed_path = os.path.join(dirname, transformed_file)

    if os.path.exists(filename):
        with open(filename, 'r') as fpr:
            fpw = open(transformed_path, 'w')
            for line in fpr:
                x = float(line.strip().strip(','))
                if abs(x) > abslimit:
                    fpw.write(line)
                else:
                    fpw.write(str(0) + '\n')

            fpw.close()
    else:
        print(f'Could not read {filename}.')


def main(argv: List[str]) -> None:
    if len(argv) >= 2:
        lowest, highest, avg = get_stats(argv[1])
        print(f'min = {lowest}, max = {highest}, avg = {avg}.')
        x = get_limits(lowest, highest, 0.005)
        print(f'Excluding signal below {x}.')
        transform(argv[1], x)
        sys.exit(0)
    else:
        print('Need filename of the CSV as an argument.')
        sys.exit(-1)


if __name__ == '__main__':
    main(sys.argv)
