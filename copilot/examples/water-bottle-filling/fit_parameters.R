# ============================================================
# BAN 780 - Semester Assignment 2 : Water bottle filling
# Input parameter estimation from semA02-bottleFilling-DataSet.csv
# ------------------------------------------------------------
# Deliverable for the rubric ("provide .R or .xlsx").
# Put this script in the SAME folder as the CSV, then run it.
# ============================================================

# ---- 1. Load the data -------------------------------------------------
# (file has 3 columns: arrive, tba, Filling_time)
csv <- "semA02-bottleFilling-DataSet.csv"
data <- read.csv(csv, stringsAsFactors = FALSE)

tba  <- as.numeric(data$tba)          # time between bottle arrivals (seconds)
fill <- as.numeric(data$Filling_time) # bottle filling time (seconds)

tba  <- tba[!is.na(tba)  & tba  >= 0]
fill <- fill[!is.na(fill)]

cat("Records: tba =", length(tba), " | filling =", length(fill), "\n\n")

# ---- 2. Bottle ARRIVALS -> Exponential --------------------------------
# Exponential is defined by one parameter: the rate (lambda) = 1 / mean.
# Course method (see Assignment2.R): round the mean to 1 decimal, then rate.
mean_tba <- round(mean(tba), 1)          # 12.3
sd_tba   <- sd(tba)
lambda   <- round(1 / mean_tba, 5)       # 1/12.3 = 0.0813

cat("=== Time between arrivals (tba) ===\n")
cat(sprintf("mean = %.4f s   sd = %.4f s\n", mean_tba, sd_tba))
cat(sprintf("Exponential rate lambda = 1/mean = %.5f per second\n", lambda))
# Goodness-of-fit: for a TRUE exponential, mean ~= sd. Confirm, then KS test.
cat(sprintf("Sanity check (mean ~ sd for exponential): %.2f ~ %.2f\n", mean_tba, sd_tba))
ks_exp <- ks.test(tba, "pexp", rate = lambda)
cat(sprintf("KS test vs exponential: D = %.4f, p = %.4f\n", ks_exp$statistic, ks_exp$p.value))
cat(sprintf(">> AnyLogic Source interarrival time:  exponential(%.4f)\n\n", lambda))

# ---- 3. FILLING time -> Normal ----------------------------------------
# Course method: round mean and sd to 1 decimal -> normal(4.0, 11.9).
mean_fill <- round(mean(fill), 1)        # 11.9
sd_fill   <- round(sd(fill), 1)          # 4.0

cat("=== Filling time ===\n")
cat(sprintf("mean = %.4f s   sd = %.4f s\n", mean_fill, sd_fill))
ks_norm <- ks.test(fill, "pnorm", mean = mean_fill, sd = sd_fill)
cat(sprintf("KS test vs normal: D = %.4f, p = %.4f\n", ks_norm$statistic, ks_norm$p.value))
# NOTE: AnyLogic's normal() takes (standard deviation, mean) IN THAT ORDER.
cat(sprintf(">> AnyLogic filling time:  normal(%.4f, %.4f)   // normal(sigma, mean)\n\n",
            sd_fill, mean_fill))

# ---- 4. Optional: nicer fits with fitdistrplus ------------------------
# install.packages("fitdistrplus")   # uncomment once if not installed
if (requireNamespace("fitdistrplus", quietly = TRUE)) {
  library(fitdistrplus)
  cat("=== fitdistrplus cross-check ===\n")
  print(fitdist(tba,  "exp"))
  print(fitdist(fill, "norm"))
}

# ---- 5. Visual check (saved to PNGs) ----------------------------------
png("fit_tba_exponential.png", width = 700, height = 450)
hist(tba, breaks = 40, freq = FALSE, main = "Bottle inter-arrival time",
     xlab = "seconds", col = "grey90")
curve(dexp(x, rate = lambda), add = TRUE, lwd = 2, col = "red")
dev.off()

png("fit_filling_normal.png", width = 700, height = 450)
hist(fill, breaks = 40, freq = FALSE, main = "Filling time",
     xlab = "seconds", col = "grey90")
curve(dnorm(x, mean = mean_fill, sd = sd_fill), add = TRUE, lwd = 2, col = "blue")
dev.off()

cat("\nDone. Two histogram PNGs written for your report.\n")
cat("FIXED VALUES TO TYPE INTO ANYLOGIC:\n")
cat(sprintf("  Bottle Source interarrival = exponential(%.4f)\n", lambda))
cat(sprintf("  Filling Service delay      = normal(%.4f, %.4f)\n", sd_fill, mean_fill))
cat("  Packing (Assembler) delay  = normal(2, 9)        // given in the paper\n")
cat("  Crate Source arrival rate  = 2.4 per minute (Poisson) -> poisson(2.4) / rate 2.4 per min\n")
cat("  Crate weight               = uniform(5.0, 6.2)   // given in the paper\n")
