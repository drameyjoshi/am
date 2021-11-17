examine_profit_impact <- function(ammonia, chloride) {
  profit <- c(NH3 = ammonia, NH4Cl = chloride)
  constraints <- matrix(
    data = c(1, 3, 0, 1, 4, 1),
    nrow = 3,
    ncol = 2,
    byrow = FALSE,
    dimnames = list(c("N", "H", "Cl"),
                    c("NH3", "NH4Cl"))
  )
  
  lp.results <-
    lp(
      direction = "max",
      objective.in = profit,
      const.mat = constraints,
      const.dir = rep("<=", 3),
      const.rhs = c("N" = 50, "H" = 180, "Cl" = 40)
    )
  
  if (lp.results$status == 0) {
    list(
      status = lp.results$status,
      profit = lp.results$objval,
      plan = lp.results$solution
    )
  } else {
    list(status = lp.results$status, NA, NA)
  }
}

show_result <- function(result) {
  if (result$status == 0) {
    cat(paste(
      "profit =",
      round(result[["profit"]], 2),
      "plan =",
      paste(round(result[["plan"]], 2), collapse = ", "),
      collapse = " "
    ),
    "\n")
  }
}

ammonia_range <- seq(from = 30, to = 60, by = 2)
chloride_range <- seq(from = 30, to = 60, by = 2)

for (a in ammonia_range) {
  cat(paste("ammonia =", a, "chloride =", 50, " "))
  show_result(examine_profit_impact(a, 50))
}

for (c in chloride_range) {
  cat(paste("ammonia =", 40, "chloride =", c, " "))
  show_result(examine_profit_impact(40, c))
}
