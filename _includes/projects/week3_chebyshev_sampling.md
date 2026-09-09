# Polynomer i blindsonen

Dette prosjektet er laget for omtrent **4–5 timer selvstendig arbeid**.
Kodeassistenter er tillatt, men du er ansvarlig for at eksperimentene faktisk
svarer på de matematiske spørsmålene.

I uke 3 har vi sett at samme vektorrom kan beskrives med forskjellige basiser.
I eksakt matematikk er dette bare forskjellige koordinater for de samme
objektene. På en datamaskin kan basisvalget likevel få stor betydning.

Vi skal undersøke polynomrommet $\mathcal P_n$. Tenk deg at vi ikke kjenner
hele grafen til et polynom, men bare leser av polynomverdien på $n+1$ steder.
Vi samler avlesningene i en tallkolonne:

$$
E(p)=
\begin{bmatrix}
p(x_0)\\p(x_1)\\\vdots\\p(x_n)
\end{bmatrix}.
$$

Å gå fra et kjent polynom til disse verdiene er vanlig evaluering. Flere
steder i prosjektet går vi motsatt vei: Vi får bare verdiene og prøver å finne
koeffisientene til polynomet som laget dem. Vi kaller denne baklengsprosessen
**reverse engineering** av polynomet.

Prosjektets hovedspørsmål er:

> **Hvordan kan matematisk likeverdige beskrivelser av det samme
> polynomrommet gi svært forskjellige numeriske resultater?**

Du skal gjøre tre kontrollerte sammenligninger. Først arbeider du med lav grad
og eksakt lineær algebra. Deretter endrer du bare basisen. Til slutt holder du
basis fast og endrer bare avlesningspunktene. Ikke bland disse eksperimentene:
Ellers vet du ikke hva som forårsaket forskjellen.

```{pyodide-python}
#| label: project-week3-setup
#| autorun: true
#| context: setup

# Felles verktøy for alle kodecellene i prosjektet. Cellen kjøres
# automatisk og vises ikke på den ferdige siden.
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import polynomial as poly
from numpy.polynomial import chebyshev as cheb
```

:::: {.callout-note}
## Kort manual: polynomer i NumPy

På papir skriver vi for eksempel

$$p(x)=1-2x+0.5x^2+x^3.$$

I Python lagrer vi koeffisientene i samme rekkefølge som leddene over: først
konstantleddet, så koeffisienten foran $x$, deretter koeffisienten foran
$x^2$, og så videre.

```python
a = np.array([1.0, -2.0, 0.5, 1.0])
```

`np.array` lager her bare en talliste som NumPy kan regne med.

Her betyr altså `a[0]` konstantleddet $1$, `a[1]` betyr $-2$, og `a[3]`
betyr koeffisienten $1$ foran $x^3$. For å regne ut $p(0.4)$ skriver vi

```python
poly.polyval(0.4, a)
```

For å regne ut polynomverdien i flere punkter på én gang sender vi inn en
liste eller en NumPy-array:

```python
x = np.array([-1.0, 0.0, 0.4, 1.0])
y = poly.polyval(x, a)
```

Da inneholder `y` de fire tallene $p(-1)$, $p(0)$, $p(0.4)$ og $p(1)$ i
samme rekkefølge. Dette er alt `poly.polyval` gjør: Det setter de oppgitte
$x$-verdiene inn i polynomet.

Senere skriver vi det samme polynomet ved hjelp av
$T_0,T_1,T_2,\ldots$ i stedet for $1,x,x^2,\ldots$. Hvis

$$p(x)=c_0T_0(x)+c_1T_1(x)+c_2T_2(x),$$

lagrer vi tallene som `c = np.array([c_0, c_1, c_2])` og bruker
`cheb.chebval(x, c)`. Forskjellen mellom `poly.polyval` og `cheb.chebval` er
derfor hvilken liste av polynomer koeffisientene hører til.

Vi bruker også to hjelpefunksjoner senere:

- `poly.polyfromroots([r1, r2])` regner ut koeffisientene til
  $(x-r_1)(x-r_2)$;
- `cheb.cheb2poly(c)` skriver et polynom fra $T$-formen om til den vanlige
  formen $a_0+a_1x+a_2x^2+\cdots$.

Bruk funksjonene med prefiksene `poly.` og `cheb.` i dette prosjektet. Ikke
bruk `np.polyval`: Den forventer koeffisientene i motsatt rekkefølge og gjør
det unødvendig lett å få et svar som ser rimelig ut, men er feil.
::::

:::: {.callout-tip}
## Forslag til arbeidsmåte

For hvert hovedeksperiment:

1. Skriv ned hva du tror vil skje.
2. Endre bare én ting.
3. Kjør forsøket og lagre tallene og figuren.
4. Finn hvor forskjellen er størst.
5. Forklar resultatet med begrepene basis, koordinater, rang og nullrom.

Store fargerike figurer er ikke et mål i seg selv. Figuren skal brukes som data
for en matematisk forklaring.
::::

## Innledning: Bli kjent med Chebyshev-polynomene

Chebyshev-polynomene bygges med rekursjonen

$$
T_0(x)=1,\qquad T_1(x)=x,\qquad
T_{n+1}(x)=2xT_n(x)-T_{n-1}(x).
$$

De første polynomene er altså ikke oppgitt ferdig. Bruk rekursjonen til å
regne ut $T_2$, $T_3$ og $T_4$ for hånd. Samle ledd med samme potens av $x$.

### Oversett rekursjonen fra papir til Python

Funksjonen under er en direkte oversettelse av definisjonen. Før du kjører,
følg kallene som trengs for å beregne $T_4(0.3)$, og forklar hvilken linje som
svarer til hvert av de tre tilfellene i den matematiske definisjonen.

```{pyodide-python}
import numpy as np
import matplotlib.pyplot as plt


def chebyshev_recursive(n, x):
    """Beregn T_n(x) direkte fra den rekursive definisjonen."""
    if n < 0:
        raise ValueError("n må være et ikke-negativt heltall")
    if n == 0:
        return 1 + 0*x       # TODO: forklar hvorfor 0*x er nyttig for arrays
    if n == 1:
        return x
    return (2*x*chebyshev_recursive(n-1, x)
            - chebyshev_recursive(n-2, x))


for n in range(5):
    print(f"T_{n}(0.3) = {chebyshev_recursive(n, 0.3): .8f}")
```

Kontroller de håndregnede uttrykkene ved å evaluere dem og
`chebyshev_recursive` i minst tre verdier av $x$.

:::: {.callout-note collapse="true"}
## Valgfri utfordring: hvor mye arbeid gjør rekursjonen?

Legg inn en teller i funksjonen og sammenlign antall funksjonskall for
$n=5,10,15$. Nullstill telleren mellom hvert forsøk. Forklar hvorfor den
direkte rekursjonen gjentar stadig flere delberegninger.
::::

Den direkte rekursjonen gjør mange av de samme beregningene flere ganger. Vi
vil dessuten snart trenge mange $T$-polynomer i mange forskjellige
$x$-verdier. Derfor lager vi én tabell som samler alt.

Hvis `x` inneholder fem punkter og vi ber om polynomene fra $T_0$ til $T_4$,
får tabellen fem rader og fem kolonner:

- rad 0 inneholder $T_0(x_0),T_1(x_0),\ldots,T_4(x_0)$;
- rad 1 inneholder de samme fem polynomene regnet ut i $x_1$;
- kolonne 2 inneholder $T_2$ regnet ut i alle de fem punktene.

Når en verdi først er regnet ut, blir den liggende i tabellen og kan brukes
til å lage neste kolonne. Dermed slipper programmet å starte rekursjonen på
nytt hver gang.

