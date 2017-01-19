import sys	#used to read command line arguments
import argparse #used to parse command line arguments
import re	#used to parse input file
import Simulation as sim
import matplotlib.pyplot as plt	#used to plot results

#	TODO
#maybe - printout of input mechanism
#maybe - condense code for parsing mechanism

#Sintax definitions-------------------------------------------------------------
irreversibleSymbol = '->'
reversibleSymbol = '<=>'
separator = '+'
assignOperator = '='
concentrationDelimiters = ['[',']']	# [prefix, suffix]
outputColSep = '\t'
#Simulation definitions (default values)----------------------------------------
steps = 1000
stepTime = 1
#-------------------------------------------------------------------------------

#Parse command-line arguments
argParser = argparse.ArgumentParser(description='''Simulates chemical reaction \
	kinetics given a set of elementary reactions.''')
argParser.add_argument( dest='inputFile', 
	help='''The input file containing elementary steps of the reaction, \
	kinetic constants and initial concentrations, see example.input.''')
argParser.add_argument('-o','-output-file', dest='outputFile',
	help='''Destination file for the datapoints calculated. By default data\
	is discarded.''')
argParser.add_argument('-s','--steps', dest='steps', type=int, 
	help='''Number of steps to perform.''')
argParser.add_argument('-t','--time-step', dest='timeStep', type=float, 
	help='''Time for each step in seconds, assuming kinetic constants are given in 1/S.''')
options = argParser.parse_args()
if options.steps != None:
	steps = options.steps
if options.timeStep != None:
	stepTime = options.timeStep

#Parse reaction mechanism data
simData = sim.Simulation() #mechanism data

inputFile = open(options.inputFile, 'r')

#Escape some of the syntax definitions, to use them as literals in RegExs
irreversibleSymbol = re.escape(irreversibleSymbol)
reversibleSymbol = re.escape(reversibleSymbol)
separator = re.escape(separator)
assignOperator = re.escape(assignOperator)

for line in inputFile:
	if re.search( irreversibleSymbol, line) != None:
		#Add a single, irreversible, elementary reaction
		chemicals = []	#Names of reagents and products
		coefficients = []	#Ordered as the names
		constName = ''
		constVal = 0
		
		line = re.split(' *'+irreversibleSymbol+' *', line)
		line[0] = re.split( ' *'+separator+' *', line[0])	#Reagents
		line[1] = re.split( ' *'+separator+' *', line[1])	#Products + const
		lastChemicalAndConst = re.split( ' +', line[1][-1], maxsplit=1)
		line[1][-1] = lastChemicalAndConst[0]
		const = re.split( ' *'+assignOperator+' *', lastChemicalAndConst[1])
		constName = const[0]
		constVal = float( const[1] )
		for word in line[0]:
			coefficients.append(-1.0)
			coefficient = re.search( '^[0-9\.e\-]+', word)
			if coefficient != None:
					word = re.sub( re.escape(coefficient.group(0)), '', word)
					coefficients[-1] = -float(coefficient.group(0))
			chemicals.append(word)
		for word in line[1]:
			coefficients.append(1.0)
			coefficient = re.search( '^[0-9\.e\-]+', word)
			if coefficient != None:
					word = re.sub( re.escape(coefficient.group(0)), '', word)
					coefficients[-1] = float(coefficient.group(0))
			chemicals.append(word)
			
		simData.addReaction(chemicals, coefficients, constName, constVal)
		
	elif re.search( reversibleSymbol, line) != None:
		#Add two elementary reactions (direct and inverse)
		chemicals = []	#Names of reagents and products
		coefficients = []	#Ordered as the names
		dirConstName = ''
		dirConstVal = 0
		invConstName = ''
		invConstVal = 0
		
		line = re.split(' *'+reversibleSymbol+' *', line)
		line[0] = re.split( ' *'+separator+' *', line[0])	#Reagents
		line[1] = re.split( ' *'+separator+' *', line[1])	#Products + consts
		lastChemicalAndConst = re.split( ' +', line[1][-1], maxsplit=1)
		line[1][-1] = lastChemicalAndConst[0]
		const = re.split( '(?: *'+assignOperator+' *)|(?: +)', lastChemicalAndConst[1])
		dirConstName = const[0]
		dirConstVal = float( const[1] )
		invConstName = const[2]
		invConstVal = float( const[3] )
		for word in line[0]:
			coefficients.append(-1.0)
			coefficient = re.search( '^[0-9\.e\-]+', word)
			if coefficient != None:
					word = re.sub( re.escape(coefficient.group(0)), '', word)
					coefficients[-1] = -float(coefficient.group(0))
			chemicals.append(word)
		for word in line[1]:
			coefficients.append(1.0)
			coefficient = re.search( '^[0-9\.e\-]+', word)
			if coefficient != None:
					word = re.sub( re.escape(coefficient.group(0)), '', word)
					coefficients[-1] = float(coefficient.group(0))
			chemicals.append(word)
		
		simData.addReaction(chemicals, coefficients, dirConstName, dirConstVal)
		for i in range(0,len(coefficients)):
			coefficients[i] = -coefficients[i]
		simData.addReaction(chemicals, coefficients, invConstName, invConstVal)
	else:
		#Set the initial concentration of one of the chemicals
		line = re.sub( re.escape(concentrationDelimiters[1])+' *'+assignOperator+' *', ' ', line)
		line = re.sub( re.escape(concentrationDelimiters[0]), '', line)
		line = re.split( ' ', line)
		simData.addChemical( line[0], float(line[1]))
inputFile.close()

#Print some info on what has been parsed
print('Parsed data:')
print(simData.concentrationsNames)
print(simData.concentrationsValues)

#Run simulation, data is stored as [ [A,B,C,..(step1)] , [A,B,..(step2)] , ... ]
if steps > 0:
	resultsByStep = [simData.concentrationsValues]
	for i in range(0, steps-1):
		resultsByStep.append(simData.step( stepTime ))
	timeValues = range(0, steps)
	for i in range(0, steps):
		timeValues[i] = timeValues[i]*stepTime
	
	#Generate output file
	if options.outputFile != None:
		outputFile = open(options.outputFile, 'w')
		#write header
		outputFile.write('Time')
		for name in simData.concentrationsNames:
			outputFile.write(outputColSep+
				concentrationDelimiters[0]+name+concentrationDelimiters[1])
		outputFile.write('\n')
		#write datapoints
		for step in range(0,len(resultsByStep)):	
			outputFile.write( str(timeValues[step]) )
			for conc in resultsByStep[step]:
				outputFile.write(outputColSep+str(conc))
			outputFile.write('\n')
		outputFile.close()
	
	#Build graph
	plt.figure().canvas.set_window_title(sys.argv[0]+' - Results')
	resultsByChemical = []
	for chemical in range(0,len(simData.concentrationsValues)):
		for step in range(0, steps):
			resultsByChemical.append( resultsByStep[step][chemical] )
		plt.plot( timeValues, resultsByChemical, 
			label=concentrationDelimiters[0]+simData.concentrationsNames[chemical]+concentrationDelimiters[1])
		resultsByChemical = []
	plt.ylabel('Concentration [M]')
	plt.xlabel('Time [S]')
	plt.legend(fontsize='medium')
	plt.show()


	
