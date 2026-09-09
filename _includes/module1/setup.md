<!--
Shared Week 1 prerequisites.

This duplication is intentional: the same implementations remain visible in
the teaching material, while this hidden setup cell makes every section usable
directly after a page reload. Running a visible implementation simply replaces
the identical definition in the shared Python session.
-->

```{pyodide-python}
#| context: setup

import math
import struct
import sys
from fractions import Fraction

import matplotlib.pyplot as plt


def normalized_binary_integer(n):
    if n <= 0:
        raise ValueError("Bruk et positivt heltall.")

    bits = bin(n)[2:]
    exponent = len(bits) - 1

    if len(bits) == 1:
        normalized = "1.0"
    else:
        normalized = bits[0] + "." + bits[1:]

    return bits, normalized, exponent


def naive(x):
    return math.sqrt(1 + x) - 1


def stable(x):
    return x / (math.sqrt(1 + x) + 1)
```
