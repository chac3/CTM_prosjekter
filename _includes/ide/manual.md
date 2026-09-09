::: {.panel-tabset}

## IDE

### Python direkte i nettleseren

Mini-IDE-en kjører Python lokalt i nettleseren ved hjelp av [Pyodide](https://pyodide.org/). Du trenger derfor ikke installere Python for å prøve eksemplene. Første oppstart kan ta litt tid mens Python og nødvendige pakker lastes inn.

### Kom raskt i gang

1. Skriv eller endre kode i et kodevindu.
2. Velg **Run Code** for å kjøre vinduet.
3. Les utskrift, feilmeldinger og figurer under kodevinduet.
4. Velg **+ Code block** når du vil ha et tomt arbeidsvindu.
5. Bruk **Restart** hvis du vil nullstille Python-miljøet på siden.

Prøv gjerne dette eksemplet:

```{pyodide-python}
import numpy as np
import matplotlib.pyplot as plt

plt.close("all")

x = np.linspace(0, 2*np.pi, 200)
y = np.sin(x)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x, y)
ax.set_xlabel("x")
ax.set_ylabel("sin(x)")
ax.set_title("En enkel sinuskurve")
ax.grid(True)

plt.show()
```

### Slik fungerer arbeidsmiljøet

Alle kodevinduer på **samme side** deler variabler, funksjoner og importer. Kjør derfor celler i naturlig rekkefølge når en celle bygger på en tidligere celle. (En **side** i konteksten av denne ressursen er en HTML-side. Hver pensumuke ligger på egen side med alle sine faner og underfaner.)

Python-miljøet deles ikke mellom ulike sider, og det opprettes på nytt når du laster inn siden eller velger **Restart**. Hver ukeside har en skjult oppstartscelle som laster inn nødvendige biblioteker og felles definisjoner. Hvis du senere kjører en synlig, endret versjon av en funksjon, brukes den endrede versjonen resten av økten.

::: {.callout-warning title="Ta vare på arbeidet ditt"}

Koden lagres ikke automatisk. Kopier kode du vil beholde til en lokal fil, VS Code eller et annet egnet sted før du lukker eller laster inn siden på nytt.
:::

### Når noe ikke virker

- Les den siste linjen i feilmeldingen først; den beskriver ofte hovedproblemet.
- Kontroller at cellene som definerer variabler og funksjoner, er kjørt.
- Kjør cellen på nytt etter at du har rettet koden.
- Få evt KI-hjelp ved å trykke på Feedback-knappen.
- Velg **Restart** og kjør nødvendige celler på nytt hvis miljøet har fått en uklar tilstand.
- Last inn hele nettsiden på nytt hvis knappene eller Python-miljøet har stoppet.

## README

### KI-feedback

#### Hvordan få KI-tilbakemeldingen?

Kode- og matematikkoppgaver kan ha en **Feedback**-knapp. Når du trykker på denne knappen, så sendes ditt input til en LLM som skal først trekke fram det som allerede er riktig, før den peker mot det neste du bør undersøke. 

I matematikkoppgavene blir hjelpen gradvis tydeligere:

1. **Lite hint:** et spørsmål eller et tips som hjelper deg å finne neste steg.
2. **Større hint:** forklaring av det relevante begrepet eller sammenhengen.
3. **Framgangsmåte:** en strukturert metode, men uten at oppgaven regnes helt ut for deg.
4. **Gjennomarbeidet løsning:** en full utregning når flere forsøk ikke har ført fram.

Forsøksnummeret gjelder tilbakemeldingen for den aktuelle oppgaven. Tilbakemeldingen erstatter ikke egen kontroll: språkmodeller kan misforstå oppgavetekst, notasjon eller tall. Sammenlign derfor rådene med definisjonene og eksemplene på siden, særlig hvis noe virker selvmotsigende.

#### Koble til NTNUs modell-tjeneste

Tilbakemeldingen bruker språkmodeller på NTNUs HPC-infrastruktur (IDUN) og krever en personlig API-nøkkel. Se [LLM API service and gpt.ntnu.no – IDUN documentation](https://www.hpc.ntnu.no/idun/documentation/ai-coding-assistant-and-large-language-models-llms-on-idun/) for tilgang og oppdaterte tjenesteinnstillinger.

Når du har fått nøkkelen:

1. Trykk på **tannhjulikonet** ved tilbakemeldingsknappen.
2. Fyll inn base-URL og modell slik IDUN-dokumentasjonen angir.
3. Lim inn nøkkelen i **API key** og lagre.
4. Velg modellen. (Prøv først uten reasoning, feks Kimi2.6-instant.) Lagre.
4. Send inn et svar med **Check**, og velg deretter **Feedback**.

::: {.callout-important title="Beskytt API-nøkkelen"}

Ikke skriv nøkkelen i Python-kode, del den med andre eller legg den i Git. Fjern den når du er ferdig hvis du bruker en delt datamaskin.
:::

#### Få mest mulig ut av tilbakemeldingen

- Send inn et svar som du har fått selv; da kan modellen kommentere det du faktisk har gjort. 
- Bruk hintet til å endre svaret før du ber om neste nivå.
- Kontroller at du svarer i formatet oppgaven ber om, for eksempel brøk, desimaltall eller bitstreng.
- Rapporter til faglærer dersom tilbakemeldingen bruker feil forutsetninger eller avslører løsningen for tidlig. 

### Problemer og forbedringsforslag

Åpne helst en [sak på GitHub](https://github.com/aacchhee/ingmat3a_ntnu/issues) med sidenavn, oppgave, hva du gjorde, og hva du forventet skulle skje. Skjermbilde og nettlesernavn er nyttig ved visningsproblemer. Du kan også rette problemet i en fork og sende en pull request.

Hvis du ikke kan bruke GitHub, kan du sende e-post til <andrey.chesnokov@ntnu.no>.

:::
