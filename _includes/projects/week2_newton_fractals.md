# Newtonfraktaler: Hvilken løsning finner iterasjonen?

Dette prosjektet er laget for omtrent **3–4 timer selvstendig arbeid**. Copilot og andre kodeassistenter er tillatt.

Når en ligning har flere løsninger, er det ikke nok å spørre om en metode
konvergerer. Vi må også spørre *hvilken* løsning den finner, hvor raskt den
kommer dit, og hvor mye svaret avhenger av startverdien. Newtons metode gjør
disse spørsmålene synlige på en særlig tydelig måte.

Metoden løser ligningen

$$
f(z)=0
$$

ved å gjenta

$$
z_{n+1}=z_n-\frac{f(z_n)}{f'(z_n)}.
$$

Dette er en fikspunktiterasjon med oppdateringsregel

$$
g(z)=z-\frac{f(z)}{f'(z)}.
$$

Her arbeider vi med komplekse tall $z=x+iy$. Ved å fargelegge hver startverdi
etter nullpunktet den finner, får vi et kart over metodens oppførsel. Noen
områder gir raske og forutsigbare iterasjoner. Langs grensene kan to nesten
like startverdier få helt forskjellige forløp. Mengden av startverdier som
konvergerer mot et bestemt nullpunkt, kalles nullpunktets
**tiltrekningsområde**.

> **Problemstilling:** Hva kjennetegner gode og dårlige startverdier for
> Newtons metode, og hvordan kan vi undersøke dette numerisk?

::: {.callout-tip}
## Hvordan jobbe med prosjektet

Koden for funksjonstildeling, Newton-iterasjon, rutenett, klassifisering og plotting er gitt. Arbeidet ditt er å planlegge numeriske eksperimenter, velge parametere, kontrollere resultatene og forklare det du observerer.

Dette er også en øvelse i å sette seg inn i eksisterende kode for en
modellmetode. Du skal ikke bygge alt fra bunnen av. Les kommentarene, kjør
koden, finn parameterne som styrer forsøket, og gjør små endringer du kan
kontrollere. Slik arbeider man ofte med vitenskapelig kode: forstå nok til å
stille et spørsmål, endre én ting, og undersøke hva som faktisk skjedde.

Endre én størrelse om gangen. Noter alltid startverdi eller plottevindu,
toleranse og `maxiter` sammen med resultatet. Målet er ikke bare å lage et
fraktalbilde, men å bruke bildet til å velge og begrunne numeriske forsøk.
:::

## 1. Du får tildelt en funksjon

Skriv fornavnet ditt i cellen under. Navnet normaliseres og hashes med SHA-256. Samme normaliserte fornavn gir alltid samme funksjon i dette prosjektet. Studenter med samme fornavn kan derfor få samme funksjon.

Tildelingen skjer lokalt i nettleseren. Navnet sendes ikke noe sted.

```{pyodide-python}
import hashlib
import unicodedata

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


def normalize_name(name):
    """Gjør små navnevariasjoner irrelevante for funksjonstildelingen."""
    name = unicodedata.normalize("NFKD", name.strip().casefold())
    name = "".join(char for char in name
                   if not unicodedata.combining(char))
    return " ".join(name.split())


def function_id(first_name, number_of_functions):
    """Gjør fornavnet om til en stabil indeks i funksjonspuljen."""
    normalized = normalize_name(first_name)
    text = f"IMAX3011-newton-2026:{normalized}"
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], byteorder="big") % number_of_functions


FUNCTIONS = [
    {"label": "A", "coefficients": [1, 0, 0, -1],
     "formula": "z³ − 1", "plot_window": (-2, 2, -2, 2)},
    {"label": "B", "coefficients": [1, -2j, -1, 2j],
     "formula": "(z − 1)(z + 1)(z − 2i)",
     "plot_window": (-2.5, 2.5, -2, 3)},
    {"label": "C", "coefficients": [1, 0, -2, -4],
     "formula": "(z − 2)(z + 1 − i)(z + 1 + i)",
     "plot_window": (-3, 3, -3, 3)},
    {"label": "D", "coefficients": [1, 0, 0, 0, -1],
     "formula": "z⁴ − 1", "plot_window": (-2, 2, -2, 2)},
    {"label": "E", "coefficients": [1, 0, -3.75, 0, -1],
     "formula": "(z − 2)(z + 2)(z − 0.5i)(z + 0.5i)",
     "plot_window": (-3, 3, -2.5, 2.5)},
    {"label": "F", "coefficients": [1, 0, 0, 1, 1],
     "formula": "z⁴ + z + 1", "plot_window": (-2.5, 2.5, -2.5, 2.5)},
    {"label": "G", "coefficients": [1, 0, 0, 0, 0, -1],
     "formula": "z⁵ − 1", "plot_window": (-2, 2, -2, 2)},
    {"label": "H", "coefficients": [1, -1.5, -0.5, -0.5, -1.5, 1],
     "formula": "(z − 2)(z + 1)(z − 0.5)(z − i)(z + i)",
     "plot_window": (-2.5, 2.5, -2.5, 2.5)},
    {"label": "I", "coefficients": [1, 0, 0, 0, -1, 1],
     "formula": "z⁵ − z + 1", "plot_window": (-2.5, 2.5, -2.5, 2.5)},
]


def prepare_function(entry):
    """Lag f, f', nullpunkter og kritiske punkter fra én tabellrad.

    Denne funksjonen gjør oppsettet for oss. I forsøkene nedenfor arbeider vi
    med f og df, og trenger vanligvis ikke å endre selve funksjonen her.
    """
    coefficients = np.asarray(entry["coefficients"], dtype=complex)
    derivative_coefficients = np.polyder(coefficients)
    roots = np.roots(coefficients)
    critical_points = np.roots(derivative_coefficients)

    def f(z):
        return np.polyval(coefficients, z)

    def df(z):
        return np.polyval(derivative_coefficients, z)

    return f, df, roots, critical_points


# Bytt teksten med ditt eget fornavn.
first_name = "Ada"

my_id = function_id(first_name, len(FUNCTIONS))
my_function = FUNCTIONS[my_id]
f, df, roots, critical_points = prepare_function(my_function)

print("Funksjons-ID:", my_function["label"])
print("Funksjon:    ", my_function["formula"])
print("Koeffisienter:", my_function["coefficients"])
print("Nullpunkter:")
for root in roots:
    print(" ", root)
print("Kritiske punkter (f'(z)=0):")
for point in critical_points:
    print(" ", point)
print("Standardvindu:", my_function["plot_window"])
```

Alle funksjonene i puljen har grad 3, 4 eller 5 og bare **enkle nullpunkter**.
Det betyr at hvert nullpunkt $r$ oppfyller både $f(r)=0$ og $f'(r)\ne0$;
ingen nullpunkter er gjentatt.
**Skriv ned** funksjons-ID, funksjon, nullpunkter og standardvindu. Bruk den
tildelte funksjonen i resten av prosjektet.

## 2. Newtons metode for én startverdi

Før vi lager et kart med tusenvis av startverdier, følger vi noen få
iterasjoner trinn for trinn. Da kan vi se hva «rask» og «langsom» konvergens
betyr i praksis.

Programmet trenger en regel for å avgjøre når svaret er godt nok. Siden vi
prøver å løse $f(z)=0$, måler vi hvor nær funksjonsverdien er null. Størrelsen

$$
|f(z_n)|
$$

kalles **residualen**. Her stopper vi når

$$
|f(z_n)|<\texttt{tol},
$$

eller når `maxiter` er nådd. En liten residual betyr at den beregnede verdien
nesten oppfyller ligningen. Den er ikke det samme som avstanden til det
eksakte nullpunktet.

Vi registrerer også skrittlengden

$$
|z_{n+1}-z_n|=\left|\frac{f(z_n)}{f'(z_n)}\right|.
$$

Den forteller hvor mye iteratet flytter seg. Den er nyttig når vi skal forstå
store hopp, men i dette prosjektet er det residualen som avgjør konvergens.
Uttrykket $|z-f(z)|$ er ikke residualen til ligningen $f(z)=0$.

```{pyodide-python}
def is_finite_complex(z):
    """Sjekk at både real- og imaginærdelen kan brukes videre."""
    return np.isfinite(np.real(z)) and np.isfinite(np.imag(z))


def nearest_root(z, roots):
    """Returner nummeret til nullpunktet som ligger nærmest z."""
    return int(np.argmin(np.abs(roots - z)))


def newton_trace(f, df, roots, z0, tol=1e-8, maxiter=50,
                 derivative_tol=1e-14):
    """Følg én startverdi slik at vi kan se hva Newton faktisk gjør.

    I forsøkene endrer du først og fremst z0, tol og maxiter. Resultatet er en
    ordbok med stoppårsak, funnet nullpunkt og hele iterasjonshistorikken.
    derivative_tol beskytter oss mot å dele på et tall som er svært nær null.
    """
    z = complex(z0)
    history = [{"n": 0, "z": z,
                "residual": float(abs(f(z))), "step": np.nan}]

    if history[-1]["residual"] < tol:
        return {"z": z, "converged": True, "root": nearest_root(z, roots),
                "reason": "liten residual", "iterations": 0,
                "history": history}

    for n in range(1, maxiter + 1):
        derivative = df(z)
        if not is_finite_complex(derivative) or abs(derivative) <= derivative_tol:
            return {"z": z, "converged": False, "root": None,
                    "reason": "for liten derivert", "iterations": n-1,
                    "history": history}

        with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
            z_new = z - f(z)/derivative

        if not is_finite_complex(z_new):
            return {"z": z_new, "converged": False, "root": None,
                    "reason": "ikke-endelig verdi", "iterations": n,
                    "history": history}

        step = float(abs(z_new-z))
        residual = float(abs(f(z_new)))
        history.append({"n": n, "z": z_new,
                        "residual": residual, "step": step})
        z = z_new

        if residual < tol:
            return {"z": z, "converged": True,
                    "root": nearest_root(z, roots),
                    "reason": "liten residual", "iterations": n,
                    "history": history}

    return {"z": z, "converged": False, "root": None,
            "reason": "maksimalt antall iterasjoner",
            "iterations": maxiter, "history": history}


def print_trace(result):
    """Skriv historikken fra newton_trace som en lesbar tabell."""
    print(" n                 z_n             |f(z_n)|       skrittlengde")
    for row in result["history"]:
        step = "     -" if np.isnan(row["step"]) else f"{row['step']:.3e}"
        print(f"{row['n']:2d}  {row['z']:>22.14g}   "
              f"{row['residual']:.3e}      {step}")
    print("\nStoppårsak:", result["reason"])
    print("Iterasjoner:", result["iterations"])
    if result["converged"]:
        print("Nærmeste nullpunkt:", roots[result["root"]])


def plot_trace(result):
    """Sammenlign residual og skrittlengde gjennom én iterasjon."""
    rows = result["history"]
    n = np.array([row["n"] for row in rows])
    residuals = np.array([row["residual"] for row in rows])
    steps = np.array([row["step"] for row in rows])

    plt.close("all")
    fig, ax = plt.subplots()
    ax.semilogy(n, residuals, "o-", label="Residual |f(zₙ)|")
    if len(steps) > 1:
        ax.semilogy(n[1:], steps[1:], "o-", label="Skritt |zₙ − zₙ₋₁|")
    ax.set_xlabel("Iterasjon n")
    ax.set_ylabel("Størrelse")
    ax.set_title("Residual og skrittlengde")
    ax.grid(True)
    ax.legend()
    plt.show()
```

Kjør først koden med de foreslåtte startverdiene. Legg deretter til minst to egne startverdier.

```{pyodide-python}
starting_values = [1.5, -1+1j, 0.1, 1j]

for z0 in starting_values:
    result = newton_trace(f, df, roots, z0, tol=1e-8, maxiter=50)
    print("\nStartverdi:", z0)
    print("  konvergert:", result["converged"])
    print("  iterasjoner:", result["iterations"])
    print("  stoppårsak:", result["reason"])
    print("  siste residual:", result["history"][-1]["residual"])
    if result["converged"]:
        print("  nullpunkt:", roots[result["root"]])
```

Velg én startverdi som konvergerer raskt, og én som konvergerer langsomt eller ikke konvergerer. Vis hele historikken og plottet for begge.

```{pyodide-python}
#| canvas: false
# Bytt startverdien med en verdi du vil undersøke nærmere.
z0 = -1 + 1j

result = newton_trace(f, df, roots, z0, tol=1e-8, maxiter=50)
print_trace(result)
plot_trace(result)
```

**Svar kort:**

1. Konvergerer alle startverdiene mot samme nullpunkt?
2. Avtar residualen i hvert eneste steg?
3. Avtar residual og skrittlengde i samme takt?
4. Hvorfor trenger programmet både en residualtoleranse og `maxiter`?
5. Hva skjer dersom et iterat kommer nær et punkt der $f'(z)=0$?

## 3. Tiltrekningsområder

Forsøkene med enkeltpunkter viser at startverdien betyr noe, men de sier lite
om hvor vanlig rask eller langsom konvergens er. Derfor gjentar vi samme
forsøk på et helt rutenett i det komplekse planet. Resultatet blir både et
kart og et datasett vi kan stille spørsmål til.

Neste funksjon kjører Newtons metode samtidig for hele rutenettet. Hvert punkt
klassifiseres som et nullpunktnummer, `-1` for ikke konvergert innen
`maxiter`, eller `-2` for ugyldig beregning.

```{pyodide-python}
def newton_grid(f, df, roots, bounds, nx=400, ny=400,
                tol=1e-8, maxiter=50, derivative_tol=1e-14):
    """Kjør det samme Newton-forsøket for alle pikslene i et rektangel.

    bounds velger delen av det komplekse planet vi ser. nx og ny bestemmer
    bildeoppløsningen, ikke nøyaktigheten til én Newton-iterasjon. Returverdien
    inneholder både funnet nullpunkt, iterasjonstall og sluttresidual.
    """
    xmin, xmax, ymin, ymax = bounds
    x = np.linspace(xmin, xmax, nx)
    y = np.linspace(ymin, ymax, ny)
    z = x[None, :] + 1j*y[:, None]

    basin = np.full(z.shape, -1, dtype=int)
    iterations = np.zeros(z.shape, dtype=int)
    # active forteller hvilke piksler som fortsatt trenger et nytt Newton-skritt.
    active = np.ones(z.shape, dtype=bool)

    for n in range(1, maxiter + 1):
        with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
            derivative = df(z)
            safe = (active & np.isfinite(z.real) & np.isfinite(z.imag)
                    & np.isfinite(derivative.real)
                    & np.isfinite(derivative.imag)
                    & (np.abs(derivative) > derivative_tol))

            # Skill ugyldige beregninger fra dem som bare trenger flere steg.
            invalid = active & ~safe
            basin[invalid] = -2
            iterations[invalid] = n-1
            active[invalid] = False

            z[safe] = z[safe] - f(z[safe])/derivative[safe]
            finite = np.isfinite(z.real) & np.isfinite(z.imag)
            invalid_after = active & ~finite
            basin[invalid_after] = -2
            iterations[invalid_after] = n
            active[invalid_after] = False

            residual = np.full(z.shape, np.inf)
            residual[active] = np.abs(f(z[active]))
            converged = active & (residual < tol)

        if np.any(converged):
            # Først nå bestemmer vi hvilket nullpunkt pikslene endte ved.
            converged_values = z[converged]
            distances = np.abs(converged_values[:, None] - roots[None, :])
            basin[converged] = np.argmin(distances, axis=1)
            iterations[converged] = n
            active[converged] = False

        if not np.any(active):
            break

    iterations[active] = maxiter
    final_residual = np.full(z.shape, np.inf)
    finite = np.isfinite(z.real) & np.isfinite(z.imag)
    with np.errstate(over="ignore", invalid="ignore"):
        final_residual[finite] = np.abs(f(z[finite]))

    return {"basin": basin, "iterations": iterations,
            "residual": final_residual, "z": z,
            "bounds": bounds, "tol": tol, "maxiter": maxiter,
            "roots": roots}


ROOT_COLORS = np.array([
    [0.90, 0.20, 0.20], [0.20, 0.65, 0.95], [0.25, 0.80, 0.35],
    [0.90, 0.65, 0.15], [0.65, 0.35, 0.90], [0.20, 0.80, 0.80],
])


def plot_basins(data, title="Newtons metode: tiltrekningsområder",
                critical_points=None, iteration_cap=20):
    """Vis resultat og arbeidsmengde i hvert sitt panel.

    Venstre panel svarer på hvilket nullpunkt som ble funnet. Høyre panel
    viser antall iterasjoner. iteration_cap bestemmer hvor fargeskalaen
    stopper; større verdier vises fortsatt, men får samme endefarge.
    """
    basin = data["basin"]
    iterations = data["iterations"]
    maxiter = data["maxiter"]
    roots = data["roots"]
    xmin, xmax, ymin, ymax = data["bounds"]

    # Basin-fargen skal bare kode nullpunkt, ikke iterasjonstall.
    basin_image = np.full(basin.shape + (3,), 0.25)
    basin_image[basin == -2] = 0.0
    legend_handles = []
    for k in range(len(roots)):
        mask = basin == k
        color = ROOT_COLORS[k % len(ROOT_COLORS)]
        basin_image[mask] = color
        legend_handles.append(Patch(facecolor=color, label=f"Mot r{k+1}"))

    plt.close("all")
    fig, (ax_basin, ax_iterations) = plt.subplots(
        1, 2, figsize=(13, 6), constrained_layout=True
    )

    ax_basin.imshow(basin_image, origin="lower",
                    extent=(xmin, xmax, ymin, ymax),
                    interpolation="nearest")
    ax_basin.scatter(roots.real, roots.imag, c="white", edgecolors="black",
                     s=70, marker="o")
    for k, root in enumerate(roots):
        ax_basin.annotate(f"r{k+1}", (root.real, root.imag),
                          xytext=(7, 7), textcoords="offset points",
                          color="black", weight="bold")
    if critical_points is not None:
        critical_handle = ax_basin.scatter(
            critical_points.real, critical_points.imag,
            c="black", edgecolors="white", s=70, marker="X",
            linewidths=1.5, label="Kritiske punkter"
        )
        legend_handles.append(critical_handle)

    ax_basin.set_title("Funnet nullpunkt")
    ax_basin.legend(handles=legend_handles, loc="best")

    converged = basin >= 0
    # Avkort skalaen slik at noen få trege piksler ikke vasker ut hele kartet.
    capped_iterations = np.ma.masked_where(
        ~converged, np.minimum(iterations, iteration_cap)
    )
    iteration_image = ax_iterations.imshow(
        capped_iterations, origin="lower", extent=(xmin, xmax, ymin, ymax),
        interpolation="nearest", cmap="viridis",
        vmin=1, vmax=iteration_cap
    )
    ax_iterations.scatter(roots.real, roots.imag, c="white",
                          edgecolors="black", s=45, marker="o")
    colorbar = fig.colorbar(iteration_image, ax=ax_iterations, shrink=0.82)
    colorbar.set_label(
        f"Antall iterasjoner ({iteration_cap} = {iteration_cap} eller flere)"
    )
    ax_iterations.set_title("Iterasjoner før residualkravet er oppfylt")

    for ax in (ax_basin, ax_iterations):
        ax.set_xlabel("Re(z₀)")
        ax.set_ylabel("Im(z₀)")
        ax.set_aspect("equal")

    fig.suptitle(title)
    plt.show()


def summarize_grid(data):
    """Trekk ut noen få tall som gjør ulike rutenett sammenlignbare."""
    basin = data["basin"]
    iterations = data["iterations"]
    residual = data["residual"]
    converged = basin >= 0
    total = basin.size

    summary = {
        "total": total,
        "converged": int(np.count_nonzero(converged)),
        "not_converged": int(np.count_nonzero(basin == -1)),
        "invalid": int(np.count_nonzero(basin == -2)),
        "fraction_converged": float(np.mean(converged)),
        "mean_iterations": (float(np.mean(iterations[converged]))
                            if np.any(converged) else np.nan),
        "max_accepted_residual": (float(np.max(residual[converged]))
                                  if np.any(converged) else np.nan),
    }
    return summary


def print_summary(summary):
    """Skriv sammendraget uten at vi må huske alle nøkkelnavnene."""
    print("Antall startverdier:     ", summary["total"])
    print("Konvergert:              ", summary["converged"])
    print("Nådde maxiter:           ", summary["not_converged"])
    print("Ugyldig beregning:       ", summary["invalid"])
    print("Andel konvergert:        ", f"{summary['fraction_converged']:.4f}")
    print("Gjennomsnitt iterasjoner:", f"{summary['mean_iterations']:.2f}")
    print("Største godkjente residual:",
          f"{summary['max_accepted_residual']:.3e}")


```

Kjør standardeksperimentet. Dersom nettleseren arbeider langsomt, kan du først bruke `nx=250, ny=250` og øke oppløsningen til slutt.

```{pyodide-python}
#| canvas: false
bounds = my_function["plot_window"]

basin_data = newton_grid(
    f, df, roots,
    bounds=bounds,
    nx=400, ny=400,
    tol=1e-8,
    maxiter=50,
)

plot_basins(basin_data, f"Funksjon {my_function['label']}: {my_function['formula']}")
print_summary(summarize_grid(basin_data))
```

Figuren til venstre bruker én fast farge for hvert nullpunkt. Den svarer derfor
bare på *hvilket* nullpunkt metoden fant. Figuren til høyre viser antall
iterasjoner før residualkravet ble oppfylt. Les iterasjonstallet fra
fargeskalaen. Verdier på 20 eller mer får samme endefarge, slik at noen få
svært langsomme punkter ikke skjuler forskjellene i resten av kartet.

Mørkegrå punkter i venstre figur nådde `maxiter`, mens svarte punkter ga en
ugyldig beregning. Slike punkter er maskert i iterasjonskartet.

For resten av prosjektet bruker vi følgende målbare beskrivelser:

- En **rask** startverdi oppfyller residualkravet innen 6 iterasjoner.
- En **langsom** startverdi konvergerer, men trenger mer enn 15 iterasjoner.
- En **mislykket** startverdi når `maxiter` eller gir en ugyldig beregning.

Grensene 6 og 15 er arbeidsdefinisjoner for dette forsøket, ikke generelle
grenser for Newtons metode. I diskusjonen bruker vi langsomme og mislykkede
startverdier som konkrete eksempler på «dårlige» startverdier. Finn ett
eksempel i hver kategori som finnes i ditt datasett. Oppgi $z_0$, funnet
nullpunkt, iterasjonstall og siste residual.

Koden under foreslår startverdier fra kategoriene. Du kan bruke dem eller
velge punkter som er lettere å se i figuren.

```{pyodide-python}
def first_start_in(data, mask):
    """Finn én startverdi i en kategori, hvis kategorien finnes."""
    indices = np.argwhere(mask)
    if len(indices) == 0:
        return None
    row, col = indices[len(indices)//2]
    xmin, xmax, ymin, ymax = data["bounds"]
    ny, nx = data["basin"].shape
    x = np.linspace(xmin, xmax, nx)
    y = np.linspace(ymin, ymax, ny)
    return x[col] + 1j*y[row]


converged = basin_data["basin"] >= 0
categories = {
    "rask": converged & (basin_data["iterations"] <= 6),
    "langsom": converged & (basin_data["iterations"] > 15),
    "mislykket": basin_data["basin"] < 0,
}

for name, mask in categories.items():
    print(f"Forslag, {name}:", first_start_in(basin_data, mask))
```

**Svar kort:**

1. Hvilke områder konvergerer mot hvert nullpunkt?
2. Hvor ligger startverdiene som krever flest iterasjoner?
3. Hvordan skiller punkter nær en grense seg fra punkter langt inne i et tiltrekningsområde?
4. Ser figuren symmetrisk ut? Sammenlign med plasseringen av nullpunktene.
5. Kan et endelig rutenett bevise at alle startverdier i vinduet konvergerer?

## 4. Finner metoden alltid nærmeste nullpunkt?

En naturlig gjetning er at Newtons metode finner nullpunktet som ligger
nærmest startverdien. Nå kan vi teste denne gjetningen på hele rutenettet.
Koden under sammenligner nærmeste nullpunkt til $z_0$ med nullpunktet
iterasjonen faktisk fant.

```{pyodide-python}
def compare_with_nearest(data):
    """Test nærmeste-nullpunkt-gjetningen på hele rutenettet."""
    basin = data["basin"]
    roots = data["roots"]
    xmin, xmax, ymin, ymax = data["bounds"]
    ny, nx = basin.shape
    x = np.linspace(xmin, xmax, nx)
    y = np.linspace(ymin, ymax, ny)
    z0 = x[None, :] + 1j*y[:, None]

    nearest = np.argmin(np.abs(z0[..., None] - roots), axis=2)
    converged = basin >= 0
    different = converged & (basin != nearest)
    fraction = np.count_nonzero(different) / np.count_nonzero(converged)
    return {"nearest": nearest, "different": different,
            "fraction": fraction, "z0": z0}


nearest_test = compare_with_nearest(basin_data)
print("Andel konvergerte startverdier som ikke fant nærmeste nullpunkt:",
      f"{nearest_test['fraction']:.4f}")

indices = np.argwhere(nearest_test["different"])
print("Noen moteksempler:")
for row, col in indices[:5]:
    z0 = nearest_test["z0"][row, col]
    nearest_index = nearest_test["nearest"][row, col]
    found_index = basin_data["basin"][row, col]
    print(f"z₀={z0:.5g}: nærmest {roots[nearest_index]:.5g}, "
          f"men fant {roots[found_index]:.5g}")
```

Velg ett av moteksemplene og vis iterasjonshistorikken med `print_trace`.

**Svar kort:**

1. Hvor stor andel av de konvergerte startverdiene fant ikke nærmeste nullpunkt?
2. Hva skjer med avstanden til de ulike nullpunktene gjennom ditt valgte forløp?
3. Hvor i tiltrekningsplottet ligger de fleste moteksemplene?
4. Hva kan du nå si om påstanden «Newton finner nærmeste nullpunkt»?

## 5. Hvorfor kan noen startverdier gi store hopp?

I Newton-formelen deler vi på $f'(z_n)$. Når $f'(z_n)$ er nær null, kan ett
Newton-skritt derfor bli svært stort selv om funksjonsverdien ikke er stor.
Punkter som oppfyller $f'(z)=0$, kalles her **kritiske punkter**. De er ikke
nødvendigvis dårlige startverdier alene, men de gir oss steder det er naturlig
å undersøke nærmere.

```{pyodide-python}
#| canvas: false
plot_basins(basin_data,
            "Nullpunkter, kritiske punkter og tiltrekningsområder",
            critical_points=critical_points)

print("Kritiske punkter:")
for point in critical_points:
    print(" ", point, "  |f(z)| =", abs(f(point)))
```

Velg ett kritisk punkt $c$. Kjør `newton_trace` for $c$, $c+10^{-3}$ og
$c+10^{-2}i$. Oppgi stoppårsak, største skrittlengde, funnet nullpunkt og
antall iterasjoner. Du kan endre perturbasjonene dersom alle tre forsøkene
blir nesten like.

```{pyodide-python}
c = critical_points[0]  # Velg eventuelt et annet kritisk punkt.
critical_starts = [c, c + 1e-3, c + 1e-2j]

for z0 in critical_starts:
    result = newton_trace(f, df, roots, z0, tol=1e-8, maxiter=100)
    steps = [row["step"] for row in result["history"]
             if np.isfinite(row["step"])]
    largest_step = max(steps) if steps else np.nan
    found = roots[result["root"]] if result["converged"] else "ikke funnet"
    print(f"z₀={z0:.8g}: stopp={result['reason']}, "
          f"største skritt={largest_step:.3e}, "
          f"iterasjoner={result['iterations']}, nullpunkt={found}")
```

**Svar kort:**

1. Hva skjer når startverdien er nøyaktig et kritisk punkt?
2. Hvordan oppfører de to nærliggende startverdiene seg?
3. Ligger områder med mange iterasjoner nær noen av de kritiske punktene?
4. Er liten $|f'(z_0)|$ alene nok til å forutsi hele iterasjonsforløpet?

## 6. Hvor følsom er metoden nær en grense?

Tiltrekningsplottet antyder at en svært liten endring i startverdien kan endre
resultatet. For å gjøre dette til et kontrollert forsøk trenger vi et konkret
grensepunkt og en oppgitt **perturbasjon**, altså en liten, kontrollert endring
av startverdien. Funksjonen under foreslår et punkt
mellom to nabopiksler med forskjellig farge. Du kan bruke forslaget eller
velge et tydeligere punkt i din egen figur.

```{pyodide-python}
def suggest_boundary_point(data):
    """Finn et sentralt sted der to nabopiksler har forskjellig farge."""
    basin = data["basin"]
    left = basin[:, :-1]
    right = basin[:, 1:]
    candidates = np.argwhere((left >= 0) & (right >= 0) & (left != right))
    if len(candidates) == 0:
        raise ValueError("Fant ingen grense mellom to tiltrekningsområder")

    ny, nx = basin.shape
    margin_y = max(1, ny//20)
    margin_x = max(1, nx//20)
    interior = candidates[(candidates[:, 0] >= margin_y)
                          & (candidates[:, 0] < ny-margin_y)
                          & (candidates[:, 1] >= margin_x)
                          & (candidates[:, 1] < nx-margin_x)]
    if len(interior) > 0:
        candidates = interior

    center = np.array([ny/2, nx/2])
    row, col = candidates[np.argmin(np.sum((candidates-center)**2, axis=1))]
    xmin, xmax, ymin, ymax = data["bounds"]
    x = np.linspace(xmin, xmax, nx)
    y = np.linspace(ymin, ymax, ny)
    return (x[col] + x[col+1])/2 + 1j*y[row]


boundary_point = suggest_boundary_point(basin_data)
delta = 1e-3
nearby_starts = [boundary_point,
                 boundary_point + delta,
                 boundary_point + 1j*delta]

print("Foreslått grensepunkt:", boundary_point)
for z0 in nearby_starts:
    result = newton_trace(f, df, roots, z0, tol=1e-8, maxiter=100)
    found = roots[result["root"]] if result["converged"] else "ikke funnet"
    print(f"z₀={z0:.8g}: {result['iterations']} iterasjoner, "
          f"nullpunkt={found}, stopp={result['reason']}")
```

Hvis alle tre startverdiene gir samme resultat, flytt grensepunktet eller gjør
`delta` mindre. Vis iterasjonshistorikken for to nærliggende startverdier som
finner forskjellige nullpunkter.

**Svar kort:**

1. Hvor stor var avstanden mellom de to valgte startverdiene?
2. Når begynte iterasjonsforløpene å bli tydelig forskjellige?
3. Fant de ulike nullpunkter, eller var forskjellen bare antall iterasjoner?
4. Er samme følsomhet synlig langt inne i et ensfarget område?

## 7. Kontroller stoppreglene

Fargene i kartet avhenger også av reglene i programmet. Før du konkluderer,
kontroller at hovedresultatet ikke bare skyldes ett tilfeldig valg av
toleranse eller `maxiter`. Bruk et mindre rutenett for å spare tid.

```{pyodide-python}
print("      tol  maxiter  konvergert  nådde grensen  gj.snitt steg")
for tolerance, maximum in [(1e-4, 50), (1e-8, 50),
                           (1e-12, 50), (1e-8, 15), (1e-8, 100)]:
    data = newton_grid(f, df, roots, bounds, nx=250, ny=250,
                       tol=tolerance, maxiter=maximum)
    summary = summarize_grid(data)
    print(f"{tolerance:9.0e}  {maximum:7d}  {summary['converged']:10d}  "
          f"{summary['not_converged']:13d}  "
          f"{summary['mean_iterations']:13.2f}")
```

Forklar med konkrete tall hvordan en strengere toleranse og en større
`maxiter` påvirker klassifiseringen. Betyr «nådde `maxiter`» at den matematiske
følgen divergerer? Betyr $|f(z_n)|<10^{-12}$ nødvendigvis at
$|z_n-r|<10^{-12}$?

## 8. Hovedproblemstilling: Følg en grense inn i fraktalen

Tiltrekningskartet har store, rolige fargeområder der resultatet er lett å
forutsi. Mellom dem ligger smale og urolige grenser. På avstand kan en slik
grense se ut som en vanlig kurve. Men når vi beregner et nytt kart over et
mindre område, dukker det ofte opp nye bukter, øyer og striper som ikke var
synlige før.

Dette er nesten selve ideen bak en fraktal: nye detaljer fortsetter å bli
synlige når vi undersøker figuren på mindre skalaer. Det betyr ikke at hvert
zoom-bilde må være en nøyaktig minikopi av det forrige. Det viktige her er at
grensen ikke raskt blir til en enkel, glatt linje.

For Newtons metode har zoomingen også en konkret numerisk betydning. Hvert
punkt i bildet er en startverdi $z_0$. Når vinduet blir ti ganger smalere, men
fortsatt tegnes med $400\times400$ piksler, undersøker vi startverdier som
ligger ti ganger tettere. En fraktalzoom er derfor et forsøk på hvor følsomt
Newton-resultatet er for stadig mindre endringer i startverdien.

### Begrepene vi trenger

Et numerisk bilde er bygget opp av små fargede ruter. I dette prosjektet
kaller vi én slik rute en **piksel**. Hver piksel representerer resultatet fra
én startverdi i rutenettet: basin-fargen viser hvilket nullpunkt startverdien
fant, mens iterasjonskartet viser hvor mange Newton-steg som ble brukt.

**Oppløsningen** `nx × ny` er antall startverdier vi beregner i vannrett og
loddrett retning. I et vindu fra `xmin` til `xmax` er avstanden mellom to
vannrette nabostartverdier

$$
\Delta x=\frac{\texttt{xmax}-\texttt{xmin}}{\texttt{nx}-1}.
$$

Tilsvarende får vi $\Delta y$ i loddrett retning. Når vinduet er kvadratisk
og `nx = ny`, omtaler vi $\Delta x$ som **pikselbredden**. Strengt tatt er
dette avstanden mellom startverdiene som to nabopiksler representerer.

**Plottevinduet** er rektangelet av komplekse startverdier som beregnes. Å
**zoome** betyr her å velge et mindre plottevindu og beregne et helt nytt
rutenett med samme oppløsning. Det er altså ikke bare en grafisk forstørrelse
av det gamle bildet.

### Delproblem 1: Hvordan kjenner vi igjen en grense?

Før vi zoomer, trenger vi en enkel måleregel. Vi kaller en piksel en
**grensepiksel** dersom minst én nabo over, under, til venstre eller til høyre
konvergerer mot et annet nullpunkt. En **indre piksel** har samme basin-farge
som alle disse naboene.

Dette er ikke en eksakt definisjon av den matematiske grensen. Det er en
praktisk regel for et endelig bilde. Regelen lar oss koble figuren til
spørsmålet vårt: En grensepiksel representerer en startverdi der en endring på
omtrent én pikselbredde kan endre hvilket nullpunkt Newton finner.

```{pyodide-python}
def boundary_mask(data):
    """Marker piksler ved en overgang mellom to konvergensområder.

    Vi teller bare overganger mellom punkter som faktisk konvergerte. Punkter
    som nådde maxiter eller ga en ugyldig beregning får ikke lage en kunstig
    basin-grense.
    """
    basin = data["basin"]
    boundary = np.zeros(basin.shape, dtype=bool)

    # Sammenlign naboer mot venstre og høyre.
    valid_horizontal = (basin[:, :-1] >= 0) & (basin[:, 1:] >= 0)
    changes_horizontal = valid_horizontal & (basin[:, :-1] != basin[:, 1:])
    boundary[:, :-1] |= changes_horizontal
    boundary[:, 1:] |= changes_horizontal

    # Gjør samme sammenligning opp og ned.
    valid_vertical = (basin[:-1, :] >= 0) & (basin[1:, :] >= 0)
    changes_vertical = valid_vertical & (basin[:-1, :] != basin[1:, :])
    boundary[:-1, :] |= changes_vertical
    boundary[1:, :] |= changes_vertical
    return boundary


def boundary_summary(data):
    """Sammenlign Newton-arbeidet på grensen og inne i basinene."""
    boundary = boundary_mask(data)
    converged = data["basin"] >= 0
    interior = converged & ~boundary
    iterations = data["iterations"]

    return {
        "boundary_fraction": np.count_nonzero(boundary)
                             / np.count_nonzero(converged),
        "mean_boundary_iterations": np.mean(iterations[boundary]),
        "mean_interior_iterations": np.mean(iterations[interior]),
        "max_boundary_iterations": np.max(iterations[boundary]),
        "visible_basins": len(np.unique(data["basin"][converged])),
    }


def print_boundary_summary(data):
    """Skriv de samme målene for hvert zoomnivå."""
    summary = boundary_summary(data)
    xmin, xmax, ymin, ymax = data["bounds"]
    pixel_width = (xmax-xmin)/(data["basin"].shape[1]-1)

    print("Bredde på vinduet:       ", f"{xmax-xmin:.4e}")
    print("Bredde per piksel:       ", f"{pixel_width:.4e}")
    print("Synlige basin:           ", summary["visible_basins"])
    print("Andel grensepiksler:     ", f"{summary['boundary_fraction']:.4f}")
    print("Gj.snitt steg, grense:   ",
          f"{summary['mean_boundary_iterations']:.2f}")
    print("Gj.snitt steg, indre:    ",
          f"{summary['mean_interior_iterations']:.2f}")
    print("Største steg, grense:    ", summary["max_boundary_iterations"])
```

Kjør oppsummeringen på hovedkartet. Bruk tallene som nullpunkt for
zoom-ekspedisjonen—ikke som en konklusjon ennå.

```{pyodide-python}
print_boundary_summary(basin_data)
```

**Tenk før du zoomer:** Tror du grensen etter hvert blir glatt dersom du bare
zoomer langt nok inn? Tror du forskjellen i iterasjonstall mellom grense og
indre områder blir større, mindre eller omtrent den samme? Skriv ned
hypotesene dine før neste delproblem.

### Delproblem 2: Hva betyr det å zoome numerisk?

En vanlig digital zoom ville bare gjort de eksisterende pikslene større. Det
skal vi ikke gjøre. For hvert nivå lager `newton_grid` et nytt
$400\times400$-rutenett med nye startverdier i et mindre vindu. Derfor kan
det nye bildet inneholde strukturer som det gamle rutenettet ikke hadde nok
punkter til å se.

Start ved `boundary_point` fra del 6. Hvis første bilde ikke viser en
interessant grense, velger du et nytt sentrum fra hovedfiguren.

```{pyodide-python}
#| canvas: false
def square_bounds(center, width):
    """Lag et kvadratisk vindu rundt startverdien vi vil følge."""
    half = width/2
    return (center.real-half, center.real+half,
            center.imag-half, center.imag+half)


def run_zoom(center, width, resolution=400, tol=1e-8, maxiter=100):
    """Beregn og vis ett nytt nivå i fraktalzoomen.

    Behold resolution, tol og maxiter når du sammenligner nivåene. Endre
    center og width for å følge grensen videre.
    """
    zoom_bounds = square_bounds(center, width)
    data = newton_grid(
        f, df, roots, zoom_bounds,
        nx=resolution, ny=resolution, tol=tol, maxiter=maxiter
    )
    plot_basins(data, f"Fraktalzoom: bredde={width:.3e}")
    print_boundary_summary(data)
    return data


# Dette er nivå 1. Endre sentrum hvis grensen forsvinner ut av bildet.
zoom_center = boundary_point
zoom_width = min(bounds[1]-bounds[0], bounds[3]-bounds[2]) / 5
zoom_data = run_zoom(zoom_center, zoom_width)
```

### Delproblem 3: Fortsetter nye detaljer å dukke opp?

Gjør `zoom_width` omtrent ti ganger mindre for hvert nivå. Før neste kjøring
velger du et nytt sentrum på en synlig grense i det siste bildet. Du kan bruke

```python
zoom_center = suggest_boundary_point(zoom_data)
zoom_width = zoom_width / 10
zoom_data = run_zoom(zoom_center, zoom_width)
```

som utgangspunkt. Kontroller alltid figuren selv. Den automatiske funksjonen
velger bare en fargeovergang i rutenettet; den vet ikke hvilken struktur du
synes er interessant.

Lag minst tre nye zoomnivåer. Bruk samme oppløsning, `tol` og `maxiter` på
alle nivåene. Da blir én piksel en stadig mindre endring i startverdien, mens
stoppreglene er de samme.

For hvert nivå lagrer du:

- figuren med tiltrekningsområder og iterasjonstall,
- sentrum og vindusbredde,
- bredden som én piksel representerer,
- antall synlige basin-farger,
- andel grensepiksler,
- gjennomsnittlig iterasjonstall på grensen og i indre områder.

### Delproblem 4: Hva forteller fraktalzoomen om Newtons metode?

Fraktalbildet er ikke pynt ved siden av den numeriske metoden. Hver ny detalj
forteller at startverdier som er svært nær hverandre kan følge forskjellige
Newton-baner og finne forskjellige nullpunkter. Iterasjonskartet forteller i
tillegg om disse områdene er numerisk krevende.

Velg på det siste zoomnivået:

- to nabostartverdier med forskjellig basin-farge,
- én startverdi et stykke inne i et ensfarget område.

Kjør `newton_trace` for alle tre. Sammenlign de første iteratene, største
skrittlengde, antall iterasjoner og siste residual. Målet er å knytte de små
fargestrukturene tilbake til faktiske iterative følger.

### Fraktalrapporten

Skriv en samlet rapport. Figurene og tabellen er data; svarene under er
analysen.

1. Hva forventet du før du zoomet, og hva viste bildene?
2. Hvilke nye detaljer dukket opp på hvert nivå? Ble grensen noen gang en
   enkel, glatt linje?
3. Så du nøyaktige kopier av tidligere mønstre, eller nye mønstre med lignende
   kompleksitet? Hvorfor kan begge deler omtales som fraktallignende?
4. Hvor liten endring i $z_0$ representerte én piksel på siste nivå?
5. Fortsatte nabopiksler å finne forskjellige nullpunkter på denne skalaen?
6. Hvordan skilte iterasjonstallene på grensen seg fra indre områder?
7. Hva viste de tre `newton_trace`-forsøkene om hvorfor fargene blir ulike?
8. Hvordan kan `tol`, `maxiter` og flyttallsregning påvirke de minste
   strukturene du ser?
9. Hvorfor er flere vellykkede zoomnivåer god numerisk evidens for en
   fraktallignende grense, men ikke et bevis på detaljer på alle skalaer?

### Ekstra nøtt: Kan grensen ha en dimensjon mellom 1 og 2?

Denne delen er frivillig. Den introduserer én idé som ikke er nødvendig for
resten av prosjektet.

Fraktalzoomen viste nye detaljer, men kan vi sette ett enkelt tall på hvor
komplisert grensen ser ut? Vi begynner uten en formel.

Se for deg at grensen var en vanlig, glatt strek gjennom bildet. Hvis vi går
fra 100 til 200 piksler i hver retning, blir pikslene omtrent halvparten så
brede. Da trenger vi omtrent dobbelt så mange små piksler for å følge den samme
streken:

$$
100\longrightarrow200
\qquad\text{gir omtrent}\qquad
N\longrightarrow2N.
$$

En strek vokser altså med omtrent faktor 2 når oppløsningen dobles.

Tenk deretter på et område som er helt fylt med grense. Når vi dobler
oppløsningen, får vi dobbelt så mange piksler vannrett *og* dobbelt så mange
loddrett. Antallet blir da omtrent fire ganger så stort:

$$
N\longrightarrow4N.
$$

En fraktalgrense kan vokse raskere enn en vanlig strek, men langsommere enn et
helt fylt område. Derfor ser vi først på den enkle **vekstfaktoren**

$$
q=\frac{\text{nytt antall grensepiksler}}
        {\text{gammelt antall grensepiksler}}.
$$

- $q\approx2$ ligner veksten til en vanlig linje.
- $q\approx4$ ligner veksten til et fylt område.
- En verdi mellom 2 og 4 tyder på noe mellom disse ytterpunktene.

Hvis vi ønsker å skrive dette som et dimensjonstall, spør vi: Hvilken potens
$D$ må vi opphøye 2 i for å få vekstfaktoren?

$$
2^D=q.
$$

Dermed gir $q=2$ dimensjonen $D=1$, mens $q=4$ gir $D=2$. For andre
vekstfaktorer regner Python ut

$$
D=\log_2(q).
$$

Dette er hele ideen bak dimensjonsanslaget i nøtten.

Vi må bruke **ett fast plottevindu**. Vi gjør pikslene mindre ved å øke
oppløsningen fra 100 til 200 og deretter 400, men vi flytter ikke vinduet. Hvis
vinduet også flyttes eller krympes, vet vi ikke om endringen skyldes mindre
piksler eller at vi har valgt en annen del av grensen.

```{pyodide-python}
def boundary_growth_experiment(test_bounds,
                               resolutions=(100, 200, 400),
                               tol=1e-8, maxiter=100):
    """Se hvor raskt antall grensepiksler vokser i ett fast vindu.

    Oppløsningen skal dobles i hvert steg. Da kan vi sammenligne veksten med
    faktor 2 for en linje og faktor 4 for et fylt område.
    """
    xmin, xmax, ymin, ymax = test_bounds
    measurements = []

    print(" oppløsning   pikselbredde   grensepiksler")
    for resolution in resolutions:
        # Samme vindu og samme Newton-parametere; bare rutenettet blir finere.
        data = newton_grid(
            f, df, roots, test_bounds,
            nx=resolution, ny=resolution, tol=tol, maxiter=maxiter
        )

        # Avstanden mellom startverdiene som to nabopiksler representerer.
        pixel_width = (xmax-xmin)/(resolution-1)

        # boundary_mask bruker den samme naboregelen som i fraktalzoomen.
        count = int(np.count_nonzero(boundary_mask(data)))
        measurements.append((resolution, pixel_width, count))
        print(f" {resolution:10d}   {pixel_width:12.4e}   {count:14d}")

    print("\nHva skjer når oppløsningen dobles?")
    for first, second in zip(measurements[:-1], measurements[1:]):
        old_resolution, old_width, old_count = first
        new_resolution, new_width, new_count = second

        if new_resolution != 2*old_resolution:
            raise ValueError("Oppløsningen må dobles i denne nøtten")

        # q forteller hvor mange ganger flere grensepiksler vi fant.
        growth = new_count/old_count

        # 2**D = q. Derfor er D lik logaritmen med grunntall 2 av q.
        dimension = np.log2(growth)
        print(f" {old_resolution:4d} → {new_resolution:4d}: "
              f"vekstfaktor {growth:.3f}, D ≈ {dimension:.3f}")

    return measurements


# Kjør nøtten i ETT av zoomvinduene dine etter at zoomserien er ferdig.
# growth_data = boundary_growth_experiment(zoom_data["bounds"])
```

Les først vekstfaktoren uten å se på $D$: Ligger den nærmest 2, nærmest 4 eller
mellom? Bruk deretter $D$ som en kort oppsummering av den samme målingen.

Vurder om de to $D$-anslagene nærmer seg hverandre. Et tall mellom 1 og 2 er
interessant evidens, men ikke et bevis eller en eksakt dimensjon. Resultatet
avhenger av vinduet, oppløsningene, grensepikselregelen, `tol` og `maxiter`.
Forklar også med egne ord hvorfor vi ikke kan bruke tre forskjellige
zoomvinduer i samme måling.

## 9. Konklusjon

Skriv en samlet konklusjon på omtrent 200–300 ord. Den skal svare på:

- Hvordan påvirker startverdien hvilket nullpunkt Newtons metode finner?
- Hvor er konvergensen rask, og hvor kreves mange iterasjoner?
- Finner metoden alltid nullpunktet som ligger nærmest startverdien?
- Hvilken rolle ser de kritiske punktene ut til å spille?
- Hva viste perturbasjonsforsøket nær en grense?
- Hva viste fraktalzoomen om følsomhet for stadig mindre endringer i startverdien?
- Hvordan påvirker residualtoleransen og `maxiter` klassifiseringen?
- Hvilke påstander bygger på numeriske eksperimenter, og hva kan eksperimentene ikke bevise?
- Når mener du det er forsvarlig å rapportere at metoden har konvergert?

## Leveranse

Lever én Quarto-side eller notebook med:

1. tildelt funksjon og nullpunkter,
2. analyserte iterasjonshistorikker for raske, langsomme og følsomme startverdier,
3. hovedfigur med tiltrekningsområder og iterasjonskart,
4. test av om nærmeste nullpunkt blir funnet,
5. undersøkelse av ett kritisk punkt,
6. perturbasjonsforsøk nær en grense,
7. kontroll av toleranse og `maxiter`,
8. minst tre zoomnivåer, grensesammenligning og fraktalrapport,
9. konkrete parameterverdier og konklusjonen.

::: {.callout-warning}
## Om bruk av kodeassistenter

Copilot og andre kodeassistenter er tillatt. Du er likevel ansvarlig for at stoppkriteriet har en matematisk betydning, at ugyldige og ikke-konvergente beregninger behandles separat, at figurene viser det du sier de viser, og at konklusjonene støttes av egne resultater.

Kode som produserer en figur, er ikke i seg selv en analyse.
:::
