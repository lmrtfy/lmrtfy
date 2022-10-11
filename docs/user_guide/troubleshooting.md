If you encounter any problems you can always contact us via [hello@lmrt.fyi](mailto:hello@lmrt.fyi). 
Alternatively, you can also open an [issue on GitHub](https://github.com/lmrtfy/lmrtfy/issues).

# How can I get debug output?
Set `#!shell LMRTFY_DEBUG="1"` before running any `#!shell lmrtfy` commands. 

# My deployed function does not receive any jobs that I submit!
There are a multiple possible explanations depending on what exactly you see

### I can retrieve results, even though my deployed has not done anything
Please check if you ran `lmrtfy deploy` for the same file in another session. If multiple runners
serve your function only one of them will receive the same call. The next call to the same function
will be routed to the next runner in the line.

### The job status is reported `UNKNOWN`
If that is the case, please let us know at [hello@lmrt.fyi](mailtohello@lmrt.fyi) or in the GitHub issues. 
This is likely a problem on our side.

# I need help to implement a specific use case
Please don't hesitate to contact us via [hello@lmrt.fyi](mailto:hello@lmrt.fyi). We are always
interested in new use cases. 

