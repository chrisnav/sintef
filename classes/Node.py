import Branch
import Generator
import numpy as np

class Node:

	rationPrice=3
	
	def __init__ (self, number, country):
		self.number=number ##A number to label the node
		self.country=country ##String with the name of the country the node is placed in (e.g. "NORWAY")
		self.generators=[] ##To hold all the generators located in the node.
		self.branches=[] ##To hold all the branches connecting this node to other nodes

	
	def addNewBranch(self,toNode,flow):  ##Add a branch from self to toNode
		newBranch=Branch.Branch(self.number,toNode.number,flow) ##The flow is positive _from_ this node _to_ node "toNode"
		invBranch=Branch.Branch(toNode.number, self.number, -flow) 
		
		self.branches.append(newBranch)
		toNode.branches.append(invBranch)	##Also add branch in the other node
	
	def addNewGenerator(self, margCost, prod):  ##Add a generator in the node
		newGen = Generator.Generator(margCost, prod)
		self.generators.append(newGen)
		

	def calcLoad(self): ##Calculates the load in the node
	
		##OBS! In the case of generators with variable production (wind, solar...), any harvested power	
		##that is not actually needed/used will be counted as a load! This is because this function 
		##assumes that power is conserved in every node (flow in + generation = load + flow out).
		##This will however not be a problem when summing up all load and generation in a zone,
		##the 'fake' load will be absorbed by the 'fake' production.
	
	
		sampleSize=len(self.branches[0].flow) 
		
		totGen=np.zeros(sampleSize)
		totFlow=np.zeros(sampleSize)
		
		for gen in self.generators:
			totGen+=gen.prod
		
		for branch in self.branches:
			totFlow+=branch.flow
		
		self.load=totGen-totFlow		##flow>0 -> export. load = generated power in node - net flow out
		

		
			
	
