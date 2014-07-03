import Branch
import Generator
import numpy as np

class Node:

	rationPrice=1000
	
	def __init__ (self, number, country, load):
		self.number=number ##A number to label the node
		self.country=country ##String with the name of the country the node is placed in (e.g. "NORWAY")
		self.load=load    ##Load in the node given as a time series 
		self.generators=[] ##To hold all the generators located in the node.
		self.branches=np.array([]) ##To hold all the branches connecting this node to other nodes
		self.consumerSurplus=0
		self.producerSurplus=0
		#self.nodePrice=nodePrice
	
	
	def addNewBranch(self,toNode,flow):  ##The flow is from this node to node "toNode"
		newBranch=Branch.Branch(self.number,toNode.number,flow)
		invBranch=Branch.Branch(toNode.number, self.number, -flow)
		
		self.branches=np.append(self.branches, newBranch) ##Should there be some function called to check if the branch already exists?
		toNode.branches=np.append(toNode.branches,invBranch)
	
	def addNewGenerator(self, type, prod,margCostDict):  
		newGen = Generator.Generator(type, prod,margCostDict)
		self.generators.append(newGen)
		
		
	def calcNodeSurplus(self,listOfAllNodes):
				
		##Calculate the producer surplus
		for producer in self.generators:
			production = producer.prod
			self.producerSurplus+=np.sum(production*(self.nodePrice-producer.margCost)) ##production*price difference = prod. surplus
		
		##Calculate the consumer surplus in the node
		self.consumerSurplus += np.sum(self.load*(rationPrice-self.nodePrice))
		
		##Calculate export
		for branch in self.branches:
			export += branch.flow*(branch.flow>0) ##The hours with positive flow (export) remain, the rest (import) are set to 0.
			exportToNode=filter(lambda x: x.number==branch.toNode, listOfAllNodes)[0] ##Find the node receiving the exported power 
			branch.cableOwnerProfit += np.sum(export*(exportToNode.nodePrice-self.nodePrice)) ##The profit made by the owners of the cable due to export to a high-price area  
				
	



			