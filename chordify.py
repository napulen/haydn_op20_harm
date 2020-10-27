import os
import music21
import harmalysis

for r, d, f in os.walk('op20'):
    if not f:
        continue
    for t in f:
        if t.endswith('.hrm'):
            harm = t
            fullname = os.path.join(r, harm)
    # print(fullname)
    # s = music21.converter.parse(fullname, format='humdrum')
    # s.show('text')
    # rna = {}
    # for harm in s.flat.getElementsByClass('RomanNumeral'):
    #     rna[harm.offset] = harm
    print(fullname)
    with open(fullname) as fd:
        lines = fd.readlines()
    with open(fullname[:-4] + '.chrd', 'w') as fdout:
        for line in lines:
            line = line.strip()
            if line.startswith('!!!'):
                harm = line
                otherSpines = ''
            else: 
                harm, otherSpines = line.split('\t', 1)
            if harm.startswith('*') and harm.endswith(':'):
                key = harm[1:-1]
                print('change of key: {}'.format(key))
            try:
                c = harmalysis.parse(f'{key}:{harm}')
                chordlabel = harmalysis.parsers.chordlabel.parse(str(c.chord))
                chordlabel = chordlabel.replace(' ', '_')
                # print(f'{chordlabel}\n')
                fdout.write(f'{chordlabel}\t{otherSpines}\n')
            except:
                # print(f'{harm}\n')
                fdout.write(f'{harm}\t{otherSpines}\n')
                pass
    # break