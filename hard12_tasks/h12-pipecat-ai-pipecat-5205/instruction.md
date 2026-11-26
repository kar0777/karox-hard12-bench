You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

expand_units always emits the plural unit, so a quantity of one reads as plural

## Description

`expand_units` always emits the plural spoken form, so a quantity of exactly one is read out with a plural unit: `"Only 1km left"` becomes `"Only 1 kilometers left"`.

`_UNIT_MAP` in `src/pipecat/utils/text/transforms/units.py` stores a single plural string per abbreviation, and `_replace` substitutes it regardless of the number that matched:

```python
def _replace(match: re.Match) -> str:
    number = match.group(1)
    unit = _UNIT_MAP[match.group(2).lower()]
    return f"{number} {unit}"
```

All 26 abbreviations in `_UNIT_MAP` are affected. `expand_units` is `expand_units: bool = True` in `VoiceFormatter.__init__`, so the plural reaches TTS output in the default configuration.

The sibling transform already handles agreement — `currency.py` picks `unit = singular if n == 1 else plural` from a `(singular, plural)` tuple, so `"$1.00"` reads as `"one dollar"`.

## Reproduction

```python
import asyncio

from pipecat.utils.text.transforms.currency import expand_currency
from pipecat.utils.text.transforms.units import expand_units


async def main():
    for text in ["Only 1km left", "Only 1mi left", "Only 1ft left", "1 lb of flour"]:
        print(repr(text), "->", repr(await expand_units(text, "*")))

    # For contrast, the currency transform agrees correctly:
    print(repr("It costs $1.00"), "->", repr(await expand_currency("It costs $1.00", "*")))


asyncio.run(main())
```

Output on `main` (`b114a36`), Python 3.12:

```
'Only 1km left' -> 'Only 1 kilometers left'
'Only 1mi left' -> 'Only 1 miles left'
'Only 1ft left' -> 'Only 1 feet left'
'1 lb of flour' -> '1 pounds of flour'
'It costs $1.00' -> 'It costs one dollar'
```

## Expected

```
'Only 1km left' -> 'Only 1 kilometer left'
'Only 1mi left' -> 'Only 1 mile left'
'Only 1ft left' -> 'Only 1 foot left'
'1 lb of flour' -> '1 pound of flour'
```

A decimal such as `"1.0km"` should keep the plural (`"1.0 kilometers"`), since that is how it reads in speech.

## Environment

- pipecat `main` at `b114a36`
- Python 3.12, Windows 11

The existing `TestExpandUnits` / `TestExpandUnitsUnambiguous` cases use quantities 5/60/2/3/9, and the two cases that do contain a `1` (`"1 in 5 people"`, `"1 m people voted"`) assert that the ambiguous unit is *not* expanded, so quantity one with a real unit is not currently covered.

I have a fix and tests ready and will open a PR.

