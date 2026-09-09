# Floating-point attack

Dette prosjektet er laget for omtrent **2–3 timer selvstendig arbeid**.

Du har allerede sett at en datamaskin ikke kan lagre alle reelle tall nøyaktig. Her skal vi ikke bruke tiden på å se de samme eksemplene én gang til. I stedet skal vi gjøre noe mer aktivt:

> **Vi skal prøve å lure en helt vanlig summeringsalgoritme.**

Først lager du eksempler der algoritmen regner dårlig. Deretter prøver du å forstå **hvorfor** den feiler. Til slutt snur vi problemet: kan du lage en bedre algoritme som tåler angrepene dine?

Det er altså litt som å teste en bro. Først belaster vi den på måter som kan avsløre svakheter. Når vi vet hvor den er svak, kan vi prøve å bygge den bedre.

Du trenger ikke finne «det perfekte angrepet» med én gang. Start enkelt. Kjør kode. Endre ett tall. Kjør igjen. Se hva som skjer.

::: {.callout-tip}
## Hvordan jobbe med siden

Alle kodevinduene er redigerbare.

1. Kjør koden slik den står.
2. Endre noe.
3. Kjør på nytt.
4. Sammenlign resultatene.
5. Prøv å forklare det du ser.

Det er helt greit at de første forsøkene dine **ikke virker**. I dette prosjektet er mislykkede forsøk en del av undersøkelsen.
:::

::: {.callout-important}
## Spilleregler

- Bruk vanlige, endelige Python-`float`-verdier.
- Ikke bruk `nan` eller `inf` i angrepene.
- Når vi trenger en god referanseverdi, bruker vi `math.fsum`.
- Ikke bruk `math.fsum` inne i selve angreps- eller forsvarsalgoritmen.
- Det viktigste er ikke bare å få stor feil, men å kunne **forklare hvorfor** den oppstår.

Du trenger ikke forstå hvordan `math.fsum` er programmert. Her bruker vi den som en målestokk.
:::

## 1. Første angrep: kan du få et tall til å forsvinne?

Tenk deg at du skal summere en liste med tall. Den mest naturlige måten er å starte på null og legge til ett tall om gangen.

Det er akkurat dette funksjonen under gjør:

```{pyodide-python}
def ordinary_sum(values):
    # Start med summen 0.
    total = 0.0

    # Legg til ett tall om gangen, fra venstre mot høyre.
    for value in values:
        total = total + value

    return total
```

I eksakt matematikk er dette helt uproblematisk. Men på en datamaskin blir hvert mellomresultat lagret som et nytt flyttall. Hvis to tall har svært forskjellig størrelse, kan et lite bidrag bli for lite til å påvirke det store tallet.

**Det er denne svakheten du skal prøve å utnytte.**

### Oppgave 1 – lag ditt første angrep

Lag en liste `values` slik at `ordinary_sum(values)` gir et tydelig dårligere resultat enn `math.fsum(values)`.

Du trenger ikke mange tall. Tre eller fire kan være nok til et første forsøk.

```{pyodide-python}
import math

# Bytt ut tallene med ditt eget første angrep.
values = [1.0, 2.0, 3.0]

ordinary = ordinary_sum(values)
reference = math.fsum(values)

print("ordinary_sum =", ordinary)
print("referanse    =", reference)
print("absolutt feil=", abs(ordinary - reference))
```

Hvis begge svarene er like, har du ikke ødelagt algoritmen ennå. Bra — endre tallene og prøv igjen.

**Hint hvis du sitter fast:** Hva skjer hvis ett tall er enormt stort og et annet er veldig lite? Hva skjer hvis et stort tall senere trekkes fra igjen?

Når du har et eksempel som virker, stopp et øyeblikk og følg summen **regnetrinn for regnetrinn**.

**Skriv ned:** Hvilke tall brukte du? I hvilket regnetrinn gikk informasjon tapt?

