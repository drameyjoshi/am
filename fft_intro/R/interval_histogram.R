dirname <- 'C:\\Users\\ameyj\\repos\\am\\fft_intro\\txtfiles_24feb2024'

extract_data <- function(pathname) {
  data <- read.csv(file = pathname, header = TRUE, sep = '\t')
  data$prev.end.time <- c(NA, data$End.Time..s.[1:(nrow(data) - 1)]) # lag function not working.
  data$interval <- data$Begin.Time..s. - data$prev.end.time
  only.intervals <- data$interval[2:length(data)]
  only.intervals
}

intervals <- c()
for (f in list.files(dirname)) {
  pathname <- paste(sep='\\', dirname, f)
  intervals <- c(intervals, extract_data(pathname = pathname))
}

# Only histogram
hist(intervals, breaks = 20, main = 'Frequency histogram')

# Probability histogram
hist(intervals, breaks = 20, probability = TRUE, main = 'Probability histogram with density')
lines(density(intervals, na.rm = TRUE))
