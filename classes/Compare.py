import numpy as np
import matplotlib.pyplot as plt


class Compare: ##A class to compare prices and surplus in different Networks.

	def __init__(self,listOfNetworks, listOfNetworkLabels):
		self.networks=listOfNetworks	##List of all networks to compare
		self.labels=listOfNetworkLabels	##List of the names/tags of the different networks
		
		self.zoneLabels=[]
		for zone in listOfNetworks[0].zoneSurplus.keys():
			self.zoneLabels.append(zone) ##List of the name of all the zones in the network (assumed to be equal for all networks in self.networks)
	
		self.colors=['b','r','g','c','m','y','k'] ##List of some basic colours to be used in plotting.

		
		
	def compareConsumerSurplus(self,save): ##A function to compare the consumer surplus in each zone in the different networks
										   ##The param. 'save'(boolean) is the choice to save or not (True/False)
		consumer=[]
		for network in self.networks:
			consumerThisNetwork=[]
			for zone in self.zoneLabels:
				consumerThisNetwork.append(network.zoneSurplus[zone][1]*10**(-6)) ##Add the consumer surplus in every zone in every network
			consumer.append(consumerThisNetwork)
		##Makes a bar plot	
		self.barPlot(consumer,self.zoneLabels,"Consumer Surplus","Zones","Million Euros",save)
	
	
	def compareProducerSurplus(self,save):  ##A function to compare the producer surplus in each zone in the different networks 
											##The param. 'save'(boolean) is the choice to save or not (True/False)
		producer=[]
		for network in self.networks:
			producerThisNetwork=[]
			for zone in self.zoneLabels:
				producerThisNetwork.append(network.zoneSurplus[zone][0]*10**(-6))	##Add the producer surplus in every zone in every network
			producer.append(producerThisNetwork)
		##Makes a bar plot
		self.barPlot(producer,self.zoneLabels,"Producer Surplus","Zones","Million Euros",save)
	
	
	def compareSystemPrices(self,save):		##A function to compare the system prices in the different networks
											##The param. 'save'(boolean) is the choice to save or not (True/False)
		t=range(self.networks[0].sampleSize)
		plt.figure()
		plt.title("System Price")
		plt.xlabel("Time")
		plt.ylabel("Euros per MWh")
		ymax=0
		ymin=100		
		
		for i in range(len(self.networks)):
			try:
				systemPrice=self.networks[i].systemPrice
				plt.plot(t,systemPrice,color=self.colors[i],label=self.labels[i]) ##Plot the system price
				plt.axhline(y=sum(systemPrice)/self.networks[i].sampleSize, xmin=min(t), xmax=max(t),label="average of "+self.labels[i],color=self.colors[i]) ##Plot the average system price
				
				if(min(systemPrice)<ymin):	##To set the y-limits
					ymin=min(systemPrice)
				if(max(systemPrice)>ymax):
					ymax=max(systemPrice)
					
			except IndexError: 	##In the unlikely event that more than 7 networks are compared...
				print "Out of standard colours! If you need to compare more than 7 networks, please extend the hard coded colour list..."
		
		plt.ylim([ymin-10,ymax+15])
		plt.legend()
		
		if(save):
			plt.savefig("System Price.eps")
		
		#plt.show()
	
	
	def compareZonePrices(self, save, zone):	##A function to compare the prices in a single zone between the different networks
												##The param. 'save'(boolean) is the choice to save or not (True/False)
		t=range(self.networks[0].sampleSize)
		plt.figure()
		plt.title("Zone Price in "+zone)	##'zone' is a string that should be the label/name of the zone. 'zone' must be a valid key in my_network.zonePrices
		plt.xlabel("Time")
		plt.ylabel("Euros per MWh")
		ymax=0
		ymin=100
		
		for i in range(len(self.networks)):
			try:
				zonePrice=self.networks[i].zonePrices[zone]
				plt.plot(t,zonePrice,self.colors[i],label=self.labels[i])
				plt.axhline(y=sum(zonePrice)/self.networks[i].sampleSize, xmin=min(t), xmax=max(t),label="average of "+self.labels[i],color=self.colors[i])
				
				if(min(zonePrice)<ymin):
					ymin=min(zonePrice)
				if(max(zonePrice)>ymax):
					ymax=max(zonePrice)
					
			except IndexError: 	##In the unlikely event that more than 7 networks are compared...
				print "Out of standard colours! If you need to compare more than 7 networks, please extend the hard coded colour list..."
				return
			except KeyError:  ##If 'zone' is not a valid key in one of the networks
				print "The zone provided in the input cannot be found."
				return
				
		plt.ylim([ymin-10,ymax+20])
		plt.legend()
		
		if(save):
			plt.savefig("Zone Price "+zone+".eps")
		
		#plt.show()
	
	def compareSystemSurplus(self,save): ##A function to compare the system surplus between the zones. The first network in self.networks will be used as a benchmark to see the relative change between networks	
										 ##The param. 'save'(boolean) is the choice to save or not (True/False)
		surplusBars=[]
		labels=['consumer','producer']#,'congestion']
		
		consumerBenchmark=self.networks[0].systemConsSurplus
		producerBenchmark=self.networks[0].systemProdSurplus
		#congestionBenchmark=self.networks[0].congestionRent
		
		for network in self.networks:
			surplusBars.append([network.systemConsSurplus/consumerBenchmark,network.systemProdSurplus/producerBenchmark])#, network.congestionRent/congestionBenchmark])

		##Makes a bar plot
		self.barPlot(surplusBars, labels, "System Surplus", "", "Relative size compared to "+self.labels[0],save,height=1.2)
	
	def compareWindGen(self,save):
		
		plots=[]

		for network in self.networks:
			allGen=[]	
			prod=np.zeros(network.sampleSize)
			for node in network.nodes:
				allGen+=node.generators
			for gen in allGen:
				if(gen.margCost!=0):
					continue
				prod+=gen.prod
			plots.append(prod*10**(-3))
		
		t=range(self.networks[0].sampleSize)
		plt.figure()
		plt.title("Wind and solar energy production")
		plt.xlabel("Time")
		plt.ylabel("GWh")
		
		for i in range(len(plots)):
			plt.plot(t,plots[i],label=self.labels[i],color=self.colors[i])
		
		plt.legend()
		
		if(save):
			plt.savefig("Wind production.eps")
		
		
	def barPlot(self,bars,barLabels,title,xlabel,ylabel,save, **kwargs):	##A function to plot a bar plot
	
		placement=np.arange(len(barLabels))+1	##Placement along the x-axis for the bars
		width=1/float(len(bars)+1)	##Width of a bar
		
		fig, ax = plt.subplots()
		plots=[]

		for i in range(len(bars)):
			try:
				plot=ax.bar(placement+i*width,bars[i],width,color=self.colors[i])
			except IndexError: 	##In the unlikely event that more than 7 networks are compared...
				print "Out of standard colours! If you need to compare more than 7 networks, please extend the hard coded colour list..."
				# shade=float(i)*width
				# plot=ax.bar(placement+i*width,bars[i],width,color=str(shade))
				
			plots.append(plot[0])
				
		ax.set_xlabel(xlabel)
		ax.set_ylabel(ylabel)
		ax.set_xbound(0,len(barLabels)+1.5)
		if(len(kwargs)==1):	##To set the y-bound if 'height' is given as en argument
			ax.set_ybound(0,kwargs.get('height',1))
		ax.set_title(title)
		ax.set_xticks(placement+len(bars)*0.5*width)
		ax.set_xticklabels(barLabels)
		ax.legend(plots,self.labels)

		if(save):	##Save the figure... or not
			plt.savefig(title+".eps")	
		
		#plt.show()
	
	
	

	