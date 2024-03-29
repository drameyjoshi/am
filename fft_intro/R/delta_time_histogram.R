dirname <- 'C:\\Users\\ameyj\\repos\\am\\fft_intro\\txtfiles_24feb2024'

extract_data <- function(pathname, filter_above=100) {
  data <- read.csv(file = pathname, header = TRUE, sep = '\t')
  delta.time <- data$Delta.Time..s.
  delta.time[delta.time < filter_above]
}

times <- c()
for (f in list.files(dirname)) {
  pathname <- paste(sep='\\', dirname, f)
  times <- c(times, extract_data(pathname = pathname, filter_above = 3))
}

# Only histogram
hist(times, breaks = 20, main = 'Frequency histogram')

# Probability histogram
hist(times, breaks = 20, probability = TRUE, main = 'Probability histogram with density')
lines(density(times, na.rm = TRUE))
