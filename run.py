
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

	nodeList=[]
	branchList=[]
	loadList=[]
	genList=[]
	
	matFilePath='C:\\Users\\christiann\\Desktop\\NetOp_Toolbox\\Net-Op DTOC 64bit 2013-02-15\\results_casestudy_meshed\\results.mat'
	xmlFilePath='C:\Users\christiann\Desktop\NetOp_Toolbox\Net-Op DTOC 64bit 2013-02-15\case_NorthSea_meshed.xml'

	mat=io.loadmat(matFilePath)
	results=mat['results'][0][0]	
	
	nodeInput=getInput(xmlFilePath,'node')   ##OBS!!These do not contain all the new nodes and branches that are added in the Netop optimization!
	branchInput=getInput(xmlFilePath,'branch') ##Only the 28 original branches, the 6 newest branches are not here!
	loadInput=getInput(xmlFilePath,'base_load')
	genInput=getInput(xmlFilePath,'base_geno')
	
	totFlow=addFlows(results[6],results[7]) ##Combine the in- and out flow
	totFlow=removeDeadBranches(totFlow) ##Remove branches that are not used (0 flow for all times) 
	
	generation=zip(*results[10])	##Time series of generation
	
	for node in nodeInput:
		newNode=[int(node[0])] ##Add node number. The country name should also be added here!
		nodeList.append(newNode)
		
	for i in range(len(branchInput)):  
		newBranch=[int(branchInput[i][0]), int(branchInput[i][1]),totFlow[i]] ##Add to-from node numbers and flow
		branchList.append(newBranch)
		
	for load in loadInput:
		newLoad=[int(load[0])] ##Add node number
		loadList.append(newLoad)
	
	for i in range(len(genInput)):
		newGen=[int(genInput[i][0]), float(genInput[i][3]), generation[i]]	##Add node number and marginal cost
		genList.append(newGen)
		


#	loadList=createLoad(nodeList,branchList,genList)
	
	
	
	
	


	

	
	##Convert to np.array after all manipulations are done...Or should it be don inside Network?

def removeDeadBranches(branchInput):


	deadBranches=[]

	for i in range(len(branchInput)):
		if(not any(branchInput[i])):
			deadBranches.append(i)

	for row in deadBranches[::-1]:
			branchInput.pop(row)


	return branchInput
	
	
def createLoad(nodeList,branchList,genList): ##Function to generate the load time series for all nodes based on power conservation in every node.
	
	
	######### OBS! THIS FUNCTION SHOULD BE DEBUGGED! ###############
	
	load=[]
	
	for node in nodeList:
		l=[]
		nodeNr=node[0]
		allGenInNode=filter(lambda x: x[0]==nodeNr, genList) ##List of lists where every row represents a generator in the node
		branchesToNode=filter(lambda x: x[1]==nodeNr, branchList) ##List of list where every row represents a branch where the node is marked as the receiver
		branchesFromNode=filter(lambda x: x[0]==nodeNr, branchList)##List of list where every row represents a branch where the node is marked as the sender
		
		l.append(nodeNr) ##Add the node number first
		
		totGenNode=[]
		totFlow=[]
		transposeToNode=zip(*branchesToNode)
		transposeFromNode=zip(*branchesFromNode)
		transposeGen=zip(*allGenInNode)	##Transpose to make it easy to sum up all columns (which are rows when transposed)
		
		############################
		############################
		###THERE ARE PROBLEMS HERE! What if one of the branch lists are empty?
		############################
		############################
		length=np.max(len(transposeGen[0][2]),len(transposeFromNode[0][3]))
		print transposeGen
		print transposeToNode
		print transposeFromNode
		
		for j in range(len(transposeGen[0][2])): 
	
			totGenNode.append(sum(transposeGen[j][0])) ##Add the sum of all the generators at every sample point
			totFlow.append(sum(transposeToNode[j][0])-sum(transposeFromNode[j][0])) ##Add the net power _increase_ due to flow at every point in time (positive number -> node imports power, negative -> export)

		
		for i in range(len(totFlow)):
			l.append(totGenNode[i]+totFlow[i]) ##Generation + power imported = load (export is negative import)
		
		load.append(l) ##Finally add the node with its load time series to the list
	
	return load
	
	
def addFlows(flowIn, flowOut): ##Combine the incoming and outgoing flows into one.
	flowInT=zip(*flowIn) ##Transpose
	flowOutT=zip(*flowOut)
	flow=[]
	samples=len(flowInT[0])
	
	for i in range(len(flowInT)): ##Rows
		f=[]
		for j in range(samples): ##Cols
			f.append(flowInT[i][j]-flowOutT[i][j]) ##The net flow in the branch
		
		flow.append(f)
		
	return flow
	
	
def getInput(xmlFile,keyWord): ##To get the info from the xml input file. Assumes the structure of the Netop xml input file.

	tree = ET.parse(xmlFile)
	root = tree.getroot()


	field=''
	for char in root.find(keyWord).text: ##Reads in the entire field 'keyWord' from the xml-file as text 
		if(char=='\n'):	##Skip this char
			continue
		if(char=='\t'): ##Change tab to space
			char=' '
		field+=char ##Build the field once again
	
	field=field.replace('[',"") ##Remove the brackets at the start and end of the field
	field=field.replace(']',"")
	
	lines=field.split(';') ##Split on every row (rows are separated by ';' in the input file)
	
		
	for i in range(len(lines)):
		lines[i]=lines[i].split() ##Split every row on every number (separated by space)
		
	return lines
	


if __name__ == "__main__":
    main(sys.argv[1:])
