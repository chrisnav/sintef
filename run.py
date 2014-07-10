
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
	
	##This should not be hardcoded!
	dict={1:'belgium',2:'germany',3:'denmark',4:'uk',5:'uk',6:'netherlands',7:'norway',21:'belgium',22:'germany',23:'denmark',24:'uk',25:'uk',26:'netherlands',27:'norway',28:'germany',29:'denmark',30:'germany',31:'netherlands',91:'norway',92:'denmark',93:'germany',94:'netherlands',95:'belgium',96:'uk',102:'germany',103:'denmark',107:'norway'}
	
	for node in nodeInput:
		nodeNumber=int(node[0])
		country=dict[nodeNumber]
		
		newNode=[nodeNumber, country] ##Add node number and country
		nodeList.append(newNode)
	
	resultsDict={'nodes':nodeList, 'branches':branchList, 'generation':genList}
	
	northSea=Network.Network(resultsDict)
	for b in northSea.nodes[1].branches:
		if(b.toNode==22):
			print len(b.flow)
			print len(filter(lambda x: x>28137.0, b.flow))

	



	
	
def getDeadBranches(flowInput): ##Find indexes of branches with 0 flow at all times. 

	deadBranches=[]

	for i in range(len(flowInput)):
		if(not any(flowInput[i])): ##If the flow is 0 for all time steps, the branch is dead
			deadBranches.append(i) ##Put the row number of the dead branch in the list

	
	return deadBranches
	

def cutDeadBranches(deadRows,listToBeCut): ##Remove dead branches
	
	for row in deadRows[::-1]: ##Pop the branches at the back first to avoid messing up the indexing
		listToBeCut.pop(row)
		
	return listToBeCut
	
	
def cutDeadNodes(trimmedBranchInput,nodeInput): ##Remove nodes with no branches connecting them to other nodes
	
	safeNodes=[]
	for branch in trimmedBranchInput: ##Branch input should not have any dead branches
		safeNodes+=[int(branch[0]),int(branch[1])] ##Put node numbers of all nodes that are connected (not to be removed) in a list
		 
	
	return filter(lambda x: int(x[0]) in safeNodes, nodeInput) ##Find all nodes with node number in the safeNodes list. Filter away the dead ones
	
	
def addFlows(flowIn, flowOut): ##Combine the incoming and outgoing flows (in the same branch) into one.
	flowInT=map(list,zip(*flowIn)) ##Transpose to get it on the right form first
	flowOutT=map(list,zip(*flowOut))
	flow=[]

	samples=len(flowInT[0])
	
	for i in range(len(flowInT)): ##Each row is a branch
		f=[]		
		for j in range(samples): 
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
