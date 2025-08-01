#!/usr/bin/env python3
import sys
processing = __import__('1-batch_processing')

##### print processed users in a batch of 50
try:
    processing.batch_processing(50)
except BrokenPipeError:
    # This handles the error when piping to `head` which closes the pipe early
    sys.stderr.close()