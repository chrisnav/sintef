
class Generator:    ##A tiny class to keep track of the different types of power generated in each node.
		
	def __init__(self, type, prod, margCostDict):
		self.type=type.lower() ##The type of generator, e.g type='hydro' (all in lower case).
		self.prod=prod ##The production in MW for this generator given as a time series (list where each element is the prod at that given time). 
		self.margCost=margCostDict[self.type] ##The marginal cost of this type of generator in euro/MW
