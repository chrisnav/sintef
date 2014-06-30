import Node

class Network:

	def __init__ (self, filenameInput):  ##input = results.mat file from the simulation     

	self.resultsDict = io.loadmat(filenameInput)
		##Add the nodes in the grid:
		
		self.nodes=[] ##nodes in the network
		
		##create list with ll the stuff needed to create an object of the Node class
		
		for i in listWithAllTheStuff: 
			newNode=Node(i[0],i[1],i[2],i[3],i[4])
			self.nodes.append(newNode)
		
		
		for i in listOfAllTheBranchRelatedStuff:
			
		##Add all the connections...
		
	def addNode(self, country, number, load, generation, genCost):
		self.nodes.append(Node.Node(country, number, load, generation, genCost))
	