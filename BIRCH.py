# This is an implementation of BIRCH clustering algorithm
# This programming is inspired by Roberto Perdisci's BIRCH implementation in Java (http://roberto.perdisci.com/projects/jbirch)
# The reference paper is BIRCH: An Efficient Data Clustering Method for Very Large Databases (http://www.cs.sfu.ca/cc/459/han/papers/zhang96.pdf)
# @author Chuhe Li(chli1403@student.miun.se)

import os
import math
import pdb
import numpy as np
import sys

class CFEntry():
    
    __LINE_SEP= '\\'#str(os.linesep()) #get line separator of current system
    n=0 #number of patterns summarized by this entry
    sumX=[] #array sumX
    sumX2=[] #array sumX2
    child=0 #CFNode()
    indexList=list() #list indexList
    subclusterID=-1 # the unique id that describes a subcluster (valid only for leaf entries)
    
    #constructor
    def __init__(self, x=None, index=None):
        if x is None and index is None:
            pass
        
        elif x is not None and index is None:
            self(x, 0)
        elif x is not None and index is not None:
            self.n=1
            #self.sumX=len(x)
            for i in range(0, len(x)):
                self.sumX.append(x[i])
            #self.sumX2=len(x)
            for i in range(0, len(x)):
                self.sumX2.append(x[i])

            indexList=list()
            indexList.append(index)

        
    #This makes a deep copy of the CFEntry e
    #WARNING: we do not make a deep copy of the child
    #@param e the entry to be cloned
    def copy(self, e):
        self.n=e.n
        self.sumX=e.sumX
        self.sumX2=e.sumX2
        self.child=e.child
        self.indexList=list()
        for i in range(0, e.getIndexList()):
            self.indexList.append(i)
            
    def getIndexList(self):
        return self.indexList
    #boolean function   
    def hasChild(self):
        return bool(self.child)
    
    def getChlid(self):
        return self.child
    
    def getChildSize(self):
        return self.child.getEntries().size()
    
    def setChild(self, n):
        self.child=n
        self.indexList=null #we don't keep this if this becomes a non-leaf entry
    
    def setSubclusterID(self, id):
        self.subclusterID=id
    
    def getSubclusterID(self):
        return self.subclusterID
        
    def update(self, e):
        self.n += e.n
        
        if self.sumX==null:
            self.sumX=e.sumX.cloned()
        else:
            for i in range(0, len(sumX)):
                self.sumX[i] += e.sumX[i]
        
        if self.sumX2==null:
            self.sumX2=e.sumX2.cloned()
        else:
            for i in range(0, len(sumX2)):
                self.sumX2[i] += e.sumX2[i]
                
        if not self.hasChild(): #we keep indexList only if we are at a leaf 
            if self.indexList!=null and e.indexList!=null:
                self.indexList.addAll(e.indexList)
            elif self.indexList==null and e.indexList!=null:
                self.indexList=e.indexList.cloned()
        
    def addToChild(self, e):
        #add directly to the child node
        self.child.getEntries().add(e)

        #boolean function
    def isWithinThreshold(self, e, threshold, distFunction):
        dist=distance(e, distFunction)
        
        if dist==0 or dist<=threshold: #read the comments in function
            return true
            
        return false
        
    #@param e
    #@return the distance between this entry and e
    def distance(e, distFunction):
        dist=Double.MAX_VALUE
        
        #switch case function
        if distFunction==CFTree.D0_DIST:
            dist=d0(self, e)
        elif distFunction==CFTree.D1_DIST:
            dist=d1(self, e)
        elif distFunction==CFTree.D2_DIST:
            dist=d2(self, e)
        elif distFunction==CFTree.D3_DIST:
            dist=d3(self, e)
        elif distFunction==CFTree.D4_DIST:
            dist=d4(self, e)
        
        return dist
    
    def d0(e1, e2):
        dist=0
        for i in range(0, len(e1.sumX)):
            diff=e1.sumX[i]/e1.n - e2.sumX[i]/e2.n
            dist += diff*diff
        
        if dist<0:
            print "d0<0!!!"
            
        #notice here that in the R implementation of BIRCH (package birch)
        #the radius parameter is based on the squared distance /dist/
        #this causes a difference in results.
        #if we change the line below into 
        #   return dist;
        #the results produced by the R implementation and this Java implementation
        #will match perfectly (notice that in the R implementation maxEntries = 100
        #and merging refinement is not implemented)
        return math.sqrt(dist)
        
    def d1(e1, e2):
        dist=0
        for i in range(0, len(e1.sumX)):
                        diff=math.abs(e1.sumX[i]/e1.n - e2.sumX[i]/e2.n)
                        dist += diff
            
        if dist<0:
            print "d1<0!!!"
            
        return dist
        
    def d2(e1, e2):
        dist=0
        n1=e1.n
        n2=e2.n
        for i in range(0, len(e1.sumX)):
            diff=(n2*e1.sumX2[i] - 2*e1.sumX[i]*e2.sumX[i] + n1*e2.sumX2[i])/(n1 * n2)
            dist += diff
        
        if dist<0:
            print "d2<0"
            
        return math.sqrt(dist)
        
    def d3(e1, e2):
        dist=0
        n1=e1.n
        n2=e2.n
        totSumX=e1.sumX.cloned()
        totSumX2=e1.sumX2.cloned()
        
        for i in range(0, len(e2.sumX)):
            totSumX[i] += e2.sumX[i]
            totSumX2[i] += e2.sumX2[i]
            
        for i in range(0, len(totSumX)):
            diff = ((n1+n2)*totSumX2[i] - 2*totSumX[i]*totSumX[i] + (n1+n2)*totSumX2[i])/((n1+n2)*(n1+n2-1))
            dist+=diff
            
        if dist<0:
            print "d3<0!!!"
            
        return math.sqrt(dist)
        
    def d4(e1, e2):
        dist = 0
        
        n1 = e1.n
        n2 = e2.n
        totSumX = e1.sumX.cloned()
        totSumX2 = e1.sumX2.cloned()
        for i in range(0, len(e2.sumX)):
            totSumX[i] += e2.sumX[i];
            totSumX2[i] += e2.sumX2[i];
                
        for i in range(0, len(totSumX)):
            diff1 = totSumX2[i] - 2*totSumX[i]*totSumX[i]/(n1+n2) + (n1+n2)*(totSumX[i]/(n1+n2))*(totSumX[i]/(n1+n2))
            diff2 = e1.sumX2[i] - 2*e1.sumX[i]*e1.sumX[i]/n1 + n1*(e1.sumX[i]/n1)*(e1.sumX[i]/n1)
            diff3 = e2.sumX2[i] - 2*e2.sumX[i]*e2.sumX[i]/n2 + n2*(e2.sumX[i]/n2)*(e2.sumX[i]/n2)
            dist += diff1 - diff2 - diff3
                
        if dist<0:
            print "d4 < 0 !!!"
        
        return math.sqrt(dist)

    #@param o is object o, CFEntry e=(CFEntry)o    
    def equals(self, o):
        
        e=o
        
        if self.n!=e.n:
            return false
        if self.child!=null and e.child==null:
            return false
        if self.child==null and e.child!=null:
            return false
        if self.child!=null  and  not self.child.equals(e.child):
            return false
        if self.indexList==null  and  e.indexList!=null:
            return false
        if self.indexList!=null  and  e.indexList==null:
            return false
        if not Arrays.equals(self.sumX, e.sumX):
            return false
        if not Arrays.equals(self.sumX2, e.sumX2):
            return false
        if self.indexList!=null  and  not self.indexList.equals(e.indexList):
            return false
        
        return true
        
    def toString(self):
        buff=""
        buff.append(" ")

    	
        l = [x/self.n for x in self.sumX]
        for i in range(len(sumX)):
            buff.append(sum[i]/n +" ")
            
        if self.indexList!=None:
            buff.append("( ")
            for i in range():
                buff.append(i+" ")
                
            buff.append(")")
            
        if self.hasChild():
            buff.append(LINE_SEP)
            buff.append("||" + LINE_SEP)
            buff.append("||" + LINE_SEP)
            buff.append(self.getChild())
            
        return str(buff)
        

