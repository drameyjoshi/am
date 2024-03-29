import os
import sys
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from typing import List

# For the range of human voice:
# https://dsp.stackexchange.com/questions/83749/what-is-the-maximum-possible-frequency-of-human-voice-speechthat-can-be-generat

def get_significant_freq(csvname: str, sampling_rate: int) -> pd.DataFrame:
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

    return significant

    
def plot_dominant_freq(csv1: str,
                       name1: str,
                       csv2: str,
                       name2: str,
                       pngname: str,
                       sname: str,
                       sampling_rate: int) -> None:
    significant_1 = get_significant_freq(csv1, sampling_rate)
    significant_2 = get_significant_freq(csv2, sampling_rate)
    
    plt.hist(significant_1['freq'], bins=100)
    plt.hist(significant_2['freq'], bins=100)
    plt.title(sname)
    plt.legend([name1, name2])
    plt.savefig(pngname)
    plt.close()


def main(argv:List[str]) -> None:
    if len(argv) == 6:
        src1 = argv[1]
        name1 = argv[2]
        src2 = argv[3]
        name2 = argv[4]
        dest = argv[5]

        if not os.path.exists(dest):
            os.makedirs(dest)

        csvfiles1 = [f for f in os.listdir(src1)
                    if os.path.isfile(os.path.join(src1, f)) and
                    os.path.splitext(f)[1] == '.csv']
        csvfiles2 = [f for f in os.listdir(src2)
                    if os.path.isfile(os.path.join(src2, f)) and
                    os.path.splitext(f)[1] == '.csv']

        assert len(csvfiles1) == len(csvfiles2)

        processing_time = np.zeros(len(csvfiles1))
        for i in range(len(csvfiles1)):
            sname = f"sample_{i}"
            start = time.time()
            plot_dominant_freq(os.path.join(src1, csvfiles1[i]),
                               name1,
                               os.path.join(src2, csvfiles2[i]),
                               name2,
                               os.path.join(dest, f"{sname}.png"),
                               sname,
                               48000)
            processing_time[i] = time.time() - start

        print("Average processing time is %0.3f s." % np.mean(processing_time))
        sys.exit(0)
    else:
        print('Need three arguments.')
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv)
    
    
