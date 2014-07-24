import numpy as np
import matplotlib.pyplot as plt

class Compare:

	def __init__(self,listOfNetworks, listOfNetworkLabels):
		self.networks=listOfNetworks
		self.labels=listOfNetworkLabels
		
		self.zoneLabels=[]
		for zone in listOfNetworks[0].zoneSurplus.keys():
			self.zoneLabels.append(zone)
	
		self.colors=['b','r','g','c','m','y','k']

		
		
	def compareConsumerSurplus(self,save):
		consumer=[]
		for network in self.networks:
			consumerThisNetwork=[]
			for zone in self.zoneLabels:
				consumerThisNetwork.append(network.zoneSurplus[zone][1]*10**(-6))
			consumer.append(consumerThisNetwork)
			
		self.barPlot(consumer,self.zoneLabels,"Consumer Surplus","Zones","Million Euros",save)
	
	
	def compareProducerSurplus(self,save):
		producer=[]
		for network in self.networks:
			producerThisNetwork=[]
			for zone in self.zoneLabels:
				producerThisNetwork.append(network.zoneSurplus[zone][0]*10**(-6))
			producer.append(producerThisNetwork)
			
		self.barPlot(producer,self.zoneLabels,"Producer Surplus","Zones","Million Euros",save)
	
	
	def compareSystemPrices(self,save):
		t=range(self.networks[0].sampleSize)
		plt.figure()
		plt.title("System Price")
		plt.xlabel("Time")
		plt.ylabel("Euros per MWh")
		ymax=0
		ymin=1000		
		
		for i in range(len(self.networks)):
			try:
				systemPrice=self.networks[i].systemPrice
				plt.plot(t,systemPrice,color=self.colors[i],label=self.labels[i])
				plt.axhline(y=sum(systemPrice)/self.networks[i].sampleSize, xmin=min(t), xmax=max(t),label="average of "+self.labels[i],color=self.colors[i])
				
				if(min(systemPrice)<ymin):
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
	
	
	def compareZonePrices(self, save, zone):	##Maximum 7 networks can be compared at the same time!
		
		t=range(self.networks[0].sampleSize)
		plt.figure()
		plt.title("Zone Price in "+zone)
		plt.xlabel("Time")
		plt.ylabel("Euros per MWh")
		ymax=0
		ymin=1000
		
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

		plt.ylim([ymin-10,ymax+20])
		plt.legend()
		
		if(save):
			plt.savefig("Zone Price "+zone+".eps")
		
		#plt.show()
	
	def compareSystemSurplus(self,save):
	
		surplusBars=[]
		labels=['consumer','producer']#,'congestion']
		
		consumerBenchmark=self.networks[0].systemConsSurplus
		producerBenchmark=self.networks[0].systemProdSurplus
		#congestionBenchmark=self.networks[0].congestionRent
		
		for network in self.networks:
			surplusBars.append([network.systemConsSurplus/consumerBenchmark,network.systemProdSurplus/producerBenchmark])#, network.congestionRent/congestionBenchmark])

		self.barPlot(surplusBars, labels, "System Surplus", "", "Relative size compared to "+self.labels[0],save,height=1.2)
	
	def barPlot(self,bars,barLabels,title,xlabel,ylabel,save, **kwargs):
	
		placement=np.arange(len(barLabels))+1
		width=1/float(len(bars)+1)
		
		fig, ax = plt.subplots()
		plots=[]

		for i in range(len(bars)):
			try:
				plot=ax.bar(placement+i*width,bars[i],width,alpha=0.6,color=self.colors[i])
			except IndexError: 	##In the unlikely event that more than 7 networks are compared...
				print "Out of standard colours! If you need to compare more than 7 networks, please extend the hard coded colour list..."
				# shade=float(i)*width
				# plot=ax.bar(placement+i*width,bars[i],width,color=str(shade))
				
			plots.append(plot[0])
				
		ax.set_xlabel(xlabel)
		ax.set_ylabel(ylabel)
		ax.set_xbound(0,len(barLabels)+1.5)
		if(len(kwargs)==1):
			ax.set_ybound(0,kwargs.get('height',1))
		ax.set_title(title)
		ax.set_xticks(placement+len(bars)*0.5*width)
		ax.set_xticklabels(barLabels)
		ax.legend(plots,self.labels)

		if(save):
			plt.savefig(title+".eps")	
		
		#plt.show()
	
	
	
	
	# bars1_rel=(bars2/bars1 -1)*100

	# bars1_rel[3]=0
	# fig_rel, ax_rel = plt.subplots()
	
	# plot_rel=ax_rel.bar(placement-width*0.5,bars1_rel,width,color='b')
	
	# ax_rel.set_xlabel(xlabel)
	# ax_rel.set_ylabel("% change")
	# ax_rel.set_xbound(0,len(zoneLabels)+1.5)
	# ax_rel.set_ybound(0.8)
	# ax_rel.axhline(y=0.0,c='r')
	# ax_rel.set_title("Relative change from radial to meshed: "+title)
	# ax_rel.set_xticks(placement)
	# ax_rel.set_xticklabels(zoneLabels)

	