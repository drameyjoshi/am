import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

fname = "aum/csv/aum_1.csv"
sname = os.path.splitext(os.path.basename(fname))[0]
aumpling_rate = 48000
pd.options.mode.copy_on_write = True

dfc = pd.read_csv(fname, header=None)
X = dfc[0].to_numpy()
Xhat = np.fft.fft(X)
N = Xhat.shape[0]
freq = [f*aumpling_rate/N for f in range(0, N)]
amplitude = np.absolute(Xhat)
phase = np.angle(Xhat)

df = pd.DataFrame(data = [freq, amplitude, phase]).T
df.columns = ['freq', 'amplitude', 'phase']
df['int_freq'] = np.round(df['freq']/10, 0) * 10
significant = df.loc[((df['freq'] <= np.mean(freq)) &
                      (df['amplitude'] >= np.mean(amplitude)))]
significant.sort_values(by='amplitude', inplace=True)
uniq_freq = significant.int_freq.unique().astype(np.int64)
significant.to_csv('aum/csv/aum_df_1.csv', index=False)
np.savetxt('aum/csv/aum_uf_1.csv', uniq_freq, delimiter=',', fmt='%d')
print(pd.DataFrame(uniq_freq).describe().loc[['mean', 'std', 'min',
                                              '25%', '50%', '75%', 'max']].T)
