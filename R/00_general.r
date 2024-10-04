
# list all packages loaded
(.packages())


# install new package
install.packages('tidyverse')

## you can install more than one at a time
install.packages(c('readr', 'ggplot2', 'tidyr'))


# load package
library(tidyverse)


# get help on a package or function
??ES.h


# STRING MANIPS
# =========================

# concat string + int
sprintf("rank_%d", x)



# LOGIC
# =========================

# if/then, if/else
if (x == y) {
    z = 0
} else {
    z = 1
}



# SHORTCUTS
# =================
# pipe: |
Ctrl/Cmd + Shift + M

- may need to make a change to R studio options
    - Tools -> Global Options
    - Code tab
    - Select "Use native pipe operator, |>"

- aka `%>%`

# assignment: <-
Alt + '-'


# FUNCTIONS 
# ==================

function_name <- function(parameters){
  function body 
}