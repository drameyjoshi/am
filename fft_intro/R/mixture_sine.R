# Reference:
# https://www.gaussianwaves.com/2015/11/interpreting-fft-results-obtaining-magnitude-and-phase-information/

nu1 <- 32 # 32 Hz
nu2 <- 5000 # In Hz
omega1 <- 2 * pi * nu1
omega2 <- 2 * pi * nu2
phase <- 2 * pi/3

fs <- 5 * max(nu1, nu2) # Sampling frequency
t <- seq(from = 0, to = 2, by=1/fs)
A <- 1 # Amplitude
N <- 1024 # Sample size

x <- A * sin(omega1 * t) + A * sin(omega2 * t + phase)
x.hat <- fft(x[1:N])
fft.index <- seq(0, N-1)
freq <- fft.index * fs/N
amplitude = sapply(x.hat, Mod)

plot(
  freq,
  amplitude,
  type = "l",
  main = "Spectrum of a mixture of sine wave",
  xlab = "Frequency",
  ylab = "Amplitude"
)

dominant.freq <- freq[which(amplitude > floor(max(amplitude)))[1]]
cat(paste("Dominant frequenct is", dominant.freq, "Hz."))
