library(lpSolve)
profit <- c(NH3 = 40, NH4Cl = 50)
constraints <- matrix(data = c(1, 3, 0, 1, 4, 1),
                      nrow = 3,
                      ncol = 2,
                      byrow = FALSE,
                      dimnames = list(c("N", "H", "Cl"),
                                      c("NH3", "NH4Cl")))
lp.results <-
  lp(direction = "max",
     objective.in = profit,
     const.mat = constraints,
     const.dir = rep("<=", 3),
     const.rhs = c("N" = 50, "H" = 180, "Cl" = 40))
if (lp.results$status == 0) {
  cat(paste(sep = "", "The maximum profit is ", lp.results$objval, ".\n"))
  s <- lp.results$solution
  names(s) <- names(profit)
  cat("A production plan to achieve it is:\n")
  print(s)
} else {
  cat("Could not solve the LP.\n")
}

