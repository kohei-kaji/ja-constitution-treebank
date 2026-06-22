# UD_Japanese-Constitution

> [!WARNING]
> **WORK IN PROGRESS**

This repository provides [Universal Dependencies](https://universaldependencies.org) (UD) annotations for [the Constitution of Japan](https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/shiryo/dl-constitution.htm).

The text was first parsed automatically with [GiNZA](https://megagonlabs.github.io/ginza/) (via [spaCy](https://spacy.io/)) and then refined by manual correction using [ConlluEditor](https://github.com/Orange-OpenSource/conllueditor#parser-front-end) (Java required).

For background on the Universal Dependencies project, see the [UD official website](https://universaldependencies.org), [de Marneffe et al. (2021)](https://direct.mit.edu/coli/article/47/2/255/98516/Universal-Dependencies), and [Nivre et al. (2020)](https://aclanthology.org/2020.lrec-1.497/).
For the Japanese UD framework specifically, see [Asahara et al. (2018)](https://aclanthology.org/L18-1287/) and [浅原ら (2019)](https://www.jstage.jst.go.jp/article/jnlp/26/1/26_3/_article/-char/ja/).

## 📁 Repository Structure

```
.
├── data/                       # Source texts
│   ├── preamble.txt            # Japanese text of the preamble
│   ├── preamble-en.txt         # English translation of the preamble
│   └── constitution.txt        # Japanese text of the constitution
├── silver/                     # Automatically parsed data (silver standard)
│   ├── preamble-ginza.conllu
│   └── constitution-ginza.conllu
├── preamble-gold.conllu        # Manually corrected, gold-standard annotation
├── constitution-gold.conllu    # Manually corrected, gold-standard annotation
├── src/                        # Scripts
│   ├── depparse.py             # Runs GiNZA parsing, writes CoNLL-U
│   ├── parse.sh                # Convenience wrapper that runs depparse.py
│   └── generate_figures.py     # Renders dependency-tree visualizations
└── figure/                     # Generated visualizations
    ├── tex/                    # LaTeX sources (tikz-dependency)
    ├── pdf/                    # Compiled PDFs
    └── png/                    # Rasterized PNGs
```

## ⚙️ Project Workflow

1.  **Automated parsing**: `src/parse.sh` runs `src/depparse.py`, which uses GiNZA to parse each source text in `data/`. The output is written to `silver/` as silver-standard CoNLL-U (e.g. `silver/preamble-ginza.conllu`).
2.  **Manual annotation**: The silver data is manually corrected with ConlluEditor into the gold-standard files (`preamble-gold.conllu`, `constitution-gold.conllu`).
3.  **Visualization**: `src/generate_figures.py` reads the gold data and produces a dependency tree per sentence. Each tree is emitted as a LaTeX source (`figure/tex/`), compiled to PDF with `lualatex` (`figure/pdf/`), and rasterized to PNG with `pdftocairo` (`figure/png/`).
