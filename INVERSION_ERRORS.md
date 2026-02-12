# Potential Inversion Errors: Viola-Cello Voice Crossing

## Overview

This report documents all instances where the viola crosses below the cello (temporarily becoming the lowest-sounding voice) at the onset of a harmony annotation. Each case is assigned a confidence level indicating whether the annotated inversion is likely wrong.

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

### Confidence levels

- 🔴 **High** — The annotated inversion's expected bass matches the cello's pitch class, but the viola (actual bass) has a *different* pitch class. The annotator almost certainly based the inversion on the cello rather than the true bass.
- 🟡 **Medium** — The expected bass matches neither the cello nor the viola exactly. This typically involves secondary dominants, applied chords, or enharmonic ambiguity where the script's chord-tone computation may not fully resolve.
- 🟢 **Low (OK)** — The annotated inversion already correctly reflects the viola as the bass, or the viola doubles the cello at the octave. No correction needed.

---

## All Flagged Cases by Movement

### Op. 20 No. 1 — I. Allegro moderato (`op20n1-01.hrm`)

| Measure | Line | Annotation | Cello | Viola (bass) | Confidence | Explanation |
|:-------:|:----:|:----------:|:-----:|:------------:|:----------:|:------------|
| 7 | 92 | Vb | D4 | Bb3 | 🔴 High | Bb=root of V in Eb; should be **V** (root pos.) |
| 9 | 110 | V7b/V | A3 | F3 | 🟡 Medium | Secondary dominant; bass matches neither computed tone exactly |
| 9 | 115 | Vb | D4 | Bb3 | 🔴 High | Same as m.7 |
| 11 | 143 | Ib | G4 | Eb4 | 🔴 High | Eb=root of I in Eb; should be **I** (root pos.) |
| 32 | 394 | V/V | F4 | A3 | 🟡 Medium | Secondary dominant |
| 33 | 401 | V | Bb4 | F3 | 🔴 High | F=5th of V in Eb; should be **Vc** (2nd inv.) |
| 63 | 803 | vi | Eb4 | C3 | 🟢 Low | C=root of vi in Eb; annotation correct |
| 77 | 953 | Ib | G4 | Eb4 | 🔴 High | Recapitulation of m.11 |
| 109 | 1354 | viiob | F#3 | F3 | 🟢 Low | Annotation matches actual bass |

### Op. 20 No. 1 — II. Menuetto. Allegretto (`op20n1-02.hrm`)

| Measure | Line | Annotation | Cello | Viola (bass) | Confidence | Explanation |
|:-------:|:----:|:----------:|:-----:|:------------:|:----------:|:------------|
| 21 | 118 | V7c/IV | F3 | D3 | 🟡 Medium | Secondary dominant of IV |
| 23 | 130 | V7c/IV | F3 | D3 | 🟡 Medium | Same pattern as m.21 |

### Op. 20 No. 1 — III. Affettuoso e sostenuto (`op20n1-03.hrm`)

| Measure | Line | Annotation | Cello | Viola (bass) | Confidence | Explanation |
|:-------:|:----:|:----------:|:-----:|:------------:|:----------:|:------------|
| 20 | 101 | viio7/V | D4 | C4 | 🟡 Medium | Applied chord |
| 21 | 105 | IM7 | C4 | Ab3 | 🟢 Low | Ab=root of I in Ab (or 7th); annotation correct |
| 33 | 159 | Ib | Ab3 | Eb3 | 🟡 Medium | Eb=root of I in Eb, but script classified ambiguous |

### Op. 20 No. 2 — I. Moderato (`op20n2-01.hrm`)