---

## 2. Fra ett triks til en angrepsmaskin

Ett spesielt eksempel viser at noe *kan* gå galt. Men vi vil forstå mer enn det.

Neste mål er derfor å lage en funksjon som kan produsere **mange varianter av samme type problem**.

Hvorfor? Fordi det er lettere å forstå en mekanisme når vi kan skru på den. Hvis feilen blir større når `n` øker, forteller det oss noe. Hvis feilen plutselig forsvinner når `scale` endres, forteller det oss også noe.

Du skal lage en liten «angrepsgenerator»:

```{pyodide-python}
def make_attack(n, scale):
    # n bestemmer hvor stort eksperimentet skal være.
    # scale kan brukes til å styre størrelsesforskjellen mellom tallene.
    #
    # TODO: lag og returner din egen liste.

    values = []

    return values
```

Her bestemmer du selv hva `n` og `scale` skal bety i angrepet ditt. For eksempel kan `n` styre hvor mange små tall du bruker, mens `scale` styrer hvor stort det største tallet er.

Test så generatoren flere ganger:

```{pyodide-python}
import math

for n in [10, 100, 1000]:
    values = make_attack(n, 1e16)

    ordinary = ordinary_sum(values)
    reference = math.fsum(values)
    error = abs(ordinary - reference)

    print(
        f"n={n:5d}   "
        f"ordinary={ordinary:.12g}   "
        f"reference={reference:.12g}   "
        f"error={error:.3e}"
    )
```

::: {.callout-tip}
## Lek med knappene du har laget

Prøv å endre

- **antall tall**,
- **størrelsen på tallene**,
- **fortegn**,
- **rekkefølgen**.

Ikke endre alt samtidig. Endre én ting og se hva den gjør med feilen.
:::

**Mål:** Finn minst tre parameterkombinasjoner som gir tydelig forskjellige feil.

Du trenger ikke skrive en lang forklaring. To–tre setninger er nok: *Hva gjorde angrepet sterkere? Hva gjorde det svakere?*

---

## 3. Nå får angrepet et mål

Så langt har du fått lov til å lage en hvilken som helst sum. Det gjør det ganske lett å produsere rare resultater.

Nå strammer vi inn oppgaven.

Den **riktige summen skal være omtrent 1**.

Det betyr at vi på forhånd vet hva svaret burde være. Din oppgave er å lage data som får den naive algoritmen til å fortelle oss noe annet.

Tenk på dette som et mer kontrollert eksperiment:

> Det riktige svaret er 1. Hvor dårlig kan du få `ordinary_sum` til å oppføre seg?

```{pyodide-python}
import math


def target_attack():
    # TODO: konstruer tallene dine her.
    values = [1.0]
    return values


values = target_attack()
ordinary = ordinary_sum(values)
reference = math.fsum(values)

print("antall tall  =", len(values))
print("ordinary_sum =", ordinary)
print("referanse    =", reference)
print("feil         =", abs(ordinary - reference))
```

Referansen må ligge nær $1$:

$$
|S_{\mathrm{ref}}-1|<10^{-10}.
$$

Bruk maksimalt 10 000 tall.

Start gjerne med å bygge videre på ideen fra oppgave 1. Deretter kan du prøve å forsterke effekten.

::: {.callout-tip}
## Når du har fått det til

Ikke stopp ved første feil.

Kan du få `ordinary_sum` til å gi

- `0.0`?
- feil fortegn?
- et resultat langt fra 1?
- en større feil uten å bruke flere tall?

Du trenger ikke klare alt. Velg én retning og se hvor langt du kommer.
:::

---

## 4. Angrep med hendene bundet

Det er lett å lage ekstreme eksempler hvis vi får bruke hva som helst. Derfor skal vi nå fjerne noen av de enkleste triksene.

Poenget er ikke å gjøre oppgaven vanskelig for vanskelighetens skyld. Vi vil finne ut **hvilken del av angrepet som faktisk skaper problemet**.

