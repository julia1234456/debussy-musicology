# Debussy & Gamelan — HPCP Analysis

Legend says that Debussy was inspired by Gamelan music. Is it a pure marketing myth, at the time were exoticism was in vogue in the 19th century, or does his compositions genuinely incorporate elements that reflect the aesthetics of Gamelan? 

---

## Overview

This project investigates whether Claude Debussy's compositions show measurable tonal similarities to Javanese Gamelan music. It does so by computing **Harmonic Pitch Class Profiles (HPCPs)**, that display the relative energy of each pitch class in a recording — and then comparing these profiles across three groups:

- **Gamelan recordings** (reference corpus)
- **Pre-Gamelan Debussy works** (composed before his 1889 exposure)
- **Post-Gamelan Debussy works**, with particular attention to pieces explicitly cited as Gamelan-inspired (*Pagodes*, *Sirènes*)

Statistical comparisons (Pearson, Spearman, KL divergence) are used to test whether post-Gamelan and Gamelan-inspired Debussy pieces show a measurably closer tonal profile to Gamelan music than his earlier work does.

---

## Repository Structure

```
.
├── data/
│   ├── A440.mp3                        # Reference pitch for tuning validation
│   ├── A432.mp3                        # Off-tune reference for tuning correction test
│   ├── ChromaticScaleUpDown.mp3        # 12-semitone scale for HPCP reliability tests
│   ├── recordings_debussy/             # Debussy piano recordings (.mp3)
│   ├── recordings_gamelan/             # Gamelan recordings (.mp3)
│   └── debussy_piece_metadata_modified.csv   # Piece metadata with Gamelan-relation labels
│
├── scripts/
|   ├── download_data.py  
|   ├── extract_onset.py  
│   ├── hpcp.py                         # Core HPCP computation and audio loading
│   └── statistics.py                   # Pairwise statistical comparison matrix
│
├── Complete_HPCP_Analysis.ipynb       
└── README.md
```

---

## Methodology

### 1. Audio Loading & Preprocessing (`scripts/hpcp.py`)

Each recording is loaded with `librosa`, trimmed of leading/trailing silence, and its **tuning deviation** from A=440 Hz is estimated using a reassigned spectrogram. This tuning offset is then fed into the HPCP computation to correct for recordings that are not tuned to standard Western pitch.

### 2. HPCP Computation

The HPCP is computed in two steps:

1. **Constant-Q Transform (CQT):** captures harmonic energy across 7 octaves at configurable frequency resolution.
2. **Chroma projection:** folds the CQT energy into pitch-class bins. The chroma-gram is then averaged over time to produce a single summary vector.

Two resolutions are used throughout the analysis:

| Resolution | Bins per semitone | Total bins | Use case |
|---|---|---|---|
| Standard | 1 | 12 | Quick overview, Western music |
| High | 10 | 120 | Microtonal structure, Gamelan |

The high-resolution setting is key: at 12 bins, Gamelan's pentatonic/heptatonic scale cannot be distinguished from the Western 12-tone system, since its pitches fall between Western semitones. At 120 bins, the distinct peaks of Gamelan scales become clearly visible.

### 3. Reliability Tests

Before running the main analysis, the HPCP method is validated on three controlled signals:

- **A440** — verifies that the dominant peak lands on the correct pitch class.
- **A432** — verifies that tuning correction maps an off-tune A to the same pitch class as A440.
- **Chromatic scale** — verifies that all 12 pitch classes contribute equally when all semitones are played.

### 4. Statistical Comparison (`scripts/statistics.py`)

Pairwise comparisons between HPCP vectors are computed using three tests, each capturing a different aspect of similarity:

| Test | What it measures |
|---|---|
| **Pearson correlation** | Linear relationship between pitch distributions |
| **Spearman correlation** | Monotonic relationship (rank-based, more robust) |
| **KL divergence** | Information-theoretic distance between distributions |

Results are displayed as annotated heatmaps. Cells can be filtered to show only statistically significant comparisons (configurable `alpha`, default 10%).

### 5. Analysis Progression

The notebook proceeds from individual pieces to dataset-wide comparisons:

1. **Single-piece exploration** — visual comparison of *Pagodes*, *Sirènes*, *Nocturne*, and individual Gamelan pieces.
2. **Pairwise statistics** — 3×4 matrix comparing Debussy pieces against each Gamelan recording.
3. **Full dataset** — pre-Gamelan vs. Gamelan corpus, and post-Gamelan vs. Gamelan corpus.
4. **Representative aggregation** — mean HPCP vectors for each category are computed and compared, giving a single summary correlation between groups.

---

## Key Findings

- At **12-bin resolution**, Gamelan pieces appear indistinguishable from Western music — their pentatonic scale is invisible because its pitches fall between Western semitones.
- At **120-bin resolution**, Gamelan pieces reveal clearly distinct, sparse peak structures (typically 5 peaks), while Western Debussy works show 12 evenly distributed peaks.
- **Debussy's *Pagodes*** shows a notably sparse pitch distribution reminiscent of a hexatonic scale, aligning more closely with Gamelan's reduced pitch set than with the *Nocturne*.
- **Debussy's *Sirènes*** is more ambiguous: it retains 12 pitch classes but shows reduced tonal hierarchy — no strong tonic/dominant emphasis — which may reflect Gamelan influence at the structural rather than scalar level.
- The Pearson/Spearman matrices between Gamelan-inspired pieces and Gamelan recordings show **positive correlations for *Pagodes* and *Sirènes***, though the picture is complicated by internal diversity within the Gamelan corpus itself.
- The aggregated representative comparison (mean HPCP per group) provides the clearest summary: post-Gamelan Debussy is measurably closer to the Gamelan profile than pre-Gamelan Debussy.

---

## Dependencies

```
librosa
numpy
matplotlib
scipy
pandas
```

Install with:

```bash
pip install librosa numpy matplotlib scipy pandas
```

---

## References

- Gómez, E. (2006). *Tonal description of music audio signals.* PhD thesis, Universitat Pompeu Fabra.
- McFee, B. et al. *librosa: Audio and Music Signal Analysis in Python.* Proceedings of SciPy, 2015.
- *Echoes of the East* — musicological source referenced in the notebook for identifying Gamelan-inspired Debussy works.
- DCMLab Debussy Piano Dataset: [github.com/DCMLab/debussy_piano](https://github.com/DCMLab/debussy_piano)
