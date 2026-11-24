You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Genelic type statement is not supported

The following code works:

```python
from serde import serde

type Point = tuple[float, float]
type Polygon = tuple[Point, ...]


@serde
class Figure:
    name: str
    polygon: Polygon


def main() -> None:
    fig = Figure("test", ((0.0, 0.0), (1.0, 1.73), (-1.0, 1.73)))
    print(fig)


if __name__ == "__main__":
    main()
```

However, the following code, which is essentially the same, does not work:

```python
from serde import serde

type Point[T] = tuple[T, T]
type Polygon[T] = tuple[Point[T], ...]


@serde
class Figure:
    name: str
    polygon: Polygon[float]


def main() -> None:
    fig = Figure("test", ((0.0, 0.0), (1.0, 1.73), (-1.0, 1.73)))
    print(fig)


if __name__ == "__main__":
    main()
```

```
serde.compat.SerdeError: Unsupported type: Polygon
```

If we write the same code using the older syntax that does not use the `type` statement, it will work correctly:

```python
from typing import TypeAlias, TypeVar

from serde import serde

T = TypeVar("T")

Point: TypeAlias = tuple[T, T]
Polygon: TypeAlias = tuple[Point[T], ...]


@serde
class Figure:
    name: str
    polygon: Polygon[float]


def main() -> None:
    fig = Figure("test", ((0.0, 0.0), (1.0, 1.73), (-1.0, 1.73)))
    print(fig)


if __name__ == "__main__":
    main()
```

---

The environment is as follows:

OS: Windows 11
Python: 3.14.7 on uv
pyserde: 0.33.1
beartype: 0.22.9
