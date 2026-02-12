#!/usr/bin/env python3
"""
check_inversions.py - Detect potential inversion annotation errors in **harm files.

This script analyzes .hrm (Humdrum **harm + **kern) files to find places where
the viola crosses below the cello, potentially invalidating the annotated chord
inversion. When the viola is the actual lowest-sounding voice, the inversion
should be calculated relative to the viola's pitch, not the cello's.

File format (columns):
  0: **harm  (harmony annotation)
  1: **commentary
  2: **kern  - Cello  (staff1, clefF4)
  3: **kern  - Viola  (staff2, clefC3)
  4: **kern  - Violin 2 (staff3, clefG2)
  5: **kern  - Violin 1 (staff4, clefG2)

Usage:
  python3 scripts/check_inversions.py

The script scans all .hrm files under the op20/ directory and reports instances
where the viola pitch is lower than the cello pitch at the onset of a new
harmony annotation, categorizing each as:
  - LIKELY ERROR: the annotated inversion matches the cello but not the viola
  - OK: the inversion correctly matches the actual bass (viola)
  - AMBIGUOUS: the inversion matches neither voice (complex harmony)
"""

import os
import re
import glob

NOTE_SEMITONES = {
    'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11
}

SEMITONE_TO_NAME = {
    0: 'C', 1: 'C#', 2: 'D', 3: 'Eb', 4: 'E', 5: 'F',
    6: 'F#', 7: 'G', 8: 'Ab', 9: 'A', 10: 'Bb', 11: 'B'
}

KEY_TO_TONIC = {
    'C': 0, 'C#': 1, 'D-': 1, 'D': 2, 'D#': 3, 'E-': 3, 'E': 4,
    'F': 5, 'F#': 6, 'G-': 6, 'G': 7, 'G#': 8, 'A-': 8, 'A': 9,
    'A#': 10, 'B-': 10, 'B': 11,
    'c': 0, 'c#': 1, 'd-': 1, 'd': 2, 'd#': 3, 'e-': 3, 'e': 4,
    'f': 5, 'f#': 6, 'g-': 6, 'g': 7, 'g#': 8, 'a-': 8, 'a': 9,
    'a#': 10, 'b-': 10, 'b': 11,
}


def kern_to_midi(token):
    """Convert a **kern pitch token to a MIDI note number. Returns None for rests."""
    if not token or token.strip() == '.' or 'r' in token:
        return None

    cleaned = re.sub(r'[\[\]_/\\LJqQ();:!@%^&{}<>~`|,\s]', '', token)
    cleaned = re.sub(r'^[\d.]+', '', cleaned)
    if not cleaned:
        return None

    note_letter = None
    count = 0
    is_upper = None
    i = 0
    while i < len(cleaned):
        ch = cleaned[i]
        if ch.lower() in NOTE_SEMITONES:
            if note_letter is None:
                note_letter = ch.lower()
                is_upper = ch.isupper()
                count = 1
            elif ch.lower() == note_letter and ch.isupper() == is_upper:
                count += 1
            else:
                break
            i += 1
        else:
            break

    if note_letter is None:
        return None

    accidental = 0
    while i < len(cleaned):
        if cleaned[i] == '#':
            accidental += 1
        elif cleaned[i] == '-':
            accidental -= 1
        elif cleaned[i] == 'n':
            pass
        else:
            break
        i += 1

    octave = (4 - count) if is_upper else (3 + count)
    return (octave + 1) * 12 + NOTE_SEMITONES[note_letter] + accidental


def get_lowest_pitch(cell):
    """Return the lowest MIDI pitch in a kern cell (which may be a chord)."""
    if not cell or cell.strip() == '.':
        return None
    pitches = [kern_to_midi(t) for t in cell.strip().split()]
    pitches = [p for p in pitches if p is not None]
    return min(pitches) if pitches else None


def midi_to_name(midi):
    """Convert MIDI note number to human-readable name (e.g. C4, Eb3)."""
    if midi is None:
        return "N/A"
    return f"{SEMITONE_TO_NAME[midi % 12]}{(midi // 12) - 1}"


def parse_harm_annotation(harm):
    """Parse a **harm token; return dict with 'main', 'inversion', 'secondary', or None."""
    if not harm or harm.strip() in ('.', '', '*'):
        return None
    harm = harm.strip()
    if harm.startswith(('=', '!', '*')):
        return None

    harm = harm.strip('()')
    parts = harm.split('/')
    main = parts[0]
    secondary = '/'.join(parts[1:]) if len(parts) > 1 else ''
    if not main:
        return None

    inversion = ''
    if len(main) > 1 and main[-1] in ('b', 'c', 'd'):
        inversion = main[-1]
        main = main[:-1]

    return {'main': main, 'inversion': inversion, 'secondary': secondary, 'full': harm}


def get_roman_root_interval(roman):
    """Return (semitone_interval_from_tonic, is_minor) for a Roman numeral, or None."""
    cleaned = re.sub(r'[mMDd]?\d+$', '', roman)
    cleaned = re.sub(r'[oO+]', '', cleaned)
    if cleaned in ('N', 'Gn'):
        return None
    intervals = {
        'I': (0, False), 'i': (0, True), 'II': (2, False), 'ii': (2, True),
        'III': (4, False), 'iii': (4, True), 'IV': (5, False), 'iv': (5, True),
        'V': (7, False), 'v': (7, True), 'VI': (9, False), 'vi': (9, True),
        'VII': (11, False), 'vii': (11, True),
    }
    return intervals.get(cleaned)


