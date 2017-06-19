import os
import argparse
import subprocess
import pprint as pp
import tempfile
import datetime


def getShortestNote(file):
	sn = -1
	#print 'Running census over: ', file	
	# It seems census is just grabbing all the numbers in the string and picks the maximum
	# Therefore, restricting to only **kern spines to make this validation, any number in harmonic
	# analysis seems to be corrupting the output, e.g., VM9.
	extract = subprocess.Popen(('extract', '-i', '**kern', file), stdout=subprocess.PIPE)
	nocommentary, err = extract.communicate()
	# Now census the output
	census = subprocess.Popen(('census', '-k'), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	out, err = census.communicate(nocommentary)	
	for line in out.split('\n'):
		tokens = line.split(':')
		if tokens[0] == 'Shortest note':		
			sn = tokens[1]		
			return sn.strip()


def addHeader(output, manfname, compfname):
	title = '!!!Title: Evaluation file for harmonic analysis\n'
	author = '!!!Author: Nestor Napoles (napulen@gmail.com)\n'
	date = '!!!Date: {:%Y-%m-%d %H:%M:%S}\n'.format(datetime.datetime.now())
	manfile = '!!!ManualAnalysis:{}\n'.format(manfname)
	autofile = '!!!AutomaticAnalysis:{}\n'.format(compfname)
	spines = '**harm\t**root\t**harm\t**root\n'
	return title+author+date+manfile+autofile+spines+output


def concatenate(groundtruth, computed):
	# Validate the shortest note using the census program
	gtShortestNote = getShortestNote(groundtruth)
	cShortestNote = getShortestNote(computed)	
	if gtShortestNote != cShortestNote:
		print 'ERROR: Not the same shortest note in {} and {}'.format(groundtruth, computed)
		return None	
	# Pre-processing groundtruth file	
	harm2kern = subprocess.Popen(('harm2kern', '-ra', '-o4', '--no-rhythm', groundtruth), stdout=subprocess.PIPE)
	stdo, stde = harm2kern.communicate()
	# Assume this file can be opened a second time, and it will be deleted automatically after closing.
	tmpgroundtruth =  tempfile.NamedTemporaryFile()
	tmpgroundtruth.write(stdo)
	tmpgroundtruth.flush()
	# Pre-processing computed file
	# First rename the **tshrm spine to **harm so it is detected by harm2kern
	with open(computed) as f:
		stdo = f.read()
	# Just expecting to find one instance of **tsharm
	stdo = stdo.replace('**tshrm', '**harm', 1)	
	harm2kern = subprocess.Popen(('harm2kern', '-ra', '-o4' , '--no-rhythm'), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	stdo, stde = harm2kern.communicate(stdo)
	# Assume this file can be opened a second time, and it will be deleted automatically after closing.
	tmpcomputed =  tempfile.NamedTemporaryFile()
	tmpcomputed.write(stdo)
	tmpcomputed.flush()
	# Everything went okay, now assemble
	assemble = subprocess.Popen(('assemble', tmpgroundtruth.name, tmpcomputed.name), stdout=subprocess.PIPE)
	stdo, stde = assemble.communicate()	
	# No need for these temporary files anymore, close them
	tmpcomputed.close()
	tmpgroundtruth.close()
	# Create a new timebase using the shortest note
	# Use either, they are the same (hopefully)
	timebase = subprocess.Popen(('timebase', '-t', gtShortestNote), stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	stdo, stde = timebase.communicate(stdo)
	# Keep only **root spines
	extract = subprocess.Popen(('extract', '-i', '**harm,**root'), stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	stdo, stde = extract.communicate(stdo)	
	# Get rid of unwanted records
	rid = subprocess.Popen(('rid', '-GLI'), stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	stdo, stde = rid.communicate(stdo)
	return stdo


def genEvaluationFiles(rootdir):
	chords = []
	total = 0
	for root, subfolder, files in os.walk(rootdir):
		for f in files:			
			if f.endswith(".hrm"):
				# Assume all manual annotations are named according to "<base>.hrm"
				groundtruth = str(os.path.join(root,f))
				# Now assume all automatic analysis follow the convention '<base>_tsroot.krn'
				# and they are in the same folder than their corresponding manual annotation
				base = f[:-4]
				compfname = '{}_tsroot.krn'.format(base)
				computed = str(os.path.join(root, compfname))
				c = concatenate(groundtruth, computed)
				c = addHeader(c, f, compfname)
				if not c:
					print 'Errors while concatenating {}'.format(base)
					continue
				evaluation = str(os.path.join(root, '{}.eval'.format(base)))
				with open(evaluation, "w") as ev:
					ev.write(c)
					ev.close()						

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Concatenates the manual and automatic annotation files into evaluation files for all the corpus. This code requires the humdrum-extra tools to be installed.''')
    parser.add_argument('-d','--rootdir', metavar='directory', help='Specify the directory of the corpus', default='../op20')
    args = parser.parse_args()
    genEvaluationFiles(args.rootdir)					
