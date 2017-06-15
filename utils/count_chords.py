import os
import argparse
import pprint as pp

def countChords(rootdir):
	chords = []
	total = 0
	for root, subfolder, files in os.walk(rootdir):
		for f in files:
			if f.endswith(".hrm"):
				filepath = str(os.path.join(root,f))
				#print filepath
				with open(filepath) as fd:
					for line in fd.readlines():
						line = line.split()[0]
						if line != '.' and '!' not in line and '*' not in line and '=' not in line:
							chords.append(line)
				print '{}\t{} chord annotations'.format(filepath,len(chords))
				pp.pprint(chords)
				print ''
				total += len(chords)
				chords = []
	print 'The total number of chords in the dataset is {}'.format(total)
	return total,chords

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Count the number of chords in the corpus')
    parser.add_argument('-d','--rootdir', metavar='directory', help='Specify the directory of the corpus', default='../op20')
    args = parser.parse_args()
    countChords(args.rootdir)					
