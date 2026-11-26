You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

ISort incorrectly removes some blank lines

When processing lines, ISort treats some whitespace-only lines incorrectly.

[isort-blank-lines.py.txt](https://github.com/user-attachments/files/29186598/isort-blank-lines.py.txt)
The attached file contains this content:

    import os
    import sys

    
    print("Hello, world!")

When ISort process that input file, it incorrectly removes one of the blank lines:

    $ python3 -m isort --check-only --diff ./isort-blank-lines.py 
    ERROR: /home/bignose/Projects/python/isort-blank-lines.py Imports are incorrectly sorted.
    --- /home/bignose/Projects/python/isort-blank-lines.py:before   2019-01-26 21:14:47.421581
    +++ /home/bignose/Projects/python/isort-blank-lines.py:after    2019-01-26 21:15:18.837737
    @@ -1,6 +1,4 @@
     import os
     import sys
     
    --
     print("Hello, world!")

The input file is valid, and should not be altered by ISort, because the second blank line (containing only U+000C FORM FEED) is a valid blank line in Python code.

According to Python [syntax rules for indentation](https://docs.python.org/3/reference/lexical_analysis.html#indentation), (and recently acknowledged in https://github.com/PyCQA/isort/pull/2436) U+000C do not constitute indentation space:

> A formfeed character may be present at the start of the line; it will be ignored for the indentation calculations […].

PEP 8 [recommendations for blank lines](https://peps.python.org/pep-0008/#blank-lines) specify that those two blank lines should remain:

> Surround top-level function and class definitions with two blank lines.

By removing one of the two blank lines, ISort renders the formerly PEP-8 conformant file, now in violation of that recommendation.

So, a line consisting of U+000C is a valid empty blank line; as part of a “two blank lines” as recommended by PEP 8, it should not be stripped, and should not be altered by ISort.
