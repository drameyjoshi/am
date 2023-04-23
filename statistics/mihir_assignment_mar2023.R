library(car) # CAR stands for Companion to Applied Regression
library(lmtest)

raw_data <-
  read.csv('datasets/mihir-dataset-1-student000942781.csv')
raw_data$industry = as.factor(raw_data$industry)
raw_data <- raw_data[raw_data$industry != 'Services', ]

# Create dummies
industry_dummies <- model.matrix( ~ raw_data$industry - 1)
colnames(industry_dummies) <- levels(raw_data$industry)

data <-
  raw_data[, c('firm_id', 'emissions', 'tax', 'employment', 'export', 'city')]
data <- cbind(data, industry_dummies[, c('Agriculture', 'Construction', 'Manufacturing')])

data <- data[complete.cases(data), ]

# Build the model
model <-
  lm(
    emissions ~ tax + employment + export + city + Agriculture + Construction + Manufacturing,
    data = data
  )
summary(model)

all_vifs <- vif(model)
if (length(all_vifs[all_vifs >= 5]) == 0) {
  cat("None of the variance inflation factors are greater than 5.")
  cat("There is no strong multi-collinearity.")
}

breusch_pagan_results <- bptest(model)
if (breusch_pagan_results$p.value <= 0.05) {
  cat("There is evidence of heteroscedasticity.")
} else {
  cat("There is no strong evidence of heteroscedasticity.")
}