```{pyodide-python}
import numpy as np

def chebyshev_table(x, n):
    """Returner en tabell med T_0(x), ..., T_n(x) som kolonner."""
    x = np.asarray(x, dtype=float)
    # En rad hører til én x-verdi. Den siste aksen reserveres for
    # polynomnummeret k: kolonne k inneholder T_k(x).
    table = np.empty(x.shape + (n+1,), dtype=float)
    table[..., 0] = 1.0
    if n >= 1:
        table[..., 1] = x
    # Tabellen tar vare på tidligere resultater. Derfor kan hver ny kolonne
    # bygges fra de to foregående uten å beregne dem på nytt.
    for k in range(1, n):
        table[..., k+1] = 2*x*table[..., k] - table[..., k-1]
    return table


x_test = np.array([-1.0, -0.25, 0.0, 0.4, 1.0])
print(chebyshev_table(x_test, 4))
```

Les den utskrevne tabellen rad for rad. Kontroller for eksempel at første rad
stemmer med $T_k(-1)$ for $k=0,\ldots,4$, og at kolonne 1 er de fem
$x$-verdiene fordi $T_1(x)=x$. Senere bruker vi den samme tabellen når vi vil
regne ut flere lineærkombinasjoner av $T_0,\ldots,T_n$ i de samme punktene.

### Se hvordan polynomene oppfører seg

Før vi bruker Chebyshev-polynomene som regneverktøy, trenger vi et bilde av
hvordan de oppfører seg på intervallet $[-1,1]$. Er de store eller små? Hvor
mange ganger svinger de? Oppfører partalls- og oddetallspolynomene seg ulikt?
Dette blir viktig senere når vi skal forstå hvorfor denne beskrivelsen av et
polynom kan være numerisk gunstig.

En graf består av mange beregnede punkter. Koden lager derfor 1200 jevnt
fordelte $x$-verdier og bruker `chebyshev_table` til å regne ut
$T_0,\ldots,T_8$ i alle sammen. Resultatet `T_plot` har 1200 rader og 9
kolonner. I løkken tegner `T_plot[:, n]` hele kolonnen som hører til $T_n$.

```{pyodide-python}
import numpy as np
import matplotlib.pyplot as plt

x_plot = np.linspace(-1.0, 1.0, 1200)
# Tabellen gjør at vi beregner alle ni kurvene i ett kall. T_plot[:, n]
# betyr: alle x-rader, men bare kolonnen som hører til T_n.
T_plot = chebyshev_table(x_plot, 8)

plt.close("all")
fig, axes = plt.subplots(3, 3, figsize=(8, 6), sharex=True, sharey=True)
for n, ax in enumerate(axes.ravel()):
    ax.plot(x_plot, T_plot[:, n], color="#277da1")
    ax.axhline(0, color="0.75", linewidth=0.8)
    ax.set_title(f"$T_{n}$")
    ax.grid(alpha=0.2)
    ax.set_ylim(-1.15, 1.15)
fig.supxlabel("x")
fig.supylabel("$T_n(x)$")
plt.tight_layout()
plt.show()
```

Undersøk figurene før du leser videre:

1. Hvor store og små blir polynomene på $[-1,1]$, og hva skjer i endepunktene?
2. Hvordan endres nullpunkter, svingninger og symmetri med $n$?
3. Velg én av observasjonene og begrunn den fra rekursjonen.

### Undersøk om Chebyshev-polynomene danner en basis

Den vanlige måten å skrive polynomer i $\mathcal P_4$ på er

$$p(x)=a_0+a_1x+a_2x^2+a_3x^3+a_4x^4.$$

Polynomene $(1,x,x^2,x^3,x^4)$ kalles her **monomialbasis** eller
**potensbasis**. Tallkolonnen $(a_0,a_1,a_2,a_3,a_4)^T$ er koordinatene til
$p$ i denne basisen. For eksempel har $3-2x^2$ koordinatkolonnen

$$\begin{bmatrix}3&0&-2&0&0\end{bmatrix}^T.$$

Vi vil avgjøre om hvert polynom i $\mathcal P_4$ også kan skrives på nøyaktig
én måte som

$$p(x)=c_0T_0(x)+c_1T_1(x)+\cdots+c_4T_4(x).$$

Hvordan kan vi kontrollere om $T_0,\ldots,T_4$ er lineært uavhengige? Vi må
undersøke om det finnes tall $b_0,\ldots,b_4$, ikke alle lik null, slik at

$$
b_0T_0(x)+b_1T_1(x)+\cdots+b_4T_4(x)=0.
$$

Høyresiden betyr **nullpolynomet**: Alle koeffisientene foran
$1,x,x^2,x^3,x^4$ er null. Vi skriver derfor hvert $T_k$ i den kjente
monomialbasisen og setter de fem koeffisientlistene som kolonner i matrisen
`Q`. Da er koeffisientkolonnen til summen over akkurat

$$
Q
\begin{bmatrix}b_0\\b_1\\b_2\\b_3\\b_4\end{bmatrix}.
$$

Polynomsummen er nullpolynomet hvis og bare hvis

$$
Qb=0.
$$

Nå kan vi bruke **rangtesten**. Det er navnet vi bruker på følgende
standardtest fra lineær algebra: En matrise med fem kolonner har fem lineært
uavhengige kolonner akkurat når rangen er 5. Da har ligningen $Qb=0$ bare
løsningen $b=0$.

Dette forklarer også hvorfor uavhengige kolonner betyr uavhengige polynomer:
Hver kolonne er bare koeffisientlisten til ett bestemt $T_k$. Hvis ingen
ikke-triviell kombinasjon av listene gir nullkolonnen, kan heller ingen
ikke-triviell kombinasjon av polynomene gi nullpolynomet.

Til slutt vet vi at $\mathcal P_4$ har dimensjon 5. Fem lineært uavhengige
polynomer i et femdimensjonalt rom fyller hele rommet. Derfor danner de en
basis. Start nå med koeffisientene du fant for hånd, og fyll kolonnene i `Q`.

```{pyodide-python}
# Hver kolonne skal inneholde monomialkoeffisientene til ett T_k.
# Rekkefølgen på radene er 1, x, x^2, x^3, x^4.
Q = np.full((5, 5), np.nan)
# Kolonne k er koeffisientlisten til T_k. Rangtesten undersøker om de fem
# listene, og dermed de fem polynomene, er lineært uavhengige.
Q[:, 0] = [1, 0, 0, 0, 0]  # T_0
Q[:, 1] = [0, 1, 0, 0, 0]  # T_1

# TODO: Fyll kolonne 2, 3 og 4 fra håndregningen.

if np.isnan(Q).any():
    print("Fyll inn de tre siste kolonnene før rangtesten.")
else:
    print("Rang:", np.linalg.matrix_rank(Q))
    print("Diagonal:", np.diag(Q))
```

Kontroller alle kolonnene mot håndregningen. Bestem deretter om
$(T_0,T_1,T_2,T_3,T_4)$ er en basis for $\mathcal P_4$. Begrunnelsen skal
bruke matrisen, ikke bare at figurene ser forskjellige ut.

Hva forteller formen til `Q` om samme spørsmål for
$(T_0,\ldots,T_n)$ ved høyere grad? Formuler en begrunnet regel. Pek på
mønsteret i matrisen; du trenger ikke bevise regelen for alle $n$.

## Del 1: Reverse engineering fra polynomverdier

Vi går tilbake til lav grad før vi gjør store numeriske eksperimenter. La
$p\in\mathcal P_3$, og les av verdien til $p$ i punktene

$$x_0=-1,\qquad x_1=-\frac13,\qquad x_2=\frac13,\qquad x_3=1.$$

Transformasjonen

$$
E(p)=
\begin{bmatrix}
p(x_0)\\p(x_1)\\p(x_2)\\p(x_3)
\end{bmatrix}
$$

sender altså et polynom til fire polynomverdier. Avbildningen er lineær:
Hvis vi dobler polynomet, dobles alle avlesningene, og avlesning av en sum
gir summen av avlesningene:

