import pprint as pp
import argparse

removed = []
added = []

def filterFile(filename):
    with open(filename) as f:
        for l in f.readlines():
            if 'pagebreak' in l or 'linebreak' in l:
                removed.append(l.split('\n')[0])
            else:
                if l.startswith('*') or l.startswith('=') or l.startswith('!!!'):
                    if 'tshrm' in l:
                        l = l.replace('tshrm', 'harm').replace('tsroot','commentary')
                    added.append(l.split('\n')[0])
                else:
                    lst = [e+'\t' for e in l.split('\t') if e]
                    #print str(len(lst)) + ''.join(lst)
                    lst[0] = '.\t'
                    lst[1] = '.\t'
                    l = ''.join(lst)
                    added.append(l.split('\n')[0])
    for x in added:
        print x

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a template for manual annotations')
    parser.add_argument('filename', help='Humdrum file to filter')
    args = parser.parse_args()
    filterFile(args.filename)
