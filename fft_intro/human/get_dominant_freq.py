import os
import sys
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from typing import List

def plot_dominant_freq(csvname: str,
                       pngname: str,
                       sname: str,
                       sampling_rate: int) -> None:    
    dfc = pd.read_csv(csvname, header=None)
    X = dfc[0].to_numpy()
    Xhat = np.fft.fft(X)
    N = Xhat.shape[0]
    freq = [f*sampling_rate/N for f in range(0, N)]
    amplitude = np.absolute(Xhat)
    phase = np.angle(Xhat)

    df = pd.DataFrame(data = [freq, amplitude, phase]).T
    df.columns = ['freq', 'amplitude', 'phase']
    significant = df.loc[((df['freq'] <= np.mean(freq)) &
                          (df['amplitude'] >= np.mean(amplitude)))]
    hist_data = plt.hist(significant['freq'], bins=100)
    plt.title(sname)
    plt.savefig(pngname)
    plt.close()


def main(argv:List[str]) -> None:
    if len(argv) == 3:
        src = argv[1]
        dest = argv[2]

        if not os.path.exists(dest):
            os.makedirs(dest)

        csvfiles = [f for f in os.listdir(src)
                    if os.path.isfile(os.path.join(src, f)) and
                    os.path.splitext(f)[1] == '.csv']

        processing_time = np.zeros(len(csvfiles))
        i = 0
        for csvname in csvfiles:
            start = time.time()
            sname = os.path.splitext(os.path.basename(csvname))[0]            
            plot_dominant_freq(os.path.join(src, csvname),
                               os.path.join(dest, f"{sname}.png"),
                               sname,
                               48000)
            processing_time[i] = time.time() - start
            i += 1
            
        print("Average processing time is %0.3f s." % np.mean(processing_time))
            

        sys.exit(0)
    else:
        print('Need two arguments.')
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv)
    
    