| Measure | Line | Annotation | Cello | Viola (bass) | Confidence | Explanation |
|:-------:|:----:|:----------:|:-----:|:------------:|:----------:|:------------|
| 1 | 30 | V7c | D4 | F3 | 🔴 High | F=7th of V7 in C; should be **V7d** (3rd inv.) |
| 2 | 36 | Ib | E4 | C3 | 🔴 High | C=root of I in C; should be **I** (root pos.) |
| 3 | 57 | V | E4 | G3 | 🟢 Low | G=root of V in C; annotation correct |
| 4 | 60 | I | C4 | C3 | 🟢 Low | Root doubling at octave; annotation correct |
| 4 | 64 | IV | F4 | C3 | 🔴 High | C=5th of IV in C; should be **IVc** (2nd inv.) |
| 5 | 69 | V7/IV | C4 | C3 | 🟡 Medium | Secondary dominant; octave doubling |
| 5 | 73 | IV | F4 | C3 | 🔴 High | Same as m.4 |
| 6 | 82 | I | C4 | C3 | 🟢 Low | Root doubling at octave; annotation correct |
| 6 | 84 | Vc | D4 | B3 | 🔴 High | B=3rd of V in C; should be **Vb** (1st inv.) |
| 6 | 88 | Ib | E4 | C4 | 🔴 High | C=root of I in C; should be **I** (root pos.) |
| 6 | 90 | Vb/V | F#4 | A3 | 🟡 Medium | Secondary dominant of V |
| 7 | 95 | V | G4 | G3 | 🟢 Low | Root doubling at octave; annotation correct |
| 49 | 616 | V7b/v | C#4 | A3 | 🟡 Medium | Secondary dominant of v |
| 51 | 650 | V7b | F#4 | C4 | 🔴 High | In G:, C=7th of V7; should be **V7d** (3rd inv.) |
| 53 | 684 | vi | G4 | B3 | 🟡 Medium | B=3rd of vi in G (E-G-B); may need review |
| 55 | 718 | V7b/vii | E4 | Bb3 | 🟡 Medium | Secondary dominant of vii |
| 57 | 752 | vb | F4 | A3 | 🔴 High | In G:, A=5th of v; should be **vc** (2nd inv.) |
| 81 | 1017 | V | D4 | F3 | 🟡 Medium | Recapitulation; F not root of V in C |
| 82 | 1023 | I | E4 | C3 | 🟢 Low | C=root of I in C; annotation correct |
| 84 | 1051 | I | G4 | C3 | 🟢 Low | C=root of I; annotation correct |
| 84 | 1056 | V7b/IV | E3 | C3 | 🟡 Medium | Secondary dominant of IV |
| 84 | 1060 | IV | F3 | C3 | 🔴 High | Recapitulation of m.4 |

### Op. 20 No. 2 — IV. Fuga a 4 soggetti (`op20n2-04.hrm`)

| Measure | Line | Annotation | Cello | Viola (bass) | Confidence | Explanation |
|:-------:|:----:|:----------:|:-----:|:------------:|:----------:|:------------|
| 12 | 116 | I | C4 | C3 | 🟢 Low | Root doubling at octave; annotation correct |
| 44 | 375 | V7b | C#4 | G3 | 🔴 High | G=5th of V7 in d; should be **V7c** (2nd inv.) |
| 44 | 378 | i | D4 | F3 | 🔴 High | F=3rd of i in d; should be **ib** (1st inv.) |
| 44 | 379 | viioD7d | Bb3 | F3 | 🔴 High | Inversion matches cello, not actual bass |
| 44 | 381 | ivb | Bb3 | D3 | 🔴 High | D=root of iv in d; should be **iv** (root pos.) |
| 45 | 383 | V7 | A3 | C#3 | 🔴 High | C#=3rd of V in d; should be **V7b** (1st inv.) |
| 48 | 416 | IIIc | G3 | C3 | 🟡 Medium | Needs review |
| 57 | 483 | viioc | G3 | E3 | 🔴 High | Inversion matches cello, not actual bass |
| 57 | 485 | V7c/IV | A3 | F#3 | 🟡 Medium | Secondary dominant of IV |
| 58 | 488 | IV | B3 | G3 | 🟢 Low | G=root of IV in d (→ G); annotation correct |
| 78 | 668 | I | G4 | F#4 | 🔴 High | F#=3rd of I in D; should be **Ib** (1st inv.) |
| 94 | 789 | v | Bb3 | A3 | 🟡 Medium | Minor interval, needs review |
| 94 | 790 | viio/IV | E4 | G3 | 🟡 Medium | Applied chord |
| 94 | 791 | IV | F4 | F3 | 🟢 Low | Root doubling at octave; annotation correct |
| 95 | 793 | V7c/IV | G4 | E3 | 🟡 Medium | Secondary dominant of IV |
| 140 | 1191 | Vb | B3 | D3 | 🟡 Medium | Needs review |
| 145 | 1250 | viiob | D4 | B3 | 🟡 Medium | Needs review |

