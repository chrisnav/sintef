import Branch
import Generator
import numpy as np

class Node:

	def __init__ (self, number, country, load):
		self.number=number ##A number to label the node
		self.country=country ##String with the name of the country the node is placed in (e.g. "NORWAY")
		self.load=load    ##Load in the node given as a time series
		self.generators=[] ##To hold all the generators located in the node.
		self.branches=np.array([]) ##To hold all the branches connecting this node to other nodes

	
	def addNewBranch(self,toNode,flow):  ##The flow is from this node to node "toNode"
		newBranch=Branch.Branch(self.number,toNode.number,flow)
		invBranch=Branch.Branch(toNode.number, self.number, -flow)
		
		self.branches=np.append(self.branches, newBranch) ##Should there be some function called to check if the branch already exists?
		toNode.branches=np.append(toNode.branches,invBranch)
	
	def addNewGenerator(self, type, prod,margCostDict):  
		newGen = Generator.Generator(type, prod,margCostDict)
		self.generators.append(newGen)
		
		
	def calcProducerSurplus(self):
		##Take care of import first
		
		# sampleSize=len(self.branches[0].flow)
		
		# powerExport=np.zeros(sampleSize)
		# powerImport=np.zeros(sampleSize)

		# prodSurplus=0
		
		# for branch in self.branches:
			# branchFlow=branch.flow
			# powerExport += filter(lambda x: x>0,branchFlow)
			# powerImport -= filter(lambda x: x<0,branchFlow) ##All negative values!
		
				
		# powerNeeded = self.load+powerExport+powerImport ##The total power that needs to be produced in the node as a time series
		
		# self.generators.sort(key=lambda x: x.margCost) ##Sort the list of generators from low to high marginal cost
		
		# for producer in self.generators:
		
			# priceDiff = self.nodePrice-producer.margCost	##nodePrice should be a time series (np.array)
			# producerProd = producer.prod
			
			# prodSurplus=(producerProd>powerNeeded)*priceDiff*powerNeeded + 
			
			
			# if(producerProd>powerNeeded):
				# prodSurplus+=priceDiff*powerNeeded
				# powerNeeded=0
				# break

			# prodSurplus += priceDiff*producerProd
			# powerNeeded -= producerProd





					
				
				