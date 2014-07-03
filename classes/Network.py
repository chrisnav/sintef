import Node
import numpy as np


class Network:

	def __init__(self,resultsDict,margCostDict):  ##input = results.mat file from the simulation     

		self.nodes=[]  ##List of all the nodes in the network
		
		
		nodeList=resultsDict['nodes'] ## Assume this is of the form: [[node number(int), country(string)],...]. 
		branchList=resultsDict['branches'] ##Assume this is of the form: [[from node (int), to node (int),flow time series from 1->2(float)],...]

		resultsLoad=resultsDict['load'] ## Assume this is of the form: [[node number(int), time series of load in the node(float)],...]
		resultsGen=resultsDict['generation'] ##Assume this is of the form [[node number(int), type(string), time series of generation in the node(float)]],...]
		
		sampleSize=len(resultsLoad[0,:])-1 ##Don't count the node number
		
		
		
		self.addAllNodes(nodeList,resultsLoad,sampleSize)
		print "Added nodes..."
		self.addAllGenerators(resultsGen,margCostDict)
		print "Added generators.."
		self.addAllBranches(branchList)
		print "Added branches...Done!"
	
	

	def addAllNodes(self,nodeList,resultsLoad,sampleSize): ##Add all the nodes
	
		for node in nodeList: 
			nodeNr=int(node[0])
			nodeCountry=node[1].upper() ##All upper case
			loadThisNode = self.getLoadTimeseries(nodeNr,resultsLoad,sampleSize) ##Time series of the load in his node, dummyIndex of no use
			newNode=Node.Node(nodeNr,nodeCountry,loadThisNode)

			self.nodes.append(newNode)
		
	
	def addAllGenerators(self,resultsGen,margCostDict): ##Add all the generators
		
		# margCostDict=self.createMargCostDict() 

		
		for generator in resultsGen:  			
			node=filter(lambda x: x.number==int(generator[0]),self.nodes)[0]
			
			genType=generator[1]
			genTimeseries=generator[2:].astype(np.float)
			
			node.addNewGenerator(genType,genTimeseries,margCostDict)
 
	
	def addAllBranches(self,branchList): ##Add all branches (connections)
		
		for branch in branchList: 
				
			node_from=filter(lambda x: x.number==branch[0],self.nodes)[0]
			node_to=filter(lambda x: x.number==branch[1],self.nodes)[0]

			flow=branch[2:]						
			
			node_from.addNewBranch(node_to,flow) ##This automatically adds a branch in the end node ('node_to') as well. 
			

	def getLoadTimeseries(self,nodeNr,timeseries,sampleSize): ##Should load be a class of it's own like generators? I don't think so...
		index=np.where(timeseries[:,0]==nodeNr)[0]
		
		if (index.size!=0):
			return timeseries[index,1:] ##Return the time series for the node in question 
			
		return np.zeros(sampleSize)
			
	
	def calcSurplus(self): ##What about the branch owner profits?
		
		consumerSurplusDict={}
		producerSurplusDict={}
		#branchOwnerProfitDict={}
		
		for node in self.nodes:			
			node.calcNodeSurplus(self.nodes)
			country=node.country
			
			if (country not in consumerSurplusDict.keys()):
				consumerSurplusDict[country]=node.consumerSurplus
				producerSurplusDict[country]=node.producerSurplus
			else:
				consumerSurplusDict[country]+= node.consumerSurplus
				producerSurplusDict[country]+= node.producerSurplus
				
		
		return[consumerSurplusDict, producerSurplusDict]

		
	def plotSurplus(self):
		pass
		
		
		
		
		
		
	
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
			