### Oppgave 4A – ingen enorme tall

Lag et angrep der alle tall tilfredsstiller

$$
|x_i|\le 10^6.
$$

Nå kan du ikke bare bruke et astronomisk stort tall for å sluke alle små bidrag.

```{pyodide-python}
import math


def bounded_attack():
    # TODO
    values = []
    return values


values = bounded_attack()

# Kontroller regelen.
print("største |x| =", max(abs(x) for x in values) if values else 0.0)

ordinary = ordinary_sum(values)
reference = math.fsum(values)

print("ordinary_sum =", ordinary)
print("referanse    =", reference)
print("absolutt feil=", abs(ordinary - reference))
```

Hvis feilen blir mindre enn før, er det forventet. Spørsmålet er om du fortsatt klarer å lage en **målbar og forklarbar** feil.

### Oppgave 4B – bare positive tall

Nå tar vi bort et annet kraftig våpen: kansellering.

Lag et angrep der

$$
x_i>0
$$

for alle tallene.

```{pyodide-python}
import math


def positive_attack():
    # TODO
    values = []
    return values


values = positive_attack()

print("alle positive =", all(x > 0 for x in values))

ordinary = ordinary_sum(values)
reference = math.fsum(values)

print("ordinary_sum =", ordinary)
print("referanse    =", reference)
print("absolutt feil=", abs(ordinary - reference))
```

Her kan ikke et stort positivt og et stort negativt tall oppheve hverandre. Hvis informasjon fortsatt går tapt, må det skje på en annen måte.

**Tenk:** Er mekanismen i 4B egentlig den samme som i ditt første angrep, eller har du funnet en ny type svakhet?

---

## 5. Bytt side: fra angriper til forsvarer

Nå kjenner du algoritmen ganske godt. Du har aktivt prøvd å finne situasjoner der den gjør en dårlig jobb.

Det er nyttig kunnskap.

I stedet for å spørre

> «Hvorfor er flyttall så irriterende?»

kan vi nå spørre

> **«Kan vi organisere beregningen på en smartere måte?»**

Vi beholder de samme tallene og den samme matematiske summen. Det eneste du får lov til å endre først, er **rekkefølgen**.

```{pyodide-python}
def defense_order(values):
    # Lag en kopi slik at originaldataene ikke endres.
    reordered = list(values)

    # TODO: bestem en bedre rekkefølge.

    return reordered
```

Test forsvaret mot et av dine egne angrep:

```{pyodide-python}
import math

values = target_attack()
reference = math.fsum(values)

before = ordinary_sum(values)
defended_values = defense_order(values)
after = ordinary_sum(defended_values)

print("referanse       =", reference)
print("før forsvar     =", before)
print("feil før        =", abs(before - reference))
print()
print("etter forsvar   =", after)
print("feil etter      =", abs(after - reference))
```

Prøv minst **tre ideer** før du bestemmer deg.

For eksempel kan du undersøke:

- små tall først,
- store tall først,
- sortering etter absoluttverdi,
- positive og negative tall hver for seg.

Dette er hypoteser, ikke fasit. En strategi som høres smart ut, kan være god på ett datasett og dårlig på et annet.

::: {.callout-note}
## Hva er egentlig målet?

Vi prøver ikke å finne en magisk rekkefølge som alltid er perfekt.

Vi prøver å forstå hvordan **algoritmen** påvirker resultatet, selv om den matematiske summen er uendret.
:::

---

## 6. Tournament: tåler forsvaret flere angrep?

Hvis du bare tester forsvaret mot datasettet du brukte da du laget det, er det lett å lure deg selv.

Derfor trenger vi en liten turnering.

Vi lar samme forsvar møte flere forskjellige angrep:

1. ditt beste frie angrep,
2. angrepet med begrenset størrelse,
3. angrepet med bare positive tall.

