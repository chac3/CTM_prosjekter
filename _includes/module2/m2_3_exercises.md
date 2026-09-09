#### Les nøyaktighet fra et semilogaritmisk plott

Når feilene blir små, kan de variere fra tideler til milliarddeler på få iterasjoner. På en vanlig loddrett akse blir de minste verdiene presset sammen nær null. Et **semilogaritmisk plott**, ofte kalt et `semilogy`-plott i Python, løser dette ved å bruke

- en vanlig, lineær akse for iterasjonsnummeret $n$, og
- en logaritmisk akse for den absolutte feilen $|e_n|$.

På den logaritmiske aksen betyr like store loddrette avstander like store *faktorer*, ikke like store differanser. Ett hovedtrinn ned fra $10^{-3}$ til $10^{-4}$ betyr at feilen er delt på $10$. En rett, synkende linje betyr derfor at feilen reduseres med omtrent samme faktor i hvert steg. En kurve som blir stadig brattere, kan tyde på raskere konvergens, for eksempel kvadratisk konvergens.

Vi sammenligner tre fikspunktiterasjoner som alle har fikspunktet $r=0$:

| Kurve | Oppdateringsregel | Startverdi | Forventet oppførsel nær $0$ |
|---|---|---:|---|
| Blå | $x_{n+1}=0.8x_n$ | $x_0=0.1$ | langsom lineær konvergens |
| Oransje | $x_{n+1}=0.1x_n$ | $x_0=0.1$ | rask lineær konvergens |
| Grønn | $x_{n+1}=x_n^2$ | $x_0=0.3$ | kvadratisk konvergens |

For de lineære reglene blir feilen multiplisert med henholdsvis $0.8$ og $0.1$ i hvert steg. For den grønne kurven er $e_{n+1}=e_n^2$, så antallet korrekte desimaler vokser mye raskere når feilen først er liten.

```{pyodide-python}
#| canvas: false

def error_history(g, x0, number_of_steps):
    values = iterate(g, x0, number_of_steps)
    return np.abs(values)  # Fikspunktet er r = 0

steps = np.arange(6)
errors_slow = error_history(lambda x: 0.8*x, 0.1, 5)
errors_fast = error_history(lambda x: 0.1*x, 0.1, 5)
errors_quadratic = error_history(lambda x: x**2, 0.3, 5)

plt.close("all")
fig, ax = plt.subplots(figsize=(8, 6))
ax.semilogy(steps, errors_slow, "o-", color="tab:blue",
            label="Blå: langsom lineær")
ax.semilogy(steps, errors_fast, "o-", color="tab:orange",
            label="Oransje: rask lineær")
ax.semilogy(steps, errors_quadratic, "o-", color="tab:green",
            label="Grønn: kvadratisk")
ax.set_xticks(steps)
ax.set_ylim(1e-18, 1)
ax.set_xlabel("Iterasjon $n$")
ax.set_ylabel("Absolutt feil $|e_n|$")
ax.set_title("Tre typer konvergens")
ax.grid(True, which="both", alpha=0.35)
ax.legend()
plt.show()
```

