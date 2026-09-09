#### Kan resultatet sendes videre?

En beregningsmodul skal finne den positive løsningen av

$$
f(x)=x^2-2=0.
$$

Resultatet skal brukes videre i et kontrollsystem. Før det skjer, må en ingeniør kontrollere at programmet faktisk har funnet en løsning. Systemkravet er

$$
|f(x)|<10^{-8}.
$$

Programmet har prøvd tre oppdateringsregler med samme startverdi $x_0=1$ og de samme innstillingene `atol=1e-10`, `rtol=1e-10` og `maxiter=10`:

$$
\begin{aligned}
\text{A:}\quad x_{n+1}&=\frac12\left(x_n+\frac{2}{x_n}\right),\\
\text{B:}\quad x_{n+1}&=\frac{2}{x_n},\\
\text{C:}\quad x_{n+1}&=x_n-10^{-12}(x_n^2-2).
\end{aligned}
$$

Alle tre reglene har $\sqrt2$ som fikspunkt, men de beveger seg svært forskjellig på vei dit. Regel C tar med vilje svært små skritt. Det gjør den nyttig for å undersøke om «lite skritt» alene er et trygt stoppkriterium.

Koden under kjører de tre reglene med `fixed_point` fra fanen «Implementasjon». For hver kjøring viser plottet

- **skrittlengden** $|x_n-x_{n-1}|$, som måler hvor mye den lagrede verdien endret seg,
- **residualen** $|f(x_n)|=|x_n^2-2|$, som måler hvor godt den siste verdien oppfyller ligningen.

En kjøring kan bare godkjennes dersom residualen er under systemkravet. En stoppmelding er ikke nok i seg selv.

```{pyodide-python}
def equation(x):
    return x*x - 2

def update_A(x):
    return 0.5*(x + 2/x)

def update_B(x):
    return 2/x

def update_C(x):
    return x - 1e-12*equation(x)

updates = {"A": update_A, "B": update_B, "C": update_C}
runs = {}

for name, update in updates.items():
    runs[name] = fixed_point(
        update, 1.0, f=equation,
        atol=1e-10, rtol=1e-10, maxiter=10
    )

plt.close("all")
fig, axes = plt.subplots(1, 3, figsize=(12, 4.2), sharey=True)

for ax, name in zip(axes, ["A", "B", "C"]):
    run = runs[name]
    iterations = np.arange(1, run["iterations"] + 1)
    ax.semilogy(iterations, run["steps"], "o-", label="skrittlengde")
    ax.semilogy(iterations, run["residuals"][1:], "s-", label="residual")
    ax.axhline(1e-8, color="black", linestyle="--",
               linewidth=1, label="krav til residual")
    ax.set_title(f"Kjøring {name}\nStopp: {run['reason']}")
    ax.set_xlabel("Iterasjon")
    ax.set_xticks(iterations)
    ax.grid(True, which="both", alpha=0.3)

axes[0].set_ylabel("Størrelse (logaritmisk skala)")
axes[0].set_ylim(1e-16, 3)
axes[2].legend(loc="lower left", fontsize=8)
fig.suptitle("Tre kjøringer av samme ligning")
fig.tight_layout()
plt.show()

for name in ["A", "B", "C"]:
    run = runs[name]
    print(
        f"{name}: x={run['x']:.12g}, iterasjoner={run['iterations']}, "
        f"stopp='{run['reason']}', residual={run['residuals'][-1]:.3e}"
    )
```

Les plottet som en kontrollrapport:

1. Se først på stoppårsaken over hvert panel.
2. Kontroller deretter om residualen ender under den stiplede kravlinjen.
3. Se til slutt på utviklingen. Verdier som gjentar seg på to nivåer, tyder på en 2-syklus. Et lite skritt sammen med stor residual tyder på at programmet har stoppet før det nådde løsningen.

::: {#diagnose-three-runs-context .math-exercise-context}

Bruk kodene **A = 1**, **B = 2** og **C = 3**.

:::

```{math-exercise}
#| label: diagnose-three-iterations
#| caption: Finn riktig diagnose
#| mode: equivalent
#| field-labels: godkjent kjøring, kjøring med 2-syklus, kjøring med falskt vellykket stopp
#| context: diagnose-three-runs-context

Oppgi nummeret til kjøringen.

- Hvilken kjøring oppfyller residualkravet og kan sendes videre? _[1]
- Hvilken kjøring alternerer mellom to verdier? _[2]
- Hvilken kjøring rapporterer «lite skritt» selv om residualen er for stor? _[3]
```

Stoppårsaken sier hva programmet observerte, ikke nødvendigvis at svaret er riktig. Bruk disse kodene:

1. lite skritt
2. maksimalt antall iterasjoner
3. ikke-endelig verdi

```{math-exercise}
#| label: identify-stop-reasons
#| caption: Les stoppårsakene
#| mode: equivalent
#| field-labels: stoppårsak A, stoppårsak B, stoppårsak C

Skriv koden for stoppårsaken til hver kjøring.

- Kjøring A: _[1]
- Kjøring B: _[2]
- Kjøring C: _[1]
```

Nå skal du velge hva en ingeniør bør gjøre med hver kjøring:

1. godkjenn resultatet,
2. bytt oppdateringsregel,
3. krev både liten skrittlengde og liten residual før resultatet godkjennes.

```{math-exercise}
#| label: choose-diagnostic-action
#| caption: Velg riktig tiltak
#| mode: equivalent
#| field-labels: tiltak A, tiltak B, tiltak C

Skriv koden for det beste tiltaket.

- Kjøring A: _[1]
- Kjøring B: _[2]
- Kjøring C: _[3]
```

For B hjelper det ikke bare å øke `maxiter`: regelen fortsetter å sende $1$ til $2$ og $2$ tilbake til $1$. For C er oppdateringsregelen på vei mot riktig fikspunkt, men så sakte at skrittlengden blir liten lenge før residualen er god nok.

#### Forbedre stoppkontrollen

Funksjonen `fixed_point` godkjenner nå et resultat når skrittlengden alene er liten. I en beregning med et eget residualkrav bør begge kravene være oppfylt:

```python
step <= step_tolerance and residual_value <= residual_tolerance
```

Bruk den redigerbare cellen under som en liten testbenk. Endre bare linjen med `return`, slik at alle tre kontrollene skriver `bestått`.

```{pyodide-python}
def approve_result(step, step_tolerance, residual_value, residual_tolerance):
    # Endre denne linjen: Begge kravene må være oppfylt.
    return step <= step_tolerance

test_cases = [
    ("lite skritt og liten residual", 1e-11, 1e-10, 1e-12, 1e-8, True),
    ("stort skritt",                 1e-4,  1e-10, 1e-12, 1e-8, False),
    ("liten endring, feil svar",     1e-12, 1e-10, 1.0,   1e-8, False),
]

for description, step, step_tol, residual, residual_tol, expected in test_cases:
    received = approve_result(step, step_tol, residual, residual_tol)
    status = "bestått" if received == expected else "må rettes"
    print(f"{description:29s}: {status}")
```

Når alle testene består, har stoppkontrollen skilt mellom «verdien endrer seg nesten ikke» og «verdien oppfyller ligningen godt nok». Det er denne forskjellen som gjør at A kan godkjennes, mens C må undersøkes videre.