```{pyodide-python}
import math

attacks = {
    "target": target_attack(),
    "bounded": bounded_attack(),
    "positive": positive_attack(),
}

print(
    f"{'datasett':12s} "
    f"{'naiv feil':>14s} "
    f"{'forsvart feil':>16s}"
)
print("-" * 46)

for name, values in attacks.items():
    reference = math.fsum(values)

    naive = ordinary_sum(values)
    defended = ordinary_sum(defense_order(values))

    naive_error = abs(naive - reference)
    defended_error = abs(defended - reference)

    print(
        f"{name:12s} "
        f"{naive_error:14.6e} "
        f"{defended_error:16.6e}"
    )
```

Se på tabellen som et lite eksperimentresultat.

- Ble alle datasettene bedre?
- Ble ett mye bedre og et annet litt dårligere?
- Finnes det et angrep som forsvaret ditt nesten ikke hjelper mot?

::: {.callout-warning}
## Hvis forsvaret taper

Det er ikke nødvendigvis et mislykket prosjekt.

Et forsvar som hjelper i én situasjon og skader i en annen er et **interessant numerisk resultat**. Finn ut hva som er forskjellig mellom datasettene.
:::

Når du er fornøyd, prøv gjerne å lage et nytt datasett som er spesielt designet for å **slå ditt eget forsvar**. Da er du både angriper og forsvarer samtidig.

---

## 7. Bonus – kan selve algoritmen bli bedre?

Til nå har `ordinary_sum` alltid gjort det samme: én lang kjede av addisjoner. Vi har bare flyttet rundt på inputen.

Men vi kan gå lenger.

I stedet for

$$
(((x_1+x_2)+x_3)+\cdots)+x_n
$$

kan vi for eksempel kombinere tall i mindre grupper og deretter kombinere gruppene.

Du trenger ikke løse denne delen for å fullføre prosjektet. Men hvis du har tid, er dette et naturlig neste steg.

```{pyodide-python}
def better_sum(values):
    # TODO: design din egen summeringsalgoritme.
    # Ikke bruk sum(), numpy.sum() eller math.fsum().

    total = 0.0
    for value in values:
        total += value

    return total
```

Test den mot datasettene fra turneringen:

```{pyodide-python}
import math

for name, values in attacks.items():
    reference = math.fsum(values)
    result = better_sum(values)

    print(
        f"{name:12s}   "
        f"resultat={result:.12g}   "
        f"feil={abs(result-reference):.3e}"
    )
```

Hvis du lager en algoritme som gjør det bedre enn `ordinary_sum` på flere av angrepene dine, har du i praksis gjort det numerisk analyse handler mye om: du har gått fra en matematisk oppgave til å tenke på **hvordan den bør beregnes**.

---

## 8. Hva har du egentlig funnet ut?

Du trenger ikke levere en lang rapport. Men før du avslutter, bør du kunne forklare historien i eksperimentet ditt med egne ord.

Bruk disse spørsmålene som sjekkliste:

1. Hva var det sterkeste angrepet ditt?
2. Hvor i beregningen gikk informasjon tapt?
3. Hvilken rolle spilte størrelsesforskjeller mellom tallene?
4. Hva skjedde da du forbød store tall?
5. Hva skjedde da du bare fikk bruke positive tall?
6. Hvilken forsvarsstrategi fungerte best?
7. Fantes det et datasett der forsvaret ditt gjorde resultatet dårligere?
8. Hvorfor kan to algoritmer som matematisk beregner samme sum gi forskjellige svar på en datamaskin?

::: {.callout-important}
## Hovedideen

En matematisk formel forteller **hva** vi ønsker å beregne.

En algoritme bestemmer **hvordan** datamaskinen faktisk gjør beregningen.

Når tallene lagres med endelig presisjon, kan dette skillet være avgjørende.

Det er nettopp derfor vi bryr oss om numeriske metoder.
:::
