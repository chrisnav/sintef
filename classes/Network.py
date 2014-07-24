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
		
		self.buildNetwork(input.resultsDict)
		
	
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
		print "Calculated the total congestion rent between countries..."
		
		self.calcSystemSurplus()
		print "Calculated system surplus...Done!"
	
	
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
			maxGen=generator[2]
			genTimeseries=np.array(generator[3:])
			
			node.addNewGenerator(genCost,maxGen,genTimeseries)
 
	
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

##########################################################################
##########################################################################


	def calcSystemSurplus(self):##Calculate the system surplus
		
		##The system price will always be equal or higher than the zone prices.
		##This means that the consumer surplus of the system will always be less than the sum
		##of the consumer surplus in the zones. The producer surplus will in turn be higher for the 
		##system than for the combined zones.
		
		
		self.systemPrice=np.zeros(self.sampleSize) 
		systemLoad=np.zeros(self.sampleSize)
		allGenerators=[]

		for node in self.nodes:
			allGenerators+=node.generators ##List of all generators in the system
			systemLoad+=node.load   ##Time series of total load in the system

		zeroCostGen=filter(lambda x: x.margCost==0.0, allGenerators) ##Variable production generators (solar, wind)
		expensiveGen = filter(lambda x: x.margCost>0.0,allGenerators) ##Other power sources
		expensiveGen.sort(key = lambda x: x.margCost) ##Sort from low to high marginal cost

		load=list(systemLoad) ##A copy

		for gen in zeroCostGen:
			load-=gen.prod		##Subtract the _production_ of the variable generators, not the max capacity. 


		for time in range(self.sampleSize):	
			loadThisHour=load[time]		##Load every time step

			for gen in expensiveGen:
				maxGen=gen.maxGen
				if(loadThisHour<=maxGen): ##We have reached the last needed generator if it can cover the remaining demand in the zone.
					self.systemPrice[time]=gen.margCost ##If load<0 at this time, this will wrong. This may happen if the demand is met by wind and solar energy. Fixed after loop.
					break
					
				loadThisHour -= maxGen	##If the generator can't cover the remaining load, subtract the generators max generation. 
		self.systemPrice=self.systemPrice*(load>0) ##If the 0 cost generators managed to fill the load at some point in time (load<0), set the system price to 0 at this time
			
		
		[self.systemProdSurplus, self.systemConsSurplus]=self.calcZoneSurplus(self.systemPrice,allGenerators,systemLoad) 
			

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

			[producerSurplus,consumerSurplus]=self.calcZoneSurplus(zonePrice,allGenerators,totLoad) 
			
			self.zoneSurplus[zone]=[producerSurplus,consumerSurplus] ##Add to network dictionary
			

	def calcZonePrice(self, allGenerators):	##Calculate the zone price  
	##In this calculation, all nodes within a zone are counted as one big node.
	##This means that we assume no congestion within the zone, so that all nodes have the same node price.
	##However, this assumption does not always hold for branches from offshore nodes (wind farms) to the mainland.
	##In the North Sea case, congestion was observed 25% of the time in one such branch in Germany.
	
		#allGenerators=filter(lambda x: x.margCost>0, allGenerators) ##Remove all 0 cost generators, they have variable production which might be 0 even though the zone produces more expensive power 
		allGenerators.sort(key=lambda x: x.margCost) ##Sort the generators from lowest to highest marginal cost
		numbOfGen=len(allGenerators)
		zonePrice=[]

		
		for time in range(self.sampleSize): ##We need the zone price at every time step
			alreadyAdded=False
			for i in range(numbOfGen):
				gen=allGenerators[i]
				if (gen.margCost==0): ##Skip past all generators with 0 marginal cost, they have variable production which might be 0 even though the zone produces more expensive power 
					continue
				if(gen.prod[time]==0.0): ##The first generator that produces 0 power (and is not of variable production) is the first generator that has too high a price. The marginal cost of the previous one will set the zone price 
					zonePrice.append(allGenerators[i-1].margCost)
					alreadyAdded=True
					break 			##Go to the next timestep

			if(not alreadyAdded):
				zonePrice.append(allGenerators[numbOfGen].margCost) ##If all generators are producing, the one with the highest price will set the zone price
		
		return np.array(zonePrice)
			
	
	def calcZoneSurplus(self,zonePrice,allGenerators,totLoad): ##Calculate the zone surplus
		
		producerSurplus=0
		rationPrice=self.nodes[0].RATION_PRICE  ##Ration price set to 500 euro/MW, see Node class
		
		for gen in allGenerators:
			cost=gen.margCost
			if(cost==20 or cost==40): ##There is no real marginal cost for producing hydro power. 
				cost=0.0			  ##OBS! These values are hard coded for a specific case since there are no markers to distinguish different types of generators in the input/results from netop (at the moment).
			producerSurplus+=np.sum(gen.prod*(zonePrice-cost))		
		
		consumerSurplus=np.sum(totLoad*(rationPrice-zonePrice))

		return [producerSurplus,consumerSurplus]

###########################################################################
###############All is fine above this line...I think#######################
###########################################################################		

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
				self.congestionRent = np.sum(export*(self.zonePrices[importNode.country] - self.zonePrices[node.country])) ##The profit made by the owners of the cable due to export to a high-price area  
				# c=[]
				# for i in range(len(export)):
					# if(export[i]>0 and (self.zonePrices[importNode.country] - self.zonePrices[node.country])[i]<0):
						# c.append(i)
				# if len(c)>0:
					# print str(node.number)+"	"+str(importNode.number)
					# print c
					# print ""
					



		
	