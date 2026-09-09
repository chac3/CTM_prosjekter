:::: {.callout-note}
## Slik bruker du siden

Siden har to leseløp. **Hovedløpet** består av en faglig gjennomgang i
3.1–3.5 og en praktisk del i 3.6. Gå gjennom 3.1–3.5 i vanlig rekkefølge, og
arbeid deretter med eksperimentene i 3.6 for å bruke begrepene selv.

**Støtteløpet** er et oppslagsverk dersom Gauss-eliminasjon, pivoter,
kolonnerom eller nullrom ikke sitter friskt. Matriserepetisjonen står i 3.7,
og papir- og kontrolloppgavene står i 3.8. Du kan deretter vende tilbake til
hovedløpet. Du trenger ikke gjennomføre hele støtteløpet dersom
forkunnskapene sitter.
::::

:::: {.callout-tip collapse="true"}
## NumPy-cheatsheet for denne uka

Koden er et verktøy for å undersøke lineær algebra, ikke et eget
programmeringspensum. Åpne denne boksen når du møter en ukjent kodelinje.
Du trenger ikke lære alt utenat.

### Lag og les arrays

```python
x = np.array([2.0, -1.0, 3.0])
X = np.array([[1.0, 2.0],
              [3.0, 4.0]])
```

`x` er en vektor med tre tall. `X` er en $2\times2$-tabell. Python teller fra
0, så `x[0]` er første tall, `X[0, 1]` er tallet i første rad og andre
kolonne, og `X.shape` er `(2, 2)`.

### Bytt mellom bilde og vektor

```python
x = X.reshape(-1)       # [1., 2., 3., 4.]
X_again = x.reshape(2, 2)
```

`reshape` flytter ikke eller endrer noen verdier. Den viser bare de samme
tallene med en annen form. `-1` betyr «la NumPy finne riktig lengde».

### Bygg matriser av vektorer

```python
A = np.column_stack([u, v])   # u og v blir kolonner
B = np.vstack([r1, r2])       # r1 og r2 blir rader
```

Bruk `column_stack` når vektorene er byggesteiner eller basisvektorer. Bruk
`vstack` når hver vektor beskriver én måling eller én ligning.

### Regn med matriser

```python
y = A @ x
c = np.linalg.solve(P, target)
```

`A @ x` er matrise-vektorproduktet $Ax$. `solve(P, target)` gjør reverse
engineering: Den finner koeffisientene `c` som oppfyller
`P @ c = target`. Den brukes her bare når den kvadratiske matrisen har én
entydig løsning.

### Kontroller et matematisk svar

```python
error = np.linalg.norm(A @ x - b)
rank = np.linalg.matrix_rank(A)
```

`norm` måler størrelsen på forskjellen. Et resultat som `1e-15` leses
vanligvis som numerisk null. `matrix_rank` teller hvor mange uavhengige
retninger NumPy kan skille med maskinpresisjonen; den erstatter ikke
begrunnelsen med pivoter eller lineær uavhengighet.

### Lag nyttige tallfølger og testdata

```python
indices = np.arange(4)                 # 0, 1, 2, 3
points = np.linspace(-1.0, 1.0, 5)    # fem jevnt fordelte punkter
rng = np.random.default_rng(8)
test = rng.random((2, 2))              # et tilfeldig 2x2-bilde
```

Et fast tall i `default_rng(8)` gjør at alle får de samme testdataene. Da kan
vi gjenta forsøket og sammenligne svar. `np.repeat` brukes senere til å
kopiere en verdi flere ganger; `np.zeros((m, n))` lager en $m\times n$-matrise
som studenten kan fylle ut.

Kode merket som **ferdig maskineri** kan brukes uten at du forstår alle
indeksene og løkkene. Les først kommentarene og spør: Hva er inputen? Hva er
outputen? Hvilken matematisk påstand skal utskriften eller figuren kontrollere?
::::

::: {.panel-tabset}

## 3.1 To bilder, samme output {#uke3-start}

En **transformasjon** er her en regel som tar en input og lager en output. Inputen kan være et bilde, en lydfil eller en tabell med målinger; outputen kan være et nytt bilde eller noen få tall som oppsummerer inputen. Vi skriver ofte

$$T(\text{input})=\text{output}.$$

Dette er også definisjonen av en **funksjon**: Hver tillatt input får nøyaktig én output. I matematikk er for eksempel $f(t)=t^2$ en funksjon som sender $3$ til $9$. I Python gjør `abs(-3)` inputen `-3` om til outputen `3`. På samme måte tar Python-funksjonen `average_pool(X)` inn et bilde og returnerer et mindre bilde.

Navnet transformasjon sier foreløpig ikke noe mer mystisk enn dette. Det framhever bare at input og output gjerne er vektorer eller bilder, ikke nødvendigvis enkelttall. Det viktige er å spørre konkret: Hvilken informasjon bruker regelen, hvilken informasjon kommer ut, og kan noe gå tapt underveis?

Denne uka bruker vi én enkel bildetransformasjon som gjennomgående eksempel. Den gjør et bilde med 16 piksler om til et mindre bilde med fire piksler. Figuren viser hele oppskriften uten matriser eller formler.

```{.jsxgraph width="760" height="430"}
var board = JXG.JSXGraph.initBoard(BOARDID, {
  boundingbox: [0, 7.1, 12.2, 0.1],
  axis: false,
  showCopyright: false,
  showNavigation: false,
  pan: { enabled: false },
  zoom: { enabled: false }
});

var colors = ['#8ecae6', '#ffcf70', '#a8d5a2', '#d7b5e8'];
var dark = ['#277da1', '#d98900', '#4f8f49', '#8b5aa7'];

function rectangle(x0, y0, x1, y1, color, opacity, border) {
  return board.create('polygon', [[x0,y0],[x1,y0],[x1,y1],[x0,y1]], {
    fillColor: color,
    fillOpacity: opacity,
    vertices: { visible: false },
    borders: { strokeColor: border || '#555555', strokeWidth: 1.5,
               fixed: true, highlight: false },
    fixed: true,
    highlight: false
  });
}

// Stort bilde: fire fargekodede områder, hvert med fire synlige piksler.
for (var row = 0; row < 4; row++) {
  for (var col = 0; col < 4; col++) {
    var group = (row < 2 ? 0 : 2) + (col < 2 ? 0 : 1);
    var x0 = 0.8 + col;
    var y1 = 6.0 - row;
    rectangle(x0, y1-1, x0+1, y1, colors[group], 0.72, '#ffffff');
  }
}
rectangle(0.8,2.0,4.8,6.0,'none',0,'#333333');
board.create('segment', [[2.8,2.0],[2.8,6.0]], {
  strokeColor:'#333333', strokeWidth:3, fixed:true, highlight:false
});
board.create('segment', [[0.8,4.0],[4.8,4.0]], {
  strokeColor:'#333333', strokeWidth:3, fixed:true, highlight:false
});

board.create('text', [2.8,6.55,'STORT BILDE'], {
  anchorX:'middle', fontSize:16, cssStyle:'font-weight:600', fixed:true
});
board.create('text', [2.8,1.55,'Fire fargede områder · fire piksler i hvert'], {
  anchorX:'middle', fontSize:13, fixed:true
});

// Lite outputbilde: ett felt for hvert område.
var output = [
  [8.0,4.7,9.3,6.0], [9.3,4.7,10.6,6.0],
  [8.0,3.4,9.3,4.7], [9.3,3.4,10.6,4.7]
];
for (var i = 0; i < 4; i++) {
  rectangle(output[i][0],output[i][1],output[i][2],output[i][3],
            colors[i],0.85,'#ffffff');
  board.create('text', [(output[i][0]+output[i][2])/2,
                        (output[i][1]+output[i][3])/2,'ett tall'], {
    anchorX:'middle', anchorY:'middle', fontSize:12, fixed:true
  });
}
rectangle(8.0,3.4,10.6,6.0,'none',0,'#333333');
board.create('segment', [[9.3,3.4],[9.3,6.0]], {
  strokeColor:'#333333', strokeWidth:3, fixed:true, highlight:false
});
board.create('segment', [[8.0,4.7],[10.6,4.7]], {
  strokeColor:'#333333', strokeWidth:3, fixed:true, highlight:false
});
board.create('text', [9.3,6.55,'MINDRE BILDE'], {
  anchorX:'middle', fontSize:16, cssStyle:'font-weight:600', fixed:true
});

// Fire piler viser hvilket område som blir hvilken outputpiksel.
var starts = [[2.25,5.35],[4.25,5.35],[2.25,2.65],[4.25,2.65]];
var ends = [[8.0,5.35],[9.95,5.35],[8.0,4.05],[9.95,4.05]];
var bends = [6.25,6.05,1.05,1.25];
for (var j = 0; j < 4; j++) {
  var sx=starts[j][0], sy=starts[j][1], ex=ends[j][0], ey=ends[j][1];
  board.create('curve', [
    [sx, sx+1.15, ex-1.15, ex],
    [sy, bends[j], bends[j], ey]
  ], {
    strokeColor: dark[j], strokeWidth: 3, lastArrow: true,
    fixed: true, highlight: false
  });
}

board.create('text', [6.35,3.58,'samle'], {
  anchorX:'middle', fontSize:14, cssStyle:'font-weight:600', fixed:true
});
board.create('text', [6.35,3.22,'fire piksler'], {
  anchorX:'middle', fontSize:13, fixed:true
});
```

Fargene og pilene viser hva som hører sammen. De fire pikslene i det blå området samles til den blå outputpikselen, og tilsvarende for de tre andre områdene. I vårt eksempel betyr «samle» at vi tar gjennomsnittet av de fire pikselverdiene. Dermed går vi fra 16 tall til fire tall. Vi begynner med to bilder som ser helt forskjellige ut: et ensfarget bilde og et tydelig sjakkmønster.

Den neste cellen er ferdig maskineri for å vise bilder og beregne de fire
gjennomsnittene. Du trenger ikke forstå `reshape`-uttrykket ennå; i 3.2 ser
vi nøye på hvordan et bilde legges over i en vektor. Akkurat nå er spørsmålet
bare hva transformasjonen beholder, og hva den mister.

```{pyodide-python}
#| label: week3-setup
#| autorun: true
#| context: setup

# Felles verktøy for hele siden. Denne cellen kjøres automatisk.
# Studentoppgavene bruker funksjonene, men krever ikke at du kan skrive dem.
import numpy as np
import matplotlib.pyplot as plt

def show_images(images, titles=None, cols=4, cmap="gray",
                vmin=None, vmax=None, figsize=None):
    """Vis flere 2D-arrays med samme fargeskala."""
    # Lukk eldre figurer før vi lager en ny. Det hindrer at en lang
    # arbeidsøkt samler mange usynlige figurer i minnet.
    plt.close("all")
    images = list(images)
    titles = [""]*len(images) if titles is None else list(titles)
    rows = int(np.ceil(len(images)/cols))
    # Små figurer er lettere å sammenligne mens siden brukes som tavle.
    figsize = (1.75*cols, 1.75*rows) if figsize is None else figsize
    fig, axes = plt.subplots(rows, cols, figsize=figsize, squeeze=False)
    axes = axes.ravel()
    for ax, image, title in zip(axes, images, titles):
        ax.imshow(image, cmap=cmap, vmin=vmin, vmax=vmax,
                  interpolation="nearest")
        ax.set_title(title, fontsize=9)
        ax.set_xticks([]); ax.set_yticks([])
    for ax in axes[len(images):]:
        ax.axis("off")
    plt.tight_layout(); plt.show()

def average_pool(X):
    """Fire gjennomsnitt, ett fra hver 2 x 2-blokk."""
    # asarray gjør inputen til en talltabell; formkontrollen gir en tydelig
    # feilmelding hvis funksjonen brukes på feil bildestørrelse.
    X = np.asarray(X, dtype=float)
    if X.shape != (4, 4):
        raise ValueError("Bildet må ha størrelse 4 x 4.")
    return X.reshape(2, 2, 2, 2).mean(axis=(1, 3))

def pooling_matrix():
    """A slik at A @ X.reshape(-1) gir de fire gjennomsnittene."""
    # Designidé: én rad per outputverdi og én kolonne per inputpiksel.
    # Vekten 0.25 betyr at fire piksler skal summeres og deles på fire.
    A = np.zeros((4, 16))
    k = 0
    for br in range(2):
        for bc in range(2):
            for r in range(2):
                for c in range(2):
                    A[k, 4*(2*br+r) + 2*bc+c] = 0.25
            k += 1
    return A

A_pool = pooling_matrix()
```

```{pyodide-python}
#| label: week3-same-output
#| autorun: true

# To bevisst svært forskjellige inputbilder: ett konstant og ett rutete.
# Eksperimentet spør om blokk-gjennomsnittene likevel kan bli de samme.
X1 = np.full((4, 4), 0.5)
X2 = np.array([
    [0.1, 0.9, 0.1, 0.9],
    [0.9, 0.1, 0.9, 0.1],
    [0.1, 0.9, 0.1, 0.9],
    [0.9, 0.1, 0.9, 0.1]
])
Y1, Y2 = average_pool(X1), average_pool(X2)

# Vi viser input og output i samme figur for å kunne sammenligne direkte.
show_images([X1, X2, Y1, Y2],
    ["Input $X_1$", "Input $X_2$", "Output fra $X_1$", "Output fra $X_2$"],
    cols=4, vmin=0, vmax=1)
```

Bildene til venstre er tydelig forskjellige, mens de to outputbildene ser like ut. For å undersøke dette uten å stole bare på øynene trekker vi bildene fra hverandre, piksel for piksel.

### Ett tall for størrelsen på en forskjell

Hvis to bilder er like, består forskjellsbildet bare av nuller. **Nullbildet** er bildet der alle pikselverdiene er 0 — bildespråkets versjon av nullvektoren eller nullmatrisen. Med en vanlig gråskala ser det svart ut. I figuren nedenfor bruker vi derimot en rød–blå skala for å vise både positive og negative forskjeller; på denne skalaen vises 0 som hvitt.

```{pyodide-python}
#| label: week3-difference-and-zero-images
#| autorun: true

# Trekk fra før og etter transformasjonen. Hvis D_output er nullbildet,
# har transformasjonen mistet hele forskjellen mellom inputbildene.
D_input=X1-X2
D_output=Y1-Y2
zero_input=np.zeros_like(D_input)
zero_output=np.zeros_like(D_output)

show_images(
    [D_input,zero_input,D_output,zero_output],
    ["$X_1-X_2$","Nullbildet (4 x 4)",
     "$Y_1-Y_2$","Nullbildet (2 x 2)"],
    cols=4,cmap="coolwarm",vmin=-0.4,vmax=0.4
)
```

Det første forskjellsbildet inneholder mange utslag fra null. Det tredje er allerede nullbildet. En figur er nyttig, men senere trenger vi også ett tall som oppsummerer hele forskjellen. Vi kan ikke bare summere pikselverdiene, fordi positive og negative forskjeller da kan oppheve hverandre.

Vi kvadrerer derfor alle verdiene i forskjellsbildet, summerer dem og tar kvadratroten. For et bilde $D$ blir dette

$$
\lVert D\rVert=\sqrt{\sum_{i,j}D_{ij}^2}.
$$

Tallet $\lVert D\rVert$ kalles **normen** til $D$. Her kan vi lese det som den numeriske avstanden fra $D$ til nullbildet. Dermed måler $\lVert X_1-X_2\rVert$ den samlede pikselforskjellen mellom de to inputbildene. Dette er en numerisk avstand mellom pikselverdier, ikke nødvendigvis et mål på hvor forskjellige bilder oppleves av et menneske.

NumPy beregner denne normen med `np.linalg.norm`. Den samme regelen virker for en vektor: Da summerer vi kvadratene av komponentene i stedet for pikslene.

```{pyodide-python}
#| label: week3-first-norm
#| autorun: true

# Første linje er definisjonen på normen skrevet direkte i NumPy.
# Deretter bruker vi den ferdige norm-funksjonen som kontroll.
input_norm_by_formula=np.sqrt(np.sum(D_input**2))

print("Inputforskjell, regnet fra formelen:",input_norm_by_formula)
print("Inputforskjell med np.linalg.norm:   ",np.linalg.norm(D_input))
print("Outputforskjell med np.linalg.norm:  ",np.linalg.norm(D_output))
```

De to første tallene er begge 1.6: formelen og NumPy gjør den samme beregningen. Outputforskjellen har norm 0, og er derfor nøyaktig nullbildet. Senere vil avrundingsfeil ofte gi svært små normer i stedet for nøyaktig 0; da leser vi resultatet som «numerisk nær null».

::: {.callout-important}
### Første observasjon

Bildene er forskjellige, men transformasjonen gir samme output. Den bevarer gjennomsnittet i hver blokk, men ikke hvordan pikselverdiene er fordelt inne i blokken.
:::

Transformasjonen arbeider blokk for blokk. I øvre venstre blokk i `X2` er pikselverdiene $0.1,0.9,0.9,0.1$. Summen er 2, og gjennomsnittet er derfor $2/4=0.5$. Det samme skjer i de tre andre blokkene. I `X1` er hver piksel allerede $0.5$, så også der blir alle fire blokkgjennomsnittene $0.5$.

```{pyodide-python}
#| label: week3-four-blocks
#| autorun: true

# Løkkene skjærer ut de fire 2 x 2-blokkene. Uttrykket a:b betyr
# «ta med indeks a, men stopp før b».
blocks=[]
for block_row in range(2):
    for block_col in range(2):
        block=X2[2*block_row:2*block_row+2,
                 2*block_col:2*block_col+2]
        blocks.append(block)

block_names=["Øvre venstre","Øvre høyre","Nedre venstre","Nedre høyre"]
show_images(blocks,
    [f"{name}\nGjennomsnitt = {np.mean(block):.1f}"
     for name,block in zip(block_names,blocks)],
    cols=4,vmin=0,vmax=1,figsize=(6.8,1.8))
```

Figuren viser de fire delene som ble klippet ut av `X2`, i samme leseretning som outputbildet: først øvre rad fra venstre mot høyre, deretter nedre rad. Ordet «gjennomsnitt» over hvert delbilde er tallet som plasseres i den tilsvarende outputpikselen. Alle fire tallene er $0.5$, og outputen blir derfor et ensfarget $2\times2$-bilde.

Dette er ikke en avrundingsfeil. Gjennomsnittene er matematisk like. Det er selve transformasjonen som ikke registrerer forskjellen mellom et jevnt felt og variasjoner med samme sum. Transformasjonen er altså mange-til-én: flere forskjellige inputbilder kan havne på samme output.

Senere skal vi undersøke to viktige egenskaper ved transformasjoner:

