# haydn_op20_harm
Manually-annotated corpus of functional harmonic analysis in **harm syntax.

> If you are interested in reproducing the results of the MSc report "*Automatic harmonic analysis of classical string quartets from symbolic score*", please read the section at the end of this document.

## Description
This dataset is a set of functional harmonic analysis annotations for the Op.20 string quartets from Joseph Haydn, commonly known as the ["Sun" quartets](https://en.wikipedia.org/wiki/String_Quartets,_Op._20_(Haydn)).

### Content
The dataset contains the following scores:
```
Haydn, Joseph
	1. E-flat major, op. 20 no. 1, Hob. III-31
		I. Allegro moderato
		II. Menuetto. Allegretto
		III. Affettuoso e sostenuto
		IV. Finale. Presto
	2. C major, op. 20 no. 2, Hob. III-32	
		I. Moderato
		II. Capriccio. Adagio
		III. Menuetto. Allegretto
		IV. Fuga a 4 soggetti
	3. G minor, op. 20 no. 3, Hob. III-33
		I. Allegro con spirito
		II. Menuetto. Allegretto
		III. Poco adagio
		IV. Finale. Allegro molto
	4. D major, op. 20 no. 4, Hob. III-34
		I. Allegro di molto
		II. Un poco adagio e affettuoso
		III. Menuet alla Zingarese & Trio
		IV. Presto e scherzando
	5. F minor, op. 20 no. 5, Hob. III-35
		I. Allegro moderato
		II. Menuetto
		III. Adagio
		IV. Finale. Fuga a due soggetti
	6. A major, op. 20 no. 6, Hob. III-36
		I. Allegro di molto e scherzando
		II. Adagio. Cantabile
		III. Menuetto. Allegretto
		IV. Fuga a 3 soggetti. Allegro
```
### Structure
The general structure of the folders is as following
```
op20/<quartet_number>/<movement_number>/
```
There are six quartets numbered from 1 to 6, and the movements are numbered in roman numerals. All of the string quartets contain four movements, therefore four subfolders can be found inside every quartet folder. Example:
```
op20/1/iv
```
Represents the path to the fourth movement of the string quartet Op.20 No.1.

#### Files
Each movement contains 3 files 
```
op20n<quartet_number>-<movement_number>.krn # Contains the original score in **kern syntax
op20n<quartet_number>-<movement_number>.hrm # Contains the original score plus manual harmonic analysis
op20n<quartet_number>-<movement_number>_tsroot.krn # Contains original score plus automatic harmonic analysis
```
The harmonic annotations are included as __\*\*harm__ spines in the humdrum format. The humdrum files were originally taken from the KernScores website, and the same algorithm for automatic harmonic analysis is used, which is based in the Melisma Music Analyzer and the Humdrum-Extra tools.

### Additions
The original corpus from the KernScores websites is missing five works from this Op.20, these files have been included in this repository

```
Op. 20 No. 1 - III. Affettuoso e sostenuto
Op. 20 No. 2 - II. Capriccio. Adagio
Op. 20 No. 3 - I. Allegro con spirito
Op. 20 No. 4 - I. Allegro di molto
Op. 20 No. 4 - II. Un poco adagio e affettuoso
```

For these files, the transcription to digital was done according to the Willhelm Altmann Edition, which is freely available at the IMSLP library [here](http://imslp.org/wiki/String_Quartets,_Op.20_(Haydn,_Joseph)).


## Reproducing the evaluations done in "*Automatic harmonic analysis of classical string quartets from symbolic score*"

The necessary scripts for reproducing the results are located in the `test` branch of this repository, under the `utils` folder.

The scripts assume that you have the [Humdrum-Extras](http://extras.humdrum.org/) binaries compiled/installed in your environment.

The scripts must be run in the following order:

1. `count_chords.py` - This is a sanity-check script that extracts every manual annotation in the dataset and summarizes the number of annotations found in the dataset. Think of this as a `hello world` script to make sure your environment is working.
2. `generate_evaluation_files.py` - This script will generate a `.eval` file at the level of every humdrum file. This evaluation file has a normalized duration for the entire score and concatenates the output of manual and automatic annotations in the same file.
3. `evaluate.py` - This script applies the evaluation metric on the generated evaluation files. The output of the script shows the percentage of automatic annotations that match, in harmonic root, the manual annotations of the dataset.

The automatic analyses computed during my MSc are provided as part of the dataset (files with `_tsroot.krn` termination). If you are interested in generating those files yourself, please refer to Chapter 4 of the MSc report to find information about that process.
