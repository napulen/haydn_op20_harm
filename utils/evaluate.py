import harmparser
import re
import os
import argparse
import subprocess
import pprint as pp

recordparser = r'''
		^(\*(?P<key>[^\]]+):)$	# Detecting key records
		|				
		^(=(?P<measure>\d+))$	# Or a measure change
		|
		^(?P<null_record>\.)$	# Or a NULL record
		'''

class HarmSpine:
	current_measure = 0
	def __init__(self):
		self.current_key = ''
		self.current_chord = ''
		self.timebase = -1
		self.measures = {0:[()]}


def compare(harmexpr1, harmexpr2):
	# Validate the shortest note using the census program
	gtShortestNote = getShortestNote(groundtruth)
	cShortestNote = getShortestNote(computed)	
	if gtShortestNote != cShortestNote:
		print 'ERROR: Not the same shortest note in {} and {}'.format(groundtruth, computed)
		return None
	# Everything went okay, now assemble
	assemble = subprocess.Popen(('assemble', groundtruth, computed), stdout=subprocess.PIPE)
	stdo, stde = assemble.communicate()
	# Get rid of unwanted records
	rid = subprocess.Popen(('rid', '-GLid'), stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	stdo, stde = rid.communicate(stdo)
	# Create a new timebase using the shortest note
	# Use either, they are the same (hopefully)
	timebase = subprocess.Popen(('timebase', '-t', gtShortestNote), stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	stdo, stde = timebase.communicate(stdo)
	# Finally, keep only **harm and **tshrm spines
	extract = subprocess.Popen(('extract', '-i', '**harm,**tshrm'), stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	stdo, stde = stde = extract.communicate(stdo)
	# The final output is in stdout, phew!
	return stdo


def parseColumn(col, harmspine):
	p = re.compile(recordparser, re.VERBOSE)
	m = p.match(col)
	if m:
		cdict = m.groupdict()
		if cdict['key']:
			harmspine.current_key = cdict['key']			
		elif cdict['measure']:
			harmspine.current_measure = int(cdict['measure'])
			harmspine.measures[harmspine.current_measure] = []		
		elif cdict['null_record']:
			harmspine.measures[harmspine.current_measure].append((harmspine.current_chord,harmspine.current_key))
	else:
		charm = harmparser.parseHarm(col)
		if charm:	
			for expr in charm:
				harmspine.current_chord = expr['root']
				harmspine.measures[harmspine.current_measure].append((harmspine.current_chord,harmspine.current_key))
				break


def parseLine(line, manual, auto):
	l = line.split('\t')	
	parseColumn(l[0], manual)
	parseColumn(l[1], auto)


def printComparison(manual, auto):
	for k,v in manual.measures.iteritems():		
		print 'Measure: {}\nManual\tAuto'.format(k)
		if len(v) != len(auto.measures[k]):
			print 'WARNING: Mismatching entries in measure {}. Skipping.'.format(k)
			continue
		for idx in range(len(v)):
			mkey = ''
			mchord = ''
			akey = ''
			achord = ''
			if len(manual.measures[k][idx]) > 0:
				mchord = manual.measures[k][idx][0]
				mkey = manual.measures[k][idx][1]
			if len(auto.measures[k][idx]) > 0:
				achord = auto.measures[k][idx][0]
				akey = auto.measures[k][idx][1]	
			print '{}:{}\t{}:{}'.format(mkey, mchord, akey, achord)


def evaluateFiles(rootdir):	
	counter = 0
	for root, subfolder, files in os.walk(rootdir):		
		for f in files:				
			if f.endswith(".eval"):
				print f
				filename = str(os.path.join(root,f))
				with open(filename) as fd:
					manual = HarmSpine()
					auto = HarmSpine()
					for line in fd.readlines():						
						parseLine(line, manual, auto)
					printComparison(manual, auto)
													
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Evaluates manual vs. automatic **harm annotation files.''')
    parser.add_argument('-d','--rootdir', metavar='directory', help='Specify the directory of the corpus', default='../op20')
    args = parser.parse_args()
    evaluateFiles(args.rootdir)					
