import Node
import numpy as np


class Network:  ##A class to keep track of all nodes in the network

	def __init__(self,resultsDict):  

		self.nodes=[]  ##List of all the nodes in the network
		
		
		nodeList=resultsDict['nodes'] ## Assume this is of the form: [[node number(int), country(string)],...]. 
		branchList=resultsDict['branches'] ##Assume this is of the form: [[from node (int), to node (int),flow time series from 1->2(float)],...]

	#	loadList=resultsDict['load'] ## Assume this is of the form: [[node number(int), time series of load in the node(float)],...]
		genList=resultsDict['generation'] ##Assume this is of the form [[node number(int), marginal cost (float), time series for this generator(float)]],...]
		
	#	sampleSize=len(loadList[0,:])-1 ##Don't count the node number
		
		
		
		self.addAllNodes(nodeList)
		print "Added nodes..."
		self.addAllGenerators(genList)
		print "Added generators.."
		self.addAllBranches(branchList)
		print "Added branches..."
		
		for node in self.nodes:
			node.calcLoad()
			node.calcNodalPrice()   ##Not yet implemented!!

		print "Calculated load and nodal prices in all nodes...Done!"

	
	
	
	def addAllNodes(self,nodeList): ##Add all the nodes
	
		for node in nodeList: 
			nodeNr=int(node[0])
			nodeCountry=node[1].upper() ##All upper case because it's cool
			#nodePrice=np.array(node[2:].astype(np.float))
			
			#loadThisNode = self.getLoadTimeseries(nodeNr,loadList,sampleSize) ##Time series of the load in his node, dummyIndex of no use
			newNode=Node.Node(nodeNr,nodeCountry)
			self.nodes.append(newNode)
		
	
	def addAllGenerators(self,genList): ##Add all the generators
		
		
		for generator in genList:  			
			node=filter(lambda x: x.number==int(generator[0]),self.nodes)[0]
			
			genCost=generator[1]
			genTimeseries=np.array(generator[2:])
			
			node.addNewGenerator(genCost,genTimeseries)
 
	
	def addAllBranches(self,branchList): ##Add all branches (connections)
		
		for branch in branchList: 
				
			node_from=filter(lambda x: x.number==branch[0],self.nodes)[0]
			node_to=filter(lambda x: x.number==branch[1],self.nodes)[0]

			flow=np.array(branch[2:])						
			
			node_from.addNewBranch(node_to,flow) ##This automatically adds a branch in the end node ('node_to') as well. 
			

	# def getLoadTimeseries(self,nodeNr,timeseries,sampleSize): ##Should load be a class of it's own like generators? I don't think so...
		# index=np.where(timeseries[:,0]==nodeNr)[0]
		
		# if (index.size!=0):
			# return timeseries[index,1:] ##Return the time series for the node in question 
			
		# return np.zeros(sampleSize)
			
	
	def calcSurplus(self): 
		
		consumerSurplusDict={}
		producerSurplusDict={}
		cableOwnerProfit = 0
		
		for node in self.nodes:			
			node.calcNodeSurplus(self.nodes)
			country=node.country
			
			if (country not in consumerSurplusDict.keys()): ##Add the country if it doesn't already exist 
				consumerSurplusDict[country]=node.consumerSurplus
				producerSurplusDict[country]=node.producerSurplus
			else:
				consumerSurplusDict[country]+= node.consumerSurplus
				producerSurplusDict[country]+= node.producerSurplus
			
			for branch in node.branches:
				cableOwnerProfit += branch.cableOwnerProfit
		
		return[consumerSurplusDict, producerSurplusDict, cableOwnerProfit]
	
		
		
		
	
	# def createMargCostDict(self):  ##Dictionary to hold all pairs of generator_type - marginal_cost. Can be improved! Like loading in the keywords first and asking the user for the price... 

		# print "Please enter the types of generators in the network with associated marginal cost."
		# print "The input should be separated by a space, like this example: solar 0"
		# print "When all pairs are entered, type in '*' to end."

		# dict={} 
		# while True:
			# s=raw_input("Please enter a new pair: ").lower()
			# if s[0]=='*':
				# break
			# [type,margCost]=s.split()
			# dict[type]=float(margCost)
		
		# return dict
	