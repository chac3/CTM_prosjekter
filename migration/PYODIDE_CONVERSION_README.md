# Converting migrated QMD code blocks to Pyodide

`qmd_python_to_pyodide.py` changes ordinary Quarto Python fences into runnable
Pyodide fences. It is deliberately separate from `ipynb_to_quarto.py`: first
perform a faithful structural migration, then decide which code should become
interactive.

## 1. Determine the engine name used by the installed extension

Inspect the working example from the extension or your colleague's repository.
Common possibilities are:

```text
pyodide-python
pyodide
pyodide-interaktiv
```

For the older `coatless-quarto/pyodide` extension, the common fence is:

````markdown
```{pyodide-python}
print("Hello")
```
````

Do not assume that the Erasmus-CTM extension uses exactly the same engine name.
Find one known-working interactive block and pass that name with `--engine`.

Useful local searches:

```bash
grep -RIn --include='*.qmd' '{pyodide' .
find _extensions -name '_extension.yml' -print
```

## 2. Install the tool

```bash
mkdir -p tools migration
cp qmd_python_to_pyodide.py tools/
chmod +x tools/qmd_python_to_pyodide.py
```

## 3. Test one project first

Dry run:

```bash
python3 tools/qmd_python_to_pyodide.py \
  projects-migrated/prosjekter-m1-jupyter/mekanikk1 \
  --engine pyodide-python \
  --dry-run
```

Convert one project, retain backups and add conservative live-cell options:

```bash
python3 tools/qmd_python_to_pyodide.py \
  projects-migrated/prosjekter-m1-jupyter/mekanikk1 \
  --engine pyodide-python \
  --backup \
  --editable \
  --run-button \
  --no-autorun
```

Then render and open that one page before changing the full tree.

## 4. Convert the complete migrated tree

```bash
python3 tools/qmd_python_to_pyodide.py \
  projects-migrated \
  --engine pyodide-python \
  --recursive \
  --backup \
  --editable \
  --run-button \
  --no-autorun \
  --report migration/pyodide-conversion.csv
```

## Incomplete student code

Cells containing `...`, `TODO`, `YOUR_CODE_HERE`, or `NotImplementedError` are
counted as incomplete. They are converted by default, but `autorun` is forced to
false. This lets students edit and run them without producing an immediate page
error.

To retain incomplete blocks as ordinary static Python blocks:

```bash
python3 tools/qmd_python_to_pyodide.py projects-migrated \
  --skip-incomplete
```

## Blocks skipped by default

The script does not convert blocks that appear to require:

- shell commands,
- local filesystem access,
- network access,
- package installation,
- Jupyter magic commands.

Pyodide runs in a browser and these patterns frequently require manual
rewriting. Use `--no-skip-unsafe` only after reviewing the report.

## What the script preserves

A fence such as:

````markdown
```{python .some-class #some-id}
#| label: example
print("Hello")
```
````

becomes:

````markdown
```{pyodide-python .some-class #some-id}
#| label: example
print("Hello")
```
````

Existing classes, identifiers and cell options are retained.

## Important limitation: shared state

Notebook cells often depend on imports and variables defined in earlier cells.
Whether that works depends on the installed Pyodide extension:

- Some extensions share one Python worker across all cells.
- Some isolate every cell.
- Some require a session or context option.

Test a page where a later cell uses `np` or a function defined in an earlier
cell. If state is isolated, either:

1. repeat required imports in each cell,
2. combine dependent cells,
3. use the extension's documented shared-session option,
4. add a hidden initialization block supported by the extension.

The conversion script cannot infer this safely for every notebook.

## Python package limitations

Pyodide supports many scientific packages, commonly including NumPy,
Matplotlib, pandas, SciPy and SymPy, but not every native Python package.
Further review is needed for notebooks using packages outside the WebAssembly
ecosystem or accessing local files.

## Reverting

If `--backup` was used, each changed file has a sibling such as:

```text
index.qmd.bak
```

Restore one file with:

```bash
mv index.qmd.bak index.qmd
```

For a Git-tracked tree, the cleaner rollback is often:

```bash
git restore projects-migrated
```

Always run the conversion on a dedicated branch:

```bash
git switch -c pyodide-migration
```