### Op. 20 No. 3 — I. Allegro con spirito (`op20n3-01.hrm`)

| Measure | Line | Annotation | Cello | Viola (bass) | Confidence | Explanation |
|:-------:|:----:|:----------:|:-----:|:------------:|:----------:|:------------|
| 96 | 564 | VII | E3 | C#3 | 🟢 Low | Annotation matches actual bass |
| 120 | 680 | IV/IV/VI | Ab3 | Eb3 | 🟡 Medium | Complex applied chord |

### Op. 20 No. 3 — III. Poco adagio (`op20n3-03.hrm`)

| Measure | Line | Annotation | Cello | Viola (bass) | Confidence | Explanation |
|:-------:|:----:|:----------:|:-----:|:------------:|:----------:|:------------|
| 19 | 176 | Vc | A3 | D3 | 🔴 High | D=root of V in G; should be **V** (root pos.) |
| 21 | 202 | Vc | A3 | D3 | 🔴 High | Same as m.19 |
| 36 | 378 | IVc | D5 | G4 | 🔴 High | G=root of IV in D; should be **IV** (root pos.) |
| 36 | 382 | I | D5 | F#4 | 🔴 High | F#=3rd of I in D; should be **Ib** (1st inv.) |
| 37 | 391 | IVc | D5 | G4 | 🔴 High | Same as m.36 |
| 37 | 395 | I | D5 | F#4 | 🔴 High | Same as m.36 |
| 52 | 526 | V7 | E4 | Ab3 | 🔴 High | In f: Ab=5th of V7? Needs key context review |
| 52 | 530 | ib | C4 | A3 | 🔴 High | Inversion matches cello, not actual bass |
| 53 | 532 | ivb | F4 | D3 | 🔴 High | D=root of iv; should be **iv** (root pos.) |
| 53 | 533 | ic | E4 | C3 | 🔴 High | Inversion matches cello, not actual bass |
| 54 | 539 | Vc | B3 | E3 | 🔴 High | E=root of V in a; should be **V** (root pos.) |
| 54 | 542 | ib | C4 | A3 | 🔴 High | A=root of i in a; should be **i** (root pos.) |
| 71 | 725 | ivb/ii | G4 | Bb3 | 🟡 Medium | Secondary applied chord |
| 72 | 738 | V7/ii | C#4 | A3 | 🟡 Medium | Secondary dominant of ii |
| 73 | 751 | ii | F4 | D3 | 🟢 Low | D=root of ii; annotation correct |
| 75 | 777 | vib | A4 | C4 | 🟢 Low | C=3rd of vi (A-C-E); annotation correct |
| 76 | 790 | V7/iii | Eb4 | B3 | 🟡 Medium | Secondary dominant of iii |
| 77 | 803 | iii | G4 | E3 | 🟢 Low | E=root of iii; annotation correct |
| 78 | 816 | V7b | G4 | B3 | 🟢 Low | B=3rd of V7; annotation correct |
| 79 | 829 | I | F4 | C4 | 🟢 Low | C=root of I; annotation correct |
| 80 | 842 | V7b/vi | E4 | Ab3 | 🟡 Medium | Secondary dominant of vi |
| 81 | 855 | vi | D4 | A3 | 🟢 Low | A=root of vi; annotation correct |
| 82 | 868 | iim7b | E4 | F#3 | 🟡 Medium | F# may be 3rd of ii; needs review |
| 83 | 881 | V | C4 | G3 | 🟢 Low | G=root of V; annotation correct |
| 83 | 889 | V7c/V/V | C#4 | E3 | 🟡 Medium | Double applied chord |
| 84 | 895 | V[V/V] | D4 | D3 | 🟢 Low | Octave doubling; unparsed label |
| 93 | 1012 | iib | C4 | C3 | 🟢 Low | Octave doubling; annotation correct |
| 106 | 1172 | IVc | G4 | C4 | 🔴 High | Recapitulation; C=root of IV; should be **IV** |
| 106 | 1176 | I | G4 | B3 | 🔴 High | B=3rd of I in G; should be **Ib** (1st inv.) |
| 107 | 1185 | IVc | G4 | C4 | 🔴 High | Same as m.106 |
| 107 | 1189 | I | G4 | B3 | 🔴 High | Same as m.106 |

