rohit <- read.csv("220217_001_Tr1_Rohit1.Waveform 1.samples.csv", header = FALSE)$V1
aum <- read.csv("220217_002_Tr1_Aum1.Waveform 1.samples.csv", header = FALSE)$V1
gaana <- read.csv("220219_002_Tr1_Gaana1.Waveform 1.samples.csv", header = FALSE)$V1

ra <- ccf(rohit, aum)
rg <- ccf(rohit, gaana)
ag <- ccf(aum, gaana)
