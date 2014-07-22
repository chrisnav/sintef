
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
	
	# for node in northSea_meshed.nodes:
		# for branch in node.branches:
			# print str(branch.fromNode)+" "+str(branch.toNode)			
			# print len(filter(lambda x: np.round(x)>0,branch.flow))
			# print ""
	print ""
	print "radial:"
	northSea_radial=Network.Network(matFilePath_radial,xmlFilePath_radial,dict)
	
	
	# for node in northSea_radial.nodes:
		# for branch in node.branches:
			# print str(branch.fromNode)+" "+str(branch.toNode)			
			# print len(filter(lambda x: np.round(x)>0,branch.flow))
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
	print ""
	print ""
	meshed=[]
	labelsMeshed=[]
	radial=[]
	labelsRadial=[]
	for z in northSea_meshed.nodesByZones.keys():
		
		labelsMeshed.append(z)
		labelsRadial.append(z)
	
		varProd=np.zeros(100)
		for node in northSea_meshed.nodesByZones[z]:
			for gen in node.generators:
				if(gen.margCost==0):
					varProd+=gen.prod
		meshed.append(sum(varProd)*10**(-3))
		
		varProd=np.zeros(100)
		for node in northSea_radial.nodesByZones[z]:
			for gen in node.generators:
				if(gen.margCost==0):
					varProd+=gen.prod
		radial.append(sum(varProd)*10**(-3))
	
	barPlot(radial, meshed, "radial", "meshed", "test", "Zones", "Renewable production/[GWh]",labelsRadial,False)
	
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


	
	
	
	
def compare(radial, meshed):
	
	zoneLabels=[]

	cons1=[]
	cons2=[]
	prod1=[]
	prod2=[]
	
	
	##Get surplus from every zone
	for zone in radial.zoneSurplus.keys():
		zoneLabels.append(zone)
		cons1.append(radial.zoneSurplus[zone][1])
		cons2.append(meshed.zoneSurplus[zone][1])
		prod1.append(radial.zoneSurplus[zone][0])
		prod2.append(meshed.zoneSurplus[zone][0])
	
	# zoneLabels.append('System')

	# cons1.append(radial.systemConsSurplus)
	# cons2.append(meshed.systemConsSurplus)
	# prod1.append(radial.systemProdSurplus)
	# prod2.append(meshed.systemProdSurplus)
	
	cons1=np.array(cons1)/10**6	
	cons2=np.array(cons2)/10**6
	prod1=np.array(prod1)/10**6
	prod2=np.array(prod2)/10**6

	sysRad=[radial.systemConsSurplus*10**(-6), radial.systemProdSurplus*10**(-6)]#cons1+prod1
	sysMeshed=[meshed.systemConsSurplus*10**(-6), meshed.systemProdSurplus*10**(-6)]#cons2+prod2
	sysLabels=["consumer","producer"]
	##Make bar plots
	barPlot(cons1,cons2,"radial","meshed","Consumer surplus", "Zones", "Million euros",zoneLabels,True)
	barPlot(prod1,prod2,"radial","meshed","Producer surplus","Zones","Million euros",zoneLabels,True)
	#barPlot(sysRad,sysMeshed,"radial","meshed","System surplus","Surplus","Million euros",sysLabels,True)
	
	# plt.figure(1, figsize=(6,6))
	# ax = plt.axes([0.1, 0.1, 0.8, 0.8])
	# fracs=[radial.systemProdSurplus/(radial.systemProdSurplus+meshed.systemProdSurplus),meshed.systemProdSurplus/(radial.systemProdSurplus+meshed.systemProdSurplus)]
	# plt.pie(fracs, labels=("radial","meshed"),colors=('r','Gold'),autopct='%1.1f%%', shadow=True, startangle=90)
	# plt.title("System producer surplus")
	# plt.savefig("lol.png", facecolor='w')
	# plt.show()
	
	##Plot system price
	t=range(radial.sampleSize)
	plt.figure()
	plt.title("System price")
	plt.plot(t,radial.systemPrice,'r',label="radial")
	plt.plot(t,meshed.systemPrice,'b',label="meshed")
	mi=np.min(np.concatenate((radial.systemPrice, meshed.systemPrice)))
	ma=np.max(np.concatenate((radial.systemPrice,meshed.systemPrice)))+10
	plt.ylim(mi,ma)
	plt.xlabel("time")
	plt.ylabel("euros/MW")
	plt.legend()
	
	#plt.savefig("system price.eps", format="eps")
	
	#plt.show()

def barPlot(bars1, bars2, barLabel1, barLabel2, title, xlabel, ylabel, zoneLabels, save):
	
	width=0.35
	placement=np.arange(len(zoneLabels))+1
	
	fig, ax = plt.subplots()
	
	plot1=ax.bar(placement,bars1,width,color='r')
	plot2=ax.bar(placement+width,bars2,width,color='Gold')
	

	
		
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.set_xbound(0,len(zoneLabels)+1.5)
	ax.set_ybound(0,np.max(np.concatenate((bars1,bars2)))*1.2)
	ax.set_title(title)
	ax.set_xticks(placement+width)
	ax.set_xticklabels(zoneLabels)
	ax.legend((plot1[0],plot2[0]),(barLabel1,barLabel2))

	# plt.savefig(title+".png")	


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

	plt.show()

	
	
	
	
	

if __name__ == "__main__":
    main(sys.argv[1:])