class CFEntryPair():
    __LINE_SEP=os.linesep
    e1=CFEntry()
    e2=CFEntry()
       
    def __init__(self, e1=None, e2=None):
        if e1 is None and e2 is None:
            pass
        else:
            self.e1=e1
            self.e2=e2

    def equals(o):
        p=CFEntryPair()
        p=o
        
        if e1.equals(p.e1)  and  e2.equals(p.e2):
            return True
            
        if e1.equals(p.e2)  and  e2.equals(p.e2):
            return True
            
        return False
        
    def toString():
        buff= ""
        
        buff.append("---- CFEntryPiar ----" + LINE_SEP)
        buff.append("---- e1 ----" + LINE_SEP)
        buff.append(str(e1) + LINE_SEP)
        buff.append("---- e2 ----" + LINE_SEP)
        buff.append(str(e2) + LINE_SEP)
        buff.append("-------- end --------" + LINE_SEP)
        
        return str(buff)
        
        
class CFNode():
    __LINE_SEP='\\' #os.linesep()
    entries=0 #stores the CFEntries for this node
    maxNodeEntries=0 #max number of entries per node(parameter B)
    distThreshold=0 #the distance threshold (parameter T), a.k.a. "radius"
    distFunction=0 #CFTree.D0_DIST #the distance function to use
    leafStatus=0 #false #if true, this is a leaf
    #nextLeaf=CFNode() #CFNode() #pointer to the next leaf (if not a leaf, pointer will be numm)
    previousleaf=0 #CFNode() #pointer to the previous leaf (if not a leaf, pointer will be null)
    applyMergingRefinement=0# false #if true, merging refinement will be applied after every split
    
    def __init__(self, maxNodeEntries=None, distThreshold=None, distFunction=None, applyMergingRefindment=None, leafStatus=None):
        self.maxNodeEntries=maxNodeEntries
        self.distThreshold=distThreshold
        self.distFunction=distFunction
        
        self.entries=list()
        self.leafStatus=leafStatus
        self.applyMergingRefindment=applyMergingRefindment
    
    #@return the number of CFEntries in the node
    def size():
        return len(entries)
    
    #@return true if this is only a place-holder node for maintaining correct pointers in the list of leaves
    def isDummy(self):
        return bool((self.maxNodeEntries==0  and  self.distThreshold==0  and  self.size()==0  and  (self.previousLeaf!=None  or  self.nextLeaf!=None)))
    
    #@return the max number of entries the node can host (parameter B)
    def getMaxNodeEntries(self):
        return self.maxNodeEntries
        
    #@return the distance threshold used to decide whether a CFEntry can absorb a new entry
    def getDistThreshold(self):
        return self.distThreshold
        
    def getDistFunction(self):
        return self.distFunction
        
    def getNextLeaf(self):
        self.nextLeaf=CFNode()
        return self.nextLeaf
        
    def getPreviousLeaf(self):
        return self.previousLeaf
        
    def addToEntryList(self, e):
        self.entries.add(e)
        
    def getEntries(self):
        return self.entries
        
    #Retrieves the subcluster id of the closet leaf entry to e
    #@param e the entry to be mapped
    #@return a positive integer, if the leaf entries were enumerated
    def mapToClosetSubcluster(e):
        closest=CFEntry()
        closest=findClosestEntry(e)
        if not closest.hasChild():
            return closest.getSubclusterID()
        
        return closest.getChild().mapToClosetSubcluster(e)
        
    #Inserts a new entry to the CFTree
    #@param e the entry to be inserted
    #@return TRUE if the new entry could be inserted without problems, otherwise we need to split the node
    def insertEntry(self, e):
        if len(self.entries)==0: #if the node is empty we can insert the entry directly here
            self.entries.append(e)
            return True #insert was successful, no split necessary
            
        closest=CFEntry()
        cloest=findCloestEntry(e)
        
        dontSplit=false
        if closest.hasChild(): # if closest has a child we go down with a recursive call
            dontSplit=closest.getChild().insertEntry(e)
            if dontSplit:
                closest.update(e) #this updates the CF to reflect the additional entry
                return True
            else:
                #if the node below/closest/didn't have enough room to host the new entry
                #we need to split it
                splitPair=CFEntryPair()
                splitPair=splitEntry(closest)
                
                #after adding the new entries derived from splitting /closest/ to this node,
                #if we have more than maxEntries we return false,
                #so that the parent node will be split as well to redistribute the "load"
                if entries.size()>maxNodeEntries:
                    return False
                else: #splitting stops at this node
                    if applyMergingRefindment:
                        mergingRefinement(splitPair) #perform step 4 of insert process (see BIRCH paper, Section 4.3)
                        
                    return True
        
        elif closet.isWithinThreshold(e, distThreshold, distFunction):
            #if  dist(closest,e) <= T, /e/ will be "absorbed" by /closest/
            closest.update(e)
            return True #no split necessary at the parent level
            
        elif entries.size()<maxNodeEntries:
            #if /closest/ does not have children, and dist(closest,e) > T
            #if there is enough room in this node, we simply add e to it
            entries.add(e)
            return True #no split necessary at the parent level
            
        else: #not enough space on this node
            entries.add(e) #adds it momentarily to this node
            return False #returns false so that the parent entry will be split
            
    
    #@param closest the entry to be split
    #@return the new entries derived from splitting
    def splitEntry(closest):
        #if there was a child, but we could not insert the new entry without problems THAN
        #split the child of closest entry
        oldNode=CFNode()
        oldNode=closest.getChild()
        oldEntries=closest.getChild().getEntries()
        p=CFEntryPair()
        p=findFarthestEntryPair(oldEntries)
        
        newEntry1=CFEntry()
        newNode1=CFNode(maxNodeEntries, distThreshold, distFunction, applyMergingRefindment, oldNode.isLeaf())
        newEntry1.setChild(newNode1)
        
        newEntry2=CFEntry()
        newNode2=CFNode(maxNodeEntries, distThreshold, distFunction, applyMergingRefindment, oldNode.isLeaf())
        newEntry2.setChild(newNode2)
        
        if oldNode.isLeaf(): #we do this to preserve the pointers in the leafList
            prevL=CFNode()
            prevL=oldNode.getPreviousLeaf()
            nextL=CFNode()
            nextL=oldNode.getNextLeaf()
            
            if prevL!=null:
                prevL.setNextLeaf(newNode1)
                
            if nextL!=null:
                nextL.setPreviousLeaf(newNode2)
                
            newNode1.setPreviousLeaf(prevL)
            newNode1.setNextLeaf(newNode2)
            newNode2.setPreviousLeaf(newNode1)
            newNode2.setNextLeaf(nextL)
            
        redistributeEntries(oldEntries, p, newEntry1, newEntry2)
        #redistributes the entries in n between newEntry1 and newEntry2
        #according to the distance to p.e1 and p.e2
        
        entries.remove(closest) # this will be substitute by two new entries
        entries.add(newEntry1)
        entries.add(newEntry2)
        
        newPair=CFEntryPair(newEntry1, newEntry2)
        
        return newPair
        
    #called when splitting is necessary
    #@param oldEntries
    #@param farEntries
    #@param newE1
    #@param newE2
    def redistributeEntries(oldEntries, farEntries, newE1, newE2):
        e=CFEntry()
        for e in range(oldEntries):
            dist1=farEntries.e1.distance(e, distFunction)
            dist2=farEntries.e2.distance(e, distFunction)
            
            if dist1<=dist2:
                newE1.addToChild(e)
                newE1.update(e)
            else:
                newE2.addToChild(e)
                newE2.update(e)
                
    #called when "merging refinement" is attempted but no actual merging can be applied
    #@param oldEntries1
    #@param oldEntries2
    #@param cloePair
    #@param e1
    #@param e2
    def redistributeEntries(oldEntries1, oldEntries2, closeEntries, newE1, newE2):
        v=list()
        v.addAll(oldEntries1)
        v.addAll(oldEntries2)
        
        e=CFEntry()
        for e in range(len(v)):
            dist1=closeEntries.e1.distance(e, distFunction)
            dist2=closeEntries.e2.distance(e, distFunction)
            
            if dist1<=dist2:
                if newE1.getChildSize()<maxNodeEntries:
                    newE1.addToChild(e)
                    newE1.update(e)
                else:
                    newE2.addToChild(e)
                    newE2.update(e)
            elif dist2<dist1:
                if newE2.getChildSize()<maxNodeEntries:
                    newE2.addToChild(e)
                    newE2.update(e)
                else:
                    newE1.addToChild(e)
                    newE1.update(e)
    
    #called when "merging refinement" is attempted and two entries are actually merged
    #@param oldEntries1
    #@param oldEntries2
    #@param cloePair
    #@param e1
    #@param e2
    def redistributeEntries(oldEntries1, oldEntries2, newE):
        v=list()
        v.addAll(oldEntries1)
        v.allAll(oldEntries2)
        
        e=CFEntries()
        for e in range(len(v)):
            newE.addToChild(e)
            newE.update(e)
            
    #@param e a CFEntry
    #@return the entry in this node that is closest to e 
    def findClosestEntry(e):
        minDist=Double.MAX_VALUE
        closest=CFEntry()
        c=CFEntry()
        for c in range(entries):
            d=c.distance(e, distFunction)
            if d< minDist:
                minDist=d
                closest=c
            
        return closest
        
    def findFarthestEntryPair(entries):
        if entries.size()<2:
            return null
        maxDist=-1
        p=CFEntryPair()
        
        for i in range(0, entries.size()-1):
            for j in range(i+1, entries.size()):
                e1=CFEntry()
                e2=CFEntry()
                e1=entries.get(i)
                e2=entries.get(j)
                
                dist=e1.distance(e2, distFunction)
                if dist>maxDist:
                    p.e1=e1
                    p.e2=e2
                    maxDist=dist
        return p
        
    def findClosestEntryPair(entries):
        if entries.size()<2:
            return null
        minDist=Double.MAX_VALUE
        p=CFEntryPair()
        for i in range(0, entries.size()-1):
            for j in range(i+1, entries.size()):
                e1=CFEntry()
                e2=CFEntry()
                e1=entries.get(i)
                e2=entries.get(j)
                
                dist=e1.distance(e2, distFunction)
                if dist<minDist:
                    p.e1=e1
                    p.e2=e2
                    minDist=dist
        return p
    
    #used during merging refinement
    #@param p
    #@param newE1
    #@param newE2
    def replaceClosestPairWithNewEntries(self, p, newE1, newE2):
        for i in range(0, self.entries.size()):
            if self.entries.get(i).equals(p.e1):
                self.entries.set(i, newE1)
            elif self.entries.get(i).equals(p.e2):
                self.entries.set(i, newE2)
    
    #used during merging refinement
    #@param p
    #@param newE
    def replaceClosestPairWithNewEntries(self, p, newE):
        for i in range(0, self.entries.size()):
            if self.entries.get(i).equals(p.e1):
                self.entries.set(i, newE)
            elif self.entries.get(i).equals(p.e2):
                self.entries.remove(i)

    #@param splitEntries the entry that got split
    def mergingRefinement(self, splitEntries):
        nodeEntries=self.entries
        p=CFEntryPair()
        p=findClosestEntryPair(nodeEntries)
        
        if p==null: #not possible to find a valid pair
            return
        if p.equals(splitEntries): #if the closest pair is the one that was just split, we terminate
            return
            
        oldNode1=CFNode()
        oldNode2=CFNode()
        oldNode1=p.e1.getChild()
        oldNode2=p.e2.getChild()
        
        oldNode1Entries=oldNode1.getEntries()
        oldNode2Entries=oldNode2.getEntries()
        
        if oldNode1.isLeaf()!=oldNode2.isLeaf():
            print "ERROR: Nodes at the same level must have same leaf status" 
            exit()
            
        if (oldNode1Entries.size()+oldNode2Entries.size())>maxNodeEntries:
            #the two nodes cannot be merged into one (they will not fit)
            # in this case we simply redistribute them between p.e1 and p.e2
            newEntry1=CFEntry()
            #note: in the CFNode construction below the last parameter is false
            #because a split cannot happen at the leaf level
            #(the only exception is when the root is first split, but that's treated separately)
            newNode1=CFNode()
            newNode1=oldNode1
            newNode1.resetEntries()
            newEntry1.setChild(newNode1)
            
            newEntry2=CFEntry()
            newNode2=CFNode()
            newNode2=2
            newNode2.resetEntries()
            newEntry2.setChild(newNode2)
            
            redistributeEntries(oldNodeEntries, oldNode2Entries, p, newEntry1, newEntry2)
            replaceClosestPairWithNewEntries(p, newEntry1, newEntry2)
        else:
            #if the two closest entries can actually be merged into one single entry
            newEntry=CFEntry()
            #note:in the CFNode construction below the last parameter is false
            #because a split cannot happen at the leaf level
            #(the only exception is when the root is first split, but that's treated separately)
            newNode=CFNode(maxNodeEntries, distThreshold, distFunction, applyMergingRefindment, oldNode1.isLeaf())
            
            redistributeEntries(oldNode1Entries, oldNode2Entries, newEntry)
            
            if oldNode1.isLeaf()  and  oldNode2.isLeaf():
                if oldNode1.getPreviousLeaf()!=null:
                    oldNode1.getPreviousLeaf().setNextLeaf(newNode)
                if oldNode1.getNextLeaf!=null:
                    oldNode1.getNextLeaf().setPreviousLeaf(newNode)
                newNode.setPreviousLeaf(oldNode1.getPreviousLeaf())
                newNode.setNextLeaf(oldNode1.getNextLeaf())
                
                #this is a dummy node that is only used to maintain proper links in the leafList
                #no CFEntry will ever point to this leaf
                dummy=CFNode(0, 0, 0, false, true)
                if oldNode2.getPreviousLeaf()!=null:
                    oldNode2.getPreviousLeaf().setNextLeaf(dummy)
                if oldNode2.getNextLeaf()!=null:
                    oldNode2.getNextLeaf().setPreviousLeaf(dummy)
                dummy.setPreviousLeaf(oldNode2.getPreviousLeaf())
                dummy.setNextLeaf(oldNode2.getNextLeaf())
                
            replaceClosestPairWithNewMergedEntry(p, newEntry)
            
    #substitutes the entries in this node with the entries of the paremeter node
    #@param n the node from which enries are copied
    
    def replaceEntries(self, n):
        self.entries=n.entries
    
    def resetEntries(self):
        self.entries=list()
        
    def isLeaf(self):
        return bool(self.leafStatus)
        
    #@return true if merging refinement is enabled
    def applyMergingRefinement(self):
        return bool(self.applyMergingRefinement)
    
    def setLeafStatus(self, status):
        self.leafStatus=status
        
    def setNextLeaf(self, l):
        self.nextLeaf=l
    
    def setPreviousLeaf(self, l):
        self.previousLeaf=l
    
    def countChildrenNodes(self):
        n=0
        e=CFEntry()
        for n in range(len(self.entries)):
            if e.hasChild():
                n +=1
                n += e.getChild().countChildrenNodes()
        return n
    
    def countEntriesInChildrenNodes(self):
        n=0
        e=CFEntry()
        for e in range(len(self.entries)):
            if e.hasChild():
                n += e.getChild().size()
                n += e.getChild().countChildrenNodes()
        
        return n
        
    def toString(self):
        buff = StringBuffer()
        
        buff.append("==============================================" + LINE_SEP)
        if self.isLeaf():
            buff.append(">>> THIS IS A LEAF " + LINE_SEP)
        buff.append("Num of Entries = " + entries.size() + LINE_SEP)
        buff.append("{")
        e=CFEntry()
        for e in range(entries):
            buff.append("[" + e + "]")
        
        buff.append("}" + LINE_SEP)
        buff.append("==============================================" + LINE_SEP)
        
        return str(buff)


