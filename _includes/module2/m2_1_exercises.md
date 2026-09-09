#### Følg de tre første stegene

::: {#fixed-point-numerical-iteration-context .math-exercise-context}

Her skal du følge den samme oppdateringsregelen steg for steg. I en fikspunktiterasjon beregnes hvert nytt ledd fra leddet rett før:

$$
x_{n+1}=g(x_n).
$$

Startverdien $x_0$ er utgangspunktet og teller ikke som en utført iterasjon. Første steg gir $x_1=g(x_0)$, andre steg gir $x_2=g(x_1)$, og tredje steg gir $x_3=g(x_2)$.

I denne oppgaven er

$$
g(x)=\sqrt[3]{1-x}
$$

Når uttrykket under rottegnet er negativt, skal den reelle kubikkroten brukes. Behold flere desimaler i mellomregningene, slik at tidlig avrunding ikke forplanter seg gjennom de neste stegene. Avrund bare $x_3$ til tre desimaler.

:::

```{math-exercise}
#| label: fixed-point-three-iterations
#| caption: Tre fikspunktiterasjoner
#| mode: numeric
#| tolerance: 5e-4
#| field-labels: x_3 avrundet til tre desimaler
#| context: fixed-point-numerical-iteration-context

Bruk iterasjonen

$$
x_{n+1}=\sqrt[3]{1-x_n},\qquad x_0=0.5.
$$

Utfør tre iterasjoner. Oppgi $x_3$ avrundet til tre desimaler.

Svarformat: Skriv ett desimaltall med punktum som desimalskilletegn, for eksempel `0.625`.

$$x_3\approx$$ _[0.742]
```
