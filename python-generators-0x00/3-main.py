#!/usr/bin/env python3
import sys
# Corrected the import to match the function name
lazy_paginator = __import__('2-lazy_paginate').lazy_paginate

try:
    # This loop will request one page at a time from the generator
    for page in lazy_paginator(100):
        # This inner loop just prints the users from the received page
        for user in page:
            # The extra print creates the blank line from the example
            print(user)
            print()

except BrokenPipeError:
    # This handles the error when piping to `head`
    sys.stderr.close()