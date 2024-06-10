

# to selectively ignore warnings for a chunk of code:

import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    ## <code that throws known warning goes here>

## <rest of your code which might throw an unexpected warning>