1. **Hva skjer når inputbilder skaleres og legges sammen?** Dette leder til lineære transformasjoner.
2. **Hvilke endringer i inputen blir usynlige i outputen?** Dette leder til nullrom, rang og dimensjon.

Fra outputen alene kan vi derfor ikke avgjøre hvilket bilde som var input. Før vi gir dette et matematisk navn, kan du prøve å endre `X2` uten å endre gjennomsnittet i noen blokk. Hvilke endringer ser ut til å være tillatt?

## 3.2 Fra bilde til vektor og matrise {#uke3-del1}

Et bilde vises som en todimensjonal rute, men pikselverdiene kan også legges etter hverandre i en liste. NumPy-funksjonen `reshape(-1)` leser først øverste rad fra venstre mot høyre, deretter neste rad, og fortsetter til alle 16 pikslene er plassert i én vektor.

```{pyodide-python}
#| label: week3-flatten-picture
#| autorun: true

# reshape(-1) leser radene etter hverandre. Resten av cellen er ferdig
# plottemaskineri som viser at ingen tall endres eller forsvinner.
x2=X2.reshape(-1)
fig,axes=plt.subplots(1,2,figsize=(7.0,1.8),
                      gridspec_kw={"width_ratios":[1,3.2]})

axes[0].imshow(X2,cmap="gray",vmin=0,vmax=1,interpolation="nearest")
for r in range(4):
    for c in range(4):
        axes[0].text(c,r,f"$x_{{{4*r+c+1}}}$\n{X2[r,c]:.1f}",
                     ha="center",va="center",fontsize=7,
                     color="white" if X2[r,c]<0.5 else "black")
axes[0].set_title("$4\\times4$-bilde",fontsize=9)
axes[0].set_xticks([]); axes[0].set_yticks([])

axes[1].imshow(x2.reshape(1,-1),cmap="gray",vmin=0,vmax=1,
               interpolation="nearest",aspect="equal")
for j,value in enumerate(x2):
    axes[1].text(j,0,f"$x_{{{j+1}}}$\n{value:.1f}",
                 ha="center",va="center",fontsize=6,
                 color="white" if value<0.5 else "black")
for boundary in [3.5,7.5,11.5]:
    axes[1].axvline(boundary,color="tab:red",linewidth=2)
axes[1].set_title("Radene lagt etter hverandre: en 16-vektor",fontsize=9)
axes[1].set_xticks([]); axes[1].set_yticks([])
fig.text(0.315,0.49,"→",ha="center",va="center",fontsize=16)
plt.tight_layout(); plt.show()
```

Venstre del av figuren viser pikselnumrene på de opprinnelige plassene. Høyre del viser nøyaktig de samme tallene i én rad. De røde strekene markerer hvor en rad fra bildet slutter og den neste begynner. Vektoren er derfor ikke et nytt bilde og ingen informasjon er borte; vi har bare valgt en nummerering som gjør at vanlig matrise-vektor-multiplikasjon kan brukes.

Husk transformasjonen fra 3.1: Den tok et stort bilde som input og ga et mindre bilde som output. Nå beskriver vi de to bildene som vektorer, men selve input–output-regelen er fortsatt den samme.

Et $4\times4$-bilde beskrives dermed med 16 koordinater og kan behandles som en vektor $x\in\mathbb R^{16}$. Bildetransformasjonen fra 3.1 kan nå skrives

$$y=Ax,$$

der $A$ har fire rader og seksten kolonner. Hver rad i $A$ lager én av de fire outputverdiene. Hver kolonne svarer til én av de 16 inputpikslene.

Det er nyttig å holde de to sidene fra hverandre:

$$
\underbrace{\mathbb R^{16}}_{\text{inputrom: store bilder}}
\xrightarrow{\quad A\quad}
\underbrace{\mathbb R^4}_{\text{outputrom: små bilder}}.
$$

På venstre side av pilen står inputen $x$ med 16 pikselverdier. På høyre side står outputen $y$ med fire blokkgjennomsnitt. Matrisen $A$ er oppskriften som lager disse fire tallene fra de seksten. Input og output har derfor forskjellige roller og forskjellig lengde; vi holder dem på hver sin side av pilen.

```{pyodide-python}
#| label: week3-pooling-as-matrix
#| autorun: true

# Samme bilder skrives som vektorer, slik at vi kan bruke vanlig Ax.
x1, x2 = X1.reshape(-1), X2.reshape(-1)
# @ er matrise-vektorproduktet. Resultatet har fire komponenter fordi
# A_pool har fire rader.
y1, y2 = A_pool @ x1, A_pool @ x2
print("Bildeform:", X1.shape, "  vektorform:", x1.shape)
print("A har form", A_pool.shape)
print("A @ x1 =", y1)
print("A @ x2 =", y2)
```

Neste figur viser produktet i vanlig oppsett: en $4\times16$-matrise ganger en vertikal 16-vektor gir en vertikal 4-vektor. Samme farge brukes på et bildeområde, de tilhørende inputverdiene, matrisraden som samler dem og outputverdien de ender i.

```{.jsxgraph width="760" height="390"}
var board = JXG.JSXGraph.initBoard(BOARDID, {
  boundingbox: [0, 8.4, 20.5, 0],
  axis: false,
  showCopyright: false,
  showNavigation: false,
  pan: { enabled: false },
  zoom: { enabled: false }
});

var rowColors = ['#8ecae6','#ffcf70','#a8d5a2','#d7b5e8'];
var rowDark = ['#277da1','#d98900','#4f8f49','#8b5aa7'];
var rowNames = ['øvre venstre','øvre høyre','nedre venstre','nedre høyre'];
var active = [
  [0,1,4,5], [2,3,6,7], [8,9,12,13], [10,11,14,15]
];
var values = [0.1,0.9,0.1,0.9, 0.9,0.1,0.9,0.1,
              0.1,0.9,0.1,0.9, 0.9,0.1,0.9,0.1];
var xStart=1.9, cellW=0.56, rowH=0.76, matrixTop=6.25;

function cell(x0,y0,w,h,fill,border,width) {
  return board.create('polygon', [[x0,y0],[x0+w,y0],[x0+w,y0+h],[x0,y0+h]], {
    fillColor:fill, fillOpacity:1,
    vertices:{visible:false},
    borders:{strokeColor:border,strokeWidth:width || 1,
             fixed:true,highlight:false},
    fixed:true,highlight:false
  });
}

board.create('text', [xStart+8*cellW,matrixTop+0.65,'MATRISE  A'], {
  anchorX:'middle',fontSize:16,cssStyle:'font-weight:600',fixed:true
});

// Alle 64 oppføringer tegnes som egne ruter.
for (var r=0; r<4; r++) {
  var y0=matrixTop-(r+1)*rowH;
  board.create('text',[1.75,y0+rowH/2,rowNames[r]],{
    anchorX:'right',anchorY:'middle',fontSize:11,
    color:rowDark[r],cssStyle:'font-weight:600',fixed:true
  });
  for (var c=0; c<16; c++) {
    var isActive=active[r].indexOf(c)>=0;
    cell(xStart+c*cellW,y0,cellW,rowH,
         isActive ? rowColors[r] : '#ffffff','#555555',1);
    board.create('text',[xStart+(c+0.5)*cellW,y0+rowH/2,
                         isActive ? '¼' : '0'],{
      anchorX:'middle',anchorY:'middle',fontSize:isActive ? 12 : 9,
      color:isActive ? '#1f2933' : '#a7a7a7',fixed:true
    });
  }
}

// Inputen vises som en vanlig kolonnevektor.
var vectorX=12.15, vectorTop=7.35, vectorH=0.37, vectorW=0.72;
board.create('text',[vectorX+vectorW/2,vectorTop+0.55,'x'],{
  anchorX:'middle',fontSize:17,cssStyle:'font-weight:600',fixed:true
});
for (var k=0; k<16; k++) {
  var group = k<8 ? (k%4<2 ? 0 : 1) : (k%4<2 ? 2 : 3);
  var vy=vectorTop-(k+1)*vectorH;
  cell(vectorX,vy,vectorW,vectorH,rowColors[group],'#555555',1);
  board.create('text',[vectorX+vectorW/2,vy+vectorH/2,
                       values[k].toFixed(1)],{
    anchorX:'middle',anchorY:'middle',fontSize:8.5,fixed:true
  });
  board.create('text',[vectorX+vectorW+0.12,vy+vectorH/2,'x'+(k+1)],{
    anchorX:'left',anchorY:'middle',fontSize:7,color:'#666666',fixed:true
  });
}
board.create('text',[11.45,4.65,'×'],{
  anchorX:'middle',anchorY:'middle',fontSize:24,fixed:true
});

// Produktet er først en vanlig kolonnevektor.
var yX=14.65, yTop=5.95, yW=0.78, yH=0.76;
board.create('text',[yX+yW/2,yTop+0.55,'y = Ax'],{
  anchorX:'middle',fontSize:16,cssStyle:'font-weight:600',fixed:true
});
for (var q=0; q<4; q++) {
  var yy=yTop-(q+1)*yH;
  cell(yX,yy,yW,yH,rowColors[q],'#333333',1.5);
  board.create('text',[yX+yW/2,yy+yH/2,'0.5'],{
    anchorX:'middle',anchorY:'middle',fontSize:13,fixed:true
  });
}
board.create('text',[13.75,4.45,'='],{
  anchorX:'middle',anchorY:'middle',fontSize:24,fixed:true
});

// De fire outputverdiene kan ordnes som et lite bilde.
var imageX=17.15, imageTop=5.75, imageW=0.92;
board.create('arrow',[[15.75,4.45],[16.75,4.45]],{
  strokeColor:'#555555',strokeWidth:2,fixed:true,highlight:false
});
board.create('text',[18.07,imageTop+0.55,'vist som bilde'],{
  anchorX:'middle',fontSize:14,cssStyle:'font-weight:600',fixed:true
});
for (var p=0; p<4; p++) {
  var pc=p%2, pr=Math.floor(p/2);
  var px=imageX+pc*imageW, py=imageTop-(pr+1)*imageW;
  cell(px,py,imageW,imageW,rowColors[p],'#333333',1.5);
  board.create('text',[px+imageW/2,py+imageW/2,'0.5'],{
    anchorX:'middle',anchorY:'middle',fontSize:12,fixed:true
  });
}
```

Les én farge om gangen. Den blå matrisraden har fire ruter med $1/4$. De fire blå tallene i inputvektoren kommer fra øvre venstre bildeområde. Når rad og vektor multipliseres, blir disse fire verdiene ganget med $1/4$ og lagt sammen. Resultatet blir den blå verdien øverst i outputvektoren. De hvite nullrutene betyr at de øvrige inputverdiene ikke bidrar til akkurat denne outputen.

De gule, grønne og lilla radene gjør det samme for de tre andre bildeområdene. Matrise-vektorproduktet kan derfor leses som fire parallelle oppskrifter: **én matrisrad gir én verdi i outputvektoren**. Til slutt ordnes de fire outputverdiene som et $2\times2$-bilde. Figuren bruker sjakkbildet fra 3.1, så alle fire gjennomsnittene blir $0.5$.

### Et eksperiment med skalering og addisjon

Målet er ikke først og fremst å lage en overgang mellom to fotografier. Vi vil undersøke om et komplisert bilde kan deles opp i enklere byggesteiner som kan behandles hver for seg.

Et bilde kan for eksempel beskrives som en kombinasjon av et jevnt lysnivå, en venstre–høyre-kontrast, en topp–bunn-kontrast, kanter, lokale mønstre og små detaljer. Å multiplisere en byggestein med et tall endrer hvor sterkt den bidrar. Addisjon setter bidragene sammen piksel for piksel til et ferdig bilde.

Det viktige spørsmålet er derfor:

> Vi kan først legge sammen de store bildene og så beregne blokkgjennomsnittene. Eller vi kan beregne blokkgjennomsnittene for hvert bilde først og deretter legge sammen de små bildene. Får vi samme resultat?

Vi bruker to vilkårlige bilder som et første eksperiment. Hver piksel i `X1` multipliseres med $0.6$, hver piksel i `X3` med $0.4$, og resultatene legges sammen piksel for piksel. Det nye bildet er

$$0.6X_1+0.4X_3.$$

Vi sammenligner to regnerekkefølger:

- **Øvre rute:** Skaler og legg sammen de store inputbildene først. Transformer deretter resultatet.
- **Nedre rute:** Transformer hvert bilde først. Skaler og legg så sammen de små outputbildene.

Hvis begge framgangsmåtene alltid gir samme resultat, kan vi forstå transformasjonen ved å teste den på enkle byggesteiner. Når vi vet hva transformasjonen gjør med hver byggestein, vet vi også hva den gjør med enhver kombinasjon av dem.

::: {.callout-note}
### Fra byggesteiner til bildekompresjon

Valget av byggesteiner kan få praktisk betydning. Vanlige bilder inneholder ofte store jevne områder, langsomme overganger, kanter og gjentatte mønstre. Hvis byggesteinene passer til denne strukturen, kan bildet kanskje beskrives godt med noen få store koeffisienter og mange små.

Da kan de minste bidragene lagres mindre nøyaktig eller utelates. En mulig kompresjonsalgoritme får dermed denne formen:

1. Del bildet opp i egnede mønsterbyggesteiner.
2. Finn styrken til hver byggestein.
3. Behold de viktigste bidragene.
4. Rekonstruer et bilde som ligner originalen.

I **uke 7** skal vi bruke singulærverdifaktorisering (SVD) til å konstruere en faktisk algoritme for bildekompresjon. Da arbeider vi med større bilder og beholder de delene som beskriver mest av strukturen i bildet.

I uke 3 er målet mindre, men grunnleggende: Vi analyserer små $2\times2$- og $4\times4$-bilder der alle byggesteiner, koeffisienter og transformasjoner kan sees direkte. De små bildeblokkene fungerer som en oversiktlig modell for ideene som senere skaleres opp i SVD-algoritmen.
:::

```{pyodide-python}
#| label: week3-check-linearity

# Fast frø gir samme testbilde ved hver kjøring.
rng=np.random.default_rng(3)
X3=rng.random((4,4))
alpha,beta=0.6,0.4
mixed_input=alpha*X1+beta*X3
# left: bland først, transformer etterpå.
# right: transformer først, bland outputene etterpå.
left=(A_pool@mixed_input.reshape(-1)).reshape(2,2)
right=alpha*average_pool(X1)+beta*average_pool(X3)

fig,axes=plt.subplots(2,4,figsize=(7.0,3.6))
top=[X1,X3,mixed_input,left]
bottom=[average_pool(X1),average_pool(X3),right,left-right]
top_titles=["Input $X_1$","Input $X_3$",
            "$0.6X_1+0.4X_3$","Redusert blanding"]
bottom_titles=["Redusert $X_1$","Redusert $X_3$",
               "$0.6A(X_1)+0.4A(X_3)$","Forskjell mellom svarene"]
for ax,image,title in zip(axes[0],top,top_titles):
    ax.imshow(image,cmap="gray",vmin=0,vmax=1,interpolation="nearest")
    ax.set_title(title,fontsize=8); ax.set_xticks([]); ax.set_yticks([])
for ax,image,title in zip(axes[1],bottom,bottom_titles):
    ax.imshow(image,cmap="gray",vmin=0,vmax=1,interpolation="nearest")
    ax.set_title(title,fontsize=8); ax.set_xticks([]); ax.set_yticks([])
for row in range(2):
    for col,symbol in enumerate(["+","→","→"]):
        axes[row,col].text(1.08,0.5,symbol,transform=axes[row,col].transAxes,
                           ha="center",va="center",fontsize=14)
plt.tight_layout(); plt.show()
print("Numerisk forskjell:",np.linalg.norm(left-right))
```

I øverste rad er de to første bildene inputene, det tredje er den pikselvise kombinasjonen, og det fjerde er outputen etter reduksjon. I nederste rad er de to første bildene allerede redusert; det tredje er kombinasjonen av disse outputene. Det siste bildet viser øvre svar minus nedre svar. Det er svart fordi alle fire forskjellene er null.

De to regnerekkefølgene gir altså samme småbilde. Dette er den sentrale regneregelen for en **lineær transformasjon**:

$$A(\alpha x+\beta z)=\alpha Ax+\beta Az.$$

Her står $x$ og $z$ for to vilkårlige inputvektorer, mens $\alpha$ og $\beta$ er vilkårlige tall. Regelen rommer to egenskaper samtidig: skalering kan flyttes gjennom transformasjonen, og addisjon kan flyttes gjennom transformasjonen.

Dette er sentralt fordi vi senere kan forstå en komplisert input ved å dele den i enkle byggesteiner. Hvis $x=c_1b_1+\cdots+c_kb_k$, trenger vi ikke analysere hele $x$ på nytt:

$$Ax=c_1Ab_1+\cdots+c_kAb_k.$$

Vi kan altså finne hva transformasjonen gjør med hver byggestein én gang og deretter kombinere resultatene. Basis, nullrom og kolonnerom bygger alle på denne ideen. Ikke alle transformasjoner er lineære: å klippe alle negative pikselverdier til null eller å sortere pikslene vil for eksempel vanligvis bryte regneregelen.

## 3.3 Beskriv bilder med forskjellige basiser {#uke3-del2}

Vi skal nå finne et systematisk språk for «byggesteiner». Vi begynner fortsatt med bilder, ikke med en abstrakt definisjon.

Tenk på et tomt $2\times2$-bilde. Vi ønsker fire skyveknapper som kan lage et hvilket som helst slikt bilde. En naturlig idé er å la hver skyveknapp styre én piksel.

Dra i skyveknappene i appleten. Hver knapp endrer styrken til ett lite byggesteinsbilde. De fire delbildene nederst legges sammen piksel for piksel, og resultatet vises til høyre. Prøv spesielt å lage et helt svart bilde, et ensfarget grått bilde og et bilde med fire forskjellige gråtoner.