### Op. 20 No. 3 — IV. Finale. Allegro molto (`op20n3-04.hrm`)

| Measure | Line | Annotation | Cello | Viola (bass) | Confidence | Explanation |
|:-------:|:----:|:----------:|:-----:|:------------:|:----------:|:------------|
| 2 | 35 | ib | Bb3 | G3 | 🔴 High | G=root of i in g; should be **i** (root pos.) |
| 6 | 76 | V7d | C4 | G3 | 🔴 High | Inversion matches cello, not actual bass |
| 21 | 222 | Ib | D4 | Bb3 | 🔴 High | Bb=root of I in Bb; should be **I** (root pos.) |
| 21 | 228 | IV | Eb4 | Bb3 | 🔴 High | Bb=5th of IV in Bb; should be **IVc** (2nd inv.) |
| 60 | 575 | V7d/III | Ab3 | Eb3 | 🟡 Medium | Secondary dominant of III |
| 72 | 702 | ib | Bb3 | G3 | 🔴 High | Recapitulation of m.2 |

### Op. 20 No. 4 — I. Allegro di molto (`op20n4-01.hrm`)

| Measure | Line | Annotation | Cello | Viola (bass) | Confidence | Explanation |
|:-------:|:----:|:----------:|:-----:|:------------:|:----------:|:------------|
| 54 | 309 | V7d | D4 | C#4 | 🔴 High | Inversion matches cello, not actual bass |
| 184 | 1107 | Vc | C#4 | B3 | 🔴 High | Inversion matches cello, not actual bass |

### Op. 20 No. 4 — II. Un poco adagio e affettuoso (`op20n4-02.hrm`)

| Measure | Line | Annotation | Cello | Viola (bass) | Confidence | Explanation |
|:-------:|:----:|:----------:|:-----:|:------------:|:----------:|:------------|
| 37 | 327 | viio | C#4 | E3 | 🔴 High | E=3rd of viio in d; should be **viiob** (1st inv.) |
| 37 | 328 | i | D4 | D3 | 🟢 Low | Root doubling at octave; annotation correct |
| 38 | 330 | viioD7d | Bb3 | G3 | 🔴 High | Inversion matches cello, not actual bass |
| 38 | 331 | ic | A3 | F3 | 🔴 High | F=root of i(?); inversion matches cello |
| 38 | 335 | V7 | A3 | G3 | 🔴 High | G=5th of V7 in d; should be **V7c** (2nd inv.) |
| 39 | 339 | VI | D4 | F3 | 🟡 Medium | F may be 3rd of VI (Bb-D-F) in context |
| 39 | 343 | viioc | G4 | G3 | 🟢 Low | Octave doubling; annotation correct |
| 41 | 358 | viiob | E4 | E3 | 🟢 Low | Octave doubling; annotation correct |
| 41 | 359 | i | F4 | D3 | 🟢 Low | D=root of i in d; annotation correct |
| 42 | 362 | ivm7 | Bb3 | G3 | 🟢 Low | G=root of ivm7; annotation correct |
| 42 | 364 | V7/III | G4 | C3 | 🟡 Medium | Secondary dominant of III |
| 43 | 372 | IIIb | A3 | F3 | 🟡 Medium | Needs review |
| 45 | 398 | ivb | Bb3 | G3 | 🔴 High | G=root of iv in d; should be **iv** (root pos.) |
| 48 | 419 | i | D4 | A3 | 🔴 High | A=5th of i in d; should be **ic** (2nd inv.) |
| 48 | 422 | Vb | C#4 | A3 | 🔴 High | A=root of V in d; should be **V** (root pos.) |
| 51 | 443 | (VI) | Bb3 | A3 | 🟡 Medium | Parenthesized; needs review |
| 52 | 452 | Gn | D4 | Bb3 | 🟡 Medium | German augmented 6th; not fully parseable |
| 53 | 461 | ic | A4 | A3 | 🟢 Low | Octave doubling; annotation correct |
| 53 | 464 | V7b | E4 | A3 | 🟡 Medium | A=root of V in d; possibly should be V7 |
| 54 | 469 | i | D4 | D3 | 🟢 Low | Root doubling at octave; annotation correct |
| 108 | 905 | V7b | C#4 | A3 | 🔴 High | A=root of V in d; should be **V7** (root pos.) |
| 109 | 912 | i | D4 | A3 | 🔴 High | A=5th of i in d; should be **ic** (2nd inv.) |
| 112 | 940 | V7b | C#4 | A3 | 🔴 High | Same as m.108 |
| 112 | 941 | i | D4 | A3 | 🔴 High | Same as m.109 |

