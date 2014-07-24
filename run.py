
from __future__ import division     # To assure that division between two integers gives a sensible result
import sys
import numpy  as np                 # A (big) library for doing array oriented numerics
import scipy.io as io
import matplotlib as mpl            # A plotting framework 
#from matplotlib import rc           # Configuration files
import matplotlib.pyplot as plt # A plotting framework similar to MATLAB
from classes import Node
from classes import Network
from classes import Generator
from classes import Compare
import xml.etree.ElementTree as ET

		

		
def main(argv):
	##This should not be hardcoded!
	dict={1:'be',2:'de',3:'dk',4:'uk',5:'uk',6:'nl',7:'no',21:'be',22:'de',23:'dk',24:'uk',25:'uk',26:'nl',27:'no',28:'de',29:'dk',30:'nl',31:'nl',91:'no',92:'dk',93:'de',94:'nl',95:'be',96:'uk',102:'de',103:'dk',104:'uk',107:'no'}

	matFilePath_meshed='C:\\Users\\christiann\\Desktop\\NetOp_Toolbox\\Net-Op DTOC 64bit 2013-02-15\\results_casestudy_meshed\\results.mat'
	xmlFilePath_meshed='C:\\Users\\christiann\\Desktop\\NetOp_Toolbox\\Net-Op DTOC 64bit 2013-02-15\\results_casestudy_meshed\\case_auto.xml'   ##The auto-generated xml file where all the new nodes and branches are also listed
	
	matFilePath_radial='C:\\Users\\christiann\\Desktop\\NetOp_Toolbox\\Net-Op DTOC 64bit 2013-02-15\\results_casestudy_radial\\results.mat'
	xmlFilePath_radial='C:\\Users\\christiann\\Desktop\\NetOp_Toolbox\\Net-Op DTOC 64bit 2013-02-15\\results_casestudy_radial\\case_auto.xml'   ##The auto-generated xml file where all the new nodes and branches are also listed

	time=63
	print "meshed:"
	northSea_meshed=Network.Network(matFilePath_meshed,xmlFilePath_meshed,dict)
	
	for node in northSea_meshed.nodes:
		if node.number>90 and node.number<100:
			avL=sum(node.load)/len(node.load)
			print node.number
			print node.load[time]/avL
			print ""
	
	# for node in northSea_meshed.nodes:
		# if node.number>90 and node.number<100:
			# continue
		# if node.number<10:
			# print node.generators[0].prod[time]*10**(-3)
		# for branch in node.branches:
			
			# print str(branch.fromNode)+" "+str(branch.toNode)			
			# print branch.flow[time]*10**(-3)
			# print ""
	print ""
	print "radial:"
	northSea_radial=Network.Network(matFilePath_radial,xmlFilePath_radial,dict)
	for node in northSea_radial.nodes:
		if node.number>90 and node.number<100:
			avL=sum(node.load)/len(node.load)
			print node.number
			print  node.load[time]/avL
			print ""
	# for node in northSea_radial.nodes:
		# if node.number>90 and node.number<100:
			# continue
		# if node.number<10:
			# print node.generators[0].prod[time]*10**(-3)
		# for branch in node.branches:
			
			# print str(branch.fromNode)+" "+str(branch.toNode)			
			# print branch.flow[time]*10**(-3)
			# print ""
	# print northSea_radial.congestionRent
	print ""
	
	# for node in northSea_radial.nodes:
		# for branch in node.branches:
			# print str(branch.fromNode)+" "+str(branch.toNode)			
			# totFlow=sum(np.abs(branch.flow))
			# print 100*(sum(filter(lambda x: np.round(x)>0,branch.flow))
			# print ""
	# print ""
	# b=[]
	# for node in northSea_radial.nodes:
		# for branch in node.branches:
			# b.append(np.round(branch.flow))
	# n=len(b)/2
	# z=np.zeros(100)
	# for flow in b:
		# for i in range(100):
			# if flow[i]==0:
				# z[i]+=0.5
			# print str(branch.fromNode)+" "+str(branch.toNode)
			# b=filter(lambda x: np.round(x)==0, branch.flow)
			# print len(b)
			# print ""
	# print "average percent of dead branches per hour: "+str(sum(z)/n)

	# compNorthSea = Compare.Compare([northSea_radial,northSea_meshed],["radial","meshed"])
	compNorthSea = Compare.Compare([northSea_meshed,northSea_radial],["meshed","radial"])
	
	# compNorthSea.compareSystemSurplus(False)
	# compNorthSea.compareSystemPrices(False)
	# compNorthSea.compareZonePrices(False, "DK")
	# compNorthSea.compareZonePrices(False,"NL")
	# compNorthSea.compareProducerSurplus(False)	
	# compNorthSea.compareConsumerSurplus(False)

	plt.show()

	# meshed=[]
	# labelsMeshed=[]
	# radial=[]
	# labelsRadial=[]
	# for z in northSea_meshed.nodesByZones.keys():
		
		# labelsMeshed.append(z)
		# labelsRadial.append(z)
	
		# varProd=np.zeros(100)
		# for node in northSea_meshed.nodesByZones[z]:
			# for gen in node.generators:
				# if(gen.margCost==0):
					# varProd+=gen.prod
		# meshed.append(sum(varProd)*10**(-3))
		
		# varProd=np.zeros(100)
		# for node in northSea_radial.nodesByZones[z]:
			# for gen in node.generators:
				# if(gen.margCost==0):
					# varProd+=gen.prod
		# radial.append(sum(varProd)*10**(-3))
	
	# barPlot(radial, meshed, "radial", "meshed", "test", "Zones", "Renewable production/[GWh]",labelsRadial,False)
	
	#compare(northSea_radial,northSea_meshed)
	
	# print northSea_meshed.congestionRent
	# print northSea_radial.congestionRent
	

	# print northSea_meshed.zoneSurplus

	# print ""
	# print northSea_radial.zoneSurplus
	
	# print ""
	# print northSea_radial.systemPrice
	# print ""
	# print sum(northSea_meshed.systemPrice)/len(northSea_meshed.systemPrice)
	
	# t=range(northSea_meshed.sampleSize)
	# plt.figure()
	# plt.plot(t,northSea_meshed.systemPrice,'Gold')
	# plt.plot(t, northSea_radial.systemPrice,'r')

	# for zone in northSea_meshed.zonePrices.keys():

	
		# plt.plot(t,northSea_meshed.zonePrices[zone])
	# plt.plot(t,northSea_meshed.zonePrices["NL"],'k')
	# plt.plot(t,northSea_radial.zonePrices["NL"],'r')
	# plt.show()
	# print pr, northSea_meshed.systemProdSurplus
	# print cons, northSea_meshed.systemConsSurplus
	
	# print pr+cons
	# print northSea_meshed.systemProdSurplus+northSea_meshed.systemConsSurplus
	# plt.show()


	
	
	
	

	
	
	
	
	

if __name__ == "__main__":
    main(sys.argv[1:])
