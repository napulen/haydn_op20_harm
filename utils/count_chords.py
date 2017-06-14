import os
import pprint as pp

cwd = '.'
chords = []
total = 0

for root, subfolder, files in os.walk(cwd):
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
