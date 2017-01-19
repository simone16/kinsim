class Simulation:
	def __init__(self):
		self.concentrationsNames = []	#concentrations of the species involved
		self.concentrationsValues = []
		self._concentrationsValuesBuffer = []
	
		self.reactions = []
	
	def addReaction(self, names, coefficients, constName, constVal):
		newReaction = Reaction()
		for i in range(0,len(names)):
			newReaction.chemicals.append( self.addChemical( names[i], 0.0) )
			newReaction.coefficients.append( coefficients[i])
		newReaction.constantName = constName
		newReaction.constantValue = constVal
		print( 'New reaction:' )
		print( newReaction.chemicals )
		print( newReaction.coefficients )
		print( constName+' = '+str(constVal) )
		self.reactions.append( newReaction )
			
		
	
	def addChemical(self, name, concentration):
		for i in range(0,len(self.concentrationsNames)):
			if name == self.concentrationsNames[i]:
				self.concentrationsValues[i] = concentration
				self._concentrationsValuesBuffer[i] = concentration
				return i
		self.concentrationsNames.append(name)
		self.concentrationsValues.append(concentration)
		self._concentrationsValuesBuffer.append(concentration)
		return len(self.concentrationsNames)-1
	
	def step(self, timestep):
		for reaction in self.reactions:
			dx= reaction.constantValue*timestep	# Reaction progress as in dx/dt = [A]*[B]*...*k
			for i in range(0,len(reaction.coefficients)):
				if reaction.coefficients[i] < 0:
					# Reagents only are multiplied toghether
					dx *= self.concentrationsValues[ reaction.chemicals[i] ]
			for i in range(0,len(reaction.coefficients)):
				self._concentrationsValuesBuffer[ reaction.chemicals[i] ] = self.concentrationsValues[ reaction.chemicals[i] ] + reaction.coefficients[i]*dx
		self.concentrationsValues = self._concentrationsValuesBuffer
		return self.concentrationsValues[:]
	
class Reaction:
	def __init__(self):
		self.chemicals = []		#Referred to by index
		self.coefficients = []
		self.constantValue = 0
		self.constantName = ''
		
