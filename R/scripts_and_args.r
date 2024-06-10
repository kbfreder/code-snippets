

# basic
args = commandArgs(trailingOnly = TRUE)

if (length(args) == 0) {
  stop("Baseline rate and effect must be supplied", call.=FALSE)
} else{
  P0 <- as.integer(args[1])
  effecti <- as.integer(args[2])
}


# using optparse
library(optparse)


option_list = list(
  make_option(c("-b", "--baseline-rate"),
              type="double",
              action = "store", # this isn't needed here, but you might need `action = "store_true"` for a boolean
              dest="baseline",
              help="Baseline conversion rate"
              ),
  make_option(c("-a", "--alpha"),
              type="double",
              default = 0.05,
              help="Alpha, or significance level, or acceptable false positive rate"
              ),
)

opt_parser = OptionParser(option_list = option_list)
opt = parse_args(opt_parser)

P0 = opt$baseline
a = opt$alpha

## lame that you have to check for whether they were supplied or not, yourself
if (is.null(P0)) {
  print_help(opt_parser)
  stop("You must supply: baseline-rate", call.=FALSE)
}


# equivalent of `if __name__ == "__main__"`:
if (!interactive()) {
  main()
}