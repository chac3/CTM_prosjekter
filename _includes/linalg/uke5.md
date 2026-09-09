::: {.panel-tabset}

## Oversikt

### Først et eksperiment

Vi begynner med en diagonaliserbar matrise som har en enkel dominant egenverdi $\lambda_1$, det vil si $|\lambda_1|>|\lambda_2|\ge\cdots$. For en startvektor med en ikke-null komponent i egenretningen til $\lambda_1$ vil de normaliserte iteratene i potensmetoden nærme seg denne egenretningen. Fortegnet kan alternere dersom $\lambda_1<0$, så det er retningen—ikke nødvendigvis selve vektoren—som stabiliserer seg.

Studentene plotter komponenter, vinkelen mellom retningene, Rayleigh-kvotienten og egenresidualen $\lVert Ax_k-\rho_kx_k\rVert_2$. Vi endrer deretter spektralgapet, velger en startvektor uten komponent i den dominante egenretningen og prøver to egenverdier med samme største absoluttverdi. Slik blir forutsetningene for potensmetoden synlige i stedet for skjult i formuleringen «gjentatt multiplikasjon stabiliserer seg».

### Begreper vi trenger

- egenverdier og egenvektorer
- invariante retninger og underrom
- dominant egenverdi
- spektralgap og konvergensfart
- symmetriske matriser og ortogonale egenvektorer

### Algoritmer og numeriske undersøkelser

- potensmetoden
- Rayleigh-kvotient og egenverdiresidual
- konvergensplott og stoppkriterier
- PageRank som egenvektorproblem

### Etter denne uken

Studentene skal kunne tolke egenvektorer som invariante retninger, implementere potensmetoden og angi sentrale konvergensbetingelser. En liten egenresidual viser at paret er en god approksimativ egenløsning, men identifiserer ikke alene hvilken egenverdi som er funnet eller hvor nær egenvektoren er når problemet er følsomt.

## Aktivitetsplan

1. **En retning vokser fram:** Kjør normalisert gjentatt matrisemultiplikasjon fra flere tilfeldige startvektorer.
2. **Mål stabiliseringen:** Plott vinkelendring, Rayleigh-kvotient og residualen $\lVert Ax_k-\lambda_kx_k\rVert$.
3. **Forklar mønsteret:** Introduser egenverdier, egenvektorer, invariante retninger og dominant egenverdi.
4. **Hva bestemmer farten?** Sammenlign matriser med stort og lite spektralgap og knytt observasjonen til konvergensplottet.
5. **Når virker det ikke?** Undersøk uheldig startvektor, negativ dominant egenverdi og to dominante egenverdier med samme absoluttverdi.
6. **PageRank-laboratorium:** Bygg en kolonnestokastisk overgangsmatrise fra en liten graf. Behandle hengende noder eksplisitt. Med en positiv teleporteringsvektor og dempingsfaktor $0<\alpha<1$ blir Google-matrisen positiv og har en entydig positiv stasjonær sannsynlighetsvektor.
7. **Kort leveranse:** En implementasjon av potensmetoden med stoppkriterium og en diagnose av ett problemtilfelle.

:::