$$E(2p)=2E(p),\qquad E(p+q)=E(p)+E(q).$$

Det er nettopp denne lineariteten som gjør at hele avlesningsprosessen kan
beskrives med en matrise.

### Bygg avlesningsmatrisene for hånd

Hvis

$$p(x)=a_0+a_1x+a_2x^2+a_3x^3,$$

er den første avlesningen

$$p(x_0)=a_0+a_1x_0+a_2x_0^2+a_3x_0^3.$$

Dermed er første rad i avlesningsmatrisen
$[1,x_0,x_0^2,x_0^3]$. Utled de tre andre radene før du fullfører funksjonen
under.

For de fire punktene i dette prosjektet kan hele håndregningen skrives slik:

$$
\begin{aligned}
p(-1) &= a_0-a_1+a_2-a_3,\\
p(-1/3) &= a_0-\frac13a_1+\frac19a_2-\frac1{27}a_3,\\
p(1/3) &= a_0+\frac13a_1+\frac19a_2+\frac1{27}a_3,\\
p(1) &= a_0+a_1+a_2+a_3.
\end{aligned}
$$

Koeffisientene foran $a_0,a_1,a_2,a_3$ blir radene i matrisen:

$$
\begin{bmatrix}
p(-1)\\p(-1/3)\\p(1/3)\\p(1)
\end{bmatrix}
=
\underbrace{
\begin{bmatrix}
1&-1&1&-1\\
1&-1/3&1/9&-1/27\\
1&1/3&1/9&1/27\\
1&1&1&1
\end{bmatrix}}_{M_{\text{small}}}
\begin{bmatrix}a_0\\a_1\\a_2\\a_3\end{bmatrix}.
$$

Her er et lite eksempel med et førstegradspolynom
$p(x)=a_0+a_1x$. Avlesning i punktene $x_0=-1$ og $x_1=2$ gir

$$
p(x_0)=a_0-a_1,
\qquad
p(x_1)=a_0+2a_1.
$$

Begge ligningene kan samles i ett matriseprodukt:

$$
\begin{bmatrix}p(-1)\\p(2)\end{bmatrix}
=
\begin{bmatrix}1&-1\\1&2\end{bmatrix}
\begin{bmatrix}a_0\\a_1\end{bmatrix}.
$$

Et andre eksempel bruker $p(x)=a_0+a_1x+a_2x^2$ og punktene $0,1,2$:

$$
\begin{bmatrix}p(0)\\p(1)\\p(2)\end{bmatrix}
=
\begin{bmatrix}1&0&0\\1&1&1\\1&2&4\end{bmatrix}
\begin{bmatrix}a_0\\a_1\\a_2\end{bmatrix}.
$$

Se spesielt på siste rad: Den kommer fra
$p(2)=a_0+2a_1+2^2a_2$. Hver rad lages ved å sette ett punkt inn i
$1,x,x^2,\ldots$. Når matrisen multipliseres med koeffisientkolonnen, får vi
én polynomverdi per rad. I Python betyr `A @ a` matriseproduktet $Aa$.

Koden under lager denne matrisen for så mange punkter og potenser som vi ber
om. Uttrykket med `None` er NumPys kompakte måte å kombinere hvert punkt med
hver potens. Bruk de to små matrisene over som fasit når du fullfører linjen.

Chebyshev-matrisen bygges på samme måte, men nå skriver vi

$$p(x)=c_0T_0(x)+c_1T_1(x)+c_2T_2(x)+c_3T_3(x).$$

Ved $x=-1$ får vi $T_0(-1)=1$, $T_1(-1)=-1$, $T_2(-1)=1$ og
$T_3(-1)=-1$. Første rad blir derfor $[1,-1,1,-1]$. Ved $x=-1/3$ gir
uttrykkene du regnet ut tidligere

$$
T_0(-1/3)=1,\quad T_1(-1/3)=-\frac13,\quad
T_2(-1/3)=-\frac79,\quad T_3(-1/3)=\frac{23}{27}.
$$

Andre rad blir dermed $[1,-1/3,-7/9,23/27]$. Regn ut de to siste radene på
samme måte, og kontroller dem mot utskriften fra `chebyshev_matrix`.

```{pyodide-python}
def monomial_matrix(points, n):
    """Avlesningsmatrise for basisen (1, x, ..., x^n)."""
    points = np.asarray(points, dtype=float)
    powers = np.arange(n+1)
    # points[:, None] lager en punktkolonne, og powers[None, :] lager en
    # potensrad. NumPy kombinerer dem til alle x_i**j samtidig.
    # TODO: Erstatt neste linje med uttrykket points[:, None] opphøyd i
    # powers[None, :]. Kontroller resultatet mot minieksemplene over.
    raise NotImplementedError("Fullfør monomial_matrix før du går videre")


def chebyshev_matrix(points, n):
    """Avlesningsmatrise for basisen (T_0, ..., T_n)."""
    # chebyshev_table har allerede riktig design: rad i = punkt x_i og
    # kolonne k = T_k evaluert i alle punktene.
    return chebyshev_table(points, n)


points_small = np.array([-1.0, -1/3, 1/3, 1.0])
M_small = monomial_matrix(points_small, 3)
C_small = chebyshev_matrix(points_small, 3)

print("Monomialbasis:\n", M_small)
print("\nChebyshev-basis:\n", C_small)
print("\nRanger:", np.linalg.matrix_rank(M_small),
      np.linalg.matrix_rank(C_small))
```

Stopp ved de to utskrevne matrisene før du løser et system. Bruk følgende
spørsmål til å knytte tallene til lineær algebra:

1. Avbildningen $E$ tar inn et polynom av grad høyst 3 og gir ut fire tall.
   Skriv derfor definisjonsrommet og verdirommet med symboler. Beskriv også
   med ord hva ett element i hvert av rommene ser ut som.
2. La $a$ være koeffisientkolonnen når $p$ skrives med
   $1,x,x^2,x^3$. Forklar hvorfor `M_small @ a` er det samme som $E(p)$.
   Pek på én bestemt rad og vis regnestykket.
3. La $c$ være koeffisientkolonnen når det samme $p$ skrives med
   $T_0,T_1,T_2,T_3$. Da er `C_small @ c` også $E(p)$. Hvorfor kan
   `M_small` og `C_small` være forskjellige selv om de ender med de samme
   fire polynomverdiene?
4. Begge matrisene har rang 4. Hva sier dette om muligheten for at to
   forskjellige polynomer i $\mathcal P_3$ har de samme fire avlesningene i
   disse fire forskjellige punktene? Knytt svaret til nullrom og entydighet.
5. Koeffisientkolonnene $a$ og $c$ vil vanligvis være forskjellige. Betyr det
   at polynomene er forskjellige, eller bare at det samme polynomet er skrevet
   med forskjellige byggeklosser? Hvordan kan du kontrollere svaret?

### Skriv det samme polynomet i to basiser

Nå prøver vi tankegangen i praksis. Vi starter med et kjent polynom,

$$p(x)=1-2x+\frac12x^2+x^3.$$

Koden regner først ut de fire avlesningene. Deretter later vi som om
koeffisientene er glemt og beholder bare avlesningene. Vi skal altså arbeide
baklengs: Fra noen målte polynomverdier prøver vi å finne ut hvilket polynom
som kan ha laget dem. Vi kaller dette **reverse engineering** av polynomet.

Vi løser to lineære systemer:

$$M_{\text{small}}a=E(p),
\qquad
C_{\text{small}}c=E(p).$$

Hvorfor finner det første systemet monomialkoeffisientene? Kolonne $j$ i
$M_{\text{small}}$ inneholder verdiene til $x^j$ i de fire punktene. Når
matrisen multipliseres med $a$, får vi derfor verdiene til

$$a_0+a_1x+a_2x^2+a_3x^3$$

i de fire punktene. Ligningen $M_{\text{small}}a=E(p)$ ber om akkurat de
tallene $a_0,\ldots,a_3$ som får disse verdiene til å passe med dataene.

