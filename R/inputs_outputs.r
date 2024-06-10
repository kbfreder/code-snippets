

# ref: https://readr.tidyverse.org/reference/read_delim.html

df <- read_csv("path_to_csv", 
    skip=2, 
    col_names = FALSE, # or c("a", "b", "c")
    comment = "#" # skip rows that start with this chr
)