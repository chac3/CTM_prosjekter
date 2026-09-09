## Oppgaver

### Programmering: Horners metode

Implementer Horners metode for et generelt polynom 

$$
p(x)=a_0+a_1x+\cdots+a_nx^n.
$$

Listen `a` inneholder koeffisientene i rekkefølgen
`[a0, a1, ..., an]`.

```{py-exercise}
#| label: horner-general
#| caption: Implementer Horners metode
def horner(a, x):
    """Beregn p(x) med Horners metode."""
    result = 0

    # Skriv koden din her

    return result

## TESTS ##
assert horner([1, 3, 0, 2], 2) == 23, "Sjekk et tredjegradspolynom med en nullkoeffisient."
assert horner([-2, 5, 3, -2, 3], 1.5) == 331/16, "Sjekk polynomet fra eksemplet i teksten."
assert horner([7], 100) == 7, "Et konstant polynom skal virke for alle x."
assert horner([0, 0, 1], -3) == 9, "Sjekk fortegn når x er negativ."
assert horner([5, -1, 4, 0, -2], 2) == -13, "Sjekk et fjerdegradspolynom."
assert horner([0, 1], 17) == 17, "Sjekk polynomet p(x)=x."
assert horner([3, -2, 1], 0) == 3, "For x=0 skal konstantleddet returneres."
```
