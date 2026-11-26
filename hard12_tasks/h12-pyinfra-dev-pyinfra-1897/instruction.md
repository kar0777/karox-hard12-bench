You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Properly document get_fact(deb.DebPackage, 'somename')

When calling `get_fact(deb.DebPackage, 'somename')` , _somename_ may be either an installed package or a package file; how this is decided should be documented. (I filed #1795 in part due to the lack of this documentation.)

The documentation needs to state three things:

1. ___This call is not idempotent.___ It may behave differently depending on the contents of the directory that happens to be the CWD when it's called.

2. The rules for whether _somename_ is treated as a request for information about a package file or an installed package are as follows.

   a. If _somename_ does not match the shell glob `*.deb` the installed package database is queried.

   b. If _somename_ does match the shell glob `*.deb`:
      1. If a file in the CWD matching that name exists, that package file is queried.
      2. If a file in the CWD matching that name does not exist, the installed package database is queried.

3. This breaks backward compatibility from versions before [whatever version this is released in]: querying e.g. `somepackage.deb.old` when a package file with that name is present will now fail.

We should probably also note that this prohibits querying any package files that do not end in `.deb`, e.g., `somepackage.deb.old` or `somepackage.deb~`.

FWIW, I still believe that, since we're going to break backward compatibility anyway, using the scheme I suggested in #1795 (put a slash in any _somename_ that's supposed to reference a file) is the better solution because it makes this idempotent and gives an error when someone expects a file to be there that isn't, rather than misleadingly giving package information for a potentially different package.

