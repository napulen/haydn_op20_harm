# Potential Inversion Errors: Viola-Cello Voice Crossing

## Overview

This report documents instances where the viola crosses below the cello (temporarily becoming the lowest-sounding voice) and the annotated chord inversion may be incorrect. The inversion was likely calculated based on the cello's pitch instead of the actual bass note in the viola.

A detection script is provided at [`scripts/check_inversions.py`](scripts/check_inversions.py) and can be re-run at any time:

```bash
python3 scripts/check_inversions.py
```

## Methodology

For each `.hrm` file, the script:
1. Tracks the current sounding pitch of the cello (3rd data column, `*clefF4`) and viola (4th data column, `*clefC3`)
2. At every new harmony annotation onset, checks whether the viola pitch is lower than the cello pitch
3. If so, computes the expected chord tones from the Roman numeral and current key
4. Compares the annotated inversion's expected bass pitch class against both the cello and viola pitch classes

Each flagged instance is categorized as:
- **LIKELY ERROR**: The annotated inversion's expected bass note matches the cello, but the viola (actual bass) has a different pitch class
- **OK**: The inversion correctly reflects the viola as bass
- **AMBIGUOUS**: The expected bass matches neither voice exactly (often secondary dominants or complex harmonies)

## Likely Inversion Errors (69 instances)

These are the strongest candidates for correction. In each case, the annotated inversion matches the cello's pitch class, but the viola is actually lower.

### Op. 20 No. 1 — I. Allegro moderato (`op20n1-01.hrm`)

| Measure | Line | Annotation | Inversion | Cello | Viola (actual bass) | Notes |
|---------|------|-----------|-----------|-------|-------------------|-------|
| 7 | 92 | Vb | b (1st inv.) | D4 | Bb3 | Bb=root of V in Eb, should be V (root pos.) |
| 9 | 115 | Vb | b (1st inv.) | D4 | Bb3 | Same pattern |
| 11 | 143 | Ib | b (1st inv.) | G4 | Eb4 | Eb=root of I in Eb, should be I (root pos.) |
| 33 | 401 | V | root | Bb4 | F3 | F=5th of V in Eb, should be Vc (2nd inv.) |
| 77 | 953 | Ib | b (1st inv.) | G4 | Eb4 | Recapitulation of m.11 pattern |

### Op. 20 No. 2 — I. Moderato (`op20n2-01.hrm`)

| Measure | Line | Annotation | Inversion | Cello | Viola (actual bass) | Notes |
|---------|------|-----------|-----------|-------|-------------------|-------|
| 1 | 30 | V7c | c (2nd inv.) | D4 | F3 | F=7th of V7 in C, should be V7d (3rd inv.) |
| 2 | 36 | Ib | b (1st inv.) | E4 | C3 | C=root of I in C, should be I (root pos.) |
| 4 | 64 | IV | root | F4 | C3 | C=5th of IV in C, should be IVc (2nd inv.) |
| 5 | 73 | IV | root | F4 | C3 | Same pattern |
| 6 | 84 | Vc | c (2nd inv.) | D4 | B3 | B=3rd of V in C, should be Vb (1st inv.) |
| 6 | 88 | Ib | b (1st inv.) | E4 | C4 | C=root of I in C, should be I (root pos.) |
| 51 | 650 | V7b | b (1st inv.) | F#4 | C4 | In G:, C=7th of V7, should be V7d |
| 57 | 752 | vb | b (1st inv.) | F4 | A3 | In G:, A=5th of v, should be vc (2nd inv.) |
| 84 | 1060 | IV | root | F3 | C3 | Recapitulation, same as m.4 |

### Op. 20 No. 2 — IV. Fuga a 4 soggetti (`op20n2-04.hrm`)

| Measure | Line | Annotation | Inversion | Cello | Viola (actual bass) |
|---------|------|-----------|-----------|-------|-------------------|
| 44 | 375 | V7b | b (1st inv.) | C#4 | G3 |
| 44 | 378 | i | root | D4 | F3 |
| 44 | 379 | viioD7d | d (3rd inv.) | Bb3 | F3 |
| 44 | 381 | ivb | b (1st inv.) | Bb3 | D3 |
| 45 | 383 | V7 | root | A3 | C#3 |
| 57 | 483 | viioc | c (2nd inv.) | G3 | E3 |
| 78 | 668 | I | root | G4 | F#4 |

### Op. 20 No. 3 — III. Poco adagio (`op20n3-03.hrm`)

| Measure | Line | Annotation | Inversion | Cello | Viola (actual bass) |
|---------|------|-----------|-----------|-------|-------------------|
| 19 | 176 | Vc | c (2nd inv.) | A3 | D3 |
| 21 | 202 | Vc | c (2nd inv.) | A3 | D3 |
| 36 | 378 | IVc | c (2nd inv.) | D5 | G4 |
| 36 | 382 | I | root | D5 | F#4 |
| 37 | 391 | IVc | c (2nd inv.) | D5 | G4 |
| 37 | 395 | I | root | D5 | F#4 |
| 52 | 526 | V7 | root | E4 | Ab3 |
| 52 | 530 | ib | b (1st inv.) | C4 | A3 |
| 53 | 532 | ivb | b (1st inv.) | F4 | D3 |
| 53 | 533 | ic | c (2nd inv.) | E4 | C3 |
| 54 | 539 | Vc | c (2nd inv.) | B3 | E3 |
| 54 | 542 | ib | b (1st inv.) | C4 | A3 |
| 106 | 1172 | IVc | c (2nd inv.) | G4 | C4 |
| 106 | 1176 | I | root | G4 | B3 |
| 107 | 1185 | IVc | c (2nd inv.) | G4 | C4 |
| 107 | 1189 | I | root | G4 | B3 |