def get_chord_tones(tonic_pc, roman):
    """Return list of pitch classes [root, 3rd, 5th, (7th)] for a Roman numeral chord."""
    info = get_roman_root_interval(roman)
    if info is None:
        return None
    root_interval, is_minor = info
    root = (tonic_pc + root_interval) % 12
    third = (root + (3 if (is_minor or 'o' in roman or 'O' in roman) else 4)) % 12
    if 'o' in roman or 'O' in roman:
        fifth = (root + 6) % 12
    elif '+' in roman:
        fifth = (root + 8) % 12
    else:
        fifth = (root + 7) % 12
    tones = [root, third, fifth]
    if '7' in roman:
        if ('o' in roman or 'O' in roman) and re.search(r'[oO]D7', roman):
            tones.append((root + 9) % 12)
        elif 'M' in roman:
            tones.append((root + 11) % 12)
        else:
            tones.append((root + 10) % 12)
    return tones


def analyze_file(filepath):
    """Analyze one .hrm file; return list of issue dicts."""
    issues = []
    measure = 0
    harmony = None
    harm_parsed = None
    tonic = 0
    cello_p = viola_p = None

    with open(filepath, 'r') as f:
        lines = f.readlines()

    for ln, line in enumerate(lines, 1):
        line = line.rstrip('\n')
        if not line or line.startswith('!!!') or line.startswith('**') or line.startswith('*-'):
            continue
        cols = line.split('\t')
        if len(cols) < 4:
            continue
        if cols[0].startswith('='):
            m = re.match(r'=(\d+)', cols[0])
            if m:
                measure = int(m.group(1))
            continue
        if cols[0].startswith('*') and ':' in cols[0]:
            key = cols[0].strip().lstrip('*').rstrip(':')
            if key in KEY_TO_TONIC:
                tonic = KEY_TO_TONIC[key]
            continue
        if cols[0].startswith('*'):
            continue

        harm_col = cols[0].strip()
        new_harm = False
        if harm_col and harm_col != '.':
            parsed = parse_harm_annotation(harm_col)
            if parsed:
                harmony = harm_col
                harm_parsed = parsed
                new_harm = True

        cello_cell = cols[2].strip()
        viola_cell = cols[3].strip()
        nc = get_lowest_pitch(cello_cell)
        nv = get_lowest_pitch(viola_cell)
        if nc is not None:
            cello_p = nc
        elif re.search(r'\d+\.?r', cello_cell) and cello_cell != '.':
            cello_p = None
        if nv is not None:
            viola_p = nv
        elif re.search(r'\d+\.?r', viola_cell) and viola_cell != '.':
            viola_p = None

        if not (new_harm and viola_p is not None and cello_p is not None
                and viola_p < cello_p and harm_parsed is not None):
            continue

        bass_pc = viola_p % 12
        cello_pc = cello_p % 12
        inv = harm_parsed['inversion']
        has7 = '7' in harm_parsed['main']
        bass_pos = {'b': 1, 'c': 2, 'd': 3}.get(inv, 0)
        tones = get_chord_tones(tonic, harm_parsed['main'])

        category = "CROSSING"
        if tones and bass_pos < len(tones):
            exp_pc = tones[bass_pos]
            if cello_pc == exp_pc and bass_pc != exp_pc:
                category = "LIKELY ERROR"
            elif bass_pc == exp_pc:
                category = "OK"
            else:
                category = "AMBIGUOUS"

        issues.append({
            'file': os.path.basename(filepath),
            'line': ln, 'measure': measure,
            'harmony': harmony,
            'inversion': inv if inv else 'root',
            'cello_note': midi_to_name(cello_p),
            'viola_note': midi_to_name(viola_p),
            'category': category,
        })
    return issues


def main():
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    hrm_files = sorted(glob.glob(os.path.join(base, 'op20', '*', '*', '*.hrm')))
    if not hrm_files:
        base = '.'
        hrm_files = sorted(glob.glob(os.path.join(base, 'op20', '*', '*', '*.hrm')))

    print(f"Scanning {len(hrm_files)} .hrm files for viola-below-cello crossings...\n")
    all_issues = []
    for fp in hrm_files:
        all_issues.extend(analyze_file(fp))

    likely = [i for i in all_issues if i['category'] == 'LIKELY ERROR']
    ok = [i for i in all_issues if i['category'] == 'OK']
    ambig = [i for i in all_issues if i['category'] == 'AMBIGUOUS']
    other = [i for i in all_issues if i['category'] == 'CROSSING']

    def print_group(title, items):
        print(f"\n{'=' * 78}")
        print(f"{title} ({len(items)})")
        print('=' * 78)
        for i in items:
            print(f"  {i['file']:<20s} m.{i['measure']:<4d} ln {i['line']:<5d} "
                  f"{i['harmony']:<20s} inv={i['inversion']:<5s} "
                  f"cello={i['cello_note']:<6s} viola={i['viola_note']}")

    print_group("LIKELY INVERSION ERRORS (annotation matches cello, not actual bass)", likely)
    print_group("CORRECTLY ANNOTATED (inversion matches actual bass)", ok)
    print_group("AMBIGUOUS (matches neither voice exactly)", ambig)
    if other:
        print_group("OTHER CROSSINGS (harmony not fully parsed)", other)

    print(f"\n{'=' * 78}")
    print(f"SUMMARY: {len(likely)} likely errors, {len(ok)} correct, "
          f"{len(ambig)} ambiguous, {len(other)} other — {len(all_issues)} total crossings")
    print('=' * 78)


if __name__ == '__main__':
    main()
