# Inversion Corrections: Viola-Cello Voice Crossing

## Overview

This report documents corrections and remaining issues for harmony annotations where the viola crosses below the cello (temporarily becoming the lowest-sounding voice). In these cases, the inversion should be calculated relative to the viola's pitch, not the cello's.

A detection script is provided at [`scripts/check_inversions.py`](scripts/check_inversions.py):

```bash
python3 scripts/check_inversions.py
```

## Summary of Changes

**88 inversion annotations corrected** across 14 `.hrm` files. These were cases where the annotated inversion matched the cello's pitch class but not the actual bass (viola). 2 additional cases remain unfixed because the viola plays a non-chord tone.

| Category | Count |
|:---------|------:|
| Corrections applied | 88 |
| Remaining (viola not a chord tone) | 2 |
| Ambiguous (secondary dominants, etc.) | 30 |
| Already correct (no change needed) | 110 |
| Unparseable harmony label | 2 |
| **Total crossings detected** | **144** |

## Corrections Applied

### Op. 20 No. 1 — I. Allegro moderato (`op20n1-01.hrm`)

| Measure | Line | Old | New | Cello | Viola (bass) |
|:-------:|:----:|:---:|:---:|:-----:|:------------:|
| 7 | 92 | Vb | **V** | D4 | Bb3 |
| 9 | 110 | V7b/V | **V7/V** | A3 | F3 |
| 9 | 115 | Vb | **V** | D4 | Bb3 |
| 11 | 143 | Ib | **I** | G4 | Eb4 |
| 32 | 394 | V/V | **Vb/V** | F4 | A3 |
| 33 | 401 | V | **Vc** | Bb4 | F3 |
| 77 | 953 | Ib | **I** | G4 | Eb4 |

### Op. 20 No. 1 — II. Menuetto. Allegretto (`op20n1-02.hrm`)

| Measure | Line | Old | New | Cello | Viola (bass) |
|:-------:|:----:|:---:|:---:|:-----:|:------------:|
| 21 | 118 | V7c/IV | **V7b/IV** | F3 | D3 |
| 23 | 130 | V7c/IV | **V7b/IV** | F3 | D3 |

### Op. 20 No. 1 — III. Affettuoso e sostenuto (`op20n1-03.hrm`)

| Measure | Line | Old | New | Cello | Viola (bass) |
|:-------:|:----:|:---:|:---:|:-----:|:------------:|
| 20 | 101 | viio7/V | **viio7d/V** | D4 | C4 |
| 32 | 156 | V7b | **V7** | G3 | Eb3 |
| 33 | 159 | Ib | **Ic** | Ab3 | Eb3 |

### Op. 20 No. 2 — I. Moderato (`op20n2-01.hrm`)

| Measure | Line | Old | New | Cello | Viola (bass) |
|:-------:|:----:|:---:|:---:|:-----:|:------------:|
| 1 | 30 | V7c | **V7d** | D4 | F3 |
| 2 | 36 | Ib | **I** | E4 | C3 |
| 4 | 64 | IV | **IVc** | F4 | C3 |
| 5 | 73 | IV | **IVc** | F4 | C3 |
| 6 | 84 | Vc | **Vb** | D4 | B3 |
| 6 | 88 | Ib | **I** | E4 | C4 |
| 6 | 90 | Vb/V | **Vc/V** | F#4 | A3 |
| 49 | 616 | V7b/v | **V7/v** | C#4 | A3 |
| 51 | 650 | V7b | **V7d** | F#4 | C4 |
| 53 | 684 | vi | **vic** | G4 | B3 |
| 57 | 752 | vb | **vc** | F4 | A3 |

### Op. 20 No. 2 — IV. Fuga a 4 soggetti (`op20n2-04.hrm`)

| Measure | Line | Old | New | Cello | Viola (bass) |
|:-------:|:----:|:---:|:---:|:-----:|:------------:|
| 44 | 375 | V7b | **V7d** | C#4 | G3 |
| 44 | 378 | i | **ib** | D4 | F3 |
| 44 | 381 | ivb | **ivc** | Bb3 | D3 |
| 45 | 383 | V7 | **V7b** | A3 | C#3 |
| 57 | 483 | viioc | **viiob** | G3 | E3 |
| 57 | 485 | V7c/IV | **V7b/IV** | A3 | F#3 |
| 94 | 790 | viio/IV | **viiob/IV** | E4 | G3 |
| 95 | 793 | V7c/IV | **V7b/IV** | G4 | E3 |
| 140 | 1191 | Vb | **V** | B3 | D3 |

### Op. 20 No. 3 — III. Poco adagio (`op20n3-03.hrm`)

| Measure | Line | Old | New | Cello | Viola (bass) |
|:-------:|:----:|:---:|:---:|:-----:|:------------:|
| 19 | 176 | Vc | **V** | A3 | D3 |
| 21 | 202 | Vc | **V** | A3 | D3 |
| 36 | 378 | IVc | **IV** | D5 | G4 |
| 36 | 382 | I | **Ib** | D5 | F#4 |
| 37 | 391 | IVc | **IV** | D5 | G4 |
| 37 | 395 | I | **Ib** | D5 | F#4 |
| 52 | 526 | V7 | **V7b** | E4 | Ab3 |
| 52 | 530 | ib | **i** | C4 | A3 |
| 53 | 532 | ivb | **iv** | F4 | D3 |
| 53 | 533 | ic | **ib** | E4 | C3 |
| 54 | 539 | Vc | **V** | B3 | E3 |
| 54 | 542 | ib | **i** | C4 | A3 |
| 106 | 1172 | IVc | **IV** | G4 | C4 |
| 106 | 1176 | I | **Ib** | G4 | B3 |
| 107 | 1185 | IVc | **IV** | G4 | C4 |
| 107 | 1189 | I | **Ib** | G4 | B3 |