### Op. 20 No. 3 — IV. Finale. Allegro molto (`op20n3-04.hrm`)

| Measure | Line | Annotation | Inversion | Cello | Viola (actual bass) |
|---------|------|-----------|-----------|-------|-------------------|
| 2 | 35 | ib | b (1st inv.) | Bb3 | G3 |
| 6 | 76 | V7d | d (3rd inv.) | C4 | G3 |
| 21 | 222 | Ib | b (1st inv.) | D4 | Bb3 |
| 21 | 228 | IV | root | Eb4 | Bb3 |
| 72 | 702 | ib | b (1st inv.) | Bb3 | G3 |

### Op. 20 No. 4 — I. Allegro di molto (`op20n4-01.hrm`)

| Measure | Line | Annotation | Inversion | Cello | Viola (actual bass) |
|---------|------|-----------|-----------|-------|-------------------|
| 54 | 309 | V7d | d (3rd inv.) | D4 | C#4 |
| 184 | 1107 | Vc | c (2nd inv.) | C#4 | B3 |

### Op. 20 No. 4 — II. Un poco adagio e affettuoso (`op20n4-02.hrm`)

| Measure | Line | Annotation | Inversion | Cello | Viola (actual bass) |
|---------|------|-----------|-----------|-------|-------------------|
| 37 | 327 | viio | root | C#4 | E3 |
| 38 | 330 | viioD7d | d (3rd inv.) | Bb3 | G3 |
| 38 | 331 | ic | c (2nd inv.) | A3 | F3 |
| 38 | 335 | V7 | root | A3 | G3 |
| 45 | 398 | ivb | b (1st inv.) | Bb3 | G3 |
| 48 | 419 | i | root | D4 | A3 |
| 48 | 422 | Vb | b (1st inv.) | C#4 | A3 |
| 108 | 905 | V7b | b (1st inv.) | C#4 | A3 |
| 109 | 912 | i | root | D4 | A3 |
| 112 | 940 | V7b | b (1st inv.) | C#4 | A3 |
| 112 | 941 | i | root | D4 | A3 |

### Op. 20 No. 4 — III. Menuet alla Zingarese & Trio (`op20n4-03.hrm`)

| Measure | Line | Annotation | Inversion | Cello | Viola (actual bass) |
|---------|------|-----------|-----------|-------|-------------------|
| 31 | 194 | Ib | b (1st inv.) | F#4 | A3 |
| 32 | 197 | Vb | b (1st inv.) | C#4 | A3 |

### Op. 20 No. 4 — IV. Presto e scherzando (`op20n4-04.hrm`)

| Measure | Line | Annotation | Inversion | Cello | Viola (actual bass) |
|---------|------|-----------|-----------|-------|-------------------|
| 16 | 158 | Vb | b (1st inv.) | C#4 | A3 |
| 16 | 160 | V7b | b (1st inv.) | C#4 | A3 |
| 16 | 161 | i | root | D4 | A3 |
| 57 | 630 | V7d | d (3rd inv.) | E4 | Bb3 |
| 116 | 1297 | I | root | D4 | F#3 |

### Op. 20 No. 5 — III. Adagio (`op20n5-03.hrm`)

| Measure | Line | Annotation | Inversion | Cello | Viola (actual bass) |
|---------|------|-----------|-----------|-------|-------------------|
| 83 | 988 | V7 | root | C4 | Bb3 |

### Op. 20 No. 5 — IV. Finale. Fuga a due soggetti (`op20n5-04.hrm`)

| Measure | Line | Annotation | Inversion | Cello | Viola (actual bass) |
|---------|------|-----------|-----------|-------|-------------------|
| 120 | 760 | Vb | b (1st inv.) | E4 | C4 |

### Op. 20 No. 6 — I. Allegro di molto e scherzando (`op20n6-01.hrm`)

| Measure | Line | Annotation | Inversion | Cello | Viola (actual bass) |
|---------|------|-----------|-----------|-------|-------------------|
| 2 | 38 | I | root | A3 | E3 |
| 6 | 70 | I | root | A3 | E3 |
| 12 | 129 | I | root | A3 | E3 |
| 110 | 985 | I | root | A3 | E3 |
| 114 | 1018 | i | root | A3 | E3 |

## Summary Statistics

| Category | Count | Description |
|----------|-------|-------------|
| **Likely errors** | **69** | Inversion matches cello but not the actual bass (viola) |
| Correct | 35 | Inversion correctly reflects viola as bass |
| Ambiguous | 44 | Could not confirm (secondary harmonies, complex chords) |
| Other | 2 | Harmony label not fully parseable |
| **Total crossings** | **150** | All points where viola is lower than cello at a harmony onset |

## Distribution by Quartet

| File | Likely Errors |
|------|:---:|
| Op.20 No.1, Mvt.I | 5 |
| Op.20 No.2, Mvt.I | 9 |
| Op.20 No.2, Mvt.IV | 7 |
| Op.20 No.3, Mvt.III | 16 |
| Op.20 No.3, Mvt.IV | 5 |
| Op.20 No.4, Mvt.I | 2 |
| Op.20 No.4, Mvt.II | 11 |
| Op.20 No.4, Mvt.III | 2 |
| Op.20 No.4, Mvt.IV | 5 |
| Op.20 No.5, Mvt.III | 1 |
| Op.20 No.5, Mvt.IV | 1 |
| Op.20 No.6, Mvt.I | 5 |