På samme måte inneholder kolonne $j$ i $C_{\text{small}}$ verdiene til $T_j$
i punktene. Produktet $C_{\text{small}}c$ gir derfor avlesningene av

$$c_0T_0+c_1T_1+c_2T_2+c_3T_3.$$

Ligningen $C_{\text{small}}c=E(p)$ finner dermed Chebyshev-koeffisientene.
Det er matrisens kolonner som bestemmer hva de ukjente tallene betyr.

Til slutt evaluerer vi begge reverse-engineering-svarene på et tett
rutenett. Hvis de representerer samme polynom, skal grafverdiene stemme selv
om koeffisientlistene ikke gjør det. Kommandoen `np.linalg.solve(A, b)` betyr
bare «finn tallkolonnen $u$ som løser $Au=b$». Den kjenner ikke til polynomer;
tolkningen kommer fra hvordan vi bygde matrisen `A`.

```{pyodide-python}
monomial_true = np.array([1.0, -2.0, 0.5, 1.0])
# Dette er de eneste dataene de to lineære systemene får.
measurements_small = poly.polyval(points_small, monomial_true)

# Begge systemene har formen «avlesningsmatrise @ koordinater = data».
# solve returnerer koordinatene; hvilken basis de tilhører bestemmes av
# matrisen på venstre side.
monomial_recovered = np.linalg.solve(M_small, measurements_small)
chebyshev_recovered = np.linalg.solve(C_small, measurements_small)

print("Avlesninger:", measurements_small)
print("Monomialkoordinater:", monomial_recovered)
print("Chebyshev-koordinater:", chebyshev_recovered)

x_dense = np.linspace(-1, 1, 1001)
p_reference = poly.polyval(x_dense, monomial_true)
p_from_monomials = poly.polyval(x_dense, monomial_recovered)
p_from_chebyshev = cheb.chebval(x_dense, chebyshev_recovered)

print("Største forskjell, monomial:",
      np.max(np.abs(p_from_monomials-p_reference)))
print("Største forskjell, Chebyshev:",
      np.max(np.abs(p_from_chebyshev-p_reference)))
```

Kontroller at de to koordinatvektorene virkelig bygger samme polynom. Skriv
polynomet som en lineærkombinasjon av $T_0,T_1,T_2,T_3$ og sammenlign med
monomialformen.

### Finn det avlesningene ikke kan se

Med fire forskjellige avlesningspunkter kunne vi finne et polynom i
$\mathcal P_3$ entydig. Nå undersøker vi hvorfor «fire tall» ikke alene er
nok: Punktene må også gi fire forskjellige opplysninger. Vi gjør to separate
endringer. Først beholder vi bare tre avlesninger. Deretter bruker vi fire
rader, men gjentar ett punkt. I begge tilfeller forventer vi at rangen blir
mindre enn 4.

Kjør de to endringene under én om gangen:

```{pyodide-python}
# Forsøk A: Fjern den siste avlesningen.
points_three = points_small[:-1]
M_three = monomial_matrix(points_three, 3)

# Forsøk B: Bruk fire plasser, men les av samme punkt to ganger.
points_repeated = np.array([-1.0, -1/3, 1/3, 1/3])
M_repeated = monomial_matrix(points_repeated, 3)

print("Form og rang med tre avlesninger:",
      M_three.shape, np.linalg.matrix_rank(M_three))
print("Form og rang med gjentatt punkt:",
      M_repeated.shape, np.linalg.matrix_rank(M_repeated))
```

En lavere rang betyr at noe ved polynomet er usynlig i avlesningene. Finn et
ikke-null polynom $z\in\mathcal P_3$ som tilfredsstiller

$$z(-1)=z(-1/3)=z(1/3)=0.$$

**Hint ved behov:** Et polynom med nullpunktene $r_1,r_2,r_3$ inneholder
faktorene $(x-r_1)(x-r_2)(x-r_3)$.

Bruk deretter koden under til å kontrollere svaret og lage to forskjellige
polynomer med identiske tre avlesninger:

```{pyodide-python}
# TODO: Utvid produktet du fant, og skriv inn de fire koeffisientene i
# rekkefølgen 1, x, x^2, x^3. NaN-verdiene skal erstattes.
invisible_coefficients = np.full(4, np.nan)
if np.isnan(invisible_coefficients).any():
    raise ValueError("Fyll inn koeffisientene til z før du går videre")

# Biblioteket brukes her bare som en uavhengig kontroll av håndregningen.
coefficients_check = poly.polyfromroots(points_three)
print("Største avvik fra polyfromroots:",
      np.max(np.abs(invisible_coefficients-coefficients_check)))

# Velg selv en synlig skaleringsfaktor.
alpha = 2.0
second_polynomial = monomial_true + alpha*invisible_coefficients

# De to polynomene er forskjellige, men z er null i alle tre punktene.
first_values = poly.polyval(points_three, monomial_true)
second_values = poly.polyval(points_three, second_polynomial)

print("Koeffisienter til z:", invisible_coefficients)
print("Avlesninger av p:       ", first_values)
print("Avlesninger av p+alpha*z:", second_values)
print("Forskjell i avlesningene:", second_values-first_values)

plt.close("all")
plt.plot(x_dense, poly.polyval(x_dense, monomial_true), label="$p$")
plt.plot(x_dense, poly.polyval(x_dense, second_polynomial),
         label="$p+\\alpha z$")
plt.scatter(points_three, first_values, color="black", zorder=3,
            label="Tre avlesninger")
plt.xlabel("x")
plt.ylabel("polynomverdi")
plt.title("Forskjellige polynomer, identiske avlesninger")
plt.grid(alpha=0.25)
plt.legend()
plt.show()
```

Gå gjennom argumentet i disse trinnene:

1. Regn ut $E(z)$ når $E$ bare leser av i de tre punktene. Hvorfor er
   resultatet nullkolonnen selv om $z$ ikke er nullpolynomet? Dette viser at
   $z$ ligger i nullrommet til $E$.
2. Bruk linearitet til å regne ut $E(p+\alpha z)$. Forklar hvorfor alle valg
   av tallet $\alpha$ gir de samme tre avlesningene som $p$.
3. Generaliser til $\mathcal P_n$, som har dimensjon $n+1$. Anta at vi bruker
   $m$ **forskjellige** punkter, at $m<n+1$, og at hvert punkt gir en
   uavhengig betingelse. Hva blir da rangen til avlesningsmatrisen?
4. Bruk rang–nullitet,
   $\dim(\ker E)+\operatorname{rang}(E)=n+1$, til å finne dimensjonen til
   nullrommet. Dette tallet er antallet uavhengige måter et polynom kan endres
   på uten at de $m$ avlesningene merker det.
5. Forklar til slutt hvorfor antakelsen om forskjellige punkter er viktig.
   Hva så du i forsøket der ett punkt ble gjentatt?

## Del 2: Hold punktene fast og bytt basis

Ved grad 3 fant begge matrisene fram til det riktige polynomet. Det kan derfor
se ut som basisvalget bare endrer hvordan koeffisientene skrives. I eksakt
matematikk er det riktig. På en datamaskin må imidlertid alle mellomresultater
lagres med et begrenset antall sifre. Nå spør vi om én skrivemåte kan føre til
større avrundingsproblemer enn den andre når graden øker.

For å gjøre sammenligningen rettferdig bruker vi nøyaktig det samme
referansepolynomet, de samme avlesningspunktene og de samme avlesningsverdiene
i begge systemene. Det eneste som byttes, er kolonnene i matrisen: enten
$1,x,\ldots,x^n$ eller $T_0,T_1,\ldots,T_n$. Hvis resultatene blir ulike, har
vi dermed isolert virkningen av basisvalget.

Vi bruker foreløpig punktene

