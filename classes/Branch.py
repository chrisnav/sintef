
class Branch: ##A tiny class to connect the nodes in the network (aka power cables) 
	def __init__(self, fromNode, toNode, flow):
		self.fromNode = fromNode ##Node number of connection point 1
		self.toNode = toNode ##Node number of connection point 2
		self.flow = flow	##Flow in MW from 1 to 2 given as a time series (each element is the flow at that given point in time).
		
		
		
		#self.cableOwnerProfit=0   ##This is the profit the company owning the cable makes when trading power between the nodes.
		