::: {#semilogy-decimals-context .math-exercise-context}

Bruk kriteriet

$$
|e_n|<\frac12 10^{-p}
$$

og finn det største heltallet $p$ som oppfyller ulikheten. Dette er antallet korrekte desimaler ved iterasjon $n$.

«Nye desimaler fra steg 4 til 5» betyr

$$
p_5-p_4,
$$

altså antallet korrekte desimaler etter steg 5 minus antallet etter steg 4. Les først omtrentlige feil fra plottet, og bruk tierpotensene på den logaritmiske aksen til å velge riktig grense.

:::

```{math-exercise}
#| label: read-semilogy-correct-decimals
#| caption: Les korrekte desimaler fra semilogy-plottet
#| mode: equivalent
#| field-labels: blå etter steg 5, oransje etter steg 5, grønn etter steg 5, nye blå fra 4 til 5, nye oransje fra 4 til 5, nye grønne fra 4 til 5
#| context: semilogy-decimals-context

Oppgi ett ikke-negativt heltall i hvert felt.

**Antall korrekte desimaler etter iterasjon 5:**

Blå kurve: _[1]<br>
Oransje kurve: _[5]<br>
Grønn kurve: _[16]

**Antall nye korrekte desimaler i overgangen fra iterasjon 4 til 5:**

Blå kurve: _[0]<br>
Oransje kurve: _[1]<br>
Grønn kurve: _[8]
```

#### Klikk på iteratet med sju korrekte desimaler

Den interaktive grafen nedenfor viser den raske lineære iterasjonen $x_{n+1}=0.1x_n$ med $x_0=0.1$. Det er den samme oransje kurven som i semilogy-plottet, forlenget med noen steg.

Den loddrette koordinaten er $\log_{10}(|e_n|)$. For eksempel betyr høyden $-4$ at feilen er $10^{-4}$. Klikk på datapunktet som har **sju korrekte desimaler** etter kriteriet $|e_n|<\frac12 10^{-7}$. Det valgte punktet markeres med rødt.

```{.jsxgraph assessment_id="seven-correct-decimals-board" width="760" height="440"}
var board = JXG.JSXGraph.initBoard(BOARDID, {
  boundingbox: [-0.7, 0, 8.8, -10],
  axis: true,
  showCopyright: false,
  showNavigation: false,
  pan: { enabled: false },
  zoom: { enabled: false }
});

var iterations = [0, 1, 2, 3, 4, 5, 6, 7, 8];
var logErrors = [-1, -2, -3, -4, -5, -6, -7, -8, -9];

board.create('curve', [iterations, logErrors], {
  strokeColor: '#ff7f0e',
  strokeWidth: 3,
  fixed: true,
  highlight: false
});

for (var i = 0; i < iterations.length; i++) {
  board.create('point', [iterations[i], logErrors[i]], {
    name: '',
    size: 3,
    face: 'o',
    fillColor: '#ff7f0e',
    strokeColor: '#ff7f0e',
    fixed: true,
    highlight: false
  });
}

board.create('text', [4.1, -0.45, 'iterasjon n'], {
  fixed: true,
  fontSize: 14
});
board.create('text', [-0.55, -9.45, 'log10(|e_n|)'], {
  fixed: true,
  fontSize: 14,
  rotate: 90
});

var selectedIndex = null;
var selectedPoint = board.create('point', [0, -1], {
  name: '',
  size: 6,
  face: 'o',
  fillColor: '#d62728',
  strokeColor: '#d62728',
  visible: false,
  fixed: true,
  highlight: false
});

board.on('down', function (event) {
  var corner = board.getCoordsTopLeftCorner(event);
  var position = JXG.getPosition(event, 0);
  var coordinates = new JXG.Coords(
    JXG.COORDS_BY_SCREEN,
    [position[0] - corner[0], position[1] - corner[1]],
    board
  );
  var x = coordinates.usrCoords[1];
  var y = coordinates.usrCoords[2];
  var bestIndex = 0;
  var bestDistance = Infinity;

  for (var j = 0; j < iterations.length; j++) {
    var distance = Math.pow(x - iterations[j], 2) +
                   Math.pow(y - logErrors[j], 2);
    if (distance < bestDistance) {
      bestDistance = distance;
      bestIndex = j;
    }
  }

  selectedIndex = bestIndex;
  selectedPoint.setPosition(
    JXG.COORDS_BY_USER,
    [iterations[bestIndex], logErrors[bestIndex]]
  );
  selectedPoint.setAttribute({ visible: true });
  board.update();
});

JXG.QuartoAssessment.register({
  board: board,
  response: function () {
    return { index: selectedIndex };
  },
  ai: {
    render: true,
    summary: function (data) {
      return { selected_iteration: data.index };
    }
  }
});
```

```{math-exercise}
#| label: click-seven-correct-decimals
#| caption: Finn punktet med sju korrekte desimaler
#| mode: custom
#| response: jsxgraph:seven-correct-decimals-board
#| embed-response: true
#| context: none
#| checker: |
#|   def check(response, symbols):
#|       index = response.get("index")
#|       if index is None:
#|           return {"score": 0, "feedback": "Klikk på ett av punktene før du kontrollerer svaret."}
#|       if int(index) == 7:
#|           return {"score": 1, "feedback": "Riktig. Ved n = 7 er feilen 10^(-8), som gir sju korrekte desimaler."}
#|       return {"score": 0, "feedback": "Ikke helt. Les av feilen i punktet og sammenlign den med 0.5·10^(-7) og 0.5·10^(-8)."}

Klikk på punktet på kurven som viser at iteratet har sju korrekte desimaler.
```

#### Finn det første kvadratiske iteratet som passerer sju desimaler

Den grønne iterasjonen $x_{n+1}=x_n^2$ med $x_0=0.3$ konvergerer kvadratisk mot fikspunktet $r=0$. Her finnes det ikke nødvendigvis et iterat med *akkurat* sju korrekte desimaler: Kvadratisk konvergens kan hoppe over flere nivåer i ett steg.

Grafen viser den samme grønne kurven som i semilogy-plottet. Klikk på det **første** punktet som har minst sju korrekte desimaler. Sammenlign feilen med grensen $\frac12 10^{-7}=5\cdot10^{-8}$. Det valgte punktet markeres med rødt.

```{.jsxgraph assessment_id="quadratic-seven-decimals-board" width="760" height="440"}
var board = JXG.JSXGraph.initBoard(BOARDID, {
  boundingbox: [-0.5, 0, 5.7, -19],
  axis: true,
  showCopyright: false,
  showNavigation: false,
  pan: { enabled: false },
  zoom: { enabled: false }
});

var iterations = [0, 1, 2, 3, 4, 5];
var errors = [];
var value = 0.3;
for (var i = 0; i < iterations.length; i++) {
  errors.push(Math.abs(value));
  value = value*value;
}
var logErrors = errors.map(function (error) {
  return Math.log10(error);
});

board.create('curve', [iterations, logErrors], {
  strokeColor: '#2ca02c',
  strokeWidth: 3,
  fixed: true,
  highlight: false
});

for (var j = 0; j < iterations.length; j++) {
  board.create('point', [iterations[j], logErrors[j]], {
    name: '',
    size: 3,
    face: 'o',
    fillColor: '#2ca02c',
    strokeColor: '#2ca02c',
    fixed: true,
    highlight: false
  });
}

var threshold = Math.log10(0.5*Math.pow(10, -7));
board.create('line', [[0, threshold], [1, threshold]], {
  straightFirst: true,
  straightLast: true,
  strokeColor: '#666666',
  strokeWidth: 2,
  dash: 2,
  fixed: true,
  highlight: false
});
board.create('text', [0.15, threshold + 0.55, 'grense for minst 7 desimaler'], {
  fixed: true,
  fontSize: 13
});
board.create('text', [2.3, -0.6, 'iterasjon n'], {
  fixed: true,
  fontSize: 14
});
board.create('text', [-0.38, -17.2, 'log10(|e_n|)'], {
  fixed: true,
  fontSize: 14,
  rotate: 90
});

var selectedIndex = null;
var selectedPoint = board.create('point', [0, logErrors[0]], {
  name: '',
  size: 6,
  face: 'o',
  fillColor: '#d62728',
  strokeColor: '#d62728',
  visible: false,
  fixed: true,
  highlight: false
});

board.on('down', function (event) {
  var corner = board.getCoordsTopLeftCorner(event);
  var position = JXG.getPosition(event, 0);
  var coordinates = new JXG.Coords(
    JXG.COORDS_BY_SCREEN,
    [position[0] - corner[0], position[1] - corner[1]],
    board
  );
  var x = coordinates.usrCoords[1];
  var y = coordinates.usrCoords[2];
  var bestIndex = 0;
  var bestDistance = Infinity;

  for (var k = 0; k < iterations.length; k++) {
    var dx = x - iterations[k];
    var dy = (y - logErrors[k])/3;
    var distance = dx*dx + dy*dy;
    if (distance < bestDistance) {
      bestDistance = distance;
      bestIndex = k;
    }
  }

  selectedIndex = bestIndex;
  selectedPoint.setPosition(
    JXG.COORDS_BY_USER,
    [iterations[bestIndex], logErrors[bestIndex]]
  );
  selectedPoint.setAttribute({ visible: true });
  board.update();
});

JXG.QuartoAssessment.register({
  board: board,
  response: function () {
    return {
      index: selectedIndex,
      error: selectedIndex === null ? null : errors[selectedIndex]
    };
  },
  ai: {
    render: true,
    summary: function (data) {
      return { selected_iteration: data.index, selected_error: data.error };
    }
  }
});
```

```{math-exercise}
#| label: click-quadratic-seven-decimals
#| caption: Finn når den kvadratiske kurven passerer sju desimaler
#| mode: custom
#| response: jsxgraph:quadratic-seven-decimals-board
#| embed-response: true
#| context: none
#| checker: |
#|   def check(response, symbols):
#|       index = response.get("index")
#|       if index is None:
#|           return {"score": 0, "feedback": "Klikk på ett av punktene før du kontrollerer svaret."}
#|       if int(index) == 4:
#|           return {"score": 1, "feedback": "Riktig. Ved n = 4 er feilen omtrent 4.3·10^(-9), så iteratet har 8 korrekte desimaler og er det første som har minst 7."}
#|       return {"score": 0, "feedback": "Ikke helt. Finn det første punktet under linjen |e_n| = 5·10^(-8)."}

Klikk på det første grønne punktet som har minst sju korrekte desimaler.
```