### Op. 20 No. 3 — IV. Finale. Allegro molto (`op20n3-04.hrm`)

| Measure | Line | Old | New | Cello | Viola (bass) |
|:-------:|:----:|:---:|:---:|:-----:|:------------:|
| 2 | 35 | ib | **i** | Bb3 | G3 |
| 21 | 222 | Ib | **I** | D4 | Bb3 |
| 21 | 228 | IV | **IVc** | Eb4 | Bb3 |
| 72 | 702 | ib | **i** | Bb3 | G3 |

### Op. 20 No. 4 — I. Allegro di molto (`op20n4-01.hrm`)

| Measure | Line | Old | New | Cello | Viola (bass) |
|:-------:|:----:|:---:|:---:|:-----:|:------------:|
| 237 | 1330 | V7d | **V7** | D4 | E3 |
| 237 | 1336 | Ib | **Ic** | F#4 | E3 |

### Op. 20 No. 4 — II. Un poco adagio e affettuoso (`op20n4-02.hrm`)

| Measure | Line | Old | New | Cello | Viola (bass) |
|:-------:|:----:|:---:|:---:|:-----:|:------------:|
| 37 | 327 | viio | **viiob** | C#4 | E3 |
| 38 | 330 | viioD7d | **viioD7c** | Bb3 | G3 |
| 38 | 331 | ic | **ib** | A3 | F3 |
| 38 | 335 | V7 | **V7d** | A3 | G3 |
| 45 | 398 | ivb | **iv** | Bb3 | G3 |
| 48 | 419 | i | **ic** | D4 | A3 |
| 48 | 422 | Vb | **V** | C#4 | A3 |
| 53 | 464 | V7b | **V7** | E4 | A3 |
| 108 | 905 | V7b | **V7** | C#4 | A3 |
| 109 | 912 | i | **ic** | D4 | A3 |
| 112 | 940 | V7b | **V7** | C#4 | A3 |
| 112 | 941 | i | **ic** | D4 | A3 |

### Op. 20 No. 4 — III. Menuet alla Zingarese & Trio (`op20n4-03.hrm`)

| Measure | Line | Old | New | Cello | Viola (bass) |
|:-------:|:----:|:---:|:---:|:-----:|:------------:|
| 31 | 194 | Ib | **Ic** | F#4 | A3 |
| 32 | 197 | Vb | **V** | C#4 | A3 |

### Op. 20 No. 4 — IV. Presto e scherzando (`op20n4-04.hrm`)

| Measure | Line | Old | New | Cello | Viola (bass) |
|:-------:|:----:|:---:|:---:|:-----:|:------------:|
| 16 | 158 | Vb | **V** | C#4 | A3 |
| 16 | 160 | V7b | **V7** | C#4 | A3 |
| 16 | 161 | i | **ic** | D4 | A3 |
| 57 | 630 | V7d | **V7b** | E4 | Bb3 |
| 116 | 1297 | I | **Ib** | D4 | F#3 |

### Op. 20 No. 5 — III. Adagio (`op20n5-03.hrm`)

| Measure | Line | Old | New | Cello | Viola (bass) |
|:-------:|:----:|:---:|:---:|:-----:|:------------:|
| 83 | 988 | V7 | **V7d** | C4 | Bb3 |

### Op. 20 No. 5 — IV. Finale. Fuga a due soggetti (`op20n5-04.hrm`)

| Measure | Line | Old | New | Cello | Viola (bass) |
|:-------:|:----:|:---:|:---:|:-----:|:------------:|
| 77 | 495 | V7d/v | **V7c/v** | Eb4 | C4 |
| 119 | 754 | V7d/V | **V7b/V** | F4 | B3 |
| 120 | 757 | Vc | **V** | F4 | C4 |
| 120 | 760 | Vb | **V** | E4 | C4 |

### Op. 20 No. 6 — I. Allegro di molto e scherzando (`op20n6-01.hrm`)

| Measure | Line | Old | New | Cello | Viola (bass) |
|:-------:|:----:|:---:|:---:|:-----:|:------------:|
| 2 | 38 | I | **Ic** | A3 | E3 |
| 6 | 70 | I | **Ic** | A3 | E3 |
| 12 | 129 | I | **Ic** | A3 | E3 |
| 110 | 985 | I | **Ic** | A3 | E3 |
| 114 | 1018 | i | **ic** | A3 | E3 |
| 127 | 1148 | V7 | **V7c** | D4 | B3 |
| 127 | 1150 | V7 | **V7c** | D4 | B3 |
| 128 | 1153 | V7 | **V7c** | D4 | B3 |
| 128 | 1155 | V7 | **V7c** | D4 | B3 |
| 128 | 1157 | V7 | **V7c** | D4 | B3 |

## Remaining Unfixed Cases

These 2 cases have the viola lower than the cello, but the viola's pitch class is not a chord tone, so the correct inversion cannot be determined automatically:

| File | Measure | Line | Annotation | Cello | Viola | Reason |
|:-----|:-------:|:----:|:----------:|:-----:|:-----:|:-------|
| op20n2-04.hrm | 44 | 379 | viioD7d | Bb3 | F3 | F not in C#-E-G-Bb |
| op20n4-01.hrm | 54 | 309 | V7d | D4 | C#4 | C# not in E-G#-B-D |
