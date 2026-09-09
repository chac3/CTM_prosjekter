::: {.panel-tabset}

## Oversikt

### Først et eksperiment

Vi bygger et diskret én-dimensjonalt Poisson-problem og løser først systemet som en tett matrise med `numpy.linalg.solve`. Når dimensjonen økes, måler studentene tid og minnebruk. Konklusjonen skal ikke være at alle direkte metoder skalerer dårlig: denne matrisen er tridiagonal, og en strukturutnyttende direkte algoritme kan løse systemet i $O(n)$ operasjoner og $O(n)$ minne. Poenget er at algoritme og datalagring må passe til strukturen.

Deretter ser vi på situasjoner der bare matrise-vektor-produktet er tilgjengelig eller der en iterativ metode er hensiktsmessig. For en symmetrisk positivt definitt matrise $A$ har

$$
\phi(x)=\frac12x^TAx-b^Tx
$$

et entydig globalt minimum i løsningen av $Ax=b$. Med residual $r=b-Ax$ er $\nabla\phi(x)=Ax-b=-r$. Dette gir en presis forbindelse mellom lineær løsning, residual og minimering.

### Begreper vi trenger

- symmetrisk positivt definitte matriser
- kvadratisk energi og minimering
- residual og løsningsfeil
- konjugerte retninger
- kondisjonering og skalering

### Algoritmer og numeriske undersøkelser

- Cholesky-faktorisering
- Gauss–Seidel som koordinatvis korreksjon
- bratteste nedstigning
- konjugerte gradienter
- enkel diagonal prekondisjonering

### Etter denne uken

Studentene skal kunne kontrollere symmetri og bruke Cholesky-faktorisering som en praktisk test for positiv definitet. De skal knytte løsning av $Ax=b$ til minimering av $\phi$, implementere konjugerte gradienter for SPD-matriser og vite at CG i eksakt aritmetikk terminerer etter høyst $n$ steg. I flyttallsaritmetikk bestemmes den praktiske konvergensen blant annet av spekteret og kondisjoneringen.

## Aktivitetsplan

1. **Et voksende problem:** Bygg Poisson-matrisen for flere dimensjoner og mål kjøretiden til `numpy.linalg.solve`.
2. **Se strukturen:** Undersøk symmetri, egenverdier og $x^TAx$ for tilfeldige $x$. Slike prøver kan gi evidens, men beviser ikke positiv definitet; koble dem til Cholesky og den matematiske definisjonen $x^TAx>0$ for alle $x\ne0$.
3. **Løsning som minimum:** Plott nivåkurver av $\phi(x)=\tfrac12x^TAx-b^Tx$ i to dimensjoner og kontroller at gradienten er den negative residualen.
4. **To enkle iterasjoner:** Implementer Gauss–Seidel og bratteste nedstigning. Plott residual, faktisk feil og energi.
5. **Konjugerte gradienter:** Bygg algoritmen trinnvis og sammenlign antall matrise-vektor-produkter med bratteste nedstigning.
6. **Kondisjonering betyr noe:** Kjør samme metoder på to like store systemer med ulike kondisjonstall.
7. **Prekondisjonering:** Bruk Jacobi-prekondisjonering $M=\operatorname{diag}(A)$ i en SPD-kompatibel formulering, og undersøk hvordan spekter og konvergenshistorikk endres. Prekondisjonering garanterer ikke forbedring; virkningen må måles.
8. **Kort leveranse:** Sammenligning av minst tre metoder med en forklaring av når residual og faktisk feil forteller forskjellige historier.

:::
