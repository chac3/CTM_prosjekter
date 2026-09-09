## Oppgaver

### Binært heltall til titallssystemet

Regn om det binære tallet til titallssystemet.

```{math-exercise}
#| label: binary-to-decimal
#| caption: Fra binært tall til titallssystemet
#| pool: true
#| mode: equivalent

$$(101101)_2$$

Svar: _[45]

---

$$(110010)_2$$

Svar: _[50]

---

$$(100111)_2$$

Svar: _[39]

---

$$(111001)_2$$

Svar: _[57]

---

$$(1010110)_2$$

Svar: _[86]
```

### Binært tall med brøkdel

Regn om til titallssystemet. Du kan svare med brøk eller desimaltall.

```{math-exercise}
#| label: binary-fraction-to-decimal
#| caption: Binær brøk til titallssystemet
#| pool: true
#| mode: equivalent

$$(101.101)_2$$

Svar: _[45/8]

---

$$(10.011)_2$$

Svar: _[19/8]

---

$$(111.01)_2$$

Svar: _[29/4]

---

$$(1.001)_2$$

Svar: _[9/8]

---

$$(100.111)_2$$

Svar: _[39/8]
```

### Brøkdel fra titallssystemet til binært

Regn om tallet til binært. Skriv **bare sifrene etter binærpunktet**.

```{math-exercise}
#| label: decimal-fraction-to-binary
#| caption: Fra titallsbrøk til binær brøk
#| pool: true
#| mode: string

$$(0.5)_{10}=(0.\ldots)_2$$

Binære sifre: _[1]

---

$$(0.75)_{10}=(0.\ldots)_2$$

Binære sifre: _[11]

---

$$(0.625)_{10}=(0.\ldots)_2$$

Binære sifre: _[101]

---

$$(0.1875)_{10}=(0.\ldots)_2$$

Binære sifre: _[0011]

---

$$(0.8125)_{10}=(0.\ldots)_2$$

Binære sifre: _[1101]
```

### Programmering: binært heltall til titallssystemet

Skriv funksjonen uten å bruke `int(bits, 2)`. Gå gjennom sifrene fra venstre mot høyre og bygg opp verdien.

```{py-exercise}
#| label: binary-string-to-decimal
#| caption: Konverter binært heltall til titallssystemet
#| forbidden-keywords: int
def bin_to_dec(bits):
    """Konverter en streng med 0 og 1 til et heltall."""
    value = 0

    # Skriv koden din her

    return value

## TESTS ##
assert bin_to_dec("0") == 0, "Sjekk tallet 0."
assert bin_to_dec("1") == 1, "Sjekk tallet 1."
assert bin_to_dec("101") == 5, "101₂ skal bli 5."
assert bin_to_dec("101101") == 45, "101101₂ skal bli 45."
assert bin_to_dec("110101") == 53, "110101₂ skal bli 53."
assert bin_to_dec("10000000") == 128, "Sjekk en ren toerpotens."
assert bin_to_dec("11111111") == 255, "Sjekk et tall med bare enere."
```

### Programmering: heltall til binært

Skriv en funksjon som bruker gjentatt divisjon med $2$. Funksjonen skal returnere svaret som en streng. Ikke bruk `bin()`.

```{py-exercise}
#| label: decimal-to-binary-string
#| caption: Konverter heltall til binært
#| forbidden-keywords: bin
def dec_to_bin(n):
    """Konverter et ikke-negativt heltall til en binær streng."""
    if n == 0:
        return "0"

    digits = ""

    # Skriv koden din her

    return digits

## TESTS ##
assert dec_to_bin(0) == "0", "0 skal bli '0'."
assert dec_to_bin(1) == "1", "1 skal bli '1'."
assert dec_to_bin(5) == "101", "5 skal bli '101'."
assert dec_to_bin(13) == "1101", "13 skal bli '1101'."
assert dec_to_bin(45) == "101101", "45 skal bli '101101'."
assert dec_to_bin(53) == "110101", "53 skal bli '110101'."
assert dec_to_bin(255) == "11111111", "255 skal bli åtte enere."
```