```{.jsxgraph width="760" height="430"}
var board = JXG.JSXGraph.initBoard(BOARDID, {
  boundingbox: [0, 8.6, 15.2, 0],
  axis: false,
  showCopyright: false,
  showNavigation: false,
  pan: { enabled: false },
  zoom: { enabled: false }
});

var basisColors=['#277da1','#d98900','#4f8f49','#8b5aa7'];
var initial=[0.2,0.7,0.4,0.9];
var sliders=[];

board.create('text',[0.75,8.25,'Fire uavhengige kontroller'],{
  fontSize:16,cssStyle:'font-weight:600',fixed:true
});

for (var i=0; i<4; i++) {
  var sy=7.55-0.72*i;
  board.create('text',[0.75,sy,'Piksel '+(i+1)],{
    anchorY:'middle',fontSize:12,color:basisColors[i],
    cssStyle:'font-weight:600',fixed:true
  });
  sliders.push(board.create('slider',[[2.05,sy],[5.25,sy],[0,initial[i],1]],{
    name:'',snapWidth:0.05,precision:2,
    strokeColor:basisColors[i],fillColor:basisColors[i],
    highline:{strokeColor:basisColors[i]},
    baseline:{strokeColor:'#b8b8b8'},
    point1:{visible:false},point2:{visible:false}
  }));
}

function basisSquare(x0,y0,size,opacityFunction,borderColor) {
  return board.create('polygon',
    [[x0,y0],[x0+size,y0],[x0+size,y0+size],[x0,y0+size]],{
      fillColor:'#111111',fillOpacity:opacityFunction,
      vertices:{visible:false},
      borders:{strokeColor:borderColor,strokeWidth:1.4,
               fixed:true,highlight:false},
      fixed:true,highlight:false
    });
}

function drawComponent(originX,originY,component) {
  var size=0.68;
  for (var p=0; p<4; p++) {
    var col=p%2, row=Math.floor(p/2);
    (function(pixel,index,x,y){
      basisSquare(x,y,size,function(){
        return pixel===index ? sliders[index].Value() : 0;
      },basisColors[index]);
    })(p,component,originX+col*size,originY+(1-row)*size);
  }
}

var componentX=[0.75,3.25,5.75,8.25];
var imageY=1.55;
for (var j=0; j<4; j++) {
  drawComponent(componentX[j],imageY,j);
  (function(index){
    board.create('text',[componentX[index]+0.68,imageY+1.75,function(){
      return sliders[index].Value().toFixed(2)+' · E'+(index+1);
    }],{
      anchorX:'middle',fontSize:12,color:basisColors[index],
      cssStyle:'font-weight:600',fixed:true
    });
  })(j);
  if (j<3) {
    board.create('text',[componentX[j]+1.82,imageY+0.68,'+'],{
      anchorX:'middle',anchorY:'middle',fontSize:22,fixed:true
    });
  }
}

board.create('arrow',[[10.05,imageY+0.68],[11.15,imageY+0.68]],{
  strokeColor:'#444444',strokeWidth:2.2,fixed:true,highlight:false
});

// I summen styres hver piksel av sin egen skyveknapp.
var sumX=11.55, size=0.92;
for (var q=0; q<4; q++) {
  var qc=q%2, qr=Math.floor(q/2);
  (function(pixel,x,y){
    basisSquare(x,y,size,function(){return sliders[pixel].Value();},'#333333');
  })(q,sumX+qc*size,imageY+(1-qr)*size);
}
board.create('text',[sumX+size,imageY+2.25,'SUMMEN'],{
  anchorX:'middle',fontSize:15,cssStyle:'font-weight:600',fixed:true
});
board.create('text',[sumX+size,imageY-0.38,
  'Fire tall kan velges uavhengig'],{
  anchorX:'middle',fontSize:12,fixed:true
});
```

Appleten antyder to viktige egenskaper før vi bruker matematisk terminologi. Alle $2\times2$-bilder med pikselverdier mellom 0 og 1 kan lages ved å velge de fire kontrollene. Samtidig har hvert ferdig bilde bare én innstilling av kontrollene: Pikselverdiene bestemmer skyveknappene.

Nå gjentar vi det samme eksperimentet i NumPy. De fire første bildene har verdi 1 i hver sin piksel og 0 i de andre. Deretter blir hvert bilde ganget med ønsket pikselverdi, og de fire delbildene legges sammen.

```{pyodide-python}
#| label: week3-pixel-basis
#| autorun: true

# Hvert E-bilde har én eneste ener. Derfor styrer hver koeffisient nøyaktig
# én piksel når de skalerte byggesteinene summeres.
E1=np.array([[1.,0.],[0.,0.]])
E2=np.array([[0.,1.],[0.,0.]])
E3=np.array([[0.,0.],[1.,0.]])
E4=np.array([[0.,0.],[0.,1.]])
pixel_basis=[E1,E2,E3,E4]
coefficients=np.array([0.2,0.7,0.4,0.9])
components=[c*E for c,E in zip(coefficients,pixel_basis)]
X=sum(components)

show_images(pixel_basis,["$E_1$","$E_2$","$E_3$","$E_4$"],
            cols=4,vmin=0,vmax=1,figsize=(6.8,1.8))
show_images(components+[X],
    ["$0.2E_1$","$0.7E_2$","$0.4E_3$","$0.9E_4$","Summen"],
    cols=5,vmin=0,vmax=1,figsize=(7.0,1.7))
```

$$X=0.2E_1+0.7E_2+0.4E_3+0.9E_4.$$

For eksempel bidrar $0.7E_2$ bare med verdien $0.7$ i øvre høyre piksel. Siden ingen av de andre tre delbildene påvirker denne pikselen, blir øvre høyre piksel i summen også $0.7$. Slik kan hver av de fire pikslene stilles inn uavhengig.

De fire tallene foran byggesteinene kalles **koordinater i denne beskrivelsen**. Her er de nøyaktig de fire pikselverdiene i $X$. Før vi gir hele byggesteinsystemet et matematisk navn, undersøker vi to mulige problemer: for få byggesteiner og overflødige byggesteiner.

### Eksperiment: Ta bort én byggestein

Vi forsøker å lage det samme målbildet uten $E_4$. De tre første pikslene kan fortsatt stilles inn, men ingen kombinasjon av $E_1,E_2,E_3$ kan påvirke pikselen nederst til høyre.

```{pyodide-python}
#| label: week3-missing-and-redundant
#| autorun: true

# Vi fjerner E4 med vilje. Forskjellsbildet viser hvilken del av målbildet
# de tre gjenværende byggesteinene ikke kan lage.
X_without_E4=coefficients[0]*E1+coefficients[1]*E2+coefficients[2]*E3
difference=X-X_without_E4
show_images([X,X_without_E4,difference,E4],
    ["Målbildet","Uten $E_4$","Det som mangler","$E_4$"],
    cols=4,vmin=0,vmax=1,figsize=(6.8,1.8))
```

Resultatet viser mer enn at akkurat vårt forsøk mislyktes: Nedre høyre piksel er null i hver av de tre tilgjengelige byggesteinene, og blir derfor null i enhver lineærkombinasjon av dem. $E_4$ tilfører en mulighet de andre ikke har.

### Eksperiment: Legg til en overflødig byggestein

Nå legger vi til $E_5=E_1+E_2$. Figuren viser at $E_5$ ikke gir en ny type bilde; den samme effekten kunne allerede lages med de gamle byggesteinene.

```{pyodide-python}
#| label: week3-redundant-building-block
#| autorun: true

# E5 er konstruert av to gamle byggesteiner og tilfører derfor ingen ny
# retning. De to oppskriftene under skal gi samme bilde.
E5=E1+E2
recipe_1=1*E1+1*E2+0*E5
recipe_2=0*E1+0*E2+1*E5
show_images([E1,E2,E5,recipe_1,recipe_2,recipe_1-recipe_2],
    ["$E_1$","$E_2$","$E_5$",
     "Oppskrift 1","Oppskrift 2","Forskjell"],
    cols=3,vmin=0,vmax=1,figsize=(5.4,3.6))
```

Øverste rad viser at $E_5$ allerede er summen av de to første byggesteinene. Nederste rad viser konsekvensen: Oppskrift 1 bruker ett eksemplar av $E_1$ og $E_2$, mens oppskrift 2 bruker ett eksemplar av $E_5$. Forskjellsbildet er null overalt. De to oppskriftene bruker altså forskjellige koeffisienter, men gir samme bilde, så beskrivelsen er ikke lenger entydig.

::: {.callout-tip}
### Fra eksperiment til begreper

- Byggesteinene **spenner ut** en samling bilder når alle bilder i samlingen kan bygges som lineærkombinasjoner av dem.
- Byggesteinene er **lineært uavhengige** når ingen av dem kan bygges av de andre. Da har hvert bilde høyst én oppskrift.
- En **basis** er et sett byggesteiner som både spenner ut hele samlingen og er lineært uavhengig: nok byggesteiner, men ingen overflødige.
:::

Et vanlig gråtonebilde har pikselverdier mellom 0 og 1: 0 er svart og 1 er hvitt. Slike $2\times2$-bilder ligger i $[0,1]^{2\times2}$. Men når vi trekker fra bilder eller skalerer mønstre, kan mellomresultatene bli negative eller større enn 1. Derfor bruker vi den større samlingen

$$\mathbb R^{2\times2},$$

som betyr «fire reelle tall ordnet som to rader og to kolonner». Elementene i denne samlingen kan regnes med som bilder, forskjellsbilder eller mønstre, selv om ikke alle kan vises direkte som vanlige gråtonebilder. Det er $\mathbb R^{2\times2}$ som er et vektorrom; $[0,1]^{2\times2}$ er bare delen som består av gyldige gråtonebilder.

$E_1,E_2,E_3,E_4$ danner en basis for $\mathbb R^{2\times2}$. **Dimensjonen** er antallet byggesteiner i en basis, altså

$$\dim(\mathbb R^{2\times2})=4.$$

Dimensjon teller antallet uavhengige tall som trengs for å beskrive et vilkårlig bilde i samlingen. Den handler ikke om at bildet ser todimensjonalt ut på skjermen. Et $4\times4$-bilde har tilsvarende 16 fritt valgbare pikselverdier og ligger i et rom med dimensjon 16.

### Bytt fra pikselbasis til mønsterbasis

Pikselbyggesteinene er enkle, men koordinatene sier bare hvor lyse de fire pikslene er. Vi prøver nå fire andre byggesteiner. I figurene betyr rødt positive verdier og blått negative verdier; hvitt ligger nær null. Negative tall er ikke «negativt lys», men beskriver at et mønster trekkes fra når bilder kombineres.

Appleten har samme oppbygning som pikselbasis-appleten tidligere i denne delen, men skyveknappene styrer nå fire mønstre. Knappene går fra $-1$ til $1$: En positiv koeffisient legger til mønsteret, mens en negativ koeffisient legger til mønsteret med motsatte fortegn. Tallet i hver piksel viser det faktiske bidraget; fargen viser fortegnet og omtrent hvor stort bidraget er.

```{.jsxgraph width="760" height="430"}
var board = JXG.JSXGraph.initBoard(BOARDID, {
  boundingbox: [0, 8.6, 15.2, 0],
  axis: false,
  showCopyright: false,
  showNavigation: false,
  pan: { enabled: false },
  zoom: { enabled: false }
});

var patternNames=['Lysnivå','Venstre–høyre','Topp–bunn','Sjakkmønster'];
var patternColors=['#555555','#277da1','#4f8f49','#8b5aa7'];
var patternValues=[
  [ 1, 1, 1, 1],
  [ 1,-1, 1,-1],
  [ 1, 1,-1,-1],
  [ 1,-1,-1, 1]
];
var patternInitial=[0.55,-0.25,-0.10,0.00];
var patternSliders=[];

board.create('text',[0.75,8.25,'Fire mønsterkontroller'],{
  fontSize:16,cssStyle:'font-weight:600',fixed:true
});

for (var i=0; i<4; i++) {
  var sy=7.55-0.72*i;
  board.create('text',[0.75,sy,patternNames[i]],{
    anchorY:'middle',fontSize:11,color:patternColors[i],
    cssStyle:'font-weight:600',fixed:true
  });
  patternSliders.push(board.create('slider',
    [[2.25,sy],[5.35,sy],[-1,patternInitial[i],1]],{
      name:'',snapWidth:0.05,precision:2,
      strokeColor:patternColors[i],fillColor:patternColors[i],
      highline:{strokeColor:patternColors[i]},
      baseline:{strokeColor:'#b8b8b8'},
      point1:{visible:false},point2:{visible:false}
    }));
}

function patternColor(value) {
  return value>=0 ? '#d6604d' : '#2166ac';
}
function patternOpacity(value) {
  return Math.min(0.88,0.88*Math.abs(value));
}
function patternSquare(x0,y0,size,valueFunction,borderColor) {
  var polygon=board.create('polygon',
    [[x0,y0],[x0+size,y0],[x0+size,y0+size],[x0,y0+size]],{
      fillColor:function(){return patternColor(valueFunction());},
      fillOpacity:function(){return patternOpacity(valueFunction());},
      vertices:{visible:false},
      borders:{strokeColor:borderColor,strokeWidth:1.4,
               fixed:true,highlight:false},
      fixed:true,highlight:false
    });
  board.create('text',[x0+size/2,y0+size/2,function(){
    return valueFunction().toFixed(2);
  }],{
    anchorX:'middle',anchorY:'middle',fontSize:9,fixed:true
  });
  return polygon;
}

function componentValue(component,pixel) {
  return function(){
    return patternSliders[component].Value()*patternValues[component][pixel];
  };
}
function sumValue(pixel) {
  return function(){
    var total=0;
    for (var m=0; m<4; m++) {
      total+=patternSliders[m].Value()*patternValues[m][pixel];
    }
    return total;
  };
}

var componentX=[0.75,3.25,5.75,8.25];
var imageY=1.55, smallSize=0.68;
for (var j=0; j<4; j++) {
  for (var p=0; p<4; p++) {
    var pc=p%2, pr=Math.floor(p/2);
    patternSquare(componentX[j]+pc*smallSize,
                  imageY+(1-pr)*smallSize,smallSize,
                  componentValue(j,p),patternColors[j]);
  }
  (function(index){
    board.create('text',[componentX[index]+smallSize,imageY+1.78,function(){
      return patternSliders[index].Value().toFixed(2)+' · '+patternNames[index];
    }],{
      anchorX:'middle',fontSize:10,color:patternColors[index],
      cssStyle:'font-weight:600',fixed:true
    });
  })(j);
  if (j<3) {
    board.create('text',[componentX[j]+1.82,imageY+0.68,'+'],{
      anchorX:'middle',anchorY:'middle',fontSize:22,fixed:true
    });
  }
}

board.create('arrow',[[10.05,imageY+0.68],[11.15,imageY+0.68]],{
  strokeColor:'#444444',strokeWidth:2.2,fixed:true,highlight:false
});

var sumX=11.55, sumSize=0.92;
for (var q=0; q<4; q++) {
  var qc=q%2, qr=Math.floor(q/2);
  patternSquare(sumX+qc*sumSize,imageY+(1-qr)*sumSize,
                sumSize,sumValue(q),'#333333');
}
board.create('text',[sumX+sumSize,imageY+2.25,'SAMME TYPE BILDE'],{
  anchorX:'middle',fontSize:14,cssStyle:'font-weight:600',fixed:true
});
board.create('text',[sumX+sumSize,imageY-0.38,
  'Nye kontroller · ny beskrivelse'],{
  anchorX:'middle',fontSize:12,fixed:true
});
```

Startinnstillingen lager det samme bildet som med pikselbasisen, men tallene på skyveknappene er nå annerledes: lysnivå $0.55$, venstre–høyre-kontrast $-0.25$, topp–bunn-kontrast $-0.10$ og ingen sjakkmønsterkontrast. Prøv å endre én kontroll om gangen og beskriv den synlige endringen i summen.

Nå konstruerer vi de samme fire mønstrene i NumPy.

```{pyodide-python}
#| label: week3-pattern-basis
#| autorun: true

# De fire arrayene er ikke tilfeldige: M styrer felles lysnivå, mens H, V
# og D har sum null og beskriver tre forskjellige kontraster.
M=np.array([[ 1., 1.],[ 1., 1.]])
H=np.array([[ 1.,-1.],[ 1.,-1.]])
V=np.array([[ 1., 1.],[-1.,-1.]])
D=np.array([[ 1.,-1.],[-1., 1.]])
pattern_basis=[M,H,V,D]
pattern_names=["Lysnivå","Venstre–høyre","Topp–bunn","Sjakkmønster"]

show_images(pattern_basis,pattern_names,cols=4,
            cmap="coolwarm",vmin=-1,vmax=1)
```

`Lysnivå` har samme fortegn overalt og gjør hele bildet lysere eller mørkere. `Venstre–høyre` øker venstre kolonne samtidig som høyre kolonne minker. `Topp–bunn` sammenligner øvre og nedre rad. `Sjakkmønster` skiller de to diagonalene. De tre siste har to $+1$ og to $-1$, så summen deres er null.

Disse mønstrene virker meningsfulle, men det er ikke nok til å kalle dem en basis. Vi må undersøke de samme to spørsmålene som for pikselbasisen: Kan de bygge alle målbilder, og er oppskriften entydig?

Vi gjør hvert mønster om til en 4-vektor og bruker vektorene som kolonner i `P`. For hvert målbilde løser vi ligningen `P @ c = target`: Finnes det koeffisienter som rekonstruerer bildet?

```{pyodide-python}
#| label: week3-test-pattern-building-blocks
#| autorun: true

# reshape(-1) gjør hvert 2 x 2-mønster til en 4-vektor.
# column_stack setter de fire byggesteinene som kolonner i P.
P=np.column_stack([pattern.reshape(-1) for pattern in pattern_basis])
# P.T er den transponerte matrisen. P.T @ P undersøker vinklene mellom
# kolonnene; null utenfor diagonalen betyr at de er ortogonale.
print("P^T P:\n",P.T@P)
print("Rang av P:",np.linalg.matrix_rank(P))

rng=np.random.default_rng(8)
targets=[rng.uniform(-1,1,size=(2,2)) for _ in range(4)]
reconstructions=[]; errors=[]
for target in targets:
    # Reverse engineering: finn mønsterkoeffisientene som lager target.
    c_test=np.linalg.solve(P,target.reshape(-1))
    reconstruction=(P@c_test).reshape(2,2)
    reconstructions.append(reconstruction)
    errors.append(np.linalg.norm(reconstruction-target))

interleaved=[]; titles=[]
for i,(target,reconstruction) in enumerate(zip(targets,reconstructions),start=1):
    interleaved.extend([target,reconstruction])
    titles.extend([f"Mål {i}",f"Bygd mål {i}"])
show_images(interleaved,titles,cols=4,cmap="coolwarm",
            vmin=-1,vmax=1,figsize=(6.8,3.5))
print("Rekonstruksjonsfeil:",errors)
```

Utskriften av $P^TP$ har verdien 4 på diagonalen og 0 ellers. Nullene betyr
at ulike mønsterkolonner er ortogonale. Hvis $Pc=0$, kan vi multiplisere med
$P^T$ og få $4c=0$, altså $c=0$. Kolonnene er derfor lineært uavhengige.
Siden vi har fire uavhengige vektorer i det firedimensjonale rommet
$\mathbb R^{2\times2}$, danner de en basis. Rangutskriften kontrollerer den
samme konklusjonen numerisk.

