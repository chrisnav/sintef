import Node

class Network:

	def __init__ (self, filenameInput):  ##input = results.mat file from the simulation     

		resultsDict = io.loadmat(filenameInput) ##OBS! I do not know how all of the input will be ordered in this file, so this is more of pseudo code atm...
		self.nodes=[]  ##List of all the nodes in the network
		
		nodeList=resultsDict['nodes'] ## Assume this is of the form: [node number, country]
				
		for node in nodeList: ##Add all the nodes
			self.addNode(node)
	
		branchList=resultsDict['branches'] ##Assume this is of the form: [from (node number), to (node number)]
	
		for branch in branchList: ##Add all branches (connections) in the network, with initial flow = 0
			index_from=self.findNode(branch[0])
			index_to=self.findNode(branch[1])
			
			if((index_from==-1) or (index_to==-1)):
				print "Node does not exist in network!"
				continue
				
			node_from=self.nodes[index_from]
			node_to=self.nodes[index_to]
			
			node_from.addNewConnection(branch[1],0.0) ##Set initial flow both ways to 0
			node_to.addNewConnection(branch[0],0.0)  
		
		
		self.timeseriesGeneration=resultsDict['generation'] ##Assume this is of the form [[node numb, sampled gen. values for this node],...]
		self.timeseriesLoad=resultsDict['load'] ##Assume this is the sampled generation for all the nodes (row = generation in a node. Every column is one sample, so )
		
		
		
		
	def addNode(self, nodeInfo):
		[number, country] = nodeInfo
		self.nodes.append(Node.Node(number, country, 0.0, 0.0, 0.0)) ##Set initial load, generation and generation cost to 0
	
	def findNode(self, nodeNumber):
		index=0
		for node in self.nodes:
			if (node.number==nodeNumber):
				return index
			index+=1
		return -1
		
	def updateNetwork(self, time): ##Update the network 1 hour (1 timestep). The flow, generation and load is updated in all nodes
		
		
	