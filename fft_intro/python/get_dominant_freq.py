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
                       sampling_rate: int) -> pd.DataFrame:    
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
    df['int_freq'] = np.round(df['freq']/10, 0) * 10
    significant = df.loc[((df['freq'] <= np.mean(freq)) &
                          (df['amplitude'] >= np.mean(amplitude)))]
    significant.sort_values(by='amplitude', inplace=True)
    uif = significant.int_freq.unique().astype(np.int64)        
    return pd.DataFrame(uif).describe().loc[['mean', 'std', 'min',
                                             '25%', '50%', '75%', 'max']].T




def main(argv:List[str]) -> None:
    if len(argv) == 4:
        src = argv[1]
        dest = argv[2]
        summary_file = argv[3]

        if not os.path.exists(dest):
            os.makedirs(dest)

        csvfiles = [f for f in os.listdir(src)
                    if os.path.isfile(os.path.join(src, f)) and
                    os.path.splitext(f)[1] == '.csv']

        processing_time = np.zeros(len(csvfiles))
        i = 0
        pd.options.mode.copy_on_write = True
        results = []
        for csvname in csvfiles:
            start = time.time()
            sname = os.path.splitext(os.path.basename(csvname))[0]            
            results.append(plot_dominant_freq(os.path.join(src, csvname),
                                              os.path.join(dest, f"{sname}.png"),
                                              sname,
                                              48000)
                           )
            processing_time[i] = time.time() - start
            i += 1
            
        print("Average processing time is %0.3f s." % np.mean(processing_time))
        summaries = pd.concat(results, ignore_index=True)
        summaries.to_csv(summary_file, index=False)

        sys.exit(0)
    else:
        print('Need two arguments.')
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv)
    
    
