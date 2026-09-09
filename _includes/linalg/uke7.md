::: {.panel-tabset}

## Oversikt

### Først et eksperiment

Vi leser et gråtonebilde som en matrise, beregner SVD og rekonstruerer bildet med én, fem, ti og flere singulære komponenter. God kompresjon er ikke garantert: den lykkes når singulærverdiene avtar raskt. Studentene ser derfor både rekonstruksjonene og kurven av singulærverdier før de foreslår en trunkeringsrang.

For $A=U\Sigma V^T$ er de høyre singulærvektorene inputretninger. En retning $v_i$ avbildes til $\sigma_i u_i$; retninger med $\sigma_i=0$ utgjør nullrommet. De venstre singulærvektorene med $\sigma_i>0$ spenner kolonnerommet. Den trunkerte SVD-en med rang $k$ er, etter Eckart–Young–Mirsky-teoremet, en beste rang-$k$-approksimasjon i både 2-normen og Frobenius-normen. Dermed samler SVD rom, ortogonalitet, rang, minste kvadrater og følsomhet i én faktorisering.

### Begreper vi trenger

- venstre og høyre singulærvektorer
- singulærverdier
- numerisk rang og nullrom
- kondisjonstall
- pseudoinvers og minimumsnormløsning
- lavrangsapproksimasjon

### Algoritmer og numeriske undersøkelser

- `numpy.linalg.svd`
- trunkert SVD og kompresjon
- minste kvadrater og pseudoinvers
- følsomhet nær rangtap
- enkel regularisering ved filtrering av små singulærverdier

### Etter denne uken

Studentene skal kunne bruke SVD til å beskrive nullrom og kolonnerom, skille eksakt fra numerisk rang og forklare hvorfor små ikke-null singulærverdier gjør inversjon og minste-kvadraters problemer følsomme. For full kolonnerang er $\kappa_2(A)=\sigma_{\max}/\sigma_{\min}$; for en rangdefekt matrise er det vanlige 2-norm-kondisjonstallet uendelig.

## Aktivitetsplan

1. **Komprimer et bilde:** Beregn SVD og vis rekonstruksjoner med forskjellig rang sammen med lagringsbehovet.
2. **Les spekteret:** Plott singulærverdiene både lineært og logaritmisk, og velg en trunkering ut fra dataene.
3. **Tolk faktorene:** Følg en vektor gjennom $V^T$, $\Sigma$ og $U$ og beskriv rotasjon, skalering og ny orientering.
4. **Finn rommene igjen:** Bruk singulærvektorene til å konstruere basiser for kolonnerom og nullrom og kontroller dem numerisk.
5. **Nær rangtap:** Perturber en matrise med en liten singulærverdi og mål hvordan løsningen av $Ax=b$ endres.
6. **Pseudoinvers og filtrering:** Sammenlign `lstsq`, `pinv` og trunkert SVD på et følsomt minste-kvadraters problem. Gjør toleransen eksplisitt: pseudoinversen behandler singulærverdier under en valgt grense som null, mens trunkering innfører en regulariserende modellbeslutning.
7. **Syntese:** Knytt SVD eksplisitt til rang, ortogonal projeksjon, minste kvadrater, kondisjonering og regularisering.
8. **Kort leveranse:** En kompresjons- eller denoisingrapport med valgt rang, feilmål og faglig begrunnelse.

:::
