
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

		

		
def main(argv):
	# nodeList=np.array([np.array([1,'Norway']),np.array([11,'Norway']),np.array([2,"Germany"])])
	# branchList=np.array([np.array([1,11,0.3,0.4,0.8,0.5]), np.array([1,2,1.2,3.1,2.2,2.1]), np.array([11,2,0.3,0.5,1.1,1.0])])
	# resultsLoad=np.array([np.array([1,0.1,0.3,0.2,0.3]),np.array([2,3.2,2.3,1.3,2.0])])
	# resultsGen=np.array([np.array([1,"Hydro",0.3,0.4,0.8,0.5]),np.array([11,'wind',0.9,1.2,1.3,1.2])])

	# testDict={'nodes':nodeList, 'branches':branchList,'load':resultsLoad,'generation':resultsGen}
	#costDict={'wind':0,'hydro':20,'oil':150}
	# network = Network.Network(testDict,costDict)
	
	# node1=Node.Node(1,'NORWAY',np.array([0,1,2]))
	# node2=Node.Node(2,'GERMANY',np.array([0,2,3]))

	test1=testingStuff.testingStuff()
	test2=testingStuff.testingStuff()

if __name__ == "__main__":
    main(sys.argv[1:])
