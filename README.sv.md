# Latex API

## Beskrivning

Detta är ett API som körs tillsammans med ett statiskt frontend i en Docker-sandbox. Syftet med projektet är att erbjuda ett alternativ till tjänster som Overleaf för LaTeX-kompilering. Projektet är också kopplat till detta [CLI](https://github.com/fyrahundra/latex_cli).

## Innehåll

- [Installation](#installation)
- [Användning](#användning)
- [Funktioner](#funktioner)

## Installation

### Förkrav

- Linux, macOS eller Windows med WSL2
- [Docker](https://docs.docker.com/get-docker/) installerat och igång
- `make` tillgängligt i terminalen
- En ledig lokal port `8080`

### Steg-för-steg

1. Klona repot och gå till projektmappen:

```bash
git clone https://github.com/fyrahundra/latex_api.git
cd latex_api
```

2. Bygg Docker-imagen (utan cache):

```bash
make build
```

Valfritt: snabbare build med Docker-cache:

```bash
make build-cached
```

3. Kör API-containern:

```bash
make run
```

4. Öppna appen i webbläsaren (eller använd CLI):

```text
http://localhost:8080
```

5. Stoppa den körande containern när du är klar (ofta inte nödvändigt):

```bash
make stop
```

6. Ta bort containern helt (valfri städning):

```bash
make terminate
```

## Användning

### Webbfrontend

1. Starta containern:

```bash
make run
```

2. Öppna:

```text
http://localhost:8080
```

3. Ladda upp en `.zip` som innehåller ditt LaTeX-projekt och kompilera.

### API-endpoint

API:t exponerar en endpoint för kompilering:

- `POST /compile`

Exempel på request med `curl`:

```bash
curl -X POST \
	-F "file=@/path/to/project.zip" \
	http://localhost:8080/compile \
	--output output.pdf
```

Om kompileringen lyckas returneras en PDF-fil.

### Noteringar för ZIP-indata

- ZIP-filen måste innehalla minst en `.tex`-fil.
- Tjänsten prioriterar `garb.tex` om den finns.
- Max uppladdningsstorlek är 5 MB.

## Funktioner

- Docker-baserad körtid med LaTeX-verktygskedja inkluderad.
- Statiskt frontend som serveras på `/` för uppladdning och kompilering.
- API-baserad kompilering via `POST /compile`.
- Automatisk upptäckt av `.tex`-filer i uppladdade projekt.
- Valfri fallback-patchning av typsnittspaket i `.sty`-filer (för miljöer där `tgpagella` saknas).
- Använder `latexmk` för robust LaTeX-byggnad i flera pass.
- Returnerar kompileringsresultatet direkt som PDF-svar.
