class Node:
	def __init__ (self, country, number, load, generation, genCost):
		self.country=country
		self.number=number
		self.load=load    #load as in power demand
		self.generation=generation
		self.genCost=genCost
		self.connections=[]
	
	def calcProfit(self):
		pass
		## calculate the consumer and producer profit for the nodes home country, and calculate consumer profit for the countries who import power from this node
	
	def addNewConnection(self,nodeNumber,capacity,flow):  ##Connections are one-way! This is FROM the "self-node" TO the node with node number "nodeNumber"
		self.connections.append([nodeNumber,capacity,flow])
	
	def updateConnection(self,nodeNumber,capacity,flow):
		index = connectionIndex(nodeNumber)
		if(index==-1):
			print "The branch does not exist!"
			return
			
		self.connections[index]=[nodeNumber,capacity,flow]
	
	def connectionIndex(self,nodeNumber):
		index=0
		for i in self.connections:
			if(i[0]==nodeNumber):
				return index 
			index+=1
		
		return -1