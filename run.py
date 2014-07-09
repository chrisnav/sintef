
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
	xmlFilePath='C:\\Users\\christiann\\Desktop\\NetOp_Toolbox\\Net-Op DTOC 64bit 2013-02-15\\results_casestudy_meshed\\case_auto.xml'   ##The auto-generated xml file where all the new nodes and branches are also listed

	mat=io.loadmat(matFilePath)
	results=mat['results'][0][0]	
	
	nodeInput=getInput(xmlFilePath,'node')   ##Contains all _allowable_ nodes, needs to be cut (see below)
	branchInput=getInput(xmlFilePath,'branch') ##Contains all _allowable_ branches, needs to be cut (see below)
	#loadInput=getInput(xmlFilePath,'base_load') ##All load nodes (no cutting needed)
	genInput=getInput(xmlFilePath,'base_geno') ##All generators (no cutting needed)

	totFlow=addFlows(results[6],results[7]) ##Combine the in- and out flow
	branchesToRemove=getDeadBranches(totFlow) ##Find branches that are not used (0 flow for all times) 

	totFlow=cutDeadBranches(branchesToRemove,totFlow) ##Remove dead branches from both the flow and list of branches
	branchInput=cutDeadBranches(branchesToRemove,branchInput)
	
	nodeInput=cutDeadNodes(branchInput,nodeInput)  ##Remove dead (not connected) nodes on the basis of the trimmed branch list
	
	
	generation=map(list,zip(*results[10]))	##Time series of generation. Transposed and converted to list of lists to be in the right format (every row is a generator)

	

	
	for i in range(len(branchInput)):  
		newBranch=[int(branchInput[i][0]), int(branchInput[i][1])] + totFlow[i]	##Add the to and from node numbers and time series flow
		branchList.append(newBranch)
	
	for i in range(len(genInput)):
		newGen=[int(genInput[i][0]), float(genInput[i][3])] + generation[i]	##Add node number, marginal cost and time series
		genList.append(newGen) ##Add generator to list
	
	# for load in loadInput:
		# newLoad=[int(load[0])] ##Add node number. Time series is created below in createLoad
		# loadList.append(newLoad)
		
	#loadList=createLoad(loadList,branchList,genList) ##Add the load
	
	dict={1:'belgium',2:'germany',3:'denmark',4:'england',5:'england',6:'netherlands',7:'norway',21:'belgium',22:'germany',23:'denmark',24:'england',25:'england',26:'netherlands',27:'norway',28:'germany',29:'denmark',30:'germany',31:'netherlands',91:'norway',92:'denmark',93:'germany',94:'netherlands',95:'belgium',96:'england',102:'germany',103:'denmark',107:'norway'}
	
	for node in nodeInput:
		nodeNumber=int(node[0])
		country=dict[nodeNumber]
		
		newNode=[nodeNumber, country] ##Add node number and country
		nodeList.append(newNode)
	
	resultsDict={'nodes':nodeList, 'branches':branchList, 'generation':genList}
	
	northSea=Network.Network(resultsDict)
	
	

	
	
def getDeadBranches(flowInput): ##The flow should be the combined flow 

	deadBranches=[]

	for i in range(len(flowInput)):
		if(not any(flowInput[i])): ##If the flow is 0 for all time steps, the branch is dead
			deadBranches.append(i) ##Put the row number of the dead branch in the list

	
	return deadBranches
	

def cutDeadBranches(deadRows,listToBeCut):
	
	for row in deadRows[::-1]: ##Pop the branches at the back first to avoid messing up the indexing
		listToBeCut.pop(row)
		
	return listToBeCut
	
	
def cutDeadNodes(trimmedBranchInput,nodeInput): ##Branch list should already be cut
	
	safeNodes=[]
	for branch in trimmedBranchInput:
		safeNodes+=[int(branch[0]),int(branch[1])] ##Put node numbers of all nodes that are connected (not to be removed) in a list
		 
	
	return filter(lambda x: int(x[0]) in safeNodes, nodeInput) ##Find all nodes with node number in the safeNodes list. Filter away the dead ones
	

# def createLoad(loadList,branchList,genList): ##Function to generate the load time series for all nodes based on power conservation in every node.
	
	#Function tried and tested
			
	# for i in range(len(loadList)):

		# nodeNr=loadList[i][0]
		# allGenInNode=filter(lambda x: x[0]==nodeNr, genList) ##List of lists where every row represents a generator in the node
		# branchesToNode=filter(lambda x: x[1]==nodeNr, branchList) ##List of list where every row represents a branch where the node is marked as the receiver
		# branchesFromNode=filter(lambda x: x[0]==nodeNr, branchList)##List of list where every row represents a branch where the node is marked as the sender
		
		# totGenNode=[]
		# totFlow=[]
		# transposeToNode=map(list,zip(*branchesToNode))		##zip to transpose, map to change type from tuple to list
		# transposeFromNode=map(list,zip(*branchesFromNode))
		# transposeGen=map(list,zip(*allGenInNode))			##Transpose to make it easy to sum up all columns (which are rows when transposed)
		
		# sampleSize=max(len(transposeToNode),len(transposeFromNode),len(transposeGen))
		
		# if(len(transposeToNode)==0):   			##If one of the lists are empty (ie no generation in the node), make a list of zeros
			# transposeToNode=[[0]]*sampleSize
		# if(len(transposeGen)==0): 				##This might not be necessary, since there is always generation in load nodes (in my case, anyway) 
			# transposeGen=[[0]]*sampleSize
		# if(len(transposeFromNode)==0):
			# transposeFromNode=[[0]]*sampleSize		

		# for j in range(2,sampleSize): 
			# totGenNode.append(sum(transposeGen[j])) ##Add the sum of all the generators at every sample point
			# totFlow.append(sum(transposeToNode[j])-sum(transposeFromNode[j])) ##Add the net power _increase_ due to flow at every point in time (positive number -> node imports power, negative -> export)

		
		# for k in range(len(totFlow)):
			# loadList[i].append(totGenNode[k]+totFlow[k]) ##Generation + power imported = load (export is negative import)
				

	# return loadList
	
	
def addFlows(flowIn, flowOut): ##Combine the incoming and outgoing flows into one.
	flowInT=map(list,zip(*flowIn)) ##Transpose
	flowOutT=map(list,zip(*flowOut))
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