class CFTree():
    #This is used when computing if the tree is reaching memory limit
    __MEM_LIM_FRAC=10
    #Centroid distance D0
    D0_DIST=0
    #Centroid distance D1
    D1_DIST=1
    #Cluster distance D2
    D2_DIST=2
    #Cluster distance D3
    D3_DIST=3
    #Cluster distance D4
    D4_DIST=4
    #The root node of CF tree
    root=CFNode() #CFNode()
    #dummy node that points to the list of leaves, which is used for fast retrieval of final subclusters
    leafListStart=0 #CFNode()
    #keeps count of the instances inserted into the tree
    instanceIndex=0
    #if true, the tree is automatically rebuilt every time the memory limit is reached
    automaticRebuild=0 #false
    #the memory limit used when automatic rebuilding is active
    memLimit=math.pow(1024, 3) #default=1GB
    #used when automatic rebuilding is active
    periodicMemLimitCheck=100000 #checks if memory limit is exceeded every 100000 insertions
    
    #@param maxNodeEntries parameter B
    #@param distThreshold parameter T
    #@param distFunction must be one of CFTree.D0_DIST, ..., CFTree.D4_DIST, otherwise it will default to D0_DIST
    #@param applyMergingRefinement if true, activates merging refinement after each node split
    def __init__(self, maxNodeEntries=None, distThreshold=None, distFunction=None, applyMergingRefinement=None):
        #global D0_DIST
        #print DO_DIST
        if distFunction<CFTree.D0_DIST or distFunction>CFTree.D4_DIST:
            distFunction=CFTree.D0_DIST
        
        self.root=CFNode(maxNodeEntries, distThreshold, distFunction, applyMergingRefinement, True)
        self.leafListStart=CFNode(0, 0, distFunction, applyMergingRefinement, True) #this is a dummy node that points to the first leaf
        self.leafListStart.setNextLeaf(self.root) #at this point root is the only node and therefore also the only leaf
        
    #@return the current memory limit used to trigger automatic rebuilding
    def getMemoryLimit():
        return CFTree.memLimit
        
    #Gets the start of the list of leaf nodes (note: the first node is a dummy node)
    #@return 
    def getLeafListStart(self):
        return self.leafListStart
    
    #@param limit memory limit in bytes
    def setMemoryLimit(self, limit):
        self.memLimit=limit
        
    #@param limit memory limit in Mbytes
    def setMemoryLimitMB(self, limit):
        self.memLimit=limit*1024*1024
    
    #@param auto if true, and memory limit is reached, the tree is automatically rebuilt when larger threshold
    def setAutomaticRebuild(self, auto):
        self.automaticRebuild=auto
        
    #@param period the number of insert operations after which we check whether the tree has reached the memory limit
    def setPeriodMemLimitCheck(self, period):
        self.periodicMemLimitCheck=period
        
    #Inserts a single pattern vector into the CFTree
    #@param x the pattern vector to be inserted in the tree
    #@return true if insertion was successful
    def insertEntry(self, x):
        self.instanceIndex += 1
        if self.automaticRebuild  and  (self.instanceIndex%self.periodMemLimitCheck)==0:
            #rebuilds the tree if we reached or exceeded memory limit
            rebuildIfAboveMemLimit()
        return bool(self.insertEntry2(x, self.instanceIndex))
        
    #Insert a pattern over with a specific associated pattern vector index
    #This method does not use periodic memory limit checks
    #@param x the pattern vector to be inserted in the tree
    #@param index a specific index associated to the pattern vector x
    #@return true if insertion was successful
    def insertEntry2(self, x, index):
        e=CFEntry(x, index)
        
        return bool(self.insertEntry3(e))
        
    #Inserts an entire CFEntry into the tree, which is used for tree rebuilding
    #@param e the CFEntry to insert
    #@return true if insertion happened without problems
    def insertEntry3(self, e):
        dontSplit=self.root.insertEntry(e)
        if not dontSplit:
            #if dontSplit is false, it means there was not enough space to insert the new entry in the tree
            #therefore we need to split the root to make more room
            splitRoot()
            
            if automaticRebuild:
                #rebuilds the tree if we reached or exceeded memory limits
                rebuildIfAboveMemLimit()
            
        return True #after root is split, we are sure x was inserted correctly in the tree, and we return true
        
    #Every time we split the root, we check whether the memory limit imposed on the tree
    #has been reached. In this case, we automatically increase the distance threshold and
    #rebuild the tree. 
    #
    #It is worth noting that since we only check memory consumption only during root split,
    #and not for all node splits (for performance reasons), we cannot guarantee that
    #the memory limit will not be exceeded. The tree may grow significantly between a 
    #root split and the next.
    #Furthermore, the computation of memory consumption using the SizeOf class is only approximate.
    #
    #Notice also that if the threshold grows to the point that all the entries fall into one entry
    #of the root (i.e., the root is the only node in the tree, and has only one sub-cluster)
    #the automatic rebuild cannot decrease the memory consumption (because increasing the threshold
    #has not effect on reducing the size of the tree)
    #@return true if rebuilt    
    def rebuildIfAboveMemLimit(self):
        if hasReachedMemoryLimit(self, memLimit):
            newThreshold=computeNewThreshold(leafListStart, root.getDistFunction(), root.getDistThreshold())
            newTree=CFTree()
            newTree=self.rebuildTree(root.getMaxNodeEntries(), newThreshold, root.getDistFunction(), root.applyMergingRefinement, false)
            copyTree(newTree)
            
            return True
        return False
        
    #Splits the root to accommodate a new entry. The height of the tree grows by one
    def splitRoot():
        #the split happens by finding the two entries in this node that are the most far apart
        #we then use these two entries as a "pivot" to redistribute the old entries 
        p=CFEntryPair()
        p=self.root.findFarthestEntryPair(self.root.getEntries())
        
        newEntry1=CFEntry()
        newNode1=CFNode(self.root.getMaxNodeEntries(), self.root.getDistThreshold, self.root.getDistFunction, self.root.applyMergingRefinement, self.root.isLeaf())
        newEntry1.setChild(newNode1)
        
        newEntry2=CFEntry()
        newNode2=CFNode(self.root.getMaxNodeEntries(), self.root.getDistThreshold, self.root.getDistFunction, self.root.applyMergingRefinement, self.root.isLeaf())
        newEntry2.setChild(newNode2)
        
        #the new root that hosts the new entries
        newRoot=CFNode(self.root.getMaxNodeEntries, self.root.getDistThreshold, self.root.getDistFunction, self.root.applyMergingRefinement, false)
        newRoot.addToEntryList(newEntry1)
        newRoot.addToEntryList(newEntry2)
        
        #this updates the pointers to the list of leaves
        if self.root.isLeaf(): #if root was a leaf
                self.leafListStart.setNextLeaf(newNode1)
                newNode1.setPreviousLeaf(leafListStart)
                newNode1.setNextLeaf(newNode2)
                newNode2.setPreviousLeaf(newNode1)
            
        #redistributes the entries in the root between newEntry1 and newEntry2
        #according to the distance to p.e1 and p.e2
        self.root.redistributeEntries(self.root.getEntries(), p, newEntry1, newEntry2)
        
        #updates the root
        self.root=newRoot
        
        #frees some memory by deleting the nodes in the tree that had to be split
        gc.collect()
        
    #Overwrites the structure of this tree (all nodes, entries, and leaf list) with the structure of newTree
    #@param newTree the tree to be copied
    def copyTree(self, newTree):
        self.root=newTree.root
        self.leafListStart=newTree.leafListStart
        
    #Computes a new threshold based on the average distance of the closest subclusters in each leaf node
    #@param leafListStart the pointer to the starter of the list (the first node is assumed to be a place-holder dummy node)
    #@param distFunction
    #@param currentThreshold
    #@param the new threshold
    def computeNewThreshold(leafListStart, distFunction, currentThreshold):
        avgDist=0
        n=0
        
        l=CFNode()
        l=leafListStart.getNextLeaf()
        while l!=null:
            if not l.isDummy():
                p=CFEntryPair()
                p=l.findClosestEntryPair(l.getEntries())
                if p!=null:
                    avgDist += p.e1.distance(p.e2, distFunction)
                    n +=1
                    
            l=l.getNextLeaf()
        
        newThreshold=0
        if n>0:
            newThreshold=avgDist/n
        
        if newThreshold <= currentThreshold:
            newThreshold = 2*currentThreshold
            
        return newThreshold
        
    #True if CFTree's memory occupation exceeds or is almost equal to the memory limit
    #@param tree the tree to be tested
    #@param limit the memory limit
    #@return true if memory limit has been reached
    def hasReachedMemoryLimit(tree, limit):
        memory=computeMemorySize(tree)
        if memory >= (limit-limit/MEM_LIM_FRAC) :
            return True
        
        return False
        
    #computes the memory usage of a CFTree
    #@param t a CFTree
    #@return memory usage in bytes
    def computeMemorySize(t):
        memSize=0
        memSize=Sizeof.iterativeSizeof(t)
        
        return memSize
        
    #This implementation of the rebuilding algorithm is different from
    #the one described in Section 4.5 of the paper. However the effect
    #is practically the same. Namely, given a tree t_i build using
    #threshold T_i, if we set a new threshold T_(i+1) and call
    #rebuildTree (assuming maxEntries stays the same) we will obtain
    #a more compact tree. 
    #
    #Since the CFTree is sensitive to the order of the data, there
    #may be cases in which, if we set the T_(i+1) so that non of the
    #sub-clusters (i.e., the leaf entries) can be merged (e.g., T_(i+1)=-1)
    #we might actually obtain a new tree t_(i+1) containing more nodes
    #than t_i. However, the obtained sub-clusters in t_(i+1) will be 
    #identical to the sub-clusters in t_i.
    #
    #In practice, though, if T_(i+1) > T_(i), the tree t_(i+1) will
    #usually be smaller than t_i.
    #Although the Reducibility Theorem in Section 4.5 may not hold
    #anymore, in practice this will not be a big problem, since 
    #even in those cases in which t_(i+1)>t_i, the growth should
    #be very small.
    #
    #The advantage is that relaxing the constraint that the size
    #of t_(i+1) must be less than t_i makes the implementation
    #of the rebuilding algorithm much easier.
    #
    #@param newMaxEntries the new number of entries per node
    #@param newThreshold the new threshold
    #@param applyMergingRefinement if true, merging refinement will e applied after every split
    #@param discardOldTree if true, the old tree will be discarded (to free memory)
    #
    #@return the new (usually more compact) CFTree
    def rebuildTree(self, newMaxEntries, newThreshold, distFunction, applyMergingRefinement, discardOldTree):
        newTree=CFTree(newMaxEntries, newThreshold, distFunction, applyMergingRefinement)
        newTree.instanceIndex=self.instanceIndex
        newTree.memLimit=self.memLimit
        
        oldLeavesList=CFNode()
        oldLeavesList=self.leafListStart.getNextLeaf() #the node self.leafListStart is a dummy node
        
        if discardOldTree:
            self.root=null
            gc.collect() #removes the old tree, only the old leaves will be kept
        
        leaf=CFNode()
        leaf=oldLeavesList
        e=CFEntry()
        while leaf!=null:
            if not leaf.isDummy():
                for e in range(leaf.getEntries):
                    newE=CFEntry()
                    newE=e
                    if not discardOldTree: #make a deep copy
                        newE=CFEntry(e)
                        
                    newTree.insertEntry(newE)
            
            leaf=leaf.getNextLeaf()
        
        if discardOldTree:
            self.leafListStart=null
            gc.collect() #removes the old list of leaves
            
        return newTree
        
    #@return a list of subcluster, and for each subcluster a list of pattern vector indexes that belong to it
    def getSubclusterMembers():
        membersList=list()
        
        l=CFNode()
        l=self.leafListStart.getNextLeaf() #the first leaf is dummy
        e=CFEntry()
        while l!=null:
            if not l.isDummy():
                for e in range(l.getEntries()):
                    membersList.append(e.getIndexList())
            l=l.getNextLeaf()
        
        return membersList
        
    #Signals the fact that we finished inserting data
    #The obtained subclusters will be assigned a positive, unique ID number
    def finishedInsertingData():
        l=CFNode()
        l=self.leafListStart.getNextLeaf() #the firs leaf is dummy
        
        id=0
        e=CFEntry()
        while l!=null:
            if not l.isDummy():
                for e in range(l.getEntries()):
                    id +=1
                    e.setSubclusterID(id)
            l=l.getNextLeaf()
    
    #Retrieves the subcluster id of the closest leaf entry to e
    #@param e the entry to be mapped
    #@return a positive integer, if the leaf entries were enumerated using finishedInsertingData(), otherwise -1
    def mapToClosetSubcluster(x):
        e=CFEntry(x)
        return self.root.mapToClosetSubcluster(e)
        
    #Computes an estimate of the cost of running an o(n^2) algorithm to split each subcluster in more fine-grained clusters
    #@return sqrt(sum_i[(n_i)^2]), where n_i is the number of members of the i-th subcluster
    def computeSumLambdaSquared():
        lambdaSS=0
        
        l=CFNode()
        l=self.leafListStart.getNextLeaf()
        e=CFEntry()
        while l!=null:
            if not l.isDummy():
                for e in range(l.getEntries()):
                    lambdaSS += math.pow(len(e.getIndexList()), 2)
            l=l.getNextLeaf()
        
        return math.sqrt(lambdaSS)
        
    #prints the CFTree
    def printCFTree(self):
        print self.root
        
    #counts the nodes of the tree (including leaves)
    #@return the number of nodes in the tree
    def countNodes(self):
        n=1 #at least root has to be present
        n += self.root.countChildrenNodes()
        
        return n
        
    #counts the number of CFEntries in the tree
    #@return the number of entries in the tree
    def countEntries(self):
        n=sys.getsizeof(self.root) #at least root has to be present
        n += self.root.countEntriesInChildrenNodes()
        
        return n
        
    #counts the number of leaf entries (i.e. the number of sub-clusters in the tree)
    #@return the number of leaf entries (i.e. the number of sub-clusters)
    def countLeafEntries():
        i=0
        l=CFNode()
        l=self.leafListStart.getNextLeaf()
        while l!=None:
            if not l.isDummy():
                i += len(l)
                
            l=l.getNextLeaf()
            
        return i 
        
    #prints the index of all the pattern vectors that fall into the leaf nodes
    #This is only useful for debugging purposes
    def printLeafIndexes():
        indexes=list()
        l=CFNode()
        l=self.leafListStart.getNextLeaf()
        e=CFEntry()
        while l!=null:
            if not l.isDummy():
                print(l)
                for e in range(l.getEntries()):
                    indexes.append(e.getIndexList())
            l=l.getNextLeaf()
        
        v=np.array(indexes)
        sorted(v)
        print "Num of Indexes=%d" %len(v)
        print str(v)
        
    #prints the index of the pattern vectors in each leaf entry (i.e. each subcluster)
    def printLeafEntries(self):
        i=0
        l=CFNode()
        l=self.leafListStart.getNextLeaf()
        e=CFEntry()
        while l!=None:
            if not l.isDummy():
                for i in range(len(l.getEntries())):
                    i=i+1
                    print "[[%d]]" %i
                    v=np.array(e.getIndexList())
                    sorted(v)
                    print str(v)
                    
            l=l.getNextLeaf()
            

