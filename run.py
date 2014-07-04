
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
	# nodeList=np.array([np.array([1,'Norway',0.32,0.5,0.45,0.37]),np.array([11,'Norway',0.4,0.6,0.55,0.55]),np.array([2,"Germany",1.2,1.3,1.25,1.31])])
	# branchList=np.array([np.array([1,11,0.3,0.4,0.8,0.5]), np.array([1,2,1.2,3.1,2.2,2.1]), np.array([11,2,0.3,0.5,1.1,1.0])])
	# resultsLoad=np.array([np.array([1,0.1,0.3,0.2,0.3]),np.array([2,3.2,2.3,1.3,2.0])])
	# resultsGen=np.array([np.array([1,"Hydro",0.3,0.4,0.8,0.5]),np.array([11,'wind',0.9,1.2,1.3,1.2])])
	# nodeList=np.array([np.array([1,'Norway',1.0]),np.array([2,"Germany",2.2])])
	# branchList=np.array([np.array([1,2,3.2])])
	# resultsLoad=np.array([np.array([1,0.1]),np.array([2,3.2])])
	# resultsGen=np.array([np.array([1,0.20,2.0]),np.array([1,0,1.3])])

	# testDict={'nodes':nodeList, 'branches':branchList,'load':resultsLoad,'generation':resultsGen}
	# costDict={'wind':0,'hydro':0.20,'oil':150}
	# network = Network.Network(testDict)
	# [cons,prod,net]=network.calcSurplus()
	
	# print cons
	# print prod
	# print net
	xmlFile='C:\Users\christiann\Desktop\NetOp_Toolbox\Net-Op DTOC 64bit 2013-02-15\case_NorthSea_meshed.xml'
	tree = ET.parse(xmlFile)
	root = tree.getroot()
	
	nodeRawInput=getInput(root,'node')
	branchRawInput=getInput(root,'branch')
	loadRawInput=getInput(root,'base_load')
	genRawInput=getInput(root,'base_geno')
	
	nodeList=[]
	branchList=[]
	loadList=[]
	genList=[]
	
	for node in nodeRawInput:
		newNode=[int(node[0])]
		nodeList.append(newNode)
		
	for branch in branchRawInput:
		newBranch=[int(branch[0]), int(branch[1])]
		branchList.append(newBranch)
		
	for load in loadRawInput:
		newLoad=[int(load[0])]
		loadList.append(newLoad)
	
	for gen in genRawInput:
		newGen=[int(gen[0])]
		genList.append(newGen)
		
	
	##Convert to np.array after all manipulations are done...Or should it be don inside Network?

def getInput(root,keyWord): ##To get the info from the xml input file.
	field=''
	for char in root.find(keyWord).text:
		if(char=='\n'):
			continue
		if(char=='\t'):
			char=' '
		field+=char
	
	field=field.replace('[',"") ##The whole field without the brackets
	field=field.replace(']',"")
	
	lines=field.split(';') ##Split on every row
	
		
	for i in range(len(lines)):
		lines[i]=lines[i].split() ##Split every row on every number (whitespace)
		
	return lines
	


if __name__ == "__main__":
    main(sys.argv[1:])
