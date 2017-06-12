import os

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
			print filepath
			print chords
			print len(chords)
			total += len(chords)
			chords = []

print total						