### Op. 20 No. 4 — III. Menuet alla Zingarese & Trio (`op20n4-03.hrm`)

| Measure | Line | Annotation | Cello | Viola (bass) | Confidence | Explanation |
|:-------:|:----:|:----------:|:-----:|:------------:|:----------:|:------------|
| 31 | 194 | Ib | F#4 | A3 | 🔴 High | A=5th of I in D; should be **Ic** (2nd inv.) |
| 32 | 197 | Vb | C#4 | A3 | 🔴 High | A=root of V in D; should be **V** (root pos.) |

### Op. 20 No. 4 — IV. Presto e scherzando (`op20n4-04.hrm`)

| Measure | Line | Annotation | Cello | Viola (bass) | Confidence | Explanation |
|:-------:|:----:|:----------:|:-----:|:------------:|:----------:|:------------|
| 16 | 158 | Vb | C#4 | A3 | 🔴 High | A=root of V in d; should be **V** (root pos.) |
| 16 | 160 | V7b | C#4 | A3 | 🔴 High | A=root of V7 in d; should be **V7** (root pos.) |
| 16 | 161 | i | D4 | A3 | 🔴 High | A=5th of i in d; should be **ic** (2nd inv.) |
| 57 | 630 | V7d | E4 | Bb3 | 🔴 High | Inversion matches cello, not actual bass |
| 116 | 1297 | I | D4 | F#3 | 🔴 High | F#=3rd of I in D; should be **Ib** (1st inv.) |

### Op. 20 No. 5 — I. Moderato (`op20n5-01.hrm`)

| Measure | Line | Annotation | Cello | Viola (bass) | Confidence | Explanation |
|:-------:|:----:|:----------:|:-----:|:------------:|:----------:|:------------|
| 132 | 1543 | vi | C#4 | Ab3 | 🟡 Medium | Enharmonic issue (Ab vs G#); needs review |

### Op. 20 No. 5 — III. Adagio (`op20n5-03.hrm`)

| Measure | Line | Annotation | Cello | Viola (bass) | Confidence | Explanation |
|:-------:|:----:|:----------:|:-----:|:------------:|:----------:|:------------|
| 83 | 988 | V7 | C4 | Bb3 | 🔴 High | Bb=7th of V7; should be **V7d** (3rd inv.) |

### Op. 20 No. 5 — IV. Finale. Fuga a due soggetti (`op20n5-04.hrm`)

| Measure | Line | Annotation | Cello | Viola (bass) | Confidence | Explanation |
|:-------:|:----:|:----------:|:-----:|:------------:|:----------:|:------------|
| 77 | 495 | V7d/v | Eb4 | C4 | 🟡 Medium | Secondary dominant of v |
| 119 | 754 | V7d/V | F4 | B3 | 🟡 Medium | Secondary dominant of V |
| 120 | 757 | Vc | F4 | C4 | 🟡 Medium | C=root of V in f; possibly should be V |
| 120 | 760 | Vb | E4 | C4 | 🔴 High | C=root of V in f; should be **V** (root pos.) |