I hvert par er bildet merket «Mål» laget tilfeldig. «Bygd mål» er rekonstruksjonen fra de fire mønstrene. Parene ser like ut, og normen av forskjellen er omkring $10^{-16}$ eller null. Forsøkene illustrerer basisresultatet på konkrete bilder; argumentet med $P^TP$ forklarer hvorfor det gjelder alle bilder.

Matrisen `P` har ett mønster i hver kolonne. Ligningen `P @ c = target` spør hvilke fire mønsterstyrker `c` som gir det ønskede bildet. Fordi kolonnene danner en basis, har hvert målbilde nøyaktig én løsning.

Vi ser nærmere på koordinatene til bildet $X$ fra pikselbasis-eksemplet tidligere i denne delen.

```{pyodide-python}
#| label: week3-change-basis
#| autorun: true

# X er kjent; c er den ukjente oppskriften i mønsterbasisen.
c=np.linalg.solve(P,X.reshape(-1))
# Hver koordinat skalerer sin byggestein. Summen skal bli X igjen.
pattern_components=[value*pattern for value,pattern in zip(c,pattern_basis)]
reconstructed=(P@c).reshape(2,2)
scale=max(np.max(np.abs(part)) for part in pattern_components)

show_images(pattern_components+[reconstructed],
    [f"{c[i]:.2f} · {pattern_names[i]}" for i in range(4)]+["Summen"],
    cols=5,cmap="coolwarm",vmin=-scale,vmax=scale,figsize=(7.0,1.8))
print("Pikselkoordinater: ",coefficients)
print("Mønsterkoordinater:",c)
print("Rekonstruksjonsfeil:",np.linalg.norm(reconstructed-X))
```

De fire første delbildene i figuren er koeffisienten ganget med det navngitte mønsteret. Det siste bildet er summen deres. Noen delbilder inneholder negative verdier, men summen rekonstruerer det opprinnelige bildet med vanlige pikselverdier.

Pikselbasisen beskriver bildet med fire lokale lysverdier. Mønsterbasisen beskriver det samme bildet som samlet lysnivå pluss tre typer kontrast. Bildet er uendret, men koordinatene har fått en annen betydning. Dette er et **basisskifte**: samme objekt, ny oppskrift.

::: {.callout-note}
### Hvorfor bytte basis?

En basis er ikke bare et sett som tilfredsstiller en definisjon. Et godt valg av basis kan skille egenskaper vi vil bevare fra egenskaper en transformasjon fjerner. Det er nettopp det som skjer i neste eksperiment.
:::

## 3.4 Hva transformasjonen ser og ikke ser {#uke3-del3}

Nå lar vi den enkleste transformasjonen vi har — gjennomsnittet av fire tall — virke på de fire mønsterbyggesteinene. Vi kaller transformasjonen for én blokk $G:\mathbb R^4\to\mathbb R$. Den skal ikke forveksles med `A_pool`, som behandler fire blokker og sender et helt $4\times4$-bilde til fire tall. Inputen i hver kolonne er et $2\times2$-mønster. Den lille outputen under viser det ene tallet $G$ produserer. Fordi gjennomsnittet er lineært, vil resultatet for disse fire byggesteinene senere fortelle oss resultatet for enhver kombinasjon av dem.

```{pyodide-python}
#| label: week3-average-patterns
#| autorun: true

# Vi sender én basisretning om gangen gjennom gjennomsnittstransformasjonen.
# Da ser vi hvilke koordinater transformasjonen beholder.
outputs=[np.array([[np.mean(pattern)]]) for pattern in pattern_basis]
show_images(pattern_basis+outputs,
    pattern_names+[f"Output: {value.item():.1f}" for value in outputs],
    cols=4,cmap="coolwarm",vmin=-1,vmax=1,figsize=(6.8,3.4))
for name,pattern in zip(pattern_names,pattern_basis):
    print(f"{name:16s} -> gjennomsnitt {np.mean(pattern): .1f}")
```

Les figuren loddrett: De fire store bildene er inputene, og de fire små rutene er de tilhørende outputene. Lysnivåbildet har fire enere, så gjennomsnittet er 1. Hvert kontrastbilde har to enere og to minusenere; summen er 0 og gjennomsnittet er derfor 0.

Resultatene deler byggesteinene i to grupper. Transformasjonen registrerer lysnivåretningen, men sender hver kontrastretning til null. En vilkårlig kombinasjon av kontrastbildene får også gjennomsnitt null, fordi lineariteten fra 3.2 lar oss kombinere de tre nullresultatene.

::: {.callout-important}
### Uformell observasjon

Kontrastmønstrene er endringer vi kan legge til et bilde uten å endre gjennomsnittet. Transformasjonen kan ikke skille mellom bilder som bare er forskjellige med en kombinasjon av slike kontraster.
:::

Vi kontrollerer også den motsatte retningen: Kan tilfeldige bilder med gjennomsnitt null bygges av de tre kontrastmønstrene?

```{pyodide-python}
#| label: week3-build-zero-mean-images
#| autorun: true

# Kolonnene i contrast_matrix er de tre kontrastbyggesteinene H, V og D.
contrast_matrix=np.column_stack([H.reshape(-1),V.reshape(-1),D.reshape(-1)])
rng=np.random.default_rng(12)
target_images=[]; reconstructed_images=[]; errors=[]
for _ in range(4):
    first_three=rng.uniform(-1,1,size=3)
    # Velg siste piksel slik at summen av alle fire blir null.
    values=np.r_[first_three,-np.sum(first_three)]
    target=values.reshape(2,2)
    # Tre uavhengige ligninger er nok til å finne tre koeffisienter.
    weights=np.linalg.solve(contrast_matrix[:3,:],values[:3])
    reconstructed=(contrast_matrix@weights).reshape(2,2)
    target_images.append(target)
    reconstructed_images.append(reconstructed)
    errors.append(np.linalg.norm(target-reconstructed))

interleaved=[]; titles=[]
for i,(target,reconstructed) in enumerate(
        zip(target_images,reconstructed_images),start=1):
    interleaved.extend([target,reconstructed])
    titles.extend([f"Målbilde {i}\n(sum = 0)",
                   f"Rekonstruksjon {i}\n(fra H, V, D)"])
show_images(interleaved,titles,cols=4,cmap="coolwarm",
            vmin=-2,vmax=2,figsize=(6.8,3.5))
print("Rekonstruksjonsfeil:",errors)
```

I hvert par er målbildet konstruert med fire tilfeldige tall som summerer til null. Bildet ved siden av er rekonstruert fra `H`, `V` og `D`. De første tre pikselverdiene gir tre ligninger for de tre ukjente mønsterkoeffisientene. Den fjerde ligningen følger automatisk fordi både målbildet og alle tre mønstrene har sum null. Derfor løser koden systemet med de tre første radene i `contrast_matrix`, men kontrollerer rekonstruksjonen i alle fire pikslene. De to bildene i hvert par er like, og rekonstruksjonsfeilen er null eller nær maskinpresisjon.

De fire forsøkene støtter påstanden: Bilder med sum null kan beskrives med tre uavhengige kontrastkoeffisienter. Hvorfor tre? Når de første tre pikselverdiene er valgt, må den siste være minus summen av dem. Vi har derfor tre frie valg og én verdi som er bestemt av de andre. Nå har vi et konkret behov for et navn på hele denne samlingen.

Fra tidligere lineær algebra kjenner vi nullrommet som løsningene av et homogent system. For en transformasjon $A:\mathbb R^n\to\mathbb R^m$ er

$$N(A)=\{z\in\mathbb R^n:Az=0\}\subseteq\mathbb R^n.$$

Nullrommet ligger altså i **inputrommet**. Vektorene der har like mange komponenter som en input, ikke som en output. For gjennomsnittet av én $2\times2$-blokk er inputen et bilde med fire tall, mens outputen bare er ett tall. Derfor ligger nullrommet i $\mathbb R^4$, og

$$N(G)=\operatorname{span}\{H,V,D\}.$$

Her er nullrommet nettopp alle $2\times2$-bilder med sum, og dermed gjennomsnitt, lik null. De tre uavhengige byggesteinene $H,V,D$ spenner ut denne samlingen, så de danner en basis og nullrommet har dimensjon 3. Nullrommet er altså ikke bare selve nullbildet; det kan inneholde mange ikke-null inputbilder som transformasjonen ikke registrerer.

Dette forklarer åpningsproblemet for én blokk. Hvis $Gx_1=Gx_2$, kan vi trekke den ene outputen fra den andre. Linearitet gir $G(x_1-x_2)=0$. Forskjellsbildet $x_1-x_2$ ligger derfor i nullrommet til $G$. Omvendt kan vi legge enhver nullromsendring til et bilde uten å endre outputen:

$$Gx_1=Gx_2\quad\Longleftrightarrow\quad G(x_1-x_2)=0.$$

```{pyodide-python}
#| label: week3-family-same-average
#| autorun: true

# base er startbildet, direction er en nullromsretning, og t bestemmer
# hvor langt vi går i denne retningen. Gjennomsnittet skal være uendret.
base=np.full((2,2),0.5)
direction=0.35*D
t_values=[-1.,-0.5,0.,0.5,1.]
family=[base+t*direction for t in t_values]
show_images(family,
    [f"$t={t:g}$\ngjennomsnitt={np.mean(image):.2f}" for t,image in zip(t_values,family)],
    cols=5,vmin=0,vmax=1,figsize=(7.0,1.7))
```

Det midterste bildet har $t=0$ og er ensfarget. Negative og positive verdier av $t$ legger til sjakkmønsteret med motsatt fortegn. Titlene viser at gjennomsnittet forblir $0.50$ i alle fem bilder, selv om kontrasten blir sterkere mot begge ender.

Når $t$ endres, flytter vi oss gjennom forskjellige bilder langs kontrastretningen $D$. Pikslene endres, men gjennomsnittet står stille. Nullrommet beskriver derfor alle forskjeller mellom inputer som denne målingen ikke kan oppdage.

### Finn de tolv usynlige bilderetningene

Vi går tilbake fra én $2\times2$-blokk til hele $4\times4$-bildet. Transformasjonen beregner fire gjennomsnitt, ett i hvert hjørneområde. Derfor kan hver blokk inneholde sine egne usynlige kontraster.

Funksjonen `place_in_block` plasserer ett av mønstrene `H`, `V` eller `D` i en valgt blokk og fyller resten av bildet med null. Figuren organiseres blokk for blokk: fire plasseringer, med tre kontrasttyper i hver plassering. Det gir $4\cdot3=12$ bilder.

```{pyodide-python}
#| label: week3-full-null-basis
#| autorun: true

def place_in_block(pattern,block_row,block_col):
    """Legg ett 2 x 2-kontrastmønster i valgt blokk av et nullbilde."""
    Z=np.zeros((4,4))
    r,c=2*block_row,2*block_col
    Z[r:r+2,c:c+2]=pattern
    return Z

null_basis=[]; null_titles=[]
# Tre kontraster i hver av fire blokker gir 3 * 4 = 12 kandidater.
for br in range(2):
    for bc in range(2):
        for pattern,name in zip([H,V,D],["H","V","D"]):
            null_basis.append(place_in_block(pattern,br,bc))
            null_titles.append(f"Blokk ({br+1},{bc+1}), {name}")

show_images(null_basis,null_titles,cols=4,cmap="coolwarm",
            vmin=-1,vmax=1,figsize=(6.8,5.2))
```

Hvert bilde endrer bare to eller fire piksler innenfor én blokk. Positive og negative bidrag opphever hverandre, så gjennomsnittet i den blokken forblir null. De tre andre blokkene er allerede null. Dermed må outputen bli nullbildet for hvert av de tolv inputbildene.

Neste celle kontrollerer dette numerisk. Deretter velger den tolv tilfeldige koeffisienter, skalerer hvert kontrastbilde og legger alle sammen. Det sammensatte inputbildet ser uregelmessig ut, men hver blokk har fortsatt sum null.

```{pyodide-python}
#| label: week3-random-null-image
#| autorun: true

# Først kontrolleres hver kandidat separat med ||A z||.
for i,Zi in enumerate(null_basis,start=1):
    print(f"Mønster {i:2d}: ||A z|| = {np.linalg.norm(A_pool@Zi.reshape(-1)):.1e}")

rng=np.random.default_rng(7)
random_coefficients=rng.normal(size=12)
# En lineærkombinasjon av nullromsvektorer skal fortsatt ligge i nullrommet.
Z=sum(c*Zi for c,Zi in zip(random_coefficients,null_basis))
pooled_Z=average_pool(Z)
limit=np.max(np.abs(Z))
show_images([Z,pooled_Z],["Tilfeldig kombinasjon av 12 mønstre","Output"],
            cols=2,cmap="coolwarm",vmin=-limit,vmax=limit,figsize=(3.6,1.8))
```

For hvert mønster er $Az$ et $2\times2$-outputbilde. Utskriften $\lVert Az\rVert$ måler avstanden fra denne outputen til nullbildet. Verdier på størrelse med avrundingsfeilen betyr at mønsteret forsvinner numerisk i transformasjonen.

Hvis $Az_1=0$ og $Az_2=0$, gir linearitet

$$A(\alpha z_1+\beta z_2)=0.$$

Det første bildet i den siste figuren er kombinasjonen av de tolv mønstrene. Det andre er outputen etter blokkgjennomsnitt. Den er null i alle fire posisjoner. Koden gjør dermed to observasjoner: Hver lokal kontrast gir output null, og en tilfeldig lineærkombinasjon av dem gir fremdeles output null. Grunnen er linearitet, ikke at vi var heldige med koeffisientene.

Nullrommet er altså en samling der vi kan addere bilder og multiplisere dem med tall uten å forlate samlingen. En slik lineær samling inni et større rom kalles et **underrom**. Vi trenger ingen nye regneregler; ordet beskriver bare at lineærkombinasjoner blir værende i samlingen.

De tolv viste byggesteinene påvirker enten forskjellige blokker eller forskjellige kontraster i samme blokk. Ingen av dem kan fjernes uten at vi mister en mulig lokal endring. Samtidig kan ethvert bilde med null gjennomsnitt i hver blokk bygges av dem, blokk for blokk. De danner derfor en basis for nullrommet, som har dimensjon 12.

### Finn hvilke outputbilder transformasjonen kan lage

Vi har undersøkt hvilke endringer i inputbildet som ikke synes i outputen. Nå snur vi spørsmålet: **Hvilke $2\times2$-bilder kan transformasjonen faktisk produsere?**

Vi begynner med det enkleste mulige inputbildet: én piksel er 1, og alle andre er 0. Kall dette **å slå på én piksel**. Klikk på en inputpiksel i figuren. Outputbildet til høyre viser hva transformasjonen gjør med akkurat denne inputen.

```{.jsxgraph width="760" height="430"}
var board = JXG.JSXGraph.initBoard(BOARDID, {
  boundingbox: [0, 8.2, 14.8, 0],
  axis: false,
  showCopyright: false,
  showNavigation: false,
  pan: { enabled: false },
  zoom: { enabled: false }
});

var groupColors = ['#8ecae6','#ffcf70','#a8d5a2','#d7b5e8'];
var groupDark = ['#277da1','#d98900','#4f8f49','#8b5aa7'];
var groupNames = ['øvre venstre','øvre høyre','nedre venstre','nedre høyre'];
var selectedPixel = 0;

function pixelGroup(index) {
  var row=Math.floor(index/4), col=index%4;
  return (row<2 ? 0 : 2)+(col<2 ? 0 : 1);
}

function box(x0,y0,size,fill,opacity,border,width) {
  return board.create('polygon',
    [[x0,y0],[x0+size,y0],[x0+size,y0+size],[x0,y0+size]],{
      fillColor:fill,fillOpacity:opacity,
      vertices:{visible:false},
      borders:{strokeColor:border,strokeWidth:width,
               fixed:true,highlight:false},
      fixed:true,highlight:false
    });
}

board.create('text',[3.0,7.75,'INPUT: klikk på én piksel'],{
  anchorX:'middle',fontSize:16,cssStyle:'font-weight:600',fixed:true
});
board.create('text',[11.15,7.75,'OUTPUT'],{
  anchorX:'middle',fontSize:16,cssStyle:'font-weight:600',fixed:true
});

var inputCells=[];
for (let i=0; i<16; i++) {
  let row=Math.floor(i/4), col=i%4, group=pixelGroup(i);
  let x0=1.0+col, y0=2.65+(3-row);
  let cell=box(x0,y0,1.0,groupColors[group],function(){
    return selectedPixel===i ? 0.95 : 0.48;
  },function(){return selectedPixel===i ? groupDark[group] : '#ffffff';},
  function(){return selectedPixel===i ? 4 : 1.5;});
  cell.on('down',function(){selectedPixel=i; board.update();});
  inputCells.push(cell);
  board.create('text',[x0+0.5,y0+0.5,String(i+1)],{
    anchorX:'middle',anchorY:'middle',fontSize:13,
    cssStyle:'font-weight:600; pointer-events:none',fixed:true
  });
}
box(1.0,2.65,4.0,'none',0,'#333333',2);
board.create('segment',[[3.0,2.65],[3.0,6.65]],{
  strokeColor:'#333333',strokeWidth:3,fixed:true,highlight:false
});
board.create('segment',[[1.0,4.65],[5.0,4.65]],{
  strokeColor:'#333333',strokeWidth:3,fixed:true,highlight:false
});

var outputXY=[[10.0,5.15],[11.15,5.15],[10.0,4.0],[11.15,4.0]];
for (let g=0; g<4; g++) {
  let x0=outputXY[g][0], y0=outputXY[g][1];
  box(x0,y0,1.15,groupColors[g],function(){
    return pixelGroup(selectedPixel)===g ? 0.95 : 0.20;
  },'#ffffff',1.5);
  board.create('text',[x0+0.575,y0+0.575,function(){
    return pixelGroup(selectedPixel)===g ? '1/4' : '0';
  }],{
    anchorX:'middle',anchorY:'middle',fontSize:15,
    cssStyle:'font-weight:600',fixed:true
  });
}
box(10.0,4.0,2.3,'none',0,'#333333',2);
board.create('segment',[[11.15,4.0],[11.15,6.3]],{
  strokeColor:'#333333',strokeWidth:3,fixed:true,highlight:false
});
board.create('segment',[[10.0,5.15],[12.3,5.15]],{
  strokeColor:'#333333',strokeWidth:3,fixed:true,highlight:false
});

var groupStarts=[[2.0,5.65],[4.0,5.65],[2.0,3.65],[4.0,3.65]];
var groupEnds=[[10.0,5.72],[11.15,5.72],[10.0,4.57],[11.15,4.57]];
for (let g=0; g<4; g++) {
  board.create('arrow',[groupStarts[g],groupEnds[g]],{
    strokeColor:groupDark[g],strokeWidth:function(){
      return pixelGroup(selectedPixel)===g ? 4 : 1.5;
    },strokeOpacity:function(){
      return pixelGroup(selectedPixel)===g ? 1 : 0.18;
    },fixed:true,highlight:false
  });
}

board.create('text',[7.55,1.75,function(){
  var g=pixelGroup(selectedPixel);
  return 'Piksel '+(selectedPixel+1)+' hører til '+groupNames[g]+' gruppe.';
}],{
  anchorX:'middle',fontSize:14,cssStyle:'font-weight:600',fixed:true
});
board.create('text',[7.55,1.15,'Én piksel med verdi 1 gir gjennomsnitt 1/4 i sitt outputfelt.'],{
  anchorX:'middle',fontSize:12,fixed:true
});
```