$$
x_k=\cos\left(\frac{(2k+1)\pi}{2(n+1)}\right),
\qquad k=0,\ldots,n.
$$

Hvorfor disse punktene er interessante, undersøker vi først i del 3. Akkurat
nå trenger du bare å merke deg at funksjonen lager $n+1$ forskjellige tall i
$[-1,1]$, og at begge basisene får de samme tallene.

De tre korte hjelpefunksjonene under gjør forsøket mulig å gjenta:
`chebyshev_points` lager punktene, `reference_coordinates` lager et fast
polynom med små Chebyshev-koeffisienter, og `max_grid_error` måler den største
observerte forskjellen på et tett rutenett.

```{pyodide-python}
def chebyshev_points(n):
    """Returner n+1 cosinusfordelte punkter i intervallet [-1,1]."""
    # P_n har dimensjon n+1, så vi bruker n+1 forskjellige avlesninger.
    k = np.arange(n+1)
    return np.cos((2*k+1)*np.pi/(2*(n+1)))


def reference_coordinates(n):
    """Moderate, deterministiske koordinater i Chebyshev-basis."""
    # En fast formel gir samme referansepolynom hver gang forsøket gjentas.
    # Avtagende koeffisienter hindrer at vi bygger inn store tall med vilje.
    k = np.arange(n+1)
    return (-1.0)**k/(k+1.0)**2


def max_grid_error(values, reference):
    # Maksimum på et tett rutenett er en numerisk måling, ikke et bevis på
    # maksimum over alle reelle x i intervallet.
    return float(np.max(np.abs(values-reference)))
```

Se på formelen i `reference_coordinates` før du kjører grad 30. Alle tallene
$c_k=(-1)^k/(k+1)^2$ ligger mellom $-1$ og $1$. Skriv ned om du tror dette
også tvinger koeffisientene foran $1,x,x^2,\ldots,x^{30}$ til å være små.
Dette er hypotesen som forsøket skal teste.

### Gjør reverse engineering i begge basiser

Funksjonen følger denne historien:

1. Lag et polynom ved å velge Chebyshev-koeffisienter.
2. Regn ut polynomets verdi i $n+1$ punkter. Deretter behandles disse
   avlesningene som de eneste kjente dataene.
3. Gjør reverse engineering: Finn koeffisienter som passer til dataene, først
   i monomialbasis og så i Chebyshev-basis.
4. Regn ut de to reverse-engineering-resultatene i mange punkter mellom
   avlesningene og sammenlign dem med polynomet vi startet med.

Det tette rutenettet brukes bare til etterkontroll. Det gir ikke de lineære
systemene ekstra informasjon.

```{pyodide-python}
def compare_bases(n, grid_size=2001):
    # Det samme polynomet leses av i de samme punktene for begge basiser.
    points = chebyshev_points(n)
    true_chebyshev = reference_coordinates(n)
    measurements = cheb.chebval(points, true_chebyshev)

    # Bare koordinatsystemet endres mellom de to lineære systemene.
    M = monomial_matrix(points, n)
    C = chebyshev_matrix(points, n)

    # Reverse engineering i to basiser: solve finner koeffisientene som gir
    # de oppgitte avlesningene. Svarvektorene kan ikke sammenlignes ledd for
    # ledd fordi basisene er ulike.
    recovered_monomial = np.linalg.solve(M, measurements)
    recovered_chebyshev = np.linalg.solve(C, measurements)

    # Det tette rutenettet gir ingen nye data til systemet. Det brukes bare
    # til å sammenligne de to ferdige polynomene mellom avlesningspunktene.
    grid = np.linspace(-1.0, 1.0, grid_size)
    reference = cheb.chebval(grid, true_chebyshev)
    from_monomials = poly.polyval(grid, recovered_monomial)
    from_chebyshev = cheb.chebval(grid, recovered_chebyshev)

    return {
        "n": n,
        "points": points,
        "measurements": measurements,
        "grid": grid,
        "reference": reference,
        "monomial_values": from_monomials,
        "chebyshev_values": from_chebyshev,
        "monomial_coordinates": recovered_monomial,
        "chebyshev_coordinates": recovered_chebyshev,
        "monomial_error": max_grid_error(from_monomials, reference),
        "chebyshev_error": max_grid_error(from_chebyshev, reference),
    }


basis_data = compare_bases(30)
print("Grad:", basis_data["n"])
print("Største |monomialkoordinat|:",
      np.max(np.abs(basis_data["monomial_coordinates"])))
print("Største |Chebyshev-koordinat|:",
      np.max(np.abs(basis_data["chebyshev_coordinates"])))
print("Maksfeil med monomialbasis:", basis_data["monomial_error"])
print("Maksfeil med Chebyshev-basis:", basis_data["chebyshev_error"])
```

Finn selv rutenettspunktet der hver av de to feilene er størst. Bruk
`np.argmax` på absoluttverdien av feilen, og rapporter både $x$-verdien og
feilen. `np.argmax` gir plassnummeret til det største tallet, ikke selve
tallet. Bruk derfor det samme plassnummeret til å hente både punktet fra
`basis_data["grid"]` og feilen fra feillisten. Dette er et nytt mål du skal
beregne; det er ikke ferdigkodet over.

Ikke gå direkte videre. Les tallene i denne rekkefølgen:

1. Bekreft i koden at `measurements` lages én gang og brukes på høyre side i
   begge systemene. Hva forteller det om dataene de to metodene får?
2. Sammenlign den største koeffisienten i de to listene. Hvor mange
   tierpotenser skiller dem? Husk at koeffisientene hører til forskjellige
   polynomer i basislistene og derfor ikke skal sammenlignes ledd for ledd.
3. Sammenlign feilene på rutenettet. Hvor ligger maksimumsfeilen du fant med
   `np.argmax`?
4. Forklar hva som ble holdt fast: polynomrom, referansepolynom,
   avlesningspunkter og avlesningsverdier. Hva var den eneste endringen?
5. I eksakt matematikk er begge basisskrivemåtene likeverdige. Hvilken del av
   forskjellen i utskriften skyldes derfor flyttallsregning?

### Valgfri utvidelse: se hva som skjer når graden øker

```{pyodide-python}
degrees = [3, 10, 20, 25, 30]
basis_results = [compare_bases(n) for n in degrees]

print(f"{'grad':>5} {'maks |a_k|':>16} {'maks |c_k|':>16} "
      f"{'feil monomial':>18} {'feil Chebyshev':>18}")
print("-"*79)
for data in basis_results:
    print(f"{data['n']:5d} "
          f"{np.max(np.abs(data['monomial_coordinates'])):16.4e} "
          f"{np.max(np.abs(data['chebyshev_coordinates'])):16.4e} "
          f"{data['monomial_error']:18.4e} "
          f"{data['chebyshev_error']:18.4e}")
```

Lag en logaritmisk feilfigur for grad 30:

```{pyodide-python}
grid = basis_data["grid"]
error_monomial = np.abs(
    basis_data["monomial_values"]-basis_data["reference"]
)
error_chebyshev = np.abs(
    basis_data["chebyshev_values"]-basis_data["reference"]
)

tiny = np.finfo(float).tiny
plt.close("all")
plt.semilogy(grid, np.maximum(error_monomial, tiny),
             label="Monomialbasis")
plt.semilogy(grid, np.maximum(error_chebyshev, tiny),
             label="Chebyshev-basis")
plt.xlabel("x")
plt.ylabel("absolutt feil")
plt.title("Samme polynom og samme avlesningspunkter")
plt.grid(alpha=0.25)
plt.legend()
plt.show()
```

Skriv en foreløpig forklaring. Bruk minst disse observasjonene:

- størrelsen på koordinatene;
- størrelsen på basisfunksjonene på $[-1,1]$;
- at et moderat sluttresultat kan bygges ved at store ledd nesten kansellerer;
- at hvert mellomresultat lagres med endelig presisjon.

