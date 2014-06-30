class Node:
	def __init__ (self, number, country, load, generation, genCost):
		self.country=country ##String with the name of the country the node is placed in (e.g. "Norway")
		self.number=number ##Int which is the node number
		self.load=load    ##Load in the node (as in power demand)
		self.generation=generation ##
		self.genCost=genCost
		self.connections=[]
	
	def calcProfit(self):
		pass
		## calculate the consumer and producer profit for the nodes home country, and calculate consumer profit for the countries who import power from this node
	
	def addNewConnection(self,nodeNumber,flow):  ##Connections are one-way! This is FROM the "self-node" TO the node with node number "nodeNumber"
		self.connections.append([nodeNumber,flow])
	
	def updateFlow(self,nodeNumber,flow):
		index = connectionIndex(nodeNumber)
		if(index==-1):
			print "The branch does not exist!"
			return			
		self.connections[index][1]=flow ##Update the flow (from this node to the other)

	
	def connectionIndex(self,nodeNumber):
		index=0
		for i in self.connections:
			if(i[0]==nodeNumber):
				return index 
			index+=1		
		return -1