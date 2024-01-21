data <- read.csv("small_sample_1.csv", header=FALSE)
X <- data$V1
X.fft <- fft(X)

analyse <- function(xhat, sample.rate=1) {
  xhat <- xhat/length(xhat)
  data.frame(freq=0 : (length(xhat) - 1) * sample.rate/length(xhat),
             amplitude=sapply(xhat, Mod), 
             phase=sapply(xhat, function(x) {Arg(x) * 180/pi}))
}

X.fft.results <- analyse(X.fft, sample.rate=48000)
plot(X.fft.results$freq, 
     X.fft.results$amplitude, 
     type="l",
     main="Spectrum",
     xlab="Frequency",
     ylab="Amplitude")

# Read https://dsp.stackexchange.com/questions/4825/why-is-the-fft-mirrored to 
# understand why the transform is symmetric. Dilip Sarwate's answer gives the
# exact details.
