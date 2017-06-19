import re
import os
import argparse
import subprocess
import pprint as pp
import collections
from harmparser import HarmParser

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

class EvaluationFile:
	current_measure = 0
	def __init__(self):	
		self.filename = ''
		self.current_root = '?'
		self.timebase = -1
		self.measures = {0:[]}
		self.roots = []
		self.totalchords = 0

def parseRootColumn(col, evalfile):
	p = re.compile(recordparser, re.VERBOSE)
	m = p.match(col)
	if m:
		cdict = m.groupdict()
		if cdict['measure']:
			# Only care about measure_numbers
			if cdict['measure_number']:
				evalfile.current_measure = int(cdict['measure_number'])
				evalfile.measures[evalfile.current_measure] = []		
		elif cdict['null_record']:
			evalfile.measures[evalfile.current_measure].append(evalfile.current_root)
		elif cdict['root']:
			evalfile.current_root = cdict['root']
			evalfile.measures[evalfile.current_measure].append(evalfile.current_root)
	else:
		evalfile.measures[evalfile.current_measure].append(evalfile.current_root)


def parseHarmColumn(col, evalfile):
	h = HarmParser()
	harmdict = h.parse(col)
	if harmdict:
		if harmdict['root']:
			root = harmdict['root'].upper()
			evalfile.roots.append(root)


def parseLine(line, manual, auto):
	l = line.strip().split('\t')
	parseHarmColumn(l[0], manual)		
	parseRootColumn(l[1], manual)
	parseHarmColumn(l[2], auto)
	parseRootColumn(l[3], auto)


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
					manual = EvaluationFile()
					auto = EvaluationFile()
					lines = fd.readlines()
					noheader = parseHeader(lines, manual, auto)
					print '{} vs. {}'.format(manual.filename, auto.filename)
					for line in noheader:						
						parseLine(line, manual, auto)
					manual.totalchords = len(manual.roots)
					manual.roots = collections.Counter(manual.roots)
					auto.totalchords = len(auto.roots)					
					auto.roots = collections.Counter(auto.roots)
					matches, totalunits = compare(manual, auto)
					percentage = 100.0*matches/totalunits
					print '\tSimilarity: {:.2f}% \t({} out of {} time units match their harmonic root)\n'.format(percentage,matches,totalunits)
					print '\tRoot distribution'
					print '\t',manual.filename
					for k,v in manual.roots.iteritems():
						rootperc = v*100.0/manual.totalchords
						print '\t\t{}: {:.2f}% \t({} out of {} chord annotations)'.format(k, rootperc, v, manual.totalchords)
					print '\n\t',auto.filename
					for k,v in auto.roots.iteritems():
						rootperc = v*100.0/auto.totalchords
						print '\t\t{}: {:.2f}% \t({} out of {} chord annotations)'.format(k, rootperc, v, auto.totalchords)
					print ''

			

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Evaluates manual vs. automatic **harm annotation files.''')
    parser.add_argument('-d','--rootdir', metavar='directory', help='Specify the directory of the corpus', default='../op20')
    args = parser.parse_args()
    evaluateFiles(args.rootdir)					
