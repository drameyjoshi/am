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


def transform(filename: str, abslimit: float) -> str:
    if os.path.exists(filename):
        basename = os.path.basename(filename)
        dirname = os.path.dirname(filename)
        transformed_file = f'transformed_{basename}'
        transformed_path = os.path.join(dirname, transformed_file)

        with open(filename, 'r') as fpr:
            fpw = open(transformed_path, 'w')
            for line in fpr:
                x = float(line.strip().strip(','))
                if abs(x) > abslimit:
                    fpw.write(str(x) + '\n')
                else:
                    fpw.write(str(0) + '\n')

            fpw.close()

        return transformed_path
    else:
        print(f'Could not read {filename}.')     
        return ''   

def print_diagnostics(data: List[List[float]]) -> None:
    x = 0
    for k in range(len(data)):
        x += len(data[k])
        print(f'File {k} will have {len(data[k])} points.')

    print(f'Total #data points is {x}.')


def split(transformed_file: str, whitespace_len=48000) -> None:
    if os.path.exists(transformed_file):
        with open(transformed_file, 'r') as fpr:
            data = [] # List of lists.
            L = []
            zeros = []
            zcount = 0
            dcount = 0
            for line in fpr:
                x = float(line.strip().strip(','))
                if x != 0:
                    dcount += 1
                    if zcount > 0 and zcount <= whitespace_len:
                        L.append(zeros)
                        zcount = 0
                        zeros.clear()                                             
                    elif zcount > whitespace_len:
                        zcount = 0
                        zeros.clear()
                        if len(L) > 0:                            
                            data.append(L)
                            L = []
                    L.append(x)   
                else:
                    zcount += 1
                    if zcount <= whitespace_len:
                        zeros.append(0)
                    elif len(zeros) > 0:
                        zeros.clear()

            if len(L) > 0:
                data.append(L)

        print(f'{len(data)} files can be created out of {transformed_file}.')
        print(f'# data points is {dcount}.') 
        print_diagnostics(data=data)
        
        basename = os.path.basename(transformed_file)
        dirname = os.path.dirname(transformed_file)
        for k in range(0, len(data)):
            fname = f'{k}_{basename}'
            fpath = os.path.join(dirname, fname)
            with open(fpath, 'w') as fpw:
                for i in range(0, len(data[k])):
                    fpw.write(str(data[k][i]) + '\n')

            fpw.close()
    else:
        print(f'Could not read {transformed_file}.')
                        


def main(argv: List[str]) -> None:
    proceed = True

    if len(argv) >= 3:
        filename = argv[1]
        pct_margin = float(argv[2].strip())
    elif len(argv) == 2:
        filename = argv[1]
        pct_margin = 0.01
    else:
        proceed = False

    if proceed:
        lowest, highest, avg = get_stats(filename)
        print(f'min = {lowest}, max = {highest}, avg = {avg}.')
        x = get_limits(lowest, highest, pct_margin=pct_margin)
        print(f'Excluding signal below amplitude {x}.')
        transformed_file = transform(argv[1], x)
        split(transformed_file=transformed_file)
        sys.exit(0)
    else:
        print('Need filename of the CSV as an argument.')
        sys.exit(-1)


if __name__ == '__main__':
    main(sys.argv)
