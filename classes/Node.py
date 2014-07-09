import Branch
import Generator
import numpy as np

class Node:

	rationPrice=3
	
	def __init__ (self, number, country):
		self.number=number ##A number to label the node
		self.country=country ##String with the name of the country the node is placed in (e.g. "NORWAY")
		self.generators=[] ##To hold all the generators located in the node.
		self.branches=np.array([]) ##To hold all the branches connecting this node to other nodes
		self.consumerSurplus=0  
		self.producerSurplus=0	
	
	def addNewBranch(self,toNode,flow):  ##The flow is from this node to node "toNode"
		newBranch=Branch.Branch(self.number,toNode.number,flow)
		invBranch=Branch.Branch(toNode.number, self.number, -flow)
		
		self.branches=np.append(self.branches, newBranch) ##Should there be some function called to check if the branch already exists?
		toNode.branches=np.append(toNode.branches,invBranch)
	
	def addNewGenerator(self, margCost, prod):  
		newGen = Generator.Generator(margCost, prod)
		self.generators.append(newGen)
		
		
	def calcNodeSurplus(self,listOfAllNodes):
				
		##Calculate the producer surplus
		for producer in self.generators:
			production = producer.prod
			self.producerSurplus+=np.sum(production*(self.nodePrice-producer.margCost)) ##production*price difference = prod. surplus
		
		##Calculate the consumer surplus in the node
		self.consumerSurplus += np.sum(self.load*(self.rationPrice-self.nodePrice))
		
		##Calculate the profit of the network company due to export
		for branch in self.branches:
			export = branch.flow*(branch.flow>0) ##The hours with positive flow (export) remain, the rest (import) are set to 0.
			exportedToNode=filter(lambda x: x.number==branch.toNode, listOfAllNodes)[0] ##Find the node receiving the exported power 
			branch.cableOwnerProfit += np.sum(export*(exportedToNode.nodePrice-self.nodePrice)) ##The profit made by the owners of the cable due to export to a high-price area  
	

	def calcLoad(self):
	
		sampleSize=len(self.branches[0].flow) 
		
		totGen=np.zeros(sampleSize)
		totFlow=np.zeros(sampleSize)
		
		for gen in self.generators:
			totGen+=gen.prod
		
		for branch in self.branches:
			totFlow+=branch.flow
		
		self.load=totGen-totFlow ##flow>0 -> export. load = generated power in node - net flow out
		
			
	
	
	def calcNodalPrice(self):
		
		self.nodePrice=np.random.rand(1,len(self.branches[0].flow))