De fire fargene deler inputbildet i fire blokker. Alle piksler med samme farge peker mot samme felt i outputbildet. Når bare én piksel har verdien 1, er gjennomsnittet i blokken $1/4$; de andre tre outputfeltene får 0. Prøv flere piksler med samme farge. Pikselnummeret endrer seg, men outputen gjør ikke det.

Her kommer forbindelsen til matrisen: **Kolonne $j$ i $A$ er outputen vi får når bare inputpiksel $j$ er slått på.** Fire piksler som gir samme output, gir derfor fire identiske kolonner. Figuren viser på denne måten fire grupper av like kolonner, én gruppe for hver farge.

Koden nedenfor utfører alle de 16 forsøkene på én gang og tegner hver matriskolonne som et lite $2\times2$-bilde.

```{pyodide-python}
#| label: week3-columns-as-images
#| autorun: true

# Kolonne j er outputen A_pool lager når bare inputpiksel j er lik 1.
# reshape gjør hver 4-komponentkolonne synlig som et 2 x 2-outputbilde.
column_images=[A_pool[:,j].reshape(2,2) for j in range(16)]
show_images(column_images,[f"Kolonne {j+1}" for j in range(16)],
            cols=4,vmin=0,vmax=0.25,figsize=(6.8,5.8))
```

De 16 små bildene bekrefter det vi så i appleten: Kolonnene kommer i fire grupper. Innenfor hver gruppe er outputbildene identiske. Mellom gruppene flytter den eneste lyse outputpikselen seg til en ny plass.

Dermed har vi funnet fire forskjellige måter å påvirke outputen på. Det neste spørsmålet er om disse fire mulighetene er nok til å lage *ethvert* $2\times2$-bilde. Vi velger fire tilfeldige målbilder. For hvert målbilde lager koden et $4\times4$-inputbilde ved å fylle hver fargede blokk med verdien vi ønsker i det tilsvarende outputfeltet. Deretter lar vi transformasjonen beregne outputen og sammenligner.

```{pyodide-python}
#| label: week3-build-arbitrary-output
#| autorun: true

def expand_block_values(Y):
    """Gjør hver verdi i et 2x2-bilde til en konstant 2x2-blokk."""
    # Gjenta først hver rad og deretter hver kolonne. Dette konstruerer en
    # input som garantert får blokkgjennomsnittene i Y.
    return np.repeat(np.repeat(Y,2,axis=0),2,axis=1)

rng=np.random.default_rng(24)
targets=[rng.random((2,2)) for _ in range(4)]
# Reverse engineering er her enkelt: kopier hver ønsket outputverdi tilbake
# til de fire inputpikslene som måles sammen.
inputs=[expand_block_values(Y) for Y in targets]
outputs=[average_pool(Xi) for Xi in inputs]

panels=[]; titles=[]
for Xi,Yi,out in zip(inputs,targets,outputs):
    panels.extend([Xi,Yi,out])
    titles.extend(["Konstruert input","Ønsket output","Faktisk output"])
show_images(panels,titles,cols=3,vmin=0,vmax=1,figsize=(6.8,5.0))
print("Største feil:",max(np.linalg.norm(out-Yi)
                          for out,Yi in zip(outputs,targets)))
```

Les hver rad i figuren fra venstre mot høyre. Først vises et konstruert $4\times4$-inputbilde. I midten står outputen vi ba om. Til høyre står outputen transformasjonen faktisk beregnet. De to små bildene er identiske i alle fire forsøk.

Målbildene ble valgt tilfeldig, men den samme oppskriften virker for alle $2\times2$-bilder: kopier hver ønsket outputverdi inn i alle fire pikslene i den tilsvarende inputblokken. Gjennomsnittet av fire like tall er tallet selv. Feilen er derfor nøyaktig null, bortsett fra eventuell avrunding. Transformasjonen kan altså produsere alle vektorer i $\mathbb R^4$.

Fra tidligere kjenner vi samlingen av alle outputvektorer en matrise kan produsere som **kolonnerommet**. For hele bildereduksjonen skriver vi

$$\operatorname{Col}(A_{\mathrm{pool}})
=\{A_{\mathrm{pool}}x:x\in\mathbb R^{16}\}\subseteq\mathbb R^4.$$

Kolonnerommet ligger altså i **outputrommet**. Vektorene i nullrommet har 16 komponenter; vektorene i kolonnerommet har fire. De to rommene kan derfor ha forskjellige dimensjoner og består i dette eksemplet ikke engang av like lange vektorer.

Navnet kan nå leses direkte fra eksperimentet. Hvis $a_j$ er kolonne $j$ i $A_{\mathrm{pool}}$, er

$$A_{\mathrm{pool}}x=x_1a_1+\cdots+x_{16}a_{16}.$$

Formelen sier at inputverdien $x_j$ skalerer kolonnebildet $a_j$, og at de 16 skalerte bidragene legges sammen. Alle outputer bygges dermed som lineærkombinasjoner av kolonnebildene. Dette er den samme byggesteinsideen som for basisbilder, men nå er byggesteinene bestemt av transformasjonsmatrisen.

I vårt eksempel holder det å beholde én kolonne fra hver av de fire gruppene, for eksempel kolonne 1, 3, 9 og 11. Disse fire kan varieres uavhengig og bygger alle mulige outputbilder. De andre tolv kolonnene gjentar virkninger vi allerede har.

**Rangen** er dimensjonen til kolonnerommet:

$$\operatorname{rank}(A_{\mathrm{pool}})
=\dim\operatorname{Col}(A_{\mathrm{pool}}).$$

Uformelt teller rangen hvor mange outputverdier som kan varieres
uavhengig. De fire blokkgjennomsnittene kan velges fritt, så rangen er 4.

```{pyodide-python}
#| label: week3-rank-check

# shape[1] teller inputkoordinater, shape[0] teller outputkoordinater.
# Rangen kan være mindre enn begge dersom noen retninger er overflødige.
print("Inputverdier:",A_pool.shape[1])
print("Outputverdier:",A_pool.shape[0])
print("Numerisk rang:",np.linalg.matrix_rank(A_pool))
```

:::: {.callout-note collapse="true"}
### Valgfri utvidelse: En overflødig femte måling

Her kan du kontrollere at flere outputtall ikke nødvendigvis betyr mer
informasjon. Vi legger til gjennomsnittet av alle de 16 inputpikslene som en
femte måling. Den nye outputverdien ser først ut som ny informasjon, men den
kan beregnes fra de fire blokkgjennomsnittene.

```{pyodide-python}
#| label: week3-redundant-output
#| autorun: true

# vstack legger til én ny måling som femte rad. Den nye raden er
# gjennomsnittet av de fire gamle radene og kan derfor ikke øke rangen.
A_five=np.vstack([A_pool,np.ones(16)/16])
X_test=rng.random((4,4))
y=A_five@X_test.reshape(-1)
print("Fem outputverdier:",y)
print("Femte verdi:",y[4])
print("Gjennomsnitt av de fire første:",np.mean(y[:4]))
print("Rang med fire outputer:",np.linalg.matrix_rank(A_pool))
print("Rang med fem outputer:",np.linalg.matrix_rank(A_five))
```

Utskriften viser at den femte outputverdien er nøyaktig gjennomsnittet av de
fire første. Matrisen har nå fem rader, men den femte målingen gir ingen ny
justeringsmulighet og ingen ny informasjon om inputen. Den er bestemt av de
fire andre, så rangen er fortsatt 4.

::::

:::: {.callout-note collapse="true"}
### Valgfri visualisering: Seksten knapper, men bare fire når fram

Vi startet med 16 uavhengige pikselverdier. Nå beskriver vi det samme inputbildet med mer passende skyveknapper. Fire fargede knapper styrer blokkgjennomsnittene. Tolv grå knapper styrer kontraster inne i blokkene uten å endre gjennomsnittene.

Prøv begge typer i figuren. De fargede knappene endrer outputen. De grå kan flyttes, men outputen står stille.

```{.jsxgraph width="760" height="440"}
var board = JXG.JSXGraph.initBoard(BOARDID, {
  boundingbox: [0, 9.1, 15.2, 0],
  axis: false,
  showCopyright: false,
  showNavigation: false,
  pan: { enabled: false },
  zoom: { enabled: false }
});

var controlColors=['#277da1','#d98900','#4f8f49','#8b5aa7'];
var controlFills=['#8ecae6','#ffcf70','#a8d5a2','#d7b5e8'];
var controlNames=['øvre venstre','øvre høyre','nedre venstre','nedre høyre'];
var initialMeans=[0.25,0.60,0.40,0.75];
var meanControls=[];
var contrastControls=[];

board.create('text',[3.0,8.72,'INPUT: 16 uavhengige knapper'],{
  anchorX:'middle',fontSize:16,cssStyle:'font-weight:600',fixed:true
});
board.create('text',[2.85,8.15,'4 blokkgjennomsnitt — disse påvirker outputen'],{
  anchorX:'middle',fontSize:12,cssStyle:'font-weight:600',fixed:true
});

for (let i=0;i<4;i++) {
  let y=7.50-0.66*i;
  board.create('text',[0.45,y,controlNames[i]],{
    anchorY:'middle',fontSize:10,color:controlColors[i],
    cssStyle:'font-weight:600',fixed:true
  });
  meanControls.push(board.create('slider',
    [[2.25,y],[5.15,y],[0,initialMeans[i],1]],{
      name:'',snapWidth:0.05,precision:2,
      strokeColor:controlColors[i],fillColor:controlColors[i],
      highline:{strokeColor:controlColors[i]},
      baseline:{strokeColor:'#b8b8b8'},
      point1:{visible:false},point2:{visible:false}
    }));
}

board.create('text',[2.85,4.60,'12 kontraster — prøv dem, outputen endres ikke'],{
  anchorX:'middle',fontSize:12,color:'#666666',
  cssStyle:'font-weight:600',fixed:true
});

for (let k=0;k<12;k++) {
  let col=Math.floor(k/4), row=k%4;
  let x0=0.65+1.72*col, y=3.92-0.63*row;
  board.create('text',[x0,y,'c'+(k+1)],{
    anchorY:'middle',fontSize:9,color:'#777777',fixed:true
  });
  contrastControls.push(board.create('slider',
    [[x0+0.34,y],[x0+1.38,y],[-1,0,1]],{
      name:'',snapWidth:0.1,precision:1,
      strokeColor:'#777777',fillColor:'#777777',
      highline:{strokeColor:'#777777'},
      baseline:{strokeColor:'#c8c8c8'},
      point1:{visible:false},point2:{visible:false},
      glider:{size:2,strokeColor:'#666666',fillColor:'#aaaaaa'}
    }));
}

board.create('arrow',[[5.75,6.55],[8.65,6.55]],{
  strokeColor:'#333333',strokeWidth:3,fixed:true,highlight:false
});
board.create('text',[7.20,6.92,'transformasjonen bruker dem'],{
  anchorX:'middle',fontSize:11,fixed:true
});

board.create('segment',[[5.75,3.05],[7.20,3.05]],{
  strokeColor:'#888888',strokeWidth:2,dash:2,fixed:true,highlight:false
});
board.create('text',[7.45,3.05,'×'],{
  anchorX:'middle',anchorY:'middle',fontSize:25,color:'#777777',fixed:true
});
board.create('text',[7.20,2.55,'sendes til null'],{
  anchorX:'middle',fontSize:11,color:'#666666',fixed:true
});

function outputBox(x0,y0,index) {
  board.create('polygon',
    [[x0,y0],[x0+1.35,y0],[x0+1.35,y0+1.35],[x0,y0+1.35]],{
      fillColor:controlFills[index],fillOpacity:0.88,
      vertices:{visible:false},
      borders:{strokeColor:'#ffffff',strokeWidth:2,
               fixed:true,highlight:false},
      fixed:true,highlight:false
    });
  board.create('text',[x0+0.675,y0+0.675,function(){
    return meanControls[index].Value().toFixed(2);
  }],{
    anchorX:'middle',anchorY:'middle',fontSize:14,
    cssStyle:'font-weight:600',fixed:true
  });
}

board.create('text',[11.35,7.75,'OUTPUT: 4 knapper'],{
  anchorX:'middle',fontSize:16,cssStyle:'font-weight:600',fixed:true
});
outputBox(10.0,5.75,0);
outputBox(11.35,5.75,1);
outputBox(10.0,4.40,2);
outputBox(11.35,4.40,3);
board.create('polygon',[[10.0,4.40],[12.70,4.40],[12.70,7.10],[10.0,7.10]],{
  fillOpacity:0,vertices:{visible:false},
  borders:{strokeColor:'#333333',strokeWidth:2,fixed:true,highlight:false},
  fixed:true,highlight:false
});

board.create('text',[11.35,3.35,'De fire outputverdiene kan stilles uavhengig.'],{
  anchorX:'middle',fontSize:12,fixed:true
});
board.create('text',[7.60,0.75,'Én uavhengig knapp = én retning'],{
  anchorX:'middle',fontSize:13,cssStyle:'font-weight:600',fixed:true
});
```

Dette er ikke 16 nye størrelser; det er en ny beskrivelse av de samme 16
inputmulighetene. Å bevege én knapp mens de andre står stille, kaller vi å
bevege oss i én **retning**.

::::

Vi kan nå oppsummere de 16 inputmulighetene, også uten å bruke den valgfrie
visualiseringen:

- De tolv kontrastmønstrene vi fant tidligere, gir tolv uavhengige
  inputretninger som sendes til nullbildet. De danner en basis for
  nullrommet. I den valgfrie visualiseringen er dette de grå knappene.
- De fire blokkgjennomsnittene kan endres uavhengig og gir fire uavhengige
  outputretninger. De danner en basis for kolonnerommet. I visualiseringen
  er dette de fargede knappene.

Flere forskjellige pikselendringer kan gi samme endring i outputen. Derfor teller rangen ikke konkrete inputendringer. Den teller hvor mange outputverdier som kan stilles uavhengig. I dette eksemplet er det fire.

De synlige og usynlige knappene gjør sammen rede for alle 16 inputmulighetene:

$$16=4+12.$$

For en matrise med $n$ kolonner sier **rang-nullitet** at

$$n=\operatorname{rank}(A)+\dim N(A).$$

::: {.callout-note}
### Tolkning

- **Nulliteten 12** teller de uavhengige inputretningene som sendes til null.
- **Rangen 4** teller de uavhengige outputretningene inputen kan produsere.
- Rangen og nulliteten teller forskjellige typer retninger i forskjellige rom, men til sammen gjør tallene rede for alle 16 inputdimensjonene.
:::

## 3.5 Overfør ideene til polynomer {#uke3-del5}

Så langt har vektorene vært bilder eller tallkolonner. Nå bruker vi de kjente
begrepene på polynomer. Dette er overgangen til ukeprosjektet.

| I bildeeksemplet | For polynomer |
|---|---|
| Pikselverdier | Polynomkoeffisienter |
| Basisbilder | Basispolynomer |
| Samme bilde i to basiser | Samme polynom i to basiser |
| Matrisemåling $Ax$ | Avlesning av polynomverdier $E(p)$ |
| En usynlig bildeendring | Et polynom som er null i avlesningspunktene |
| Rekonstruksjon fra output | Reverse engineering fra polynomverdier |

Et vektorrom trenger ikke å bestå av piler eller tallkolonner. Det avgjørende
er at objektene kan legges sammen og ganges med tall, og at disse operasjonene
følger de vanlige regnereglene. Polynomer er et viktig eksempel.

### Polynomer som vektorer

Vi begynner med polynomer av grad høyst 2. For et polynom som ikke er null,
er **graden** den høyeste potensen av $x$ som har en koeffisient forskjellig
fra null. Polynomet $3-x+x^2$ har for eksempel grad 2.

$$
\mathcal P_2=\{a+bx+cx^2:a,b,c\in\mathbb R\}.
$$

Dette er et vektorrom. Vektorene er nå polynomer, og vi regner ved å samle
ledd med samme potens av $x$. For eksempel, hvis

$$p(x)=1+2x,\qquad q(x)=3-x+x^2,$$

så er

$$
p+q=4+x+x^2,
\qquad
2p-q=-1+5x-x^2.
$$

Et uttrykk som $2p-q$ kalles en **lineærkombinasjon** av $p$ og $q$: Vi
ganger hvert polynom med et tall og legger resultatene sammen. Dette er samme
type regning som når vi lager en lineærkombinasjon av tallkolonner.

```{math-exercise}
#| label: week3-polynomial-arithmetic
#| caption: Regn med polynomer
#| vars: x
#| partial-credit: true
#| field-labels: p + q, 2p − q

La $p(x)=1+2x$ og $q(x)=3-x+x^2$. Regn ut og samle ledd med samme potens:

$(p+q)(x)=$ __[4+x+x^2]

$(2p-q)(x)=$ __[-1+5*x-x^2]
```

### Fra polynom til tallkolonne

Hvert polynom i $\mathcal P_2$ kan bygges på nøyaktig én måte av de tre
polynomene

$$1,\qquad x,\qquad x^2.$$

For eksempel er

$$4-2x+3x^2=4\cdot1+(-2)\cdot x+3\cdot x^2.$$

Tallene foran byggesteinene samles i en koordinatvektor:

$$
4-2x+3x^2
\quad\longleftrightarrow\quad
\begin{bmatrix}4\\-2\\3\end{bmatrix}.
$$

Den ordnede samlingen $(1,x,x^2)$ kalles en **basis** for $\mathcal P_2$.
Fordi dette er det enkleste og vanligste valget, kalles den ofte
**standardbasisen**, **monomialbasisen** eller **potensbasisen**. De tre
navnene viser her til den samme ordnede listen. Ordet «standard» betyr ikke
at dette er den eneste mulige basisen.

Rekkefølgen bestemmer hvor tallene skal stå: konstantleddet øverst, deretter
koeffisienten til $x$, så koeffisienten til $x^2$. Hvis en potens mangler, er
koeffisienten null.

