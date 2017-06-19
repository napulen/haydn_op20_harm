import re
import os
import argparse
import subprocess
import pprint as pp

recordparser = r'''			
		^(?P<measure>					# Find measure information
		(=								# Assumming anything that starts with = as a measure
		(?P<measure_number>\d+)			# But I only care about measure numbers
		(?P<measure_reminder>[/S/s]*)	
		))$
		|
		^(?P<null_record>\.)$			# Detect NULL records
		|
		^(?P<root>[a-gA-G]+[-#]{0,2})	# And root changes
		'''

class RootSpine:
	current_measure = 0
	def __init__(self):	
		self.filename = ''
		self.current_root = '?'
		self.timebase = -1
		self.measures = {0:[]}


def parseColumn(col, rootspine):
	p = re.compile(recordparser, re.VERBOSE)
	m = p.match(col)
	if m:
		cdict = m.groupdict()
		if cdict['measure']:
			# Only care about measure_numbers
			if cdict['measure_number']:
				rootspine.current_measure = int(cdict['measure_number'])
				rootspine.measures[rootspine.current_measure] = []		
		elif cdict['null_record']:
			rootspine.measures[rootspine.current_measure].append(rootspine.current_root)
		elif cdict['root']:
			rootspine.current_root = cdict['root']
			rootspine.measures[rootspine.current_measure].append(rootspine.current_root)
	else:
		rootspine.measures[rootspine.current_measure].append(rootspine.current_root)


def parseLine(line, manual, auto):
	l = line.strip().split('\t')
		
	parseColumn(l[1], manual)
	parseColumn(l[3], auto)


def compare(manual, auto):
	matches = 0
	totalunits = 0
	for k,v in manual.measures.iteritems():		
		#print 'Measure: {}\nManual\tAuto'.format(k)
		if len(v) != len(auto.measures[k]):
			print 'WARNING: Mismatching entries in measure {}. Skipping.'.format(k)
			continue
		for idx in range(len(v)):
			mfield = manual.measures[k][idx]
			afield = auto.measures[k][idx]
			matches += int(mfield == afield)
			totalunits += 1
			#print '{}\t{} --> {}/{}'.format(mfield, afield, matches, totalunits)
	return matches,totalunits


def parseHeader(lines, manual, auto):
	for idx,l in enumerate(lines):
		if l.startswith('!!!'):
			l = l.strip()[3:].split(':')
			if l[0] == 'ManualAnalysis':				
				manual.filename = l[1]
			elif l[0] == 'AutomaticAnalysis':
				auto.filename = l[1]
		elif l.startswith('**harm'):
			break
	return lines[idx+1:]



def evaluateFiles(rootdir):	
	counter = 0
	for root, subfolder, files in os.walk(rootdir):		
		for f in files:				
			if f.endswith(".eval"):				
				filename = str(os.path.join(root,f))
				with open(filename) as fd:
					manual = RootSpine()
					auto = RootSpine()
					lines = fd.readlines()
					noheader = parseHeader(lines, manual, auto)
					print '{} vs. {}'.format(manual.filename, auto.filename)
					for line in noheader:						
						parseLine(line, manual, auto)
					matches, totalunits = compare(manual, auto)
					percentage = 100.0*matches/totalunits
					print '\t{}/{} identical time units\n\t{}%\n'.format(matches,totalunits, percentage)
													
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Evaluates manual vs. automatic **harm annotation files.''')
    parser.add_argument('-d','--rootdir', metavar='directory', help='Specify the directory of the corpus', default='../op20')
    args = parser.parse_args()
    evaluateFiles(args.rootdir)					
