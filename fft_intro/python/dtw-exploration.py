#import sys
#import os.path

import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

X1, fs1 = librosa.load('../human/small-samples/aum-0.wav')
X2, fs2 = librosa.load('../human/small-samples/sam-0.wav')

plt.subplot(2, 1, 1)
librosa.display.waveshow(X1, sr=fs1, color='red')
plt.title('Aum')
plt.subplot(2, 1, 2)
librosa.display.waveshow(X2, sr=fs2, color='blue')
plt.title('Sam')
plt.tight_layout()
plt.show()