```{math-exercise}
#| label: week3-polynomial-coefficients
#| caption: Les av koeffisientene
#| partial-credit: true

Skriv koordinatvektoren til $p(x)=4-2x+3x^2$ i basisen $(1,x,x^2)$:

$[p]_{(1,x,x^2)}=$ vec[4,-2,3]
```

Vi kan også gå motsatt vei. Koordinatvektoren forteller hvilke tall som skal
stå foran $1$, $x$ og $x^2$.

```{math-exercise}
#| label: week3-polynomial-from-coordinates
#| caption: Bygg polynomet fra koordinatene
#| vars: x

Et polynom har koordinatvektoren
$[r]_{(1,x,x^2)}=\begin{bmatrix}-1\\2\\3\end{bmatrix}$.
Skriv polynomet:

$r(x)=$ __[-1+2*x+3*x^2]
```

### Hva gjør en samling til en basis?

At noen polynomer **spenner ut** et rom, betyr uformelt at hvert polynom i
rommet kan bygges ved å skalere og legge sammen de valgte polynomene. Med
andre ord kan hvert polynom skrives som en lineærkombinasjon av dem.

En basis må oppfylle to krav:

1. **Ingen hull:** Alle polynomene i rommet kan bygges som en
   lineærkombinasjon av basispolynomene.
2. **Ingen overflødige byggesteiner:** Ingen av basispolynomene kan bygges av
   de andre. Dette kalles lineær uavhengighet.

Samlingen $(1,x,x^2)$ er derfor en basis for $\mathcal P_2$. Samlingen
$(1,x,1+x)$ er ikke en basis for $\mathcal P_2$: Den mangler en byggestein
for $x^2$, og dessuten er $1+x$ summen av de to første polynomene.

En basis behøver ikke bestå av bare enkeltpotenser. Også

$$\mathcal B=(1+x,\ x,\ x^2)$$

er en basis for $\mathcal P_2$. For eksempel kan samme polynom skrives

$$2-x+3x^2=2(1+x)-3x+3x^2,$$

så koordinatene i denne basisen er $(2,-3,3)^T$.

```{math-exercise}
#| label: week3-polynomial-simple-change-basis
#| caption: Koordinater i en annen basis
#| partial-credit: true

La $\mathcal B=(1+x,x,x^2)$. Finn koordinatvektoren til
$s(x)=5+2x-x^2$ i denne basisen:

$[s]_{\mathcal B}=$ vec[5,-3,-1]
```