Ikke skriv at «datamaskinen er unøyaktig» uten å identifisere hvilke tall som
er store, og hvor kanselleringen oppstår.

### Legg den samme lille feilen til begge systemene

Virkelige avlesninger er sjelden eksakte. Vi legger derfor til en svært liten
feil, omtrent $10^{-10}$, i hver polynomverdi. Først løser vi systemet med de
opprinnelige dataene, deretter med de litt endrede dataene. Vi gjør dette i
begge basiser med nøyaktig den samme feillisten. Spørsmålet er hvor mye en
liten målefeil påvirker reverse engineering av koeffisientene.

Vi sammenligner `a_after-a_before` fordi begge vektorene bruker
monomialbasis. Tilsvarende sammenligner vi `c_after-c_before` fordi begge
bruker Chebyshev-basis. Derimot ville `a_after-c_after` ikke hatt en enkel
betydning: Plass nummer 2 står foran $x^2$ i den ene listen og foran $T_2$ i
den andre.

```{pyodide-python}
n = 30
points = chebyshev_points(n)
true_chebyshev = reference_coordinates(n)
measurements = cheb.chebval(points, true_chebyshev)

rng = np.random.default_rng(2026)
# Fast startverdi gjør forsøket reproduserbart: alle får nøyaktig samme
# forstyrrelse når cellen kjøres på nytt.
measurement_noise = 1e-10*rng.standard_normal(n+1)

M = monomial_matrix(points, n)
C = chebyshev_matrix(points, n)

a_before = np.linalg.solve(M, measurements)
a_after = np.linalg.solve(M, measurements+measurement_noise)
c_before = np.linalg.solve(C, measurements)
c_after = np.linalg.solve(C, measurements+measurement_noise)

# Normen samler endringene i hele koordinatvektoren til ett tall. Vi
# sammenligner før og etter innen samme basis, ikke koeffisienter på tvers.
print("Største endring i avlesning:", np.max(np.abs(measurement_noise)))
print("Endring i monomialkoordinater:", np.linalg.norm(a_after-a_before))
print("Endring i Chebyshev-koordinater:", np.linalg.norm(c_after-c_before))
```

Bruk denne forklaringen til å tolke de tre utskrevne tallene. Hvor stor var
endringen i selve dataene? Hvor stor ble endringen i hver koeffisientliste?
Hvilken representasjon forsterket den lille dataendringen mest?

## Del 3: Hold basisen fast og flytt punktene

I del 2 holdt vi punktene fast og byttet basis. Nå gjør vi det motsatte:
Chebyshev-basis brukes i begge systemene, men avlesningspunktene flyttes.
Spørsmålet er om $n+1$ avlesninger alltid er like informative, eller om
plasseringen av dem betyr noe for hva polynomet kan gjøre mellom punktene.

De to punktfamiliene er

$$
x_k^{\mathrm{jevn}}=-1+\frac{2k}{n}
$$

og

$$
x_k^{\mathrm{Cheb}}
=\cos\left(\frac{(2k+1)\pi}{2(n+1)}\right),
$$

for $k=0,\ldots,n$.

### Sammenlign punktplasseringene før du regner

Før vi løser et eneste system, tegner vi bare punktene på en tallinje. De
jevne punktene har samme avstand overalt. Cosinuspunktene ligger tettere ved
endene av intervallet og glisnere nær midten. Figuren skal hjelpe deg å lage
en hypotese: Hvis et polynom er tvunget til å passe data i mange punkter nær
endene, blir det da lettere eller vanskeligere for polynomet å få store
utslag der mellom avlesningene?

```{pyodide-python}
n = 30
equal_points = np.linspace(-1.0, 1.0, n+1)
cheb_points = chebyshev_points(n)

# Punktene tegnes på hver sin tallinje før løsing. Figuren kontrollerer den
# variabelen vi skal endre: punktplasseringen.
plt.close("all")
fig, axes = plt.subplots(2, 1, figsize=(8, 2.5), sharex=True)
axes[0].scatter(equal_points, np.zeros_like(equal_points), marker="|", s=180)
axes[0].set_title("Like langt mellom avlesningspunktene")
axes[1].scatter(cheb_points, np.zeros_like(cheb_points), marker="|", s=180,
                color="#d98900")
axes[1].set_title("Cosinusfordelte avlesningspunkter")
for ax in axes:
    ax.set_yticks([])
    ax.grid(axis="x", alpha=0.2)
axes[1].set_xlabel("x")
plt.tight_layout()
plt.show()
```

Hvor er punktavstanden størst og minst i hvert oppsett? Hvilket oppsett ville
du valgt dersom du var spesielt redd for at polynomet skulle gjøre noe
uventet nær $-1$ eller $1$? Skriv hypotesen før forsøket med forstyrrelser.

### Bruk den samme lille feilen med begge punktsettene

Vi forstyrrer avlesningene med det faste mønsteret

$$\delta y_k=10^{-10}(-1)^k.$$

Det er viktig at både størrelsen og fortegnsmønsteret er identisk i de to
forsøkene. Dermed kan ikke forskjellen forklares med at det ene forsøket fikk
en større eller mer gunstig feil.

Funksjonen lager først nøyaktige avlesninger fra referansepolynomet. Deretter
legger den til feilen og gjør reverse engineering: Den finner det ene
polynomet av grad høyst $n$ som passer til de forstyrrede verdiene. Til slutt
sammenlignes dette polynomet med referansen på 5001 punkter. Forholdet

$$
\frac{\text{største feil på det tette rutenettet}}
{\text{største feil i de oppgitte avlesningene}}
$$

kalles her **forsterkning**. En forsterkning på $10^6$ betyr at en feil på
$10^{-10}$ ved avlesningspunktene har blitt til en feil på omtrent $10^{-4}$
et sted mellom dem.

```{pyodide-python}
def point_placement_experiment(n, points, noise_size=1e-10,
                               grid_size=5001):
    # Lag de nøyaktige avlesningene fra ett fast referansepolynom.
    true_coordinates = reference_coordinates(n)
    measurements = cheb.chebval(points, true_coordinates)
    # Det samme fortegnsmønsteret brukes uansett hvor punktene ligger.
    noise = noise_size*(-1.0)**np.arange(n+1)

    # Reverse engineering: Finn koeffisientene til polynomet som passer til
    # de litt forstyrrede avlesningene.
    C = chebyshev_matrix(points, n)
    recovered = np.linalg.solve(C, measurements+noise)

    # Sammenlign med referansepolynomet også mellom avlesningspunktene. Det
    # tette rutenettet påvirker ikke løsningen; det fungerer som måleinstrument.
    grid = np.linspace(-1.0, 1.0, grid_size)
    reference = cheb.chebval(grid, true_coordinates)
    perturbed = cheb.chebval(grid, recovered)
    error = perturbed-reference

    return {
        "n": n,
        "points": points,
        "noise": noise,
        "grid": grid,
        "error": error,
        "max_data_error": float(np.max(np.abs(noise))),
        "max_curve_error": float(np.max(np.abs(error))),
    }


equal_data = point_placement_experiment(
    n, equal_points, noise_size=1e-10
)
cheb_data = point_placement_experiment(
    n, cheb_points, noise_size=1e-10
)

for name, data in [("Jevne punkter", equal_data),
                   ("Cosinusfordelte punkter", cheb_data)]:
    amplification = data["max_curve_error"]/data["max_data_error"]
    print(f"{name:27s}",
          f"feil i avlesning={data['max_data_error']:.3e}",
          f"kurvefeil={data['max_curve_error']:.3e}",
          f"forsterkning={amplification:.3e}")
```

Sammenlign først `feil i avlesning` i de to utskriftene: De skal være like.
Sammenlign så `kurvefeil` og `forsterkning`. Hvor mange tierpotenser skiller
forsøkene? Forklar hvorfor forskjellen ikke kan skyldes ulik basis eller ulik
størrelse på forstyrrelsen.

