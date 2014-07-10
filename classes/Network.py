import Node
import FormatInput
import numpy as np


class Network:  ##A class to keep track of all nodes in the network

	def __init__(self,matFilePath,xmlFilePath,dict):  ##Format the input data before running buildNetwork
		
		self.nodes=[]  ##List of all the nodes in the network
		self.nodesByZones={} ##Dict to organize the nodes by zone (country) (key=country name as string, value=list of Nodes)
		self.zoneSurplus={}	 ##Dict to hold surplus (key=country name as string, value=[producerSurplus,consumerSurplus])
		self.zonePrices={} 	##Dict to hold the zone prices (key=country name as string, value=time series of zone price as np.array)
		self.systemPrice=np.array([])
		self.systemProdSurplus=0
		self.systemConsSurplus=0
		self.congestionRent=0 ##Total congestion rent between zones
		

		input=FormatInput.FormatInput(matFilePath,xmlFilePath,dict)
		resultsDict=input.resultsDict
	
		self.buildNetwork(resultsDict)
	
	def buildNetwork(self, resultsDict): ##Create the network
	

		nodeList=resultsDict['nodes'] ## Assume this is of the form: [[node number(int), country(string)],...]. 
		branchList=resultsDict['branches'] ##Assume this is of the form: [[from node (int), to node (int),flow time series from 1->2(float)],...]
		genList=resultsDict['generation'] ##Assume this is of the form [[node number(int), marginal cost (float), time series for this generator(float)]],...]
				
		
		self.addAllNodes(nodeList)
		print "Added nodes..."
		self.addAllGenerators(genList)
		print "Added generators.."
		self.addAllBranches(branchList)
		print "Added branches..."
		
		self.sampleSize=len(self.nodes[0].branches[0].flow)
		for node in self.nodes:
			node.calcLoad()
		print "Calculated load in all nodes..."
		
		self.calcSurplusAllZones()
		print "Calculated the consumer and producer surplus in all zones..."

		self.calcCongestionRent()
		print "Calculated the total congestion rent between countries...Done!"
		
		self.calcSystemSurplus()
		print "done.s,ldkf"
	
	def addAllNodes(self,nodeList): ##Add all nodes in the network
	
		for node in nodeList: 
			nodeNr=int(node[0])
			nodeCountry=node[1].upper() ##All upper case because it's cool
			
			newNode=Node.Node(nodeNr,nodeCountry)
			self.nodes.append(newNode)
		
	
	def addAllGenerators(self,genList): ##Add all generators in the network
		
		
		for generator in genList:  			
			try:
				node= filter(lambda x: x.number==int(generator[0]),self.nodes)[0] 
			except IndexError: ##This error might occur if netop decides not to connect a generating node (wind farm) to the power grid. The node is removed by FormatInput, but the generator is not removed.
				print "Generator node number "+str(generator[0])+" could not be found! Skipping to next generator..." 
				continue
			genCost=generator[1]
			genTimeseries=np.array(generator[2:])
			
			node.addNewGenerator(genCost,genTimeseries)
 
	
	def addAllBranches(self,branchList): ##Add all branches (connections) in the network
		
		for branch in branchList: 
			
			try:
				node_from=filter(lambda x: x.number==branch[0],self.nodes)[0]
				node_to=filter(lambda x: x.number==branch[1],self.nodes)[0]
			except IndexError:
				print "Some of the endpoint nodes "+str(branch[0])+" and "+str(branch[1])+" for this branch could not be found! Skipping to next branch..."
				continue
				
				
			flow=np.array(branch[2:])						
			
			node_from.addNewBranch(node_to,flow) ##This automatically adds a branch in the end node ('node_to') as well. 
			

	def calcSurplusAllZones(self): ##Calculate the surplus for each zone in the network 
		
		for node in self.nodes: ##Make a dict organizing all nodes according to zone
			if(node.country not in self.nodesByZones.keys()):
				self.nodesByZones[node.country]=[node]
				continue
			
			self.nodesByZones[node.country].append(node)
			


		for zone in self.nodesByZones:
			
			nodesInZone = self.nodesByZones[zone] ##All nodes in the zone
		
			
			allGenerators=[] 
			totLoad=np.zeros(self.sampleSize)
			for node in nodesInZone: 
				allGenerators+=node.generators  ##List of all generators in the zone
				totLoad+=node.load
			
			zonePrice=self.calcZonePrice(allGenerators) ##Calculate the zone price.
			self.zonePrices[zone]=zonePrice
			
			# if(zone=="NORWAY"):
				# print zonePrice
				# print ""
				
				# for gen in allGenerators:
					# print gen.margCost
					# print gen.prod
					# print ""


			[producerSurplus,consumerSurplus]=self.calcZoneSurplus(zonePrice,allGenerators,totLoad,500) ##Ration price set to 500 euro/MW
			
			self.zoneSurplus[zone]=[producerSurplus,consumerSurplus] ##Add to network dictionary
			

	def calcZonePrice(self, allGenerators):	##Calculate the zone price
	##In this calculation, all nodes within a zone are counted as one big node.
	##This means that we assume no congestion within the zone, so that all nodes have the same node price.
	##However, this assumption does not always hold for branches from offshore nodes (wind farms) to the mainland.
	##In the North Sea case, congestion was observed 25% of the time in one such branch in Germany.
	
		allGenerators.sort(key=lambda x: x.margCost) ##Sort the generators from lowest to highest marginal cost
		numbOfGen=len(allGenerators)
		zonePrice=[]
			
		for time in range(self.sampleSize): ##We need the zone price at every time step
			alreadyAdded=False
			for i in range(numbOfGen):
				gen=allGenerators[i]
				if (gen.margCost==0): ##Skip past all generators with 0 marginal cost, they have variable production which might be 0 even though the zone produces more expensive power 
					continue
				if(gen.prod[time]==0.0): ##The first generator that produces 0 power (and is not of variable production) is the first generator that has too high a price. The marginal cost of the previous one will be the zone price 
					zonePrice.append(allGenerators[i-1].margCost)
					alreadyAdded=True
					break 			##Go to the next timestep
			
			if(not alreadyAdded):
				zonePrice.append(allGenerators[numbOfGen].margCost) ##If all generators are producing, the one with the highest price will set the zone price
		
		return np.array(zonePrice)
			
	
	def calcZoneSurplus(self,zonePrice,allGenerators,totLoad,rationPrice): ##Calculate the zone surplus
		
		
		producerSurplus=0
		#totGen=np.zeros(sampleSize)

		for gen in allGenerators:
			production = gen.prod
		#	totGen+=production
			producerSurplus+=np.sum(production*(zonePrice-gen.margCost))		
		
		consumerSurplus=np.sum(totLoad*(rationPrice-zonePrice))

		return [producerSurplus,consumerSurplus]

			
	def calcCongestionRent(self): ##To be debugged!
		##Calculate the net owner's profit due to congestion in the cables (limited cable capacity)
		##Here we ignore congestion within a zone because it is neglected when calculating the zone price.
		
		
		for node in self.nodes:

			for branch in node.branches:
				
				importNode=filter(lambda x: x.number==branch.toNode, self.nodes)[0] ##Find the node receiving the exported power 
				
				if(importNode.country==node.country): ##Skip congestion inside a zone
					continue
				
				export = branch.flow*(branch.flow>0) ##The hours with positive flow (export) remain, the rest (import) are set to 0.
				
				##OBS! Is this correct? Should there be a np.abs() here or not? 
				self.congestionRent += np.sum(export*np.abs(self.zonePrices[importNode.country] - self.zonePrices[node.country])) ##The profit made by the owners of the cable due to export to a high-price area  
		
		
	def calcSystemSurplus(self):## Is this a relevant parameter to consider? system surplus!=sum(zone surplus)
		
		self.systemPrice=np.zeros(self.sampleSize)
		systemLoad=np.zeros(self.sampleSize)
		
		for time in range(self.sampleSize):
			hourPrice=[]
			for zone in self.zonePrices.keys():
				hourPrice.append(self.zonePrices[zone][time])
				
			self.systemPrice[time]=max(hourPrice)
	
		allGenerators=[]
		
		for node in self.nodes:
			allGenerators+=node.generators
			systemLoad+=node.load
		
		[self.systemProdSurplus, self.systemConsSurplus]=self.calcZoneSurplus(self.systemPrice,allGenerators,systemLoad,500)
		
	
	
	
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
	