:::: {#week3-polynomial-basis-context .math-exercise-context}

Et polynom i $\mathcal P_3$ skrives som
$a_0+a_1x+a_2x^2+a_3x^3$. I en koeffisientmatrise representerer hver kolonne
ett polynom. Radene inneholder koeffisientene til henholdsvis
$1,x,x^2,x^3$.

En basis består av polynomer som er lineært uavhengige og som spenner ut hele
det etterspurte rommet. Basisvektorene kan stå i hvilken som helst rekkefølge.
Røde kolonner er null eller ligger utenfor rommet. Hvis de gyldige kolonnene
er lineært avhengige, farges hele familien gul. En grønn familie er gyldig og
uavhengig, men kan fortsatt være for liten til å spenne ut hele rommet.

::::

### En basis for alle polynomer i P₃

I rommet

$$
\mathcal P_3=\{a_0+a_1x+a_2x^2+a_3x^3:a_i\in\mathbb R\}
$$

kan vi bruke andre basispolynomer enn $1,x,x^2,x^3$. I svarmatrisen under er
hver kolonne ett polynom. Du bestemmer selv hvor mange kolonner som trengs.

```{math-exercise}
#| label: week3-polynomial-p3-basis
#| caption: En valgfri basis for P₃
#| mode: custom
#| context: week3-polynomial-basis-context
#| checker: |
#|   def check(response, symbols):
#|       A = response["inputs"]["P3basis"]["matrix"]
#|       result = assess_basis(
#|           A,
#|           axis="columns",
#|           target_dimension=4,
#|           belongs=lambda vector: vector.rows == 4,
#|           name="P3basis",
#|           space_name="P3",
#|       )
#|       statuses = result["assessment"]["P3basis"]["columns"]
#|       if result["score"] < 1:
#|           if "incorrect" in statuses:
#|               result["feedback"] = "En rød kolonne er null og kan ikke være en basisvektor."
#|           elif "dependent" in statuses:
#|               result["feedback"] = "De gule polynomene er lineært avhengige. Behold en uavhengig del og juster familien videre."
#|           elif statuses:
#|               result["feedback"] = "De grønne polynomene er uavhengige, men de spenner ennå ikke ut hele P3."
#|           else:
#|               result["feedback"] = "Legg inn polynomer som kolonner i koeffisientmatrisen."
#|       return result

Finn en basis for $\mathcal P_3$. Oppgi ett polynom per kolonne. Radene er
koeffisientene til henholdsvis $1,x,x^2,x^3$:

$A=$ mat{name=P3basis, rows=4, cols=auto, initial-cols=2, min-cols=0, max-cols=5}
```

### Polynomer som bare bygger en del av P₃

Vi kan også begynne med noen polynomer og undersøke alle
lineærkombinasjonene de kan lage. En slik samling kan være mindre enn hele
$\mathcal P_3$, men fortsatt tåle addisjon og multiplikasjon med tall uten at
vi forlater samlingen. Da kalles den et **underrom**. Underrommet inneholder
også nullpolynomet.

La

$$
\begin{aligned}
p_1&=1+x, & p_2&=x+x^2,\\
p_3&=1+x^2+x^3, & p_4&=2-x-x^2+x^3.
\end{aligned}
$$

Notasjonen $\operatorname{Span}$ betyr «alle lineærkombinasjoner». Mengden

$$U=\operatorname{Span}(p_1,p_2,p_3,p_4)$$

er derfor alle polynomer som kan bygges av $p_1,p_2,p_3,p_4$. Dette er et
underrom av $\mathcal P_3$. En basis for $U$ kan bestå av noen av polynomene
over, eller av andre polynomer som spenner ut nøyaktig det samme rommet.

```{math-exercise}
#| label: week3-polynomial-subspace-basis
#| caption: Basis for et polynomunderrom
#| mode: custom
#| context: week3-polynomial-basis-context
#| checker: |
#|   def check(response, symbols):
#|       A = response["inputs"]["Ubasis"]["matrix"]
#|       T = Matrix([
#|           [1, 0, 1],
#|           [1, 1, 0],
#|           [0, 1, 1],
#|           [0, 0, 1],
#|       ])
#|       target_rank = T.rank()
#|       result = assess_basis(
#|           A,
#|           axis="columns",
#|           target_dimension=target_rank,
#|           belongs=lambda vector: vector.rows == 4 and T.row_join(vector).rank() == target_rank,
#|           name="Ubasis",
#|           space_name="U",
#|       )
#|       statuses = result["assessment"]["Ubasis"]["columns"]
#|       if result["score"] < 1:
#|           if "incorrect" in statuses:
#|               result["feedback"] = "En rød kolonne er null eller representerer et polynom utenfor U."
#|           elif "dependent" in statuses:
#|               result["feedback"] = "De gule polynomene ligger i U, men familien er lineært avhengig. Behold en uavhengig del og juster familien videre."
#|           elif statuses:
#|               result["feedback"] = "De grønne polynomene ligger i U og er uavhengige, men de spenner ennå ikke ut hele U."
#|           else:
#|               result["feedback"] = "Legg inn basispolynomer som kolonner i koeffisientmatrisen."
#|       return result

Finn en basis for $U$. Oppgi ett polynom per kolonne, med koeffisientene til
$1,x,x^2,x^3$ ovenfra og ned:

$B_U=$ mat{name=Ubasis, rows=4, cols=auto, initial-cols=2, min-cols=0, max-cols=5}
```

### Koordinater i en mer sammensatt basis

Når basisen skifter, skifter koordinatene, selv om polynomet er det samme. I
$\mathcal P_2$ bruker vi nå basisen $\mathcal C=(p_1,p_2,p_3)$, der

$$
p_1=x^2-2,\qquad
p_2=-x^2+x+2,\qquad
p_3=3x^2+x-5.
$$

Å finne $[q]_{\mathcal C}$ betyr å finne tall $c_1,c_2,c_3$ slik at

$$q=c_1p_1+c_2p_2+c_3p_3.$$

Sammenligner vi koeffisientene til $1$, $x$ og $x^2$ på begge sider, får vi
et vanlig lineært ligningssystem for $c_1,c_2,c_3$.

```{math-exercise}
#| label: week3-polynomial-coordinates
#| caption: Koordinater i en polynombasis
#| partial-credit: true

Finn koordinatvektoren til $q(x)=4x^2+x-7$ i basisen $\mathcal C$:

$[q]_{\mathcal C}=$ mat[1;0;1]
```

Polynomrom krever altså ingen ny type lineær algebra. Vi bruker de samme
begrepene som for tallkolonner: lineærkombinasjon, spenn, lineær uavhengighet,
basis og koordinater.

I prosjektet **Polynomer i blindsonen** går vi videre fra koeffisienter til
målinger. Vi får verdiene $p(x_0),\ldots,p(x_n)$ og gjør reverse engineering:
Hvilke koeffisienter kan ha produsert disse verdiene? Bildeeksemplene har
allerede gitt oss de sentrale spørsmålene: Hvilken basis bruker vi, hvilken
informasjon mister målingen, og kan små endringer være nesten usynlige?


## 3.6 Praktisk hovedløp: Utforsk bildetransformasjoner selv {#uke3-del4}

Nå går vi tilbake til bildetransformasjonen fra 3.1–3.4. Denne gangen skal du
ikke bare følge ferdige eksempler, men selv konstruere, teste og forklare
transformasjoner. Dette er den praktiske delen av hovedløpet, ikke valgfritt
støttestoff.

Hjelpefunksjonene, transformasjonen og mønsterbildene fra de foregående
delene er tilgjengelige under. Her skal du endre kode og lete etter mønstre
selv.

Gjør aktivitet **A og D**, og velg deretter **enten B eller C**. Aktivitet E er
en valgfri numerisk fordypning. For hvert valgt eksperiment arbeider du i
denne rekkefølgen:

1. Gjett først hva figuren eller outputen vil vise.
2. Kjør eksperimentet og beskriv det du faktisk ser.
3. Kontroller observasjonen med et tall, for eksempel en residual eller en rang.
4. Forklar til slutt observasjonen med begrepene fra uka.

Startcellene gjør plotting og bokføring, men gir ikke ferdige svar. Et forsøk som ikke virker ved første kjøring kan være nyttig: undersøk forskjellen mellom det du forventet og det koden faktisk produserte.

### Obligatorisk A: Lag et nytt mønster med output null

Endre `Z`. Hver $2\times2$-blokk skal ha gjennomsnitt null, men bruk ikke sjakkmønsteret uendret. Før du kjører cellen, regn ut minst ett blokkgjennomsnitt for hånd. Figuren viser om mønsteret forsvinner, mens normen under figuren måler outputens avstand fra nullbildet.

```{pyodide-python}
# Dette er startforslaget, ikke et fasitsvar. Endre minst to av tallene,
# men pass på at hver 2 x 2-blokk fortsatt har sum null.
Z=np.array([
    [ 1.,-1., 0., 0.],
    [ 0., 0., 0., 0.],
    [ 0., 0., 1.,-1.],
    [ 0., 0., 0., 0.]
])
show_images([Z,average_pool(Z)],["Mitt mønster","Output"],
            cols=2,cmap="coolwarm",vmin=-1,vmax=1)
print("||A z|| =",np.linalg.norm(A_pool@Z.reshape(-1)))
```

Legg deretter en liten versjon av mønsteret til et vanlig bilde. Velg størrelsen slik at pikselverdiene fortsatt ligger mellom 0 og 1. Vis originalbildet, det endrede bildet og begge outputene. Forklar både hvorfor inputbildene er forskjellige og hvorfor transformasjonen ikke kan skille dem.

### Valgoppgave B: Hva kan tre byggesteiner lage?

Velg tre mønsterbilder og generer åtte tilfeldige lineærkombinasjoner. Se etter en egenskap som går igjen i alle bildene: finnes det for eksempel en symmetri, en fast sum eller en type kontrast som aldri opptrer? Bytt deretter ut én byggestein og se hvilken ny variasjon som blir mulig.

```{pyodide-python}
rng=np.random.default_rng(10)
# Studentvalg: Bytt byggesteiner her. Tre byggesteiner kan høyst gi tre
# uavhengige retninger i rommet av alle 2 x 2-bilder.
my_building_blocks=[M,H,V]
my_images=[]
for _ in range(8):
    # Nye koeffisienter, men de samme tre byggesteinene, i hvert forsøk.
    c=rng.uniform(-1,1,size=3)
    my_images.append(sum(value*block for value,block
                         in zip(c,my_building_blocks)))
show_images(my_images,[""]*8,cols=4,cmap="coolwarm",vmin=-2,vmax=2)
```

Forsøk å lage et konkret $2\times2$-målbilde som de tre byggesteinene ikke kan treffe. Dette er den eksperimentelle siden av dimensjon: tre uavhengige justeringsmuligheter kan ikke styre fire uavhengige pikselverdier.

### Valgoppgave C: Lag en annen basis

Bytt ut minst to av bildene. Prøv gjerne først et valg der ett bilde kan bygges av de andre. Observer hva rangen blir og om ligningssystemet kan løses. Endre deretter byggesteinene til rangen blir 4; da skal fire koeffisienter kunne styre de fire pikselverdiene uavhengig.

```{pyodide-python}
# Studentvalg: Endre B1, ..., B4 før resten av cellen kjøres.
B1,B2,B3,B4=E1.copy(),E2.copy(),E3.copy(),E4.copy()
my_basis=[B1,B2,B3,B4]
# Q har én foreslått basisvektor i hver kolonne.
Q=np.column_stack([B.reshape(-1) for B in my_basis])
show_images(my_basis,["$B_1$","$B_2$","$B_3$","$B_4$"],
            cols=4,cmap="coolwarm",vmin=-1,vmax=1)
print("Rang:",np.linalg.matrix_rank(Q))

target=rng.uniform(-1,1,size=(2,2))
if np.linalg.matrix_rank(Q)==4:
    # Reverse engineering: finn koordinatene til et tilfeldig målbilde.
    coordinates=np.linalg.solve(Q,target.reshape(-1))
    reconstruction=(Q@coordinates).reshape(2,2)
    show_images([target,reconstruction],["Målbilde","Rekonstruksjon"],
                cols=2,cmap="coolwarm",vmin=-1,vmax=1)
else:
    print("Byggesteinene er avhengige. Endre dem og prøv igjen.")
```

### Obligatorisk D: Design en ny bildereduksjon

Lag en lineær transformasjon fra 16 inputpiksler til høyst 6 outputverdier. Hver rad i `A_new` er én måling av bildet. Tegn først hvilke piksler målingen skal bruke, og sett så inn de tilsvarende vektene i raden. Mulige ideer er radgjennomsnitt, kolonnegjennomsnitt, diagonalsummer eller utvalgte piksler.

```{pyodide-python}
# Fire rader betyr fire målinger. Endre også antallet rader dersom
# transformasjonen din skal ha et annet antall outputverdier.
A_new=np.zeros((4,16))

# TODO: Sett inn vekter. Rad i beskriver nøyaktig hvordan output i beregnes.

test_image=rng.random((4,4))
# reshape(-1) gjør testbildet til inputvektoren som A_new forventer.
test_output=A_new@test_image.reshape(-1)
show_images([test_image],["Testbilde"],cols=1,vmin=0,vmax=1)
print("Output:",test_output)
print("Rang:",np.linalg.matrix_rank(A_new))
print("Nullitet:",16-np.linalg.matrix_rank(A_new))
```

Test flere bilder med tydelig struktur, ikke bare det tilfeldige bildet. Finn deretter et ikke-null bilde som transformasjonen sender til null. Vis dette bildet og outputen ved siden av hverandre. Forklar hva hver rad i matrisen måler, og hvilke bildeendringer som derfor ikke registreres.

### Valgfri fordypning E: Nesten samme måling

To målinger kan være matematisk forskjellige, men så like at maskinen får problemer med å skille dem. Vi begynner med å tegne vektene i de to målingene. Den første summerer alle piksler likt. Den andre gir bare den siste pikselen en ørliten ekstra vekt.

```{pyodide-python}
#| label: week3-nearly-same-measurements-picture
#| autorun: true

def nearly_redundant_measurements(eps,dtype=float):
    """To nesten like målinger lagret med valgt tallpresisjon."""
    first=np.ones(16)
    # Bare vekten til siste piksel skiller rad 2 fra rad 1.
    second=first.copy(); second[-1]+=eps
    return np.vstack([first,second]).astype(dtype)

eps_picture=0.05
A_picture=nearly_redundant_measurements(eps_picture)
show_images([A_picture[0].reshape(4,4),
             A_picture[1].reshape(4,4),
             (A_picture[1]-A_picture[0]).reshape(4,4)],
            ["Måling 1","Måling 2","Forskjellen"],
            cols=3,cmap="coolwarm",vmin=-0.05,vmax=1.05,
            figsize=(5.4,1.8))
```

Forskjellsbildet har bare én ikke-null piksel. Gjør nå denne forskjellen mindre ved å endre `eps`, og sammenlign hva som skjer når tallene lagres som `float64` og `float32`.

```{pyodide-python}
#| label: week3-nearly-same-measurements-rank

# Gjør forskjellen 10 000 ganger mindre for hver runde og sammenlign hvor
# lenge de to tallformatene klarer å skille radene.
for exponent in [2,6,10,14,18]:
    eps=10.0**(-exponent)
    A64=nearly_redundant_measurements(eps,np.float64)
    A32=nearly_redundant_measurements(eps,np.float32)
    print(f"eps={eps:.0e}",
          "rang float64 =",np.linalg.matrix_rank(A64),
          "rang float32 =",np.linalg.matrix_rank(A32))
```

På papiret er målingene uavhengige for enhver $\varepsilon\neq0$: den lille ekstravekten kan ikke lages ved bare å skalere den første raden. I maskinen kan ekstravekten bli avrundet bort, eller bli vurdert som for liten til å være pålitelig. `matrix_rank` bruker derfor en toleranse og rapporterer en **numerisk rang**. Beskriv når de to tallformatene slutter å skille målingene, og knytt resultatet til feil- og toleransebegrepene fra uke 2.

Trenger du en kort repetisjon av forskjellen på eksakt og numerisk rang, kan
du åpne underdelen om numerisk rang i 3.7.

## 3.7 Støtteløp: Matriseregning ved behov {#uke3-stotte-matriser}

Denne delen repeterer lineær algebra fra tidligere emner. Den er med slik at
du ikke trenger å finne fram gamle notater. Hvis du allerede kan radredusere
en matrise, finne pivotkolonner og beregne en basis for nullrommet, trenger du
ikke lese hele delen. Åpne bare underdelen du vil slå opp.

Bruk spørsmålene som en rask selvtest:

1. Kan du radredusere en matrise og finne pivotkolonnene?
2. Vet du hvorfor en kolonneromsbasis hentes fra den opprinnelige matrisen?
3. Kan du skrive løsningene av $Ax=0$ ved hjelp av frie variabler?
4. Kan du finne en basis for nullrommet og kontrollere rang–nullitet?
5. Kan du avgjøre om $Ax=b$ har en løsning?

Hvis svaret er ja på alle fem, kan du gå til papir- og kontrolloppgavene i
3.8 dersom du ønsker ekstra trening, eller avslutte siden her.

Bildene i hovedløpet gjorde begrepene synlige. I støtteløpet legger vi bort
bildebakgrunnen og regner direkte med én matrise. Målet er å repetere hvordan
vi finner rang, basis for kolonnerommet og basis for nullrommet — først med
papir og blyant, deretter med kode som kontroll.

Selve matriseberegningene var pensum i Matematikk 1: radoperasjoner, ligningssystemer og Gauss-eliminasjon. Det er en stund siden, så vi forventer ikke at framgangsmåten sitter friskt. Denne siden repeterer regningen steg for steg og kobler den til ordene vi bruker nå — pivot, rang, kolonnerom og nullrom.

Vi bruker samme matrise gjennom hele eksemplet:

$$
A=
\begin{bmatrix}
1&2&0&1\\
0&1&1&1\\
1&3&1&2
\end{bmatrix}.
$$

Matrisen har fire kolonner og tre rader, og beskriver derfor transformasjonen

$$
A:\underbrace{\mathbb R^4}_{\text{inputrom}}
\longrightarrow
\underbrace{\mathbb R^3}_{\text{outputrom}}.
$$

Nullrommet består av 4-vektorer og ligger i inputrommet: $N(A)\subseteq\mathbb R^4$. Kolonnerommet består av 3-vektorer og ligger i outputrommet: $\operatorname{Col}(A)\subseteq\mathbb R^3$. Vi vil svare på tre spørsmål:

1. Hvor mange uavhengige outputretninger har transformasjonen?
2. Hvilke inputretninger gir output null?
3. Kan en gitt vektor $b$ produseres som $Ax$?

Vi bruker de samme fargene gjennom hele regningen:

| Farge | I eliminasjonen | Senere i regningen |
|---|---|---|
| 🟦 Blå | første pivot, kolonne 1 | basisvektor $a_1$ og pivotvariabel $x_1$ |
| 🟧 Oransje | andre pivot, kolonne 2 | basisvektor $a_2$ og pivotvariabel $x_2$ |
| 🟩 Grønn | kolonne uten pivot | fri variabel $x_3=s$ og første nullromsretning |
| 🟪 Lilla | kolonne uten pivot | fri variabel $x_4=t$ og andre nullromsretning |

```{pyodide-python}
#| label: week3-pure-matrix-setup
#| autorun: true

# Denne matrisen er felles eksempel i hele 3.7. Rad 3 er summen av de to
# første radene, noe eliminasjonen snart skal avdekke.
A=np.array([
    [1.,2.,0.,1.],
    [0.,1.,1.,1.],
    [1.,3.,1.,2.]
])
print(A)
```

:::: {.callout-note collapse="true"}
### Eliminasjon og rang

::: {.callout-tip}
#### Først på papir

Trekk første rad fra tredje rad. Sammenlign deretter den nye tredje raden med andre rad, og eliminer én gang til. Marker den første ikke-null-oppføringen i hver ikke-null-rad.
:::

Regningen blir

$$
\begin{bmatrix}
1&2&0&1\\
0&1&1&1\\
1&3&1&2
\end{bmatrix}
\longrightarrow
\begin{bmatrix}
1&2&0&1\\
0&1&1&1\\
0&1&1&1
\end{bmatrix}
\longrightarrow
\begin{bmatrix}
\color{#277da1}{\boxed{1}}&2&0&1\\
0&\color{#d98900}{\boxed{1}}&1&1\\
0&0&0&0
\end{bmatrix}.
$$

Den siste raden inneholder ingen ny ligning. To rader er igjen, og de ledende oppføringene — **pivotene** — ligger i kolonne 1 og 2. Dermed er rangen 2.

Koden under utfører vanlig framovereliminasjon. Den går fra venstre mot høyre og bruker den første tilgjengelige ikke-null-oppføringen som pivot. Dette er tilstrekkelig for eksemplene våre og følger papirregningen tett.

```{pyodide-python}
#| label: week3-row-echelon-function
#| autorun: true

def row_echelon(A,tol=1e-12,show_steps=False):
    """Returner trappeform og indeksene til pivotkolonnene."""
    # copy=True er viktig: Vi vil radredusere R uten å endre originalen A.
    R=np.array(A,dtype=float,copy=True)
    rows,cols=R.shape
    pivot_row=0
    pivot_columns=[]

    for col in range(cols):
        # Gå fra venstre mot høyre og finn én pivot om gangen.
        if pivot_row==rows:
            break

        # Finn den første brukbare pivoten, ikke den største.
        candidate=None
        for row in range(pivot_row,rows):
            if abs(R[row,col])>tol:
                candidate=row
                break

        if candidate is None:
            continue

        if candidate!=pivot_row:
            R[[pivot_row,candidate]]=R[[candidate,pivot_row]]
            if show_steps:
                print(f"Bytt rad {pivot_row+1} og {candidate+1}:\n",R)

        for row in range(pivot_row+1,rows):
            # Trekk et multiplum av pivotraden fra raden under, akkurat som
            # ved Gauss-eliminasjon på papir.
            factor=R[row,col]/R[pivot_row,col]
            if abs(factor)>tol:
                R[row]-=factor*R[pivot_row]

        # Små avrundingsrester behandles som null, styrt av tol.
        R[np.abs(R)<=tol]=0.0
        pivot_columns.append(col)
        pivot_row+=1
        if show_steps:
            print(f"Etter pivot i kolonne {col+1}:\n",R)

    return R,pivot_columns

R,pivot_columns=row_echelon(A,show_steps=True)
print("Trappeform:\n",R)
print("Pivotkolonner, nummerert fra 1:",[j+1 for j in pivot_columns])
print("Rang fra eliminasjon:",len(pivot_columns))
print("Kontroll med NumPy:",np.linalg.matrix_rank(A))
```

`matrix_rank` er nyttig som kontroll, men eliminasjonen viser *hvorfor* rangen er 2. Mer robuste eliminasjonsalgoritmer kan omstokke rader og eventuelt kolonner for å unngå dårlige pivoter. Det tar vi ikke nå. Senere skal vi se at numerisk rang alltid avhenger av hva som regnes som «tilstrekkelig nær null».

::::

:::: {.callout-note collapse="true"}
### Basis for kolonnerommet

Pivotene forteller hvilke opprinnelige kolonner som tilfører en ny outputretning. Vi henter derfor kolonne 1 og 2 fra den opprinnelige matrisen:

$$
\color{#277da1}{a_1=\begin{bmatrix}1\\0\\1\end{bmatrix}},
\qquad
\color{#d98900}{a_2=\begin{bmatrix}2\\1\\3\end{bmatrix}}.
$$

::: {.callout-warning}
#### En vanlig feil

Pivotposisjonene finnes ved å radredusere, men basisvektorene hentes fra den **opprinnelige** matrisen. Radoperasjoner endrer kolonnene.
:::

De to andre kolonnene kan bygges av disse:

$$
a_3=a_2-2a_1,
\qquad
a_4=a_2-a_1.
$$

Kontroller begge relasjonene før du kjører cellen.

```{pyodide-python}
#| label: week3-column-space-basis
#| autorun: true

# Pivotindeksene ble funnet fra trappeformen, men selve basisvektorene må
# hentes som kolonner fra den opprinnelige matrisen A.
column_basis=A[:,pivot_columns]
a1,a2,a3,a4=[A[:,j] for j in range(4)]

print("Basisvektorer som kolonner:\n",column_basis)
print("Feil i a3 = a2 - 2*a1:",np.linalg.norm(a3-(a2-2*a1)))
print("Feil i a4 = a2 - a1:  ",np.linalg.norm(a4-(a2-a1)))
print("Rang av basisvektorene:",np.linalg.matrix_rank(column_basis))
```

Kolonne 1 og 2 er uavhengige og bygger alle kolonnene i $A$. De danner derfor en basis for kolonnerommet, som har dimensjon 2.

::::

:::: {.callout-note collapse="true"}
### Basis for nullrommet

Nullrommet finnes ved å løse det homogene systemet $Ax=0$. Trappeformen gir

$$
\begin{aligned}
x_1+2x_2+x_4&=0,\\
x_2+x_3+x_4&=0.
\end{aligned}
$$

Pivotvariablene er $\color{#277da1}{x_1}$ og $\color{#d98900}{x_2}$. Variablene $\color{#4f8f49}{x_3}$ og $\color{#8b5aa7}{x_4}$ er frie. Sett

$$\color{#4f8f49}{x_3=s},\qquad \color{#8b5aa7}{x_4=t}.$$

::: {.callout-tip}
#### Fortsett på papir

Løs den andre ligningen for $x_2$, og bruk resultatet i den første ligningen. Samle deretter alle ledd som inneholder $s$, og alle ledd som inneholder $t$.
:::

Resultatet er

$$
x=
\color{#4f8f49}{s\begin{bmatrix}2\\-1\\1\\0\end{bmatrix}}
+\color{#8b5aa7}{t\begin{bmatrix}1\\-1\\0\\1\end{bmatrix}}.
$$

Dermed er de to viste vektorene en basis for nullrommet. Koden kontrollerer både at de gir output null, og at en tilfeldig lineærkombinasjon fortsatt gjør det.

```{pyodide-python}
#| label: week3-null-space-basis-matrix
#| autorun: true

# z1 og z2 kommer fra håndregningen. Z samler dem som kolonner slik at
# A @ Z kontrollerer begge nullromsligningene samtidig.
z1=np.array([2.,-1.,1.,0.])
z2=np.array([1.,-1.,0.,1.])
Z=np.column_stack([z1,z2])

print("A ganger nullromsbasisen:\n",A@Z)
print("Rang av basisvektorene:",np.linalg.matrix_rank(Z))

rng=np.random.default_rng(31)
s,t=rng.normal(size=2)
# Hvis z1 og z2 ligger i nullrommet, gjør enhver kombinasjon det samme.
z=s*z1+t*z2
print("Tilfeldige koeffisienter:",s,t)
print("||A z|| =",np.linalg.norm(A@z))
```

I dette eksemplet har både kolonnerommet og nullrommet dimensjon 2. Det betyr ikke at de er samme rom: Kolonneromsbasisen består av 3-vektorer i outputrommet, mens nullromsbasisen består av 4-vektorer i inputrommet. At dimensjonene tilfeldigvis er like her, skyldes at $4=2+2$.

::::

:::: {.callout-note collapse="true"}
### Rang–nullitet som regnskap

Matrisen har fire kolonner, altså fire inputvariabler. Eliminasjonen ga to pivotvariabler og to frie variabler:

$$
\underbrace{4}_{\text{inputdimensjon}}
=
\underbrace{
\color{#277da1}{1}+\color{#d98900}{1}
}_{\text{rang}=2}
+
\underbrace{
\color{#4f8f49}{1}+\color{#8b5aa7}{1}
}_{\text{nullitet}=2}.
$$

Rangen kommer fra de to pivotene. Nulliteten kommer **uavhengig** fra nullromsberegningen: Vi fant en basis med to vektorer. Først nå bruker vi disse to resultatene til å kontrollere rang–nullitet.

```{pyodide-python}
#| label: week3-rank-nullity-check

# Antall pivotkolonner gir rang; antall kolonner i nullromsbasisen gir
# nullitet. A.shape[1] er inputdimensjonen n.
rank_A=len(pivot_columns)
nullity_A=Z.shape[1]
print(f"{A.shape[1]} = {rank_A} + {nullity_A}")
print("Stemmer rang–nullitet?",A.shape[1]==rank_A+nullity_A)
```

::::

:::: {.callout-note collapse="true"}
### Kan en bestemt output produseres?

Siden $a_1$ og $a_2$ er en basis for kolonnerommet, kan alle mulige outputvektorer bygges av disse to. La $\alpha$ og $\beta$ være to fritt valgte tall. De bestemmer hvor mye av henholdsvis $a_1$ og $a_2$ vi bruker:

$$
\color{#277da1}{\alpha a_1}+\color{#d98900}{\beta a_2}
=
\begin{bmatrix}
\alpha+2\beta\\\beta\\\alpha+3\beta
\end{bmatrix}.
$$

Uansett hvilke tall vi velger for $\alpha$ og $\beta$, er tredje komponent summen av de to første. Vi tester derfor to ønskede outputvektorer:

$$
b=\begin{bmatrix}2\\-1\\1\end{bmatrix},
\qquad
d=\begin{bmatrix}2\\-1\\4\end{bmatrix}.
$$

Vektoren $b$ oppfyller $b_3=b_1+b_2$, mens $d$ ikke gjør det. Den utvidede matrisen $[A\mid b]$ får derfor samme rang som $A$, men $[A\mid d]$ får én ekstra pivot.

```{pyodide-python}
#| label: week3-reachable-outputs
#| autorun: true

b=np.array([2.,-1.,1.])
d=np.array([2.,-1.,4.])

def augmented_rank(A,rhs):
    """Rang av den utvidede matrisen [A | rhs]."""
    # rhs legges til som siste kolonne, ikke som ny rad.
    return np.linalg.matrix_rank(np.column_stack([A,rhs]))

print("rang(A)       =",np.linalg.matrix_rank(A))
print("rang([A | b]) =",augmented_rank(A,b))
print("rang([A | d]) =",augmented_rank(A,d))
```

Dermed gjelder kriteriet

$$
Ax=b\text{ har løsning}
\quad\Longleftrightarrow\quad
\operatorname{rank}(A)=\operatorname{rank}([A\mid b]).
$$

Hva gjør vi når en ønsket output som $d$ ikke kan produseres nøyaktig? Det spørsmålet leder direkte til projeksjon og minste kvadraters metode i uke 4.

::::

:::: {.callout-note collapse="true"}
### Forskjellige inputer, samme output

Velg en input $x_0$ og beregn $y=Ax_0$. Hvis $z$ ligger i nullrommet, gir $x_0+z$ samme output:

$$A(x_0+z)=Ax_0+Az=Ax_0.$$

Her er en hel familie av forskjellige inputvektorer med samme output.

```{pyodide-python}
#| label: week3-same-output-pure-matrix
#| autorun: true

# Start med én input x0 og dens output y.
x0=np.array([1.,2.,0.,-1.])
y=A@x0

# z1 ligger i nullrommet. Derfor skal x0 + alpha*z1 gi samme output for
# enhver verdi av alpha.
for alpha in [-2.,-1.,0.,1.,2.]:
    x=x0+alpha*z1
    print(f"alpha={alpha:4.1f}  x={x}  A@x={A@x}")

print("Felles output:",y)
```

Dette er den rene matriseversjonen av åpningsproblemet: Nullrommet beskriver alle endringer i inputen som ikke endrer outputen.

::::

:::: {.callout-note collapse="true"}
### Eksakt og numerisk rang {#uke3-numerisk-rang}

Til slutt endrer vi den avhengige tredje raden med et svært lite tall. For enhver $\varepsilon\ne0$ er den perturberte matrisen eksakt sett av rang 3. Numerisk må vi likevel avgjøre om den nye pivoten er stor nok til å skille fra avrundingsfeil.

```{pyodide-python}
#| label: week3-nearly-dependent-row
#| autorun: true

# direction bestemmer hvordan vi forstyrrer den avhengige tredje raden.
direction=np.array([1.,-1.,1.,-1.])
for eps in [1e-4,1e-8,1e-12,1e-16]:
    # copy hindrer at forstyrrelsen samler seg opp fra én runde til neste.
    A_eps=A.copy()
    A_eps[2]+=eps*direction
    R_eps,pivots_eps=row_echelon(A_eps,tol=1e-10)
    print(f"eps={eps:.0e}",
          "rang med tol=1e-10:",len(pivots_eps),
          "NumPy-rang:",np.linalg.matrix_rank(A_eps))
```

Dette er ikke en motsigelse. **Eksakt rang** gjelder en idealisert matrise med eksakte tall. **Numerisk rang** beskriver hvor mange uavhengige retninger vi kan skille pålitelig med den valgte presisjonen og toleransen.

::::

## 3.8 Støtteløp: Papir- og kontrolloppgaver {#uke3-stotte-oppgaver}

Dette er repetisjonsoppgaver, ikke en obligatorisk fortsettelse av
hovedløpet. Bruk matrisen $B$ som selvtest. Hvis regningen går greit, kan du
gå direkte til kodekontrollen eller avslutte. Bruk matrisen $C$ som ekstra
trening dersom du trenger mer øvelse med avhengige rader, nullrom og
rang–nullitet.

Start alltid på papir. Bruk kodeoppgaven nederst etterpå til å kontrollere
regningen og eksperimentere videre. Arbeid med én matrise om gangen:

$$
B=\begin{bmatrix}
1&0&1\\
0&1&1\\
1&1&2
\end{bmatrix},
\qquad
C=\begin{bmatrix}
1&2&3\\
2&4&6
\end{bmatrix}.
$$

### På papir

Oppgavene under vurderes eksakt med SymPy. Du velger selv hvor mange
pivotindekser og basisvektorer du vil levere. Bruk knappene under matrisen for å
legge til eller fjerne kolonner. Antallet er en del av svaret.

::: {#week3-paper-assessment-context .math-exercise-context}

For en matrise med $n$ kolonner gjelder
$n=\operatorname{rank}(M)+\operatorname{nullity}(M)$. Pivotkolonnene bestemmes
fra en trappeform, men en basis for kolonnerommet hentes fra de tilsvarende
kolonnene i den opprinnelige matrisen. En basis for nullrommet må bestå av
lineært uavhengige vektorer $z$ som oppfyller $Mz=0$.

I basisoppgavene farges en gyldig og uavhengig familie grønn. Hvis gyldige
vektorer er lineært avhengige, blir hele familien gul; rekkefølgen skal ikke
avgjøre hvilken vektor som får skylden. En nullvektor eller en vektor utenfor
det etterspurte rommet blir rød. En grønn familie kan fortsatt mangle vektorer
før den spenner ut hele rommet.

:::

#### Selvtest med $B$

```{math-exercise}
#| label: week3-paper-b-echelon
#| caption: Trappeform og pivoter for B
#| mode: custom
#| partial-credit: true
#| field-labels: r₁₁, r₁₂, r₁₃, r₂₁, r₂₂, r₂₃, r₃₁, r₃₂, r₃₃
#| context: week3-paper-assessment-context
#| checker: |
#|   def check(response, symbols):
#|       values = response["expressions"]
#|       R = Matrix(3, 3, values)
#|       P = response["inputs"]["PBstep"]["matrix"]
#|       submitted_pivots = list(P)
#|       expected_rref = Matrix([[1, 0, 1], [0, 1, 1], [0, 0, 0]])
#|       def leading_columns(matrix):
#|           leads = []
#|           zero_row_seen = False
#|           for row in range(matrix.rows):
#|               lead = None
#|               for col in range(matrix.cols):
#|                   if simplify(matrix[row, col]) != 0:
#|                       lead = col
#|                       break
#|               if lead is None:
#|                   zero_row_seen = True
#|               elif zero_row_seen or (leads and lead <= leads[-1]):
#|                   return None
#|               else:
#|                   leads.append(lead)
#|           return leads
#|       leads = leading_columns(R)
#|       echelon_ok = leads is not None
#|       rowspace_ok = R.rref()[0] == expected_rref
#|       expected_pivots = [Integer(j + 1) for j in leads] if echelon_ok else []
#|       pivot_status = [
#|           i < len(expected_pivots) and value == expected_pivots[i]
#|           for i, value in enumerate(submitted_pivots)
#|       ]
#|       pivot_score = sum(pivot_status) / max(len(expected_pivots), len(submitted_pivots), 1)
#|       score = (int(echelon_ok) + int(rowspace_ok) + pivot_score) / 3
#|       return {
#|           "score": score,
#|           "show_score": False,
#|           "feedback": "" if score == 1 else "Kontroller trappeformen, og juster antallet pivotindekser slik at listen svarer til de ledende elementene fra venstre mot høyre.",
#|           "assessment": {"PBstep": {"columns": pivot_status}},
#|       }

Radreduser $B$. Oppgi en gyldig trappeform $R$ og numrene til pivotkolonnene i
stigende rekkefølge:

$R=$ mat[1,0,1;0,1,1;0,0,0]

Skriv pivotkolonnenes numre i stigende rekkefølge, én indeks per kolonne:

$P_B=$ mat{name=PBstep, rows=1, cols=auto, initial-cols=1, min-cols=0, max-cols=3}
```

```{math-exercise}
#| label: week3-paper-b-rank
#| caption: Rang og pivotkolonner for B
#| mode: custom
#| partial-credit: true
#| field-labels: Rang
#| context: week3-paper-assessment-context
#| checker: |
#|   def check(response, symbols):
#|       rank_value = response["expressions"][0]
#|       P = response["inputs"]["PBrank"]["matrix"]
#|       B = Matrix([[1, 0, 1], [0, 1, 1], [1, 1, 2]])
#|       expected_pivots = [Integer(j + 1) for j in B.rref()[1]]
#|       submitted_pivots = list(P)
#|       pivot_status = [
#|           i < len(expected_pivots) and value == expected_pivots[i]
#|           for i, value in enumerate(submitted_pivots)
#|       ]
#|       pivot_score = sum(pivot_status) / max(len(expected_pivots), len(submitted_pivots), 1)
#|       score = (int(rank_value == B.rank()) + pivot_score) / 2
#|       return {
#|           "score": score,
#|           "show_score": False,
#|           "feedback": "" if score == 1 else "Rangen er antall pivoter. Kontroller både rangverdien, antallet pivotindekser og rekkefølgen deres.",
#|           "assessment": {"PBrank": {"columns": pivot_status}},
#|       }

Finn rangen og pivotkolonnene til $B$:

$\operatorname{rank}(B)=$ _[2]

Pivotkolonner, én indeks per kolonne:

$P_B=$ mat{name=PBrank, rows=1, cols=auto, initial-cols=1, min-cols=0, max-cols=3}
```

```{math-exercise}
#| label: week3-paper-b-column-basis
#| caption: Basis for kolonnerommet til B
#| mode: custom
#| context: week3-paper-assessment-context
#| checker: |
#|   def check(response, symbols):
#|       Q = response["inputs"]["QB"]["matrix"]
#|       B = Matrix([[1, 0, 1], [0, 1, 1], [1, 1, 2]])
#|       original_columns = [B[:, j] for j in range(B.cols)]
#|       result = assess_basis(
#|           Q,
#|           axis="columns",
#|           target_dimension=B.rank(),
#|           belongs=lambda vector: Q.rows == B.rows and any(vector == column for column in original_columns),
#|           name="QB",
#|           space_name="kolonnerommet til B",
#|       )
#|       statuses = result["assessment"]["QB"]["columns"]
#|       if result["score"] < 1:
#|           if "incorrect" in statuses:
#|               result["feedback"] = "En rød kolonne er null eller er ikke en kolonne fra den opprinnelige matrisen B."
#|           elif "dependent" in statuses:
#|               result["feedback"] = "De gule kolonnene kommer fra B, men familien er lineært avhengig. Fjern eller bytt kolonner."
#|           elif statuses:
#|               result["feedback"] = "De grønne kolonnene er tillatte og uavhengige, men de danner ennå ikke en basis for hele kolonnerommet."
#|           else:
#|               result["feedback"] = "Legg til kolonner fra den opprinnelige matrisen B."
#|       return result

Sett pivotkolonnene fra den opprinnelige matrisen $B$ inn som kolonner i en
basismatrise. Du må selv velge hvor mange kolonner som trengs:

$Q_B=$ mat{name=QB, rows=3, cols=auto, initial-cols=1, min-cols=0, max-cols=3}
```

```{math-exercise}
#| label: week3-paper-b-null-basis
#| caption: Basis for nullrommet til B
#| mode: custom
#| context: week3-paper-assessment-context
#| checker: |
#|   def check(response, symbols):
#|       Z = response["inputs"]["ZB"]["matrix"]
#|       B = Matrix([[1, 0, 1], [0, 1, 1], [1, 1, 2]])
#|       result = assess_basis(
#|           Z,
#|           axis="columns",
#|           target_dimension=B.cols - B.rank(),
#|           belongs=lambda vector: Z.rows == B.cols and B * vector == zeros(B.rows, 1),
#|           name="ZB",
#|           space_name="nullrommet til B",
#|       )
#|       statuses = result["assessment"]["ZB"]["columns"]
#|       if result["score"] < 1:
#|           if "incorrect" in statuses:
#|               result["feedback"] = "En rød kolonne er null eller oppfyller ikke Bz=0."
#|           elif "dependent" in statuses:
#|               result["feedback"] = "De gule kolonnene ligger i nullrommet, men familien er lineært avhengig."
#|           elif statuses:
#|               result["feedback"] = "De grønne kolonnene er gyldige og uavhengige, men de spenner ennå ikke hele nullrommet."
#|           else:
#|               result["feedback"] = "Legg til basisvektorer for nullrommet."
#|       return result

Oppgi en basis for nullrommet til $B$, med én basisvektor per kolonne. Enhver
basis godtas, og du må selv velge antallet kolonner:

$Z_B=$ mat{name=ZB, rows=3, cols=auto, initial-cols=1, min-cols=0, max-cols=3}
```

```{math-exercise}
#| label: week3-paper-b-rank-nullity
#| caption: Rang–nullitet for B
#| mode: custom
#| partial-credit: true
#| field-labels: Inputdimensjon, Rang, Nullitet
#| context: week3-paper-assessment-context
#| checker: |
#|   def check(response, symbols):
#|       n, rank_value, nullity = response["expressions"]
#|       checks = [n == 3, rank_value == 2, nullity == 1, n == rank_value + nullity]
#|       return {"score": sum(int(value) for value in checks) / 4, "feedback": "Tell kolonnene, pivotene og de frie variablene, og kontroller deretter n = rang + nullitet."}

Fyll inn rang–nullitetsregnskapet for $B$:

inputdimensjon _[3] $=$ rang _[2] $+$ nullitet _[1]
```

#### Ekstra trening med $C$

```{math-exercise}
#| label: week3-paper-c-echelon
#| caption: Trappeform og pivoter for C
#| mode: custom
#| partial-credit: true
#| field-labels: r₁₁, r₁₂, r₁₃, r₂₁, r₂₂, r₂₃
#| context: week3-paper-assessment-context
#| checker: |
#|   def check(response, symbols):
#|       values = response["expressions"]
#|       R = Matrix(2, 3, values)
#|       P = response["inputs"]["PCstep"]["matrix"]
#|       submitted_pivots = list(P)
#|       expected_rref = Matrix([[1, 2, 3], [0, 0, 0]])
#|       def leading_columns(matrix):
#|           leads = []
#|           zero_row_seen = False
#|           for row in range(matrix.rows):
#|               lead = None
#|               for col in range(matrix.cols):
#|                   if simplify(matrix[row, col]) != 0:
#|                       lead = col
#|                       break
#|               if lead is None:
#|                   zero_row_seen = True
#|               elif zero_row_seen or (leads and lead <= leads[-1]):
#|                   return None
#|               else:
#|                   leads.append(lead)
#|           return leads
#|       leads = leading_columns(R)
#|       echelon_ok = leads is not None
#|       rowspace_ok = R.rref()[0] == expected_rref
#|       expected_pivots = [Integer(j + 1) for j in leads] if echelon_ok else []
#|       pivot_status = [
#|           i < len(expected_pivots) and value == expected_pivots[i]
#|           for i, value in enumerate(submitted_pivots)
#|       ]
#|       pivot_score = sum(pivot_status) / max(len(expected_pivots), len(submitted_pivots), 1)
#|       score = (int(echelon_ok) + int(rowspace_ok) + pivot_score) / 3
#|       return {
#|           "score": score,
#|           "show_score": False,
#|           "feedback": "" if score == 1 else "Kontroller trappeformen, og juster antallet pivotindekser slik at listen svarer til de ledende elementene fra venstre mot høyre.",
#|           "assessment": {"PCstep": {"columns": pivot_status}},
#|       }

Radreduser $C$. Oppgi en gyldig trappeform $R$:

$R=$ mat[1,2,3;0,0,0]

Skriv pivotkolonnenes numre i stigende rekkefølge, én indeks per kolonne:

$P_C=$ mat{name=PCstep, rows=1, cols=auto, initial-cols=1, min-cols=0, max-cols=3}
```

```{math-exercise}
#| label: week3-paper-c-rank
#| caption: Rang og pivotkolonner for C
#| mode: custom
#| partial-credit: true
#| field-labels: Rang
#| context: week3-paper-assessment-context
#| checker: |
#|   def check(response, symbols):
#|       rank_value = response["expressions"][0]
#|       P = response["inputs"]["PCrank"]["matrix"]
#|       C = Matrix([[1, 2, 3], [2, 4, 6]])
#|       expected_pivots = [Integer(j + 1) for j in C.rref()[1]]
#|       submitted_pivots = list(P)
#|       pivot_status = [
#|           i < len(expected_pivots) and value == expected_pivots[i]
#|           for i, value in enumerate(submitted_pivots)
#|       ]
#|       pivot_score = sum(pivot_status) / max(len(expected_pivots), len(submitted_pivots), 1)
#|       score = (int(rank_value == C.rank()) + pivot_score) / 2
#|       return {
#|           "score": score,
#|           "show_score": False,
#|           "feedback": "" if score == 1 else "Rangen er antall pivoter. Kontroller både rangverdien, antallet pivotindekser og rekkefølgen deres.",
#|           "assessment": {"PCrank": {"columns": pivot_status}},
#|       }

Finn rangen og pivotkolonnene til $C$:

$\operatorname{rank}(C)=$ _[1]

Pivotkolonner, én indeks per kolonne:

$P_C=$ mat{name=PCrank, rows=1, cols=auto, initial-cols=1, min-cols=0, max-cols=3}
```

```{math-exercise}
#| label: week3-paper-c-column-basis
#| caption: Basis for kolonnerommet til C
#| mode: custom
#| context: week3-paper-assessment-context
#| checker: |
#|   def check(response, symbols):
#|       Q = response["inputs"]["QC"]["matrix"]
#|       C = Matrix([[1, 2, 3], [2, 4, 6]])
#|       original_columns = [C[:, j] for j in range(C.cols)]
#|       result = assess_basis(
#|           Q,
#|           axis="columns",
#|           target_dimension=C.rank(),
#|           belongs=lambda vector: Q.rows == C.rows and any(vector == column for column in original_columns),
#|           name="QC",
#|           space_name="kolonnerommet til C",
#|       )
#|       statuses = result["assessment"]["QC"]["columns"]
#|       if result["score"] < 1:
#|           if "incorrect" in statuses:
#|               result["feedback"] = "En rød kolonne er null eller er ikke en kolonne fra den opprinnelige matrisen C."
#|           elif "dependent" in statuses:
#|               result["feedback"] = "De gule kolonnene kommer fra C, men familien er lineært avhengig. Fjern eller bytt kolonner."
#|           elif statuses:
#|               result["feedback"] = "De grønne kolonnene er tillatte og uavhengige, men de danner ennå ikke en basis for hele kolonnerommet."
#|           else:
#|               result["feedback"] = "Legg til kolonner fra den opprinnelige matrisen C."
#|       return result

Sett pivotkolonnene fra den opprinnelige matrisen $C$ inn som kolonner i en
basismatrise. Du må selv velge hvor mange kolonner som trengs:

$Q_C=$ mat{name=QC, rows=2, cols=auto, initial-cols=1, min-cols=0, max-cols=3}
```

```{math-exercise}
#| label: week3-paper-c-null-basis
#| caption: Basis for nullrommet til C
#| mode: custom
#| context: week3-paper-assessment-context
#| checker: |
#|   def check(response, symbols):
#|       Z = response["inputs"]["ZC"]["matrix"]
#|       C = Matrix([[1, 2, 3], [2, 4, 6]])
#|       result = assess_basis(
#|           Z,
#|           axis="columns",
#|           target_dimension=C.cols - C.rank(),
#|           belongs=lambda vector: Z.rows == C.cols and C * vector == zeros(C.rows, 1),
#|           name="ZC",
#|           space_name="nullrommet til C",
#|       )
#|       statuses = result["assessment"]["ZC"]["columns"]
#|       if result["score"] < 1:
#|           if "incorrect" in statuses:
#|               result["feedback"] = "En rød kolonne er null eller oppfyller ikke Cz=0."
#|           elif "dependent" in statuses:
#|               result["feedback"] = "De gule kolonnene ligger i nullrommet, men familien er lineært avhengig."
#|           elif statuses:
#|               result["feedback"] = "De grønne kolonnene er gyldige og uavhengige, men de spenner ennå ikke hele nullrommet."
#|           else:
#|               result["feedback"] = "Legg til basisvektorer for nullrommet."
#|       return result

Oppgi en basis for nullrommet til $C$, med én basisvektor per kolonne. Enhver
basis godtas, og du må selv velge antallet kolonner:

$Z_C=$ mat{name=ZC, rows=3, cols=auto, initial-cols=1, min-cols=0, max-cols=3}
```

```{math-exercise}
#| label: week3-paper-c-rank-nullity
#| caption: Rang–nullitet for C
#| mode: custom
#| partial-credit: true
#| field-labels: Inputdimensjon, Rang, Nullitet
#| context: week3-paper-assessment-context
#| checker: |
#|   def check(response, symbols):
#|       n, rank_value, nullity = response["expressions"]
#|       checks = [n == 3, rank_value == 1, nullity == 2, n == rank_value + nullity]
#|       return {"score": sum(int(value) for value in checks) / 4, "feedback": "Tell kolonnene, pivotene og de frie variablene, og kontroller deretter n = rang + nullitet."}

Fyll inn rang–nullitetsregnskapet for $C$:

inputdimensjon _[3] $=$ rang _[1] $+$ nullitet _[2]
```

### Med kode

Bruk denne delen først etter at du har arbeidet med den valgte matrisen på
papir. Cellen under inneholder en kort, selvstendig kopi av
`row_echelon`, slik at kontrolloppgaven virker selv om du ikke har åpnet og
kjørt kodecellen i matriserepetisjonen i 3.7.

1. Kontroller trappeformen og pivotkolonnene med `row_echelon`.
2. Kontroller nullromsvektorene ved å beregne `M @ Z`.
3. Lag to forskjellige inputer med samme output.
4. Finn én output som kan produseres, og én som ikke kan produseres.

```{pyodide-python}
#| label: week3-pure-matrix-exercises

import numpy as np

# Selvstendig hjelpekode: Cellen skal kunne kjøres uten kodecellene i 3.7.
def row_echelon(A,tol=1e-12):
    """Returner trappeform og indeksene til pivotkolonnene."""
    R=np.array(A,dtype=float,copy=True)
    rows,cols=R.shape
    pivot_row=0
    pivot_columns=[]

    for col in range(cols):
        if pivot_row==rows:
            break
        candidate=next(
            (row for row in range(pivot_row,rows) if abs(R[row,col])>tol),
            None,
        )
        if candidate is None:
            continue
        if candidate!=pivot_row:
            R[[pivot_row,candidate]]=R[[candidate,pivot_row]]
        for row in range(pivot_row+1,rows):
            R[row]-=(R[row,col]/R[pivot_row,col])*R[pivot_row]
        R[np.abs(R)<=tol]=0.0
        pivot_columns.append(col)
        pivot_row+=1

    return R,pivot_columns

B=np.array([[1.,0.,1.],
            [0.,1.,1.],
            [1.,1.,2.]])
C=np.array([[1.,2.,3.],
            [2.,4.,6.]])

# Studentvalg: Arbeid ferdig med B på papir og i kode før du bytter til C.
M=B
R_M,pivots_M=row_echelon(M)
print("Trappeform:\n",R_M)
print("Pivotkolonner:",[j+1 for j in pivots_M])

# TODO: Sett inn nullromsvektorene fra papirregningen som kolonner i Z_M.
# Kontrollen under skal da bli en nullmatrise.
Z_M=np.zeros((M.shape[1],0))
print("Kontroll M @ Z_M:\n",M@Z_M)

# TODO: Velg x0 og én kolonne z fra Z_M. Sammenlign M@x0 med M@(x0+z).

# TODO: Lag rhs_yes som M@x for en selvvalgt x. Lag deretter rhs_no som du
# mener ligger utenfor kolonnerommet. Sammenlign rang(M) med rang([M | rhs]).
```


:::