### Gjør det nesten usynlige feilpolynomet synlig

For å forstå forsterkningen ser vi ikke bare på to hele polynomer. Vi trekker
dem fra hverandre. Forskjellen mellom reverse-engineering-resultatet og det
opprinnelige polynomet er selv et polynom:

$$r(x)=p_{\mathrm{forstyrret}}(x)-p_{\mathrm{opprinnelig}}(x).$$

Ved hvert avlesningspunkt er $r(x_k)$ akkurat den lille forstyrrelsen vi la
til. Hvis vi bare så på disse $n+1$ tallene, ville $r$ virke nesten som
nullpolynomet. Men avlesningspunktene forteller ikke direkte hva som skjer
mellom dem. Figuren tegner derfor både de små svarte verdiene $r(x_k)$ og hele
kurven $r(x)$ på det tette rutenettet.

```{pyodide-python}
plt.close("all")
fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

for ax, title, data, color in [
    (axes[0], "Like langt mellom punktene", equal_data, "#277da1"),
    (axes[1], "Cosinusfordelte punkter", cheb_data, "#d98900"),
]:
    ax.plot(data["grid"], data["error"], color=color,
            label="$r(x)$ mellom avlesningene")
    ax.scatter(data["points"], data["noise"], color="black", s=16,
               zorder=3, label="$r(x_k)$ ved avlesningspunktene")
    ax.axhline(0, color="0.7", linewidth=0.8)
    ax.set_title(title)
    ax.set_ylabel("feil")
    ax.grid(alpha=0.25)
    ax.legend(loc="upper center")

axes[1].set_xlabel("x")
plt.tight_layout()
plt.show()
```

Les først de svarte punktene og deretter kurvene:

1. Hvor små er $r(x_k)$ ved de oppgitte avlesningspunktene? Sammenlign med
   maksimum av $|r(x)|$ på hele rutenettet.
2. Hvor i intervallet blir $|r(x)|$ størst for jevne punkter? Se tilbake på
   punktfiguren: Er det få eller mange avlesningspunkter i dette området?
3. Gjør den samme sammenligningen for cosinuspunktene. Hvordan har de ekstra
   punktene nær endene påvirket feiltoppene?
4. I del 1 fant vi et eksakt nullromspolynom $z$ med $E(z)=0$. Her er
   $E(r)$ ikke null; det består av tall med størrelse $10^{-10}$. Forklar
   både likheten og forskjellen mellom $z$ og $r$.

Vi kan uformelt kalle $r$ en **numerisk nullromsretning**: Et ikke-null
polynom blir sendt til en svært liten, men ikke helt null, avlesningskolonne.
Dette er ikke et nytt eksakt nullrom. Uttrykket beskriver at avlesningene
nesten ikke ser en endring som likevel kan være stor mellom punktene.

### Valgfri utvidelse: finn graden der forskjellen blir synlig

```{pyodide-python}
degrees = [5, 10, 15, 20, 25, 30, 35]

print(f"{'grad':>5} {'forsterkning, jevn':>22} "
      f"{'forsterkning, cosinus':>25}")
print("-"*57)
for n_test in degrees:
    equal = point_placement_experiment(
        n_test, np.linspace(-1.0, 1.0, n_test+1)
    )
    cosine = point_placement_experiment(
        n_test, chebyshev_points(n_test)
    )
    amp_equal = equal["max_curve_error"]/equal["max_data_error"]
    amp_cosine = cosine["max_curve_error"]/cosine["max_data_error"]
    print(f"{n_test:5d} {amp_equal:22.4e} {amp_cosine:25.4e}")
```

Hvis du gjør utvidelsen, velg minst to ekstra grader selv. Beskriv når
forskjellen først blir tydelig, og om veksten ser jevn ut. Tallene viser hva
som skjer i forsøkene dine, men de beviser ikke hva som skjer for alle grader.

## Finale: Beregn det samme polynomet på tre måter

Plottene i starten antydet at $T_n$ holder seg mellom $-1$ og $1$ på
intervallet. Identiteten

$$T_n(x)=\cos(n\arccos x),\qquad -1\le x\le1,$$

gir oss en uavhengig måte å kontrollere dette på. Dermed kjenner vi størrelsen
på det riktige svaret før vi bruker NumPy: $T_{50}(0.99)$ må ligge i
$[-1,1]$.

Vi skal nå evaluere $T_{50}(0.99)$ på tre matematisk likeverdige måter:

1. konverter til monomialkoeffisienter og bruk vanlig polynomevaluering;
2. bruk Chebyshev-representasjonen direkte;
3. bruk cosinusidentiteten som referanse.

Den første metoden skriver $T_{50}$ som
$a_0+a_1x+\cdots+a_{50}x^{50}$ før den setter inn $x=0.99$. Den andre bruker
Chebyshev-rekursjonen direkte, uten å lage denne lange potensformen. Den
tredje regner ut cosinusuttrykket og fungerer som en kontroll som ikke bruker
noen av koeffisientlistene.

Skriv ned hvilken metode du forventer vil være mest pålitelig før du kjører,
og hvorfor. Følg deretter variablene i koden: `cheb_coordinates` beskriver
nøyaktig ett $T$-polynom, `monomial_coordinates` beskriver det samme polynomet
med potenser av $x$, og de tre variablene som begynner med `value_` er de tre
svarene.

```{pyodide-python}
n = 50
x0 = 0.99

cheb_coordinates = np.zeros(n+1)
# Denne koordinatvektoren betyr 0*T_0 + ... + 1*T_50.
cheb_coordinates[n] = 1.0
# Konverteringen endrer koordinatene, ikke polynomet. Etterpå evalueres det
# samme matematiske objekt med to forskjellige representasjoner.
monomial_coordinates = cheb.cheb2poly(cheb_coordinates)

value_monomial = poly.polyval(x0, monomial_coordinates)
value_chebyshev = cheb.chebval(x0, cheb_coordinates)
value_reference = np.cos(n*np.arccos(x0))

print("Største monomialkoeffisient:",
      np.max(np.abs(monomial_coordinates)))
print("Monomialevaluering:   ", value_monomial)
print("Chebyshev-evaluering: ", value_chebyshev)
print("Cosinusreferanse:     ", value_reference)
print("Feil, monomial:       ", abs(value_monomial-value_reference))
print("Feil, Chebyshev:      ", abs(value_chebyshev-value_reference))
```

Hvis et svar ligger langt utenfor intervallet $[-1,1]$, vet du fra
cosinusidentiteten at det ikke kan være riktig. Se da på den største
monomialkoeffisienten. Når mange svært store ledd til slutt skal gi et svar
mellom $-1$ og $1$, må positive og negative bidrag nesten kansellere
hverandre. Små avrundinger i de store mellomresultatene kan da overleve etter
kanselleringen og bli store sammenlignet med det riktige svaret.

### Se hvordan feilen vokser fram mot grad 50

For å se om problemet dukker opp plutselig eller bygger seg opp, gjentar vi de
tre evalueringene for grad 10, 20, 30, 40 og 50. Tabellen viser ved siden av
hverandre hvor stor den største monomialkoeffisienten er og hvor mye de to
beregningsmåtene avviker fra cosinuskontrollen.

```{pyodide-python}
print(f"{'grad':>5} {'største koeff.':>18} "
      f"{'feil monomial':>18} {'feil Chebyshev':>18}")
print("-"*63)

for n_test in [10, 20, 30, 40, 50]:
    c = np.zeros(n_test+1)
    c[n_test] = 1.0
    a = cheb.cheb2poly(c)
    reference = np.cos(n_test*np.arccos(x0))
    monomial_value = poly.polyval(x0, a)
    chebyshev_value = cheb.chebval(x0, c)
    print(f"{n_test:5d} {np.max(np.abs(a)):18.4e} "
          f"{abs(monomial_value-reference):18.4e} "
          f"{abs(chebyshev_value-reference):18.4e}")
```

