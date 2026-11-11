You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Add support for cross section groups with numerical labels

In this section of the docs it says that numbers are allowable to use as cross section groups: https://terrapower.github.io/armi/user/inputs.html#assemblies

<img width="740" height="390" alt="Image" src="https://github.com/user-attachments/assets/4aa8d36e-4ad2-415f-870d-5aaf467d8a08" />

However this does not work in practice. I am finding that ARMI will bomb if you try to load a DB that used numbers. The failure looks like this:
```
 r = db.load(cycleIdx, node)
  File "/anfhome/team/nala/ckeckler/nala-v302/framework/armi/bookkeeping/db/database.py", line 722, in load
    self._readParams(h5group, compType, compTypeList, allowMissing=allowMissing)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/anfhome/team/nala/ckeckler/nala-v302/framework/armi/bookkeeping/db/database.py", line 1050, in _readParams
    c.p[paramName] = val
    ~~~^^^^^^^^^^^
  File "/anfhome/team/nala/ckeckler/nala-v302/framework/armi/reactor/parameters/parameterCollections.py", line 327, in __setitem__
    setattr(self, name, value)
    ~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "/anfhome/team/nala/ckeckler/nala-v302/framework/armi/reactor/parameters/parameterCollections.py", line 269, in __setattr__
    object.__setattr__(self, key, value)
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/anfhome/team/nala/ckeckler/nala-v302/framework/armi/reactor/parameters/parameterDefinitions.py", line 350, in __set__
    self._setter(obj, val)
    ~~~~~~~~~~~~^^^^^^^^^^
  File "/anfhome/team/nala/ckeckler/nala-v302/framework/armi/reactor/parameters/parameterDefinitions.py", line 414, in paramSetter
    setter(p_self, value)
    ~~~~~~^^^^^^^^^^^^^^^
  File "/anfhome/team/nala/ckeckler/nala-v302/framework/armi/reactor/blockParameters.py", line 332, in xsTypeNum
    self._p_xsType = crossSectionGroupManager.getXSTypeLabelFromNumber(value)
                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^
  File "/anfhome/team/nala/ckeckler/nala-v302/framework/armi/physics/neutronics/crossSectionGroupManager.py", line 112, in getXSTypeLabelFromNumber
    raise ValueError(
    ...<2 lines>...
    )
ValueError: Cannot convert invalid xsTypeNumber `49` to char. The number must be >= 65 (corresponding to 'A').
```

The offending code is this:
https://github.com/terrapower/armi/blob/20f683e06c1789383e5cd87f271dccaa12d05c78/armi/physics/neutronics/crossSectionGroupManager.py#L106-L114

That code explicitly enforces that only letters are allowed.

Other places in the code seem to do the same:
https://github.com/terrapower/armi/blob/20f683e06c1789383e5cd87f271dccaa12d05c78/armi/physics/neutronics/crossSectionGroupManager.py#L84

I imagine other places in the codebase might break as well. I believe that we sometimes try to cast the capital letter down to its lowercase version during cross section generation, which I imagine would fail if the XS type were a number to start with.
