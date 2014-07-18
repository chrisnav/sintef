import scipy.io as io
import xml.etree.ElementTree as ET
import numpy as np

class FormatInput: ##A class to format the results from netop, so that it may be used to create a Network class
	
	def __init__ (self,matFilePath,xmlFilePath,dict): 
		
		nodeList=[]								 ##The xml-file should be the 'case_auto.xml' file that is created after running netop 
		branchList=[]							 ##The mat-file should be the 'results.mat' file that is created after running netop 
		genList=[]
	
		mat=io.loadmat(matFilePath)		##Load in mat file as a dict
		results=mat['results'][0][0]	##Contains the info about the time series of generation and flow
	
		nodeInput=self.getInput(xmlFilePath,'node')   ##Get basic node info. Contains all _allowable_ nodes, needs to be cut (see below)
		branchInput=self.getInput(xmlFilePath,'branch') ##Get basic branch info. Contains all _allowable_ branches, needs to be cut (see below)
		genInput=self.getInput(xmlFilePath,'base_geno') ##Get basic generator info, contains all generators (no cutting needed)

		totFlow=self.addFlows(results[6],results[7]) ##Combine the in- and out flow. Netop treats branches as one way connections (when solving the mip), and therefore has two branches for every branch. 
		branchesToRemove=self.getDeadBranches(totFlow) ##Find branches that are not used (0 flow for all times) 
		totFlow=self.cutDeadBranches(branchesToRemove,totFlow) ##Remove dead branches from both the flow and list of branches
		
		branchInput=self.cutDeadBranches(branchesToRemove,branchInput)
		

		nodeInput=self.cutDeadNodes(branchInput,nodeInput)  ##Remove dead (not connected) nodes. This is based on a trimmed branch list with no dead branches
	

	
		generation=map(list,zip(*results[10]))	##Time series of generation. Transposed and converted to list of lists to be in the right format (every row is a generator instead of every column)
		# print generation[1]
		# print""
		for i in range(len(branchInput)):  
			newBranch=[int(branchInput[i][0]), int(branchInput[i][1])] + totFlow[i]	##Add the to and from node numbers and time series flow
			branchList.append(newBranch)
	
		for i in range(len(genInput)):
			newGen=[int(genInput[i][0]), float(genInput[i][3]), float(genInput[i][2])] + generation[i]	##Add node number, marginal cost, max generation and time series of the generator
			genList.append(newGen) ##Add generator to list
	
		
		for node in nodeInput:
			nodeNumber=int(node[0])
			country=dict[nodeNumber]
		
			newNode=[nodeNumber, country] ##Add node number and country
			nodeList.append(newNode)

		self.resultsDict={'nodes':nodeList, 'branches':branchList, 'generation':genList} ##The finished input is put in  a dict to be used by Network
		

		
	def getDeadBranches(self, flowInput): ##Find indexes of branches with 0 flow at all times. 

		deadBranches=[]

		for i in range(len(flowInput)):
			rounded=np.round(flowInput[i]) ##To still cut branches with minuscule flow caused by float point errors 
			if(not any(rounded)): ##If the flow is 0 for all time steps, the branch is dead
				deadBranches.append(i) ##Put the row number of the dead branch in the list

	
		return deadBranches
	

	def cutDeadBranches(self,deadRows,listToBeCut): ##Remove dead branches
	
		for row in deadRows[::-1]: ##Pop the branches at the back first to avoid messing up the indexing
			listToBeCut.pop(row)
		
		return listToBeCut
	
	
	def cutDeadNodes(self,trimmedBranchInput,nodeInput): ##Remove nodes with no branches connecting them to other nodes
	
		safeNodes=[]
		for branch in trimmedBranchInput: ##Branch input should not have any dead branches
			safeNodes+=[int(branch[0]),int(branch[1])] ##Put node numbers of all nodes that are connected (not to be removed) in a list
	
		return filter(lambda x: int(x[0]) in safeNodes, nodeInput) ##Find all nodes with node number in the safeNodes list. Filter away the dead ones
	
	
	def addFlows(self, flowIn, flowOut): ##Combine the incoming and outgoing flows (in the same branch) into one.
	
		flowInT=map(list,zip(*flowIn)) ##Transpose to get it on the right form first
		flowOutT=map(list,zip(*flowOut))
		flow=[]

		samples=len(flowInT[0])
	
		for i in range(len(flowInT)): ##Each row is a branch
			f=[]		
			for j in range(samples): 
				f.append(flowInT[i][j]-flowOutT[i][j]) ##The net flow in the branch at a given time
		
			flow.append(f)
		
		return flow
	
	
	def getInput(self,xmlFile,keyWord): ##To get the info from case_auto.xml.

		tree = ET.parse(xmlFile)	##Parsing the file
		root = tree.getroot()


		field=''
		for char in root.find(keyWord).text: ##Reads in the entire field 'keyWord' from the xml-file as text 
			if(char=='\n'):	##Skip this char (new line)
				continue
			if(char=='\t'): ##Change tab to space
				char=' '
			field+=char ##Build the field once again
	
		field=field.replace('[',"") ##Remove the brackets at the start and end of the field
		field=field.replace(']',"")
	
		lines=field.split(';') ##Split on every row (rows should be separated by ';' in the case_auto file)
	
		
		for i in range(len(lines)):
			lines[i]=lines[i].split() ##Split every row on every number (separated by space)
		
		return lines
	

	
	
	