Bygg forklaringen i denne rekkefølgen:

1. Skill mellom størrelsen på et polynom på intervallet og størrelsen på
   koeffisientene i en bestemt basis. Hvorfor er ikke disse det samme?
2. Bruk utskriften til å beskrive hvordan de største
   monomialkoeffisientene vokser. Hvorfor må store positive og negative ledd
   kansellere hvis sluttverdien skal ligge i $[-1,1]$?
3. Knytt avrunding av de store mellomresultatene til flyttallsregningen fra
   uke 1. Hva blir igjen når den nesten perfekte kanselleringen ikke lenger er
   perfekt?
4. Knytt valget mellom monomialbasis og Chebyshev-basis til uke 3. De to
   uttrykkene er algebraisk like, så hvorfor kan beregningene likevel få ulik
   kvalitet?
5. Det brukes ingen avlesningsmatrise eller interpolasjon i dette forsøket.
   Forklar derfor hvorfor feilen her ikke skyldes plasseringen av
   avlesningspunkter.

## Åpen utfordring: Lag din egen blindsone

Nå får du bruke ideene fra prosjektet mer fritt. Du skal gjenta historien fra
del 3, men velge graden, punktene og fortegnene selv. Start med et
referansepolynom, legg en svært liten feil til avlesningene, gjør reverse
engineering av polynomet som passer de endrede dataene, og mål hvor stort
avviket blir mellom punktene.

Plasser avlesningspunktene
slik at en svært liten feil i avlesningene gir en stor feil mellom punktene,
og slik at du kan forklare mekanismen. Målet er ikke et kunstig rekordtall.
Følg disse reglene:

- polynomgraden skal være høyst 35;
- alle $n+1$ avlesningspunkter skal være forskjellige og ligge i $[-1,1]$;
- avstanden mellom to nabopunkter skal være minst $10^{-3}$;
- hver avlesningsfeil skal ha absoluttverdi høyst $10^{-10}$;
- polynomet skal finnes i Chebyshev-basis;
- forsterkningen skal beregnes på et tett rutenett med minst 5001 punkter.

Du kan endre graden, punktene og fortegnsmønsteret i forstyrrelsen. Du kan
ikke gjøre avlesningsfeilen større eller bryte kravet til minste
punktavstand. Før koden kjøres, skriv hvilken endring du prøver og hvorfor du
tror den kan skjule feilpolynomet for avlesningene.

Variablene med prefikset `my_` er delene du skal følge og senere endre:
`my_points` er avlesningspunktene, `my_noise` er de små feilene,
`my_recovered` er polynomet som passer de endrede dataene, og `my_error` er
forskjellen fra referansepolynomet på det tette rutenettet. `assert`-linjene
stopper forsøket hvis reglene ikke er fulgt.

```{pyodide-python}
# Startforslag: Bytt ut både punktene og fortegnsmønsteret i feilen.
n_design = 20
my_points = np.linspace(-1.0, 1.0, n_design+1)
my_noise = 1e-10*(-1.0)**np.arange(n_design+1)

true_coordinates = reference_coordinates(n_design)
my_measurements = cheb.chebval(my_points, true_coordinates)
my_matrix = chebyshev_matrix(my_points, n_design)
# Reverse engineering i Chebyshev-basis: Vi finner koeffisientene som passer
# de endrede avlesningene. Dermed undersøker vi punktplasseringen uten å bytte
# basis samtidig.
my_recovered = np.linalg.solve(my_matrix, my_measurements+my_noise)

my_grid = np.linspace(-1.0, 1.0, 5001)
my_reference = cheb.chebval(my_grid, true_coordinates)
my_curve = cheb.chebval(my_grid, my_recovered)
my_error = my_curve-my_reference

assert len(np.unique(my_points)) == n_design+1
assert np.all(np.abs(my_points) <= 1.0)
assert np.max(np.abs(my_noise)) <= 1.000001e-10
minimum_spacing = np.min(np.diff(np.sort(my_points)))
assert minimum_spacing >= 1e-3

# Et stort utslag er bare interessant hvis systemet faktisk løser de oppgitte
# avlesningene. Derfor rapporterer vi både rang og residual.
my_rank = np.linalg.matrix_rank(my_matrix)
my_residual = np.linalg.norm(
    my_matrix @ my_recovered - (my_measurements+my_noise), ord=np.inf
)
assert my_rank == n_design+1

# Sammenlign den største feilen mellom punktene med den største feilen
# vi faktisk la inn i avlesningene.
my_amplification = (np.max(np.abs(my_error))
                    / np.max(np.abs(my_noise)))
print("Forsterkning:", my_amplification)
print("Minste punktavstand:", minimum_spacing)
print("Rang:", my_rank)
print("Største residual i avlesningene:", my_residual)

plt.close("all")
plt.plot(my_grid, my_error, label="feilpolynomet")
plt.scatter(my_points, my_noise, color="black", s=15,
            label="feil ved avlesningspunktene")
plt.xlabel("x")
plt.ylabel("feil")
plt.title("Min blindsone")
plt.grid(alpha=0.25)
plt.legend()
plt.show()
```

Prøv minst to ideer, og endre én egenskap om gangen. Det beste forsøket er
ikke nødvendigvis det med størst tall. Du må også kunne forklare hvorfor
plasseringen av punktene skjuler feilpolynomet.

## Samlet analyse: Forklar hva forsøkene viste

Skriv en sammenhengende analyse på omtrent **400–600 ord**. Figurer og
tabeller underbygger analysen, men de erstatter ikke forklaringen.

Analysen skal skille tydelig mellom:

1. polynomrommet og koordinatene i en valgt basis;
2. avlesningsavbildningen og matrisen som representerer den;
3. eksakt informasjonstap og numerisk nesten-informasjonstap;
4. effekten av å bytte basis med punktene faste;
5. effekten av å flytte avlesningspunktene med basisen fast;
6. algebraisk likeverdighet og numerisk pålitelighet.

Besvar også følgende hovedspørsmål:

- Hvilket eksperiment ga den største forskjellen, og hvor stor var den?
- Hvor i intervallet oppstod de største feilene?
- Hvilke store tall eller nesten-kanselleringer fant du?
- Hva var nesten usynlig for avlesningsavbildningen?
- Hvilke påstander har du vist matematisk, og hvilke bygger bare på numeriske
  forsøk?
- Hva lærte $T_{50}$-forsøket som ikke allerede var synlig ved grad 3?

## Dette skal leveres

Lever én Quarto-side eller notebook med:

1. håndregnede $T_2,T_3,T_4$ og kontroll av rekursjonen;
2. oppvarmingsfigurene og observasjonene dine;
3. basis- og rangargumentet for $T_0,\ldots,T_4$;
4. begge avlesningsmatrisene i lav grad og nullromseksperimentet;
5. resultater og feilfigur for basiseksperimentet ved grad 30;
6. resultater, punktfigur og feilpolynom for forsøket med avlesningspunkter;
7. $T_{50}$-resultatene og forklaringen på sammenbruddet;
8. minst to forsøk i den åpne utfordringen;
9. den samlede analysen.

Oppgi alltid grad, punkter, størrelsen på forstyrrelsen og rutenettstørrelse sammen
med et resultat. Ellers kan forsøket ikke gjentas.

:::: {.callout-warning}
## Krav til kodeassistenter og numeriske påstander

Kodeassistenter kan hjelpe med Python-syntaks og plotting, men de kan også
blande sammen effekten av basisvalg og plasseringen av avlesningspunktene. Du må kunne forklare
hvorfor hvert eksperiment bare endrer én av dem.

Et tall fra `np.linalg.solve` er ikke i seg selv en matematisk forklaring.
Kontroller dimensjoner, rang, residualer og hva koordinatene representerer.
Påstander om «stabilitet» skal støttes av konkrete forstyrrelser og beregnede
feil.
::::