### Op. 20 No. 6 — I. Allegro di molto e scherzando (`op20n6-01.hrm`)

| Measure | Line | Annotation | Cello | Viola (bass) | Confidence | Explanation |
|:-------:|:----:|:----------:|:-----:|:------------:|:----------:|:------------|
| 2 | 38 | I | A3 | E3 | 🔴 High | E=5th of I in A; should be **Ic** (2nd inv.) |
| 6 | 70 | I | A3 | E3 | 🔴 High | Same as m.2 |
| 12 | 129 | I | A3 | E3 | 🔴 High | Same as m.2 |
| 110 | 985 | I | A3 | E3 | 🔴 High | Recapitulation of m.2 |
| 114 | 1018 | i | A3 | E3 | 🔴 High | E=5th of i in a; should be **ic** (2nd inv.) |
| 127 | 1148 | V7 | D4 | B3 | 🟡 Medium | B=3rd of V7 in A; possibly should be V7b |
| 127 | 1149 | I | C#4 | A3 | 🟢 Low | A=root of I; annotation correct |
| 127 | 1150 | V7 | D4 | B3 | 🟡 Medium | Same as ln 1148 |
| 127 | 1151 | I | C#4 | A3 | 🟢 Low | A=root of I; annotation correct |
| 128 | 1153 | V7 | D4 | B3 | 🟡 Medium | Same pattern |
| 128 | 1154 | I | C#4 | A3 | 🟢 Low | Annotation correct |
| 128 | 1155 | V7 | D4 | B3 | 🟡 Medium | Same pattern |
| 128 | 1156 | I | C#4 | A3 | 🟢 Low | Annotation correct |
| 128 | 1157 | V7 | D4 | B3 | 🟡 Medium | Same pattern |
| 128 | 1158 | I | C#4 | A3 | 🟢 Low | Annotation correct |

### Op. 20 No. 6 — IV. Fuga a 3 soggetti. Allegro (`op20n6-04.hrm`)

| Measure | Line | Annotation | Cello | Viola (bass) | Confidence | Explanation |
|:-------:|:----:|:----------:|:-----:|:------------:|:----------:|:------------|
| 81 | 1015 | iim7 | F#4 | F#3 | 🟡 Medium | Octave doubling but script ambiguous on chord tones |
| 82 | 1019 | V | E4 | E3 | 🟢 Low | Octave doubling; annotation correct |
| 82 | 1026 | iiom7 | D4 | D3 | 🟡 Medium | Octave doubling; diminished quality edge case |
| 83 | 1030 | iii | C#4 | C#3 | 🟢 Low | Octave doubling; annotation correct |

---

## Summary

| Confidence | Count | Description |
|:----------:|:-----:|:------------|
| 🔴 High | 69 | Inversion clearly matches cello, not the actual bass (viola) |
| 🟡 Medium | 44 | Uncertain — secondary dominants, applied chords, or enharmonic ambiguity |
| 🟢 Low (OK) | 37 | Annotation already correct, or octave doubling — no change needed |
| **Total** | **150** | All viola-below-cello crossings at harmony onsets |

### Distribution of 🔴 High-confidence errors by movement

| Movement | Count |
|:---------|:-----:|
| Op.20 No.3, Mvt.III | 16 |
| Op.20 No.4, Mvt.II | 11 |
| Op.20 No.2, Mvt.I | 9 |
| Op.20 No.2, Mvt.IV | 7 |
| Op.20 No.1, Mvt.I | 5 |
| Op.20 No.3, Mvt.IV | 5 |
| Op.20 No.4, Mvt.IV | 5 |
| Op.20 No.6, Mvt.I | 5 |
| Op.20 No.4, Mvt.I | 2 |
| Op.20 No.4, Mvt.III | 2 |
| Op.20 No.5, Mvt.III | 1 |
| Op.20 No.5, Mvt.IV | 1 |
