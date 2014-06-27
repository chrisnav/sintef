
from __future__ import division     # To assure that division between two integers gives a sensible result
import sys
import numpy  as np                 # A (big) library for doing array oriented numerics
import scipy.io as io
import matplotlib as mpl            # A plotting framework 
#from matplotlib import rc           # Configuration files
import matplotlib.pyplot as plt # A plotting framework similar to MATLAB

class Network:

	def __init__ (self,filenameInput):  ##input = results.mat file from the simulation
		self.resultsDict = io.loadmat(filenameInput)
		## Add the nodes in the grid:
		
		self.nodes=[] ##nodes in the network
		
		##create list with ll the stuff needed to create an object of the Node class
		
		for i in listWithAllTheStuff: 
			newNode=Node(i[0],i[1],i[2],i[3],i[4])
			self.nodes.append(newNode)
		
		
		for i in listOfAllTheBranchRelatedStuff:
			
		##Add all the connections...
		
		##Do more stuff!
		
		
class Node:
	def __init__ (self, country, number, load, generation, genCost)
		self.country=country
		self.number=number
		self.load=load    #load as in power demand
		self.generation=generation
		self.genCost=genCost
		self.loadCost=loadCost
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
		
def main(argv):
	pass
	
	
	
	
if __name__ == "__main__":
    main(sys.argv[1:])
