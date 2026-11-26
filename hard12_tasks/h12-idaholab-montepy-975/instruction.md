You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

🎉500 Issues🎉 The 'xM' shortcut can fail to parse

**Describe the bug**

![image](https://github.com/user-attachments/assets/7c9aaeed-8ebc-4184-a8f7-2a31018ce8b7)

Parsing the `XM` shortcut in a `U` (Universe) input leads to `node` being `None`

**To Reproduce**


``` python
montepy.read_input("testi.i")
```

**Error Message**


``` python
Traceback (most recent call last):
  File "./badinterp/mwe.py", line 2, in <module>
    deck = montepy.read_input("testi.i")
  File "./badinterp/montepy/input_parser/input_reader.py", line 29, in read_input
    problem.parse_input(replace=replace)
  File "./badinterp/montepy/mcnp_problem.py", line 272, in parse_input
    obj = obj_parser(input)
  File "./badinterp/montepy/data_inputs/data_parser.py", line 46, in parse_data
    return data_class(input)
  File "./badinterp/montepy/data_inputs/universe_input.py", line 44, in __init__
    node.is_negatable_identifier = True
AttributeError: 'NoneType' object has no attribute 'is_negatable_identifier'
```

**MCNP input file snippet**

```
MCNP Test Model
C Cells
C Graveyard
99    0 +1010
C Seven spheres within a sphere
1 1 -10 -1001
2 1 -10 -1002
3 1 -10 -1003
4 1 -10 -1004
5 1 -10 -1005
6 1 -10 -1006
7 1 -10 -1007
8     0 -1010  1001  1002  1003  1004  1005  1006  1007

C surfaces
1001 SO      0.1
1002 SX -1.1 0.1
1003 SX +1.1 0.1
1004 SY -1.1 0.1
1005 SY +1.1 0.1
1006 SZ -1.1 0.1
1007 SZ +1.1 0.1
1010 SO 3

C data
C mX fails to parse
C     _ 1  2 10 _ 3 21 21
U     J 1 2M 5M J 3 7M 1M
C materials
C UO2 5 atpt enriched
m1        92235.80c           5
          92238.80c          95
C execution
ksrc 0 0 0
kcode 100000 1.000 50 1050
mode n p

```

**Version**

 - Version 0.2.10 - 0.3.3


**Additional context**

Other shortcut issues: #397, #489, and #499 

This one appears to be just a code bug, rather than a problem with shortcut expansions.
