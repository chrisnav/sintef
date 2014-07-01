import Branch
import Generator
import numpy as np

class Node:

	def __init__ (self, number, country, load):
		self.number=number ##A number to label the node
		self.country=country ##String with the name of the country the node is placed in (e.g. "NORWAY")
		self.load=load    ##Load in the node given as a time series
		self.generators=np.array([]) ##To hold all the generators located in the node.
		self.branches=np.array([]) ##To hold all the branches connecting this node to other nodes
	
	def calcProfit(self):
		pass
		## calculate the consumer and producer profit for the nodes home country, and calculate consumer profit for the countries who import power from this node
	
	def addNewBranch(self,toNode,flow):  ##The flow is from this node to node "toNode"
		newBranch=Branch.Branch(self.number,toNode.number,flow)
		invBranch=Branch.Branch(toNode.number, self.number, -flow)
		
		self.branches=np.append(self.branches, newBranch) ##Should there be some function called to check if the branch already exists?
		toNode.branches=np.append(toNode.branches,invBranch)
	
	def addNewGenerator(self, type, prod,margCostDict):  
		newGen = Generator.Generator(type, prod,margCostDict)
		self.generators=np.append(self.generators,newGen)

	
