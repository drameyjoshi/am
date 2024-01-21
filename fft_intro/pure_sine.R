nu <- 32 # 32 Hz
omega <- 2 * pi * nu
fs <- 100 * nu # Sampling frequency
t <- seq(from = 0, to = 2, by=1/fs)
A <- 1 # Amplitude
N <- 1024 # Sample size

x <- A * sin(omega * t)
x.hat <- fft(x[1:N])
fft.index <- seq(0, N-1)
freq <- fft.index * fs/N
amplitude = sapply(x.hat, Mod)

plot(
  freq,
  amplitude,
  type = "l",
  main = "Spectrum of pure sine wave",
  xlab = "Frequency",
  ylab = "Amplitude"
)

dominant.freq <- freq[which(amplitude > floor(max(amplitude)))[1]]
cat(paste("Dominant frequenct is", dominant.freq, "Hz."))