if __name__ == '__main__':
    maxNodeEntries = 10
    distThreshold = 10
    distFunction = 10
    applyMergingRefinement = 10
    #datasetFile = open("KL20.txt")

        
    birchTree = CFTree(maxNodeEntries,distThreshold,CFTree.D0_DIST,applyMergingRefinement)
    birchTree.setMemoryLimit(100*1024*1024)
        
    input = open("KL20.txt")
        
    line = ''

    #pdb.set_trace()
    #while (line == input.readline())!=None:
    line == input.readline()
    tmp = line.split(",")
                
    x = [len(tmp)]
    for i in range(0, len(x)):
        x[i] = tmp[i]
                
        inserted = birchTree.insertEntry(x)
        if not inserted:
            print("NOT INSERTED!")
            #exit()
        
    
    print("*************************************************")
    print("*************************************************")
    birchTree.printCFTree();
    print("*************************************************")
    print("*************************************************")
    
    print("****************** LEAVES *******************")
    #birchTree.printLeafEntries()
    print("****************** END *******************")
    #print("****************** INDEXES *******************")
    # birchTree.printLeafIndexes()
    #print("****************** END *******************")
    print "Total CF-Nodes = %d" %birchTree.countNodes()
    print "Total CF-Entries = %d" %birchTree.countEntries()
    print "Total CF-Leaf_Entries = %d" %birchTree.countLeafEntries()
    
    
    
    oldTree = CFTree()
    oldTree = birchTree
    newTree = CFTree()
    newTree = None
    newThreshold = distThreshold
    for i in range(0, 10):
        newThreshold = oldTree.computeNewThreshold(oldTree.getLeafListStart(), distFunction, newThreshold)
        
        print "new Threshold [%d] = %d" %(i, newThreshold)
        
        newTree = oldTree.rebuildTree(maxNodeEntries, newThreshold, distFunction, true, false)
        print "Total CF-Nodes in new Tree[%d] = %d" %(i, newTree.countNodes())
        print "Total CF-Entries in new Tree[%d] = %d"%(i, newTree.countEntries())
        print "Total CF-Leaf_Entries in new Tree[%d] = %d"%(i, newTree.countLeafEntries())
        print "Total CF-Leaf_Entries lambdaSS in new Tree[%d] = %d"%(i, newTree.computeSumLambdaSquared())
        i = i+1
        oldTree = newTree;
    
    members = newTree.getSubclusterMembers();
