
import sys
import numpy  as np        
import matplotlib.pyplot as plt         
from classes import Network
from classes import Compare
	

		
def main(argv):
	##This should not be hardcoded!
	dict={1:'be',2:'de',3:'dk',4:'uk',5:'uk',6:'nl',7:'no',21:'be',22:'de',23:'dk',24:'uk',25:'uk',26:'nl',27:'no',28:'de',29:'dk',30:'nl',31:'nl',91:'no',92:'dk',93:'de',94:'nl',95:'be',96:'uk',102:'de',103:'dk',104:'uk',107:'no'}

	matFilePath_meshed='C:\\Users\\christiann\\Desktop\\NetOp_Toolbox\\Net-Op DTOC 64bit 2013-02-15\\results_casestudy_meshed\\results.mat'
	xmlFilePath_meshed='C:\\Users\\christiann\\Desktop\\NetOp_Toolbox\\Net-Op DTOC 64bit 2013-02-15\\results_casestudy_meshed\\case_auto.xml'   ##The auto-generated xml file where all the new nodes and branches are also listed
	
	matFilePath_radial='C:\\Users\\christiann\\Desktop\\NetOp_Toolbox\\Net-Op DTOC 64bit 2013-02-15\\results_casestudy_radial\\results.mat'
	xmlFilePath_radial='C:\\Users\\christiann\\Desktop\\NetOp_Toolbox\\Net-Op DTOC 64bit 2013-02-15\\results_casestudy_radial\\case_auto.xml'   ##The auto-generated xml file where all the new nodes and branches are also listed


	
	print "meshed:"
	northSea_meshed=Network.Network(matFilePath_meshed,xmlFilePath_meshed,dict)
	# node_m=northSea_meshed.nodes[13]
	# for branch in node_m.branches:
		# if(branch.toNode==24 or branch.toNode==30 or branch.toNode==28):
			# print branch.toNode
			# print len(filter(lambda x: np.round(x)!=1400,branch.flow))
			# print ""
			# continue
		# if(branch.toNode==29):	
			# print branch.toNode
			# print len(filter(lambda x: np.round(x)!=1700,branch.flow))
			# print ""
	print ""
	print "radial:"
	northSea_radial=Network.Network(matFilePath_radial,xmlFilePath_radial,dict)
	print ""
	# print (northSea_meshed.zoneSurplus['NO'][0]-northSea_radial.zoneSurplus['NO'][0])*10**(-6)
	# print (northSea_meshed.zoneSurplus['DE'][0]-northSea_radial.zoneSurplus['DE'][0])*10**(-6)

	n=northSea_meshed.nodes[24]
	for branch in n.branches:
		if(branch.toNode==104):
			print len(filter(lambda x: np.abs(x)==1000,branch.flow))

	# node_r=northSea_meshed.nodes[13]			
	# for branch in node_r.branches:
		# if(branch.toNode==24 or branch.toNode==30 or branch.toNode==28):
			# print branch.toNode
			# print len(filter(lambda x: np.round(x)!=1400,branch.flow))
			# print ""
			# continue
		# if(branch.toNode==29):	
			# print branch.toNode
			# print len(filter(lambda x: np.round(x)!=1700,branch.flow))
			# print ""
	
	# print "System Price meshed..."
	# print "low wind: "+str(northSea_meshed.systemPrice[40])
	# print "high wind: "+str(northSea_meshed.systemPrice[63])
	# print ""
	# print "System Price radial..."
	# print "low wind: "+str(northSea_radial.systemPrice[40])
	# print "high wind: "+str(northSea_radial.systemPrice[63])
	# print ""
	
	
	# for zone in northSea_meshed.zonePrices.keys():
		# print "Price in "+zone+", meshed..."
		# print "low wind: "+str(northSea_meshed.zonePrices[zone][40])
		# print "high wind: "+str(northSea_meshed.zonePrices[zone][63])
		# print ""
		# print "Price in "+zone+", radial..."
		# print "low wind: "+str(northSea_radial.zonePrices[zone][40])
		# print "high wind: "+str(northSea_radial.zonePrices[zone][63])
		# print ""	
	
	
	
	
	
	
	
	# compNorthSea = Compare.Compare([northSea_radial,northSea_meshed],["radial","meshed"])
	# compNorthSea = Compare.Compare([northSea_meshed,northSea_radial],["meshed","radial"])
	
	# compNorthSea.compareSystemSurplus(False)
	# compNorthSea.compareSystemPrices(False)
	# compNorthSea.compareZonePrices(False, "DE")
	# compNorthSea.compareProducerSurplus(False)	
	# compNorthSea.compareConsumerSurplus(False)
	# compNorthSea.compareWindGen(False)
	# plt.show()


	
	
	
	

	
	
	
	
	

if __name__ == "__main__":
    main(sys.argv[1:])
