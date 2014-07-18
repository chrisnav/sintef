
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
from classes import testingStuff
import xml.etree.ElementTree as ET

		

		
def main(argv):
	##This should not be hardcoded!
	dict={1:'be',2:'de',3:'dk',4:'uk',5:'uk',6:'nl',7:'no',21:'be',22:'de',23:'dk',24:'uk',25:'uk',26:'nl',27:'no',28:'de',29:'dk',30:'de',31:'nl',91:'no',92:'dk',93:'de',94:'nl',95:'be',96:'uk',102:'de',103:'dk',107:'no'}

	matFilePath_meshed='C:\\Users\\christiann\\Desktop\\NetOp_Toolbox\\Net-Op DTOC 64bit 2013-02-15\\results_casestudy_meshed\\results.mat'
	xmlFilePath_meshed='C:\\Users\\christiann\\Desktop\\NetOp_Toolbox\\Net-Op DTOC 64bit 2013-02-15\\results_casestudy_meshed\\case_auto.xml'   ##The auto-generated xml file where all the new nodes and branches are also listed
	matFilePath_radial='C:\\Users\\christiann\\Desktop\\NetOp_Toolbox\\Net-Op DTOC 64bit 2013-02-15\\results_casestudy_radial\\results.mat'
	xmlFilePath_radial='C:\\Users\\christiann\\Desktop\\NetOp_Toolbox\\Net-Op DTOC 64bit 2013-02-15\\results_casestudy_radial\\case_auto.xml'   ##The auto-generated xml file where all the new nodes and branches are also listed

	
	print "meshed:"
	northSea_meshed=Network.Network(matFilePath_meshed,xmlFilePath_meshed,dict)
	print ""
	print "radial:"
	northSea_radial=Network.Network(matFilePath_radial,xmlFilePath_radial,dict)
	print ""
	print ""
	

	# b= sum(northSea_meshed.nodes[6].branches[0].flow)
	print ""
	# b+= sum(northSea_meshed.nodes[6].branches[1].flow)
	print ""
	# a=sum(northSea_meshed.nodes[6].generators[0].prod)
	print ""
	# c= sum(northSea_meshed.nodes[6].load)
	# print a-b, c
	# for i in range(7):
		# a=northSea_meshed.nodes[i].generators[0].prod

		# b=northSea_radial.nodes[i].generators[0].prod
	
	
		# print a==b
		# d=0
		# c=0
		# for i in a==b:
			# if(i):
				# d+=1
				# c+=1
				# continue
			# print str(b[c])+"	"+str(a[c])
			# c+=1
		# print ""
		# print 100-d
	
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
	# plt.plot(t,northSea_meshed.systemPrice,'black')
	# pr=0.0
	# cons=0.0
	# for zone in northSea_meshed.zonePrices.keys():
		# pr+=northSea_meshed.zoneSurplus[zone][0]
		# cons+=northSea_meshed.zoneSurplus[zone][1]
	
		# plt.plot(t,northSea_meshed.zonePrices[zone]/northSea_meshed.systemPrice)
	
	# plt.show()
	# print pr, northSea_meshed.systemProdSurplus
	# print cons, northSea_meshed.systemConsSurplus
	
	# print pr+cons
	# print northSea_meshed.systemProdSurplus+northSea_meshed.systemConsSurplus
	# plt.show()

	compare(northSea_radial,northSea_meshed)
	
	
	
	
def compare(radial, meshed):
	
	labels=[]

	cons1=[]
	cons2=[]
	prod1=[]
	prod2=[]
	
	
	
	for zone in radial.zoneSurplus.keys():
		labels.append(zone)
		cons1.append(radial.zoneSurplus[zone][1])
		cons2.append(meshed.zoneSurplus[zone][1])
		prod1.append(radial.zoneSurplus[zone][0])
		prod2.append(meshed.zoneSurplus[zone][0])
	
	# labels.append('Sys')

	# cons1.append(radial.systemConsSurplus)
	# cons2.append(meshed.systemConsSurplus)
	# prod1.append(radial.systemProdSurplus)
	# prod2.append(meshed.systemProdSurplus)
	
	cons1=np.array(cons1)/10**6
	cons2=np.array(cons2)/10**6
	prod1=np.array(prod1)/10**6
	prod2=np.array(prod2)/10**6

	totRad=cons1+prod1
	totMeshed=cons2+prod2
	
	placement=np.arange(len(labels))
	width=0.35
	
	
	figCons, axCons = plt.subplots()
	
	cons1Bars=axCons.bar(placement,cons1,width,color='r')
	cons2Bars=axCons.bar(placement+width,cons2,width,color='y')
	

	
		
	axCons.set_xlabel('Zones')
	axCons.set_ylabel('Million euros')
	axCons.set_title('Consumer surplus')
	axCons.set_xticks(placement+width)
	axCons.set_xticklabels(labels)
	#axCons.legend((cons1Bars[0],cons2Bars[0]),("radial","meshed"))

	
	#plt.savefig("consumer.png")	
	
	figProd, axProd = plt.subplots()
	
	prod1Bars=axProd.bar(placement,prod1,width,color='r')
	prod2Bars=axProd.bar(placement+width,prod2,width,color='y')
	
	axProd.set_xlabel('Zones')
	axProd.set_ylabel('Million euros')
	axProd.set_title('Producer surplus')
	axProd.set_xticks(placement+width)
	axProd.set_xticklabels(labels)
	#axProd.legend((prod1Bars[0],prod2Bars[0]),("radial","meshed"))

	#plt.savefig("producer.png")	
	
	labels.append('Con.Rent')
	placement=np.arange(len(labels))

	totRad=np.append(totRad,radial.congestionRent/10**6)
	totMeshed=np.append(totMeshed,meshed.congestionRent/10**6)
	figTot, axTot = plt.subplots()
	
	totRadBars=axTot.bar(placement,totRad,width,color='r')
	totMeshedBars=axTot.bar(placement+width,totMeshed,width,color='y')
	
	axTot.set_xlabel('Zones')
	axTot.set_ylabel('Million euros')
	axTot.set_title('Total surplus')
	axTot.set_xticks(placement+width)
	axTot.set_xticklabels(labels)
	#axTot.legend((totRadBars[0],totMeshedBars[0]),("radial","meshed"))

		
	#plt.savefig("total.png")	
	t=range(radial.sampleSize)
	plt.figure()
	plt.plot(t,radial.systemPrice,'r')
	plt.plot(t,meshed.systemPrice,'b')
	
	
	plt.show()


	

	
	
	
	
	

if __name__ == "__main__":
    main(sys.argv[1:])
