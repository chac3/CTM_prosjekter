::: {.panel-tabset}

## Oversikt

### Først et eksperiment

Vi lager flere støyfylte målepunkter enn modellen har parametre, og velger dataene slik at $b\notin C(A)$. At systemet er overbestemt gjør det ikke i seg selv inkonsistent; det er plasseringen av $b$ utenfor kolonnerommet som gjør at $Ax=b$ mangler en eksakt løsning.

`numpy.linalg.lstsq` finner en minimizer $x_*$ for $\lVert Ax-b\rVert_2$. Med residualen definert som $r=b-Ax_*$ får vi normalbetingelsen

$$
A^Tr=0,
$$

altså $r\perp C(A)$. Den tilpassede vektoren $Ax_*$ er den ortogonale projeksjonen av $b$ på kolonnerommet. Selve den projiserte vektoren er entydig, mens parametervektoren $x_*$ bare er entydig når kolonnene i $A$ er lineært uavhengige. `lstsq` returnerer en minimumsnormløsning dersom minimizeren ikke er entydig.

### Begreper vi trenger

- indreprodukt, norm og vinkel
- ortogonalitet og ortogonalt komplement
- projeksjon på et underrom
- minste kvadraters metode
- ortogonale og ortonormale basiser

### Algoritmer og numeriske undersøkelser

- klassisk og modifisert Gram–Schmidt
- QR-faktorisering
- minste kvadrater med QR
- sammenligning av normalligningene, QR og `numpy.linalg.lstsq`

### Etter denne uken

Studentene skal kunne formulere et tilpasningsproblem som et minste-kvadraters problem og tolke $Ax_*$ og residualen som en ortogonal oppdeling av $b$. De skal også kunne forklare at normalligningene har kondisjonstall omtrent $\kappa_2(A)^2$ når $A$ har full kolonnerang, mens en stabil QR-metode unngår denne kvadreringen.

## Aktivitetsplan

1. **Et system uten løsning:** Bygg designmatrisen for en linjetilpasning og vis numerisk at ingen parametervektor gir null residual.
2. **Hva betyr «best»?** Sammenlign flere parametervektorer og residualnormer med løsningen fra `numpy.linalg.lstsq`.
3. **Den overraskende testen:** Beregn $A^Tr$ og bruk resultatet til å motivere ortogonal projeksjon på kolonnerommet.
4. **Lag en ortonormal basis:** Implementer klassisk Gram–Schmidt og kontroller $Q^TQ\approx I$.
5. **Bryt algoritmen:** Bruk nesten parallelle kolonner og sammenlign klassisk og modifisert Gram–Schmidt.
6. **Tre løsningsmetoder:** Sammenlign normalligninger, egen QR-implementasjon og `numpy.linalg.lstsq` på en dårlig kondisjonert Vandermonde-matrise.
7. **Kort leveranse:** Et konvergens- eller feildiagram og en begrunnet anbefaling av metode.

:::
