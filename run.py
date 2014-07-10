
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
	dict={1:'belgium',2:'germany',3:'denmark',4:'uk',5:'uk',6:'netherlands',7:'norway',21:'belgium',22:'germany',23:'denmark',24:'uk',25:'uk',26:'netherlands',27:'norway',28:'germany',29:'denmark',30:'germany',31:'netherlands',91:'norway',92:'denmark',93:'germany',94:'netherlands',95:'belgium',96:'uk',102:'germany',103:'denmark',107:'norway'}

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
	# print northSea_meshed.congestionRent
	# print northSea_radial.congestionRent
	

	# print northSea_meshed.zoneSurplus

	# print ""
	# print northSea_radial.zoneSurplus
	
	# print ""
	# print sum(northSea_radial.systemPrice)/len(northSea_radial.systemPrice)
	# print ""
	# print sum(northSea_meshed.systemPrice)/len(northSea_meshed.systemPrice)
	
	t=range(northSea_meshed.sampleSize)
	plt.figure()
	plt.plot(t,northSea_meshed.systemPrice,'black')
	# for zone in northSea_meshed.zonePrices.keys():
		# plt.plot(t,northSea_meshed.zonePrices[zone])
		
	plt.show()

if __name__ == "__main__":
    main(sys.argv[1:])
