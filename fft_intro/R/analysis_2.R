analyse <- function(filename, pname) {
  data <- read.csv(filename, header = FALSE)
  X <- data$V1
  X.fft <- fft(X)
  
  analyse <- function(xhat, sample.rate = 1) {
    xhat <- xhat / length(xhat)
    data.frame(
      freq = 0:(length(xhat) - 1) * sample.rate / length(xhat),
      amplitude = sapply(xhat, Mod),
      phase = sapply(xhat, function(x) {
        Arg(x) * 180 / pi
      })
    )
  }
  
  X.fft.results <- analyse(X.fft, sample.rate = 48000)
  png(filename = paste(sep = ".", pname, "png"))
  plot(
    X.fft.results$freq,
    X.fft.results$amplitude,
    type = "l",
    main = paste("Spectrum -", pname),
    xlab = "Frequency",
    ylab = "Amplitude"
  )
  dev.off()
  
  # Choose amplitudes greater than the mean of all amplitudes
  selected <-
    which(X.fft.results$amplitude > mean(X.fft.results$amplitude))
  # Focus on the left half of the spectrum.
  left.selected <- selected[selected < nrow(X.fft.results) / 2]
  
  # Here's the data of our interest.
  interesting.freq <- X.fft.results[left.selected, ]
  interesting.freq <-
    interesting.freq[order(-interesting.freq$amplitude), ]
  
  write.csv(interesting.freq,
            file = paste(sep = ".", pname, "csv"),
            row.names = FALSE)
}
