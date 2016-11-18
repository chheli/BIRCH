# This is an implementation of BIRCH clustering algorithm
# This programming is inspired by Roberto Perdisci's BIRCH implementation in Java (http://roberto.perdisci.com/projects/jbirch)
# The reference paper is BIRCH: An Efficient Data Clustering Method for Very Large Databases (http://www.cs.sfu.ca/cc/459/han/papers/zhang96.pdf)
# @author Chuhe Li(chli1403@student.miun.se)

import os
import math
import pdb
import numpy as np
import sys
import gc
import copy

class CFEntry():
    
    LINE_SEP=os.linesep #get line separator of current system
    n=0 #number of patterns summarized by this entry
    sumX=[] #array sumX
    sumX2=[] #array sumX2
    child=None
    indexList=[] #list indexList
    subclusterID=-1 # the unique id that describes a subcluster (valid only for leaf entries)
    
    def __init__(self, x=None, index=None):
        #if type(x) is list:
            
        if x is None and index is None:
            pass
            
        elif x is not None and index is None:
            self(x, 0)
        elif x is not None and index is not None:
            self.n=1
                
            self.sumX=[]
            #print "###"
            #print type(x)
            #print "###"
            #if type(x) is list:
            for i in x:
                self.sumX.append(i)
            #else:
                #self.sumX.append(x)
            #print self.sumX
            #print "self.sumX is %s" %self.sumX
            self.sumX2=[]
            #if type(x) is list:
            for i in range(len(self.sumX)):
                self.sumX2.append(x[i]*x[i])
            #else:
                #self.sumX2.append(x*x)
            self.indexList=[]
            self.indexList.append(index)
            #print "index is %s" %index
            #print "indexList is %s" %self.indexList
    
        #else:
            #self.n=x.n
            #print x.n
            
            #self.sumX=copy.deepcopy(x.sumX)
            #print "deepcopy"
            #print copy.deepcopy(x.sumX)
            #self.sumX2=copy.deepcopy(x.sumX2)
            #self.child=x.child
            #self.indexList=list()
            #for i in x.getIndexList():
                #self.indexList.append(i)

        
    #This makes a deep copy of the CFEntry e
    #WARNING: we do not make a deep copy of the child
    #@param e the entry to be cloned
    def copy(self, e):
        self.n=e.n
        self.sumX=copy.deepcopy(e.sumX)
        self.sumX2=copy.deepcopy(e.sumX2)
        self.child=e.child
        
        #print e.getIndexList()
        
        #e.indexList=list()
        #self.child=None
        #print self.indexList
        
        self.indexList=list()
        
        #print e.getIndexList()
        
        for i in e.indexList:
            self.indexList.append(i)
            
        #print e.getIndexList()
        
            
    def getIndexList(self):
        #print "##############"
        #print self.indexList
        return self.indexList
   
    def hasChild(self):
        #self.child=CFNode()
        return bool(self.child != None)
    
    def getChild(self):
        return self.child
    
    def getChildSize(self):
        return len(self.child.getEntries())
    
    def setChild(self, n):
        self.child=n
        self.indexList=[] #we don't keep this if this becomes a non-leaf entry
    
    def setSubclusterID(id):
        self.subclusterID=id
    
    def getSubclusterID(self):
        return self.subclusterID
        
    def update(self, e):
        self.n += e.n
        
        if self.sumX==None:
            self.sumX=copy.deepcopy(e.sumX)
        else:
            for i in range(len(self.sumX)):
                self.sumX[i] += e.sumX[i]
        
        if self.sumX2==None:
            self.sumX2=copy.deepcopy(e.sumX2)
        else:
            for i in range(len(self.sumX2)):
                self.sumX2[i] += e.sumX2[i]
                
        if not self.hasChild(): #we keep indexList only if we are at a leaf 
            if self.indexList is not None and e.indexList is not None:
                self.indexList.extend(e.indexList) ###extend can take e.indexList as an iterable but not a object
            elif self.indexList is None and e.indexList is not None:
                self.indexList=copy.deepcopy(e.indexList)
        
    def addToChild(self, e):
        #add directly to the child node
        self.child=CFNode()
        self.child.getEntries().append(e)


    def isWithinThreshold(self, e, threshold, distFunction):
        dist=self.distance(e, distFunction)
        
        if dist==0 or dist<=threshold:
            return True
            
        return False
        
    #@param e
    #@return the distance between this entry and e
    def distance(self, e, distFunction):
        dist=sys.float_info.max        
        
        #switch case function
        if distFunction==CFTree.D0_DIST:
            dist = self.d0(self, e)
        elif distFunction==CFTree.D1_DIST:
            dist = self.d1(self, e)
        elif distFunction==CFTree.D2_DIST:
            dist = self.d2(self, e)
        elif distFunction==CFTree.D3_DIST:
            dist = self.d3(self, e)
        elif distFunction==CFTree.D4_DIST:
            dist = self.d4(self, e)
        else:
            dist = self.d0(self, e)
        
        return dist
    
    def d0(self, e1, e2):
        dist=0
        #print "e1.sumX is %s" %e1.sumX
        for i in range(len(e1.sumX)):
            
            #print e2.sumX
            #print e1.n
            #print e2.n
        
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
        
    def d1(self, e1, e2):
        dist=0
        for i in range(len(e1.sumX)):
            diff=math.abs(e1.sumX[i]/e1.n - e2.sumX[i]/e2.n)
            dist += diff
            
        if dist<0:
            print "d1<0!!!"
            
        return dist
        
    def d2(self, e1, e2):
        dist=0
        n1=e1.n
        n2=e2.n
        for i in range(len(e1.sumX)):
            diff=(n2*e1.sumX2[i] - 2*e1.sumX[i]*e2.sumX[i] + n1*e2.sumX2[i])/(n1 * n2)
            dist += diff
        
        if dist<0:
            print "d2<0!!!"
            
        return math.sqrt(dist)
        
    def d3(self, e1, e2):
        dist=0
        n1=e1.n
        n2=e2.n
        totSumX=copy.deepcopy(e1.sumX)
        totSumX2=copy.deepcopy(e1.sumX2)
        
        for i in range(len(e2.sumX)):
            totSumX[i] += e2.sumX[i]
            totSumX2[i] += e2.sumX2[i]
            
        for i in range(len(totSumX)):
            diff = ((n1+n2)*totSumX2[i] - 2*totSumX[i]*totSumX[i] + (n1+n2)*totSumX2[i])/((n1+n2)*(n1+n2-1))
            dist+=diff
            
        if dist<0:
            print "d3<0!!!"
            
        return math.sqrt(dist)
        
    def d4(self, e1, e2):
        dist = 0
        
        n1 = e1.n
        n2 = e2.n
        totSumX = copy.deepcopy(e1.sumX)
        totSumX2 = copy.deepcopy(e1.sumX2)
        for i in range(len(e2.sumX)):
            totSumX[i] += e2.sumX[i];
            totSumX2[i] += e2.sumX2[i];
                
        for i in range(len(totSumX)):
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
            return False
        if self.child is not None and e.child==None:
            return False
        if self.child==None and e.child is not None:
            return False
        if self.child is not None  and  not self.child is e.child:
            return False
        if self.indexList==None  and  e.indexList is not None:
            return False
        if self.indexList is not None  and  e.indexList==None:
            return False
        if not self.sumX is e.sumX:
            return False
        if not self.sumX2 is e.sumX2:
            return False
        if self.indexList is not None  and  not self.indexList is e.indexList:
            return False
        
        return True
        
    def __str__(self):
        buff=""
        buff += " "

        #print self.sumX
        #print self.n
        #print self.indexList
        for sumx in self.sumX:

            buff += str(sumx/self.n) +" "
            
        if self.indexList is not None:
            buff += "( "
            #print self.indexList
            for i in self.indexList:
                #print str(self.indexList[i])
                buff += str(i)+" "
            #print self.indexList
            #buff += str(self.indexList)    
            buff += ")"
            
        if self.hasChild():
            buff += CFEntry.LINE_SEP
            buff += "||" + CFEntry.LINE_SEP
            buff += "||" + CFEntry.LINE_SEP
            buff += str(self.getChild())
            
        return buff        


class CFEntryPair():
    LINE_SEP=os.linesep
    e1=CFEntry()
    e2=CFEntry()
       
    def __init__(self, e1=None, e2=None):
        if e1 is None and e2 is None:
            pass
        else:
            self.e1=e1
            self.e2=e2
    
   
    def equals(self, o):
        #p=CFEntryPair()
        p=o
        
        if self.e1.equals(p.e1)  and  self.e2.equals(p.e2):
            return True
            
        if self.e1.equals(p.e2)  and  self.e2.equals(p.e2):
            return True
            
        return False
        
    def __str__():
        buff= ""
        
        buff += "---- CFEntryPiar ----" + CFEntryPair.LINE_SEP
        buff += "---- e1 ----" + CFEntryPair.LINE_SEP
        buff += str(e1) + CFEntryPair.LINE_SEP
        buff += "---- e2 ----" + CFEntryPair.LINE_SEP
        buff += str(e2) + CFEntryPair.LINE_SEP
        buff += "-------- end --------" + CFEntryPair.LINE_SEP
        
        return buff
        
        
class CFNode():
    LINE_SEP=os.linesep
    entries=list() #stores the CFEntries for this node
    maxNodeEntries=0 #max number of entries per node(parameter B)
    distThreshold=0 #the distance threshold (parameter T), a.k.a. "radius"
    distFunction=0 #CFTree.D0_DIST #the distance function to use
    leafStatus=False #if true, this is a leaf
    nextLeaf=None #CFNode() #pointer to the next leaf (if not a leaf, pointer will be numm)
    previousleaf=None #CFNode() #pointer to the previous leaf (if not a leaf, pointer will be None)
    applyMergingRefinement=False #if true, merging refinement will be applied after every split
    
    def __init__(self, maxNodeEntries=None, distThreshold=None, distFunction=None, applyMergingRefinement=None, leafStatus=None):
        self.maxNodeEntries=maxNodeEntries
        self.distThreshold=distThreshold
        self.distFunction=distFunction
        
        self.entries=list()
        self.leafStatus=leafStatus
        self.applyMergingRefinement=applyMergingRefinement


    #@return the number of CFEntries in the node
    def size(self):
        return len(self.entries)
    
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
        #self.nextLeaf=CFNode()
        return self.nextLeaf
        
    def getPreviousLeaf(self):
        return self.previousLeaf
        
    def addToEntryList(self, e):
        self.entries.append(e)
        
    def getEntries(self):
        return self.entries
        
    #Retrieves the subcluster id of the closest leaf entry to e
    #@param e the entry to be mapped
    #@return a positive integer, if the leaf entries were enumerated
    def mapToClosestSubcluster(e):
        #closest=CFEntry()
        closest=self.findClosestEntry(e)
        if not closest.hasChild():
            return closest.getSubclusterID()
        
        return closest.getChild().mapToClosestSubcluster(e)
        
    #Inserts a new entry to the CFTree
    #@param e the entry to be inserted
    #@return TRUE if the new entry could be inserted without problems, otherwise we need to split the node
    def insertEntry(self, e):
        if len(self.entries)==0: #if the node is empty we can insert the entry directly here
            self.entries.append(e)
            return True #insert was successful, no split necessary
            
        #closest=CFEntry()
        #print str(e)
        closest=self.findClosestEntry(e)
        #print "Closest Entry = %s"%closest
        
        dontSplit=False
        if closest.hasChild(): # if closest has a child we go down with a recursive call
            dontSplit=closest.getChild().insertEntry(e)
            if dontSplit:
                closest.update(e) #this updates the CF to reflect the additional entry
                return True
            else:
                #if the node below/closest/didn't have enough room to host the new entry
                #we need to split it
                splitPair=CFEntryPair()
                splitPair=self.splitEntry(closest)
                
                #after adding the new entries derived from splitting /closest/ to this node,
                #if we have more than maxEntries we return false,
                #so that the parent node will be split as well to redistribute the "load"
                if len(self.entries)>self.maxNodeEntries:
                    return False
                else: #splitting stops at this node
                    if self.applyMergingRefinement:
                        #print splitPair.e1
                        self.mergingRefinement(splitPair) #perform step 4 of insert process (see BIRCH paper, Section 4.3)
                        
                    return True
        
        elif closest.isWithinThreshold(e, self.distThreshold, self.distFunction):
            #if  dist(closest,e) <= T, /e/ will be "absorbed" by /closest/
            closest.update(e)
            return True #no split necessary at the parent level
            
        elif len(self.entries)<self.maxNodeEntries:
            #if /closest/ does not have children, and dist(closest,e) > T
            #if there is enough room in this node, we simply add e to it
            self.entries.append(e)
            return True #no split necessary at the parent level
            
        else: #not enough space on this node
            self.entries.append(e) #adds it momentarily to this node
            return False #returns false so that the parent entry will be split
            
    
    #@param closest the entry to be split
    #@return the new entries derived from splitting
    def splitEntry(self, closest):
        #if there was a child, but we could not insert the new entry without problems THAN
        #split the child of closest entry
        #oldNode=CFNode()
        oldNode=closest.getChild()
        oldEntries=closest.getChild().getEntries()
        #p=CFEntryPair()
        p=self.findFarthestEntryPair(oldEntries)
        
        newEntry1=CFEntry()
        newNode1=CFNode(self.maxNodeEntries, self.distThreshold, self.distFunction, self.applyMergingRefinement, oldNode.isLeaf())
        newEntry1.setChild(newNode1)
        
        newEntry2=CFEntry()
        newNode2=CFNode(self.maxNodeEntries, self.distThreshold, self.distFunction, self.applyMergingRefinement, oldNode.isLeaf())
        newEntry2.setChild(newNode2)
        
        if oldNode.isLeaf(): #we do this to preserve the pointers in the leafList
            #prevL=CFNode()
            prevL=oldNode.getPreviousLeaf()
            #nextL=CFNode()
            nextL=oldNode.getNextLeaf()
            
            if prevL is not None:
                prevL.setNextLeaf(newNode1)
                
            if nextL is not None:
                nextL.setPreviousLeaf(newNode2)
                
            newNode1.setPreviousLeaf(prevL)
            newNode1.setNextLeaf(newNode2)
            newNode2.setPreviousLeaf(newNode1)
            newNode2.setNextLeaf(nextL)
            
        self.redistributeEntries(oldEntries, p, newEntry1, newEntry2)
        #redistributes the entries in n between newEntry1 and newEntry2
        #according to the distance to p.e1 and p.e2
        
        self.entries.remove(closest) # this will be substitute by two new entries
        self.entries.append(newEntry1)
        self.entries.append(newEntry2)
        
        newPair=CFEntryPair(newEntry1, newEntry2)
        
        return newPair
        
    #called when splitting is necessary
    #@param oldEntries
    #@param farEntries
    #@param newE1
    #@param newE2
    def redistributeEntries(self, oldEntries, farEntries, newE1, newE2):
        #e=CFEntry()
        #print newE1, newE2
        for e in oldEntries:
            #print e
            dist1=farEntries.e1.distance(e, self.distFunction)
            dist2=farEntries.e2.distance(e, self.distFunction)
            
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
    def redistributeEntries1(self, oldEntries1, oldEntries2, closeEntries, newE1, newE2):
        v=[]
        v.extend(oldEntries1)
        v.extend(oldEntries2)
        
        #e=CFEntry()
        for e in v:
            dist1=closeEntries.e1.distance(e, self.distFunction)
            dist2=closeEntries.e2.distance(e, self.distFunction)
            
            if dist1<=dist2:
                if newE1.getChildSize()<self.maxNodeEntries:
                    newE1.addToChild(e)
                    newE1.update(e)
                else:
                    newE2.addToChild(e)
                    newE2.update(e)
            elif dist2<dist1:
                if newE2.getChildSize()<self.maxNodeEntries:
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
    def redistributeEntries2(self, oldEntries1, oldEntries2, newE):
        v=[]
        v.extend(oldEntries1)
        v.extend(oldEntries2)
        #print v
        
        for e in v:
            
            newE.addToChild(e)
            newE.update(e)
            
    #@param e a CFEntry
    #@return the entry in this node that is closest to e 
    def findClosestEntry(self, e):
        minDist=sys.float_info.max
        closest=CFEntry()
        #c=CFEntry()
        for c in self.entries:
            d=c.distance(e, self.distFunction)
            #print d
            if d< minDist:
                minDist=d
                closest=c
            
        return closest
        
    def findFarthestEntryPair(self, entries):
        if len(entries)<2:
            return None
        
        maxDist=-1
        p=CFEntryPair()
        
        for i in range(len(entries)-1):
            for j in range(i+1, len(entries)):
                #e1=CFEntry()
                #e2=CFEntry()
                
                e1=entries[i]
                e2=entries[j]
                
                dist=e1.distance(e2, self.distFunction)
                if dist>maxDist:
                    p.e1=e1
                    p.e2=e2
                    maxDist=dist
        return p
        
    def findClosestEntryPair(self, entries):
        if len(entries)<2:
            return None

        minDist=sys.float_info.max
        p=CFEntryPair()

        for i in range(len(entries)-1):
            for j in range(i+1, len(entries)):
                #e1=CFEntry()
                #e2=CFEntry()
                e1=entries[i]
                e2=entries[j]
                
                dist=e1.distance(e2, self.distFunction)
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
        for i in range(len(self.entries)):
            if self.entries[i].equals(p.e1):
                self.entries.insert(i, newE1)
                
            elif self.entries[i].equals(p.e2):
                self.entries.insert(i, newE2)
    
    #used during merging refinement
    #@param p
    #@param newE
    def replaceClosestPairWithNewMergedEntry(self, p, newE):
        for i in range(len(self.entries)):
            if self.entries[i].equals(p.e1):
                self.entries.insert(i, newE)
            elif self.entries[i].equals(p.e2):
                self.entries.pop(i)

    #@param splitEntries the entry that got split
    def mergingRefinement(self, splitEntries):
        print ">>>>>>>>>>>>>>> Merging Refinement <<<<<<<<<<<<"
        print splitEntries.e1
        print splitEntries.e2

        nodeEntries=self.entries
        #p=CFEntryPair()
        p=self.findClosestEntryPair(nodeEntries)
        
        if p==None: #not possible to find a valid pair
            return
        if p.equals(splitEntries): #if the closest pair is the one that was just split, we terminate
            return
            
        oldNode1=CFNode()
        oldNode2=CFNode()
        oldNode1=p.e1.getChild()
        oldNode2=p.e2.getChild()
        
        oldNode1Entries=oldNode1.getEntries()
        oldNode2Entries=oldNode2.getEntries()
        
        if oldNode1.isLeaf()!= oldNode2.isLeaf():
            print "ERROR: Nodes at the same level must have same leaf status" 
            exit()
            
        if (len(oldNode1Entries)+len(oldNode2Entries))>self.maxNodeEntries:
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
            newNode2=oldNode2
            newNode2.resetEntries()
            newEntry2.setChild(newNode2)
            
            self.redistributeEntries1(oldNode1Entries, oldNode2Entries, p, newEntry1, newEntry2)
            self.replaceClosestPairWithNewEntries(p, newEntry1, newEntry2)
        else:
            #if the two closest entries can actually be merged into one single entry
            newEntry=CFEntry()
            #note:in the CFNode construction below the last parameter is false
            #because a split cannot happen at the leaf level
            #(the only exception is when the root is first split, but that's treated separately)
            newNode=CFNode(self.maxNodeEntries, self.distThreshold, self.distFunction, self.applyMergingRefinement(), oldNode1.isLeaf())
            newEntry.setChild(newNode)
            
            self.redistributeEntries2(oldNode1Entries, oldNode2Entries, newEntry)
            
            if oldNode1.isLeaf()  and  oldNode2.isLeaf():
                if oldNode1.getPreviousLeaf() is not None:
                    oldNode1.getPreviousLeaf().setNextLeaf(newNode)
                if oldNode1.getNextLeaf is not None:
                    oldNode1.getNextLeaf().setPreviousLeaf(newNode)
                newNode.setPreviousLeaf(oldNode1.getPreviousLeaf())
                newNode.setNextLeaf(oldNode1.getNextLeaf())
                
                #this is a dummy node that is only used to maintain proper links in the leafList
                #no CFEntry will ever point to this leaf
                dummy=CFNode(0, 0, 0, False, True)
                if oldNode2.getPreviousLeaf() is not None:
                    oldNode2.getPreviousLeaf().setNextLeaf(dummy)
                if oldNode2.getNextLeaf() is not None:
                    oldNode2.getNextLeaf().setPreviousLeaf(dummy)
                dummy.setPreviousLeaf(oldNode2.getPreviousLeaf())
                dummy.setNextLeaf(oldNode2.getNextLeaf())
                
            self.replaceClosestPairWithNewMergedEntry(p, newEntry)
            
    #substitutes the entries in this node with the entries of the paremeter node
    #@param n the node from which enries are copied
    
    def replaceEntries(self, n):
        self.entries=n.entries
    
    def resetEntries(self):
        self.entries=list()
        
    def isLeaf(self):
        return bool(self.leafStatus)
        #return bool(self.leafStatus)
        
    #@return true if merging refinement is enabled
    def applyMergingRefinementFunction(self):
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
        for e in self.entries:
            if e.hasChild():
                n +=1
                n += e.getChild().countChildrenNodes()
        return n
    
    def countEntriesInChildrenNodes(self):
        n=0
        #e=CFEntry()
        for e in self.entries:
            if e.hasChild():
                
                n += e.getChild().size()
                n += e.getChild().countChildrenNodes()
        
        return n
        
    def __str__(self):
        buff = ""
        
        buff += "==============================================" + CFNode.LINE_SEP

        if self.isLeaf():
            buff += ">>> THIS IS A LEAF " + CFNode.LINE_SEP
           
        buff += "Num of Entries = " + str(len(self.entries)) + CFNode.LINE_SEP
        buff += "{"

        
        for e in self.entries:
            buff += "["  + str(e) + "]"

        buff += "}" + CFNode.LINE_SEP
        buff += "==============================================" + CFNode.LINE_SEP
        
        return buff


class CFTree():
    #This is used when computing if the tree is reaching memory limit
    __MEM_LIM_FRAC=10
    #Centroid Euclidian distance D0
    D0_DIST=0
    #Centroid Manhattan distance D1
    D1_DIST=1
    #Cluster distance D2
    D2_DIST=2
    #Cluster distance D3
    D3_DIST=3
    #Cluster distance D4
    D4_DIST=4
    #The root node of CF tree
    root=CFNode() 
    #dummy node that points to the list of leaves, which is used for fast retrieval of final subclusters
    leafListStart=CFNode()
    #keeps count of the instances inserted into the tree
    instanceIndex=0
    #if true, the tree is automatically rebuilt every time the memory limit is reached
    automaticRebuild=False
    #the memory limit used when automatic rebuilding is active
    memLimit=math.pow(1024, 3) #default=1GB
    #used when automatic rebuilding is active
    periodicMemLimitCheck=100000 #checks if memory limit is exceeded every 100000 insertions
    
    #@param maxNodeEntries parameter B
    #@param distThreshold parameter T
    #@param distFunction must be one of CFTree.D0_DIST, ..., CFTree.D4_DIST, otherwise it will default to D0_DIST
    #@param applyMergingRefinement if true, activates merging refinement after each node split
    def __init__(self, maxNodeEntries, distThreshold, distFunction, applyMergingRefinement):
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
            self.rebuildIfAboveMemLimit()
        #print x
        #print self.instanceIndex
        return bool(self.insertEntry2(x, self.instanceIndex))
        
    #Insert a pattern over with a specific associated pattern vector index
    #This method does not use periodic memory limit checks
    #@param x the pattern vector to be inserted in the tree
    #@param index a specific index associated to the pattern vector x
    #@return true if insertion was successful
    def insertEntry2(self, x, index):
        #print index
        e=CFEntry(x, index)
        #print e
        #print "x is %s"%x
        #print "e is %s"%e
        #print "Inserting %s" %e
        
        return bool(self.insertEntry3(e))
        
    #Inserts an entire CFEntry into the tree, which is used for tree rebuilding
    #@param e the CFEntry to insert
    #@return true if insertion happened without problems
    i = 1
    def insertEntry3(self, e):
        #print e
        dontSplit=self.root.insertEntry(e)
        #print self.i, dontSplit
        self.i += 1
        if not dontSplit:
            #if dontSplit is false, it means there was not enough space to insert the new entry in the tree
            #therefore we need to split the root to make more room
            self.splitRoot()
            
            if self.automaticRebuild:
                #rebuilds the tree if we reached or exceeded memory limits
                self.rebuildIfAboveMemLimit()
            
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
            newThreshold=self.computeNewThreshold(self.leafListStart, self.root.getDistFunction(), self.root.getDistThreshold())
            #newTree=CFTree()
            newTree=self.rebuildTree(self.root.getMaxNodeEntries(), newThreshold, self.root.getDistFunction(), self.root.applyMergingRefinement(), False)
            self.copyTree(newTree)
            
            return True
        return False
        
    #Splits the root to accommodate a new entry. The height of the tree grows by one
    def splitRoot(self):
        #the split happens by finding the two entries in this node that are the most far apart
        #we then use these two entries as a "pivot" to redistribute the old entries 
        #p=CFEntryPair()
        p=self.root.findFarthestEntryPair(self.root.getEntries())
        
        newEntry1=CFEntry()
        newNode1=CFNode(self.root.getMaxNodeEntries(), self.root.getDistThreshold(), self.root.getDistFunction(), self.root.applyMergingRefinementFunction(), self.root.isLeaf())
        newEntry1.setChild(newNode1)
        
        newEntry2=CFEntry()
        newNode2=CFNode(self.root.getMaxNodeEntries(), self.root.getDistThreshold(), self.root.getDistFunction(), self.root.applyMergingRefinementFunction(), self.root.isLeaf())
        newEntry2.setChild(newNode2)
        
        #the new root that hosts the new entries
        newRoot=CFNode(self.root.getMaxNodeEntries(), self.root.getDistThreshold(), self.root.getDistFunction(), self.root.applyMergingRefinementFunction(), False)
        newRoot.addToEntryList(newEntry1)
        newRoot.addToEntryList(newEntry2)
        
        #this updates the pointers to the list of leaves
        if self.root.isLeaf(): #if root was a leaf
            self.leafListStart.setNextLeaf(newNode1)
            newNode1.setPreviousLeaf(self.leafListStart)
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
    def computeNewThreshold(self, leafListStart, distFunction, currentThreshold):
        avgDist=0
        n=0
        
        #l=CFNode()
        l=leafListStart.getNextLeaf()
        while l is not None:
            if not l.isDummy():
                #p=CFEntryPair()
                p=l.findClosestEntryPair(l.getEntries())
                if p is not None:
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
        memory=self.computeMemorySize(tree)
        if memory >= (limit-limit/CFTree.MEM_LIM_FRAC) :
            return True
        
        return False
        
    #computes the memory usage of a CFTree
    #@param t a CFTree
    #@return memory usage in bytes
    def computeMemorySize(t):
        memSize=0
        memSize=sys.getsizeof(t)
        
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
        #print "self.instanceIndex is %s" %self.instanceIndex
        newTree.memLimit=self.memLimit
        
        oldLeavesList=CFNode()
        oldLeavesList=self.leafListStart.getNextLeaf() #the node self.leafListStart is a dummy node
        
        if discardOldTree:
            self.root=CFNode()
            gc.collect() #removes the old tree, only the old leaves will be kept
        
        leaf=CFNode()
        leaf=oldLeavesList
        #print "leaf is %s"%leaf
        e=CFEntry()
        #print str(leaf.getEntries())
        while leaf is not None:
            if not leaf.isDummy():
                for e in leaf.getEntries():
                    
                    newE=CFEntry()
                    #newE=e
                    #print e
                    if not discardOldTree: #make a deep copy
                        newE.copy(e)
                        #print e
                    #print e  
                    #print "newE is %s" %newE    
                    newTree.insertEntry3(newE)
            #print "leaf.getNextLeaf() is %s"%leaf.getNextLeaf()
            leaf=leaf.getNextLeaf()
            
        
        if discardOldTree:
            self.leafListStart=None
            gc.collect() #removes the old list of leaves
            
        return newTree
        
    #@return a list of subcluster, and for each subcluster a list of pattern vector indexes that belong to it
    def getSubclusterMembers(self):
        membersList=list()
        
        #l=CFNode()
        l=self.leafListStart.getNextLeaf() #the first leaf is dummy
        #e=CFEntry()
        while l!=None:
            if not l.isDummy():
                for e in l.getEntries():
                    membersList.append(e.getIndexList())
            l=l.getNextLeaf()
        
        return membersList
        
    #Signals the fact that we finished inserting data
    #The obtained subclusters will be assigned a positive, unique ID number
    def finishedInsertingData():
        #l=CFNode()
        l=self.leafListStart.getNextLeaf() #the firs leaf is dummy
        
        id=0
        #e=CFEntry()
        while l is not None:
            if not l.isDummy():
                for e in l.getEntries():
                    id +=1
                    e.setSubclusterID(id)
            l=l.getNextLeaf()
    
    #Retrieves the subcluster id of the closest leaf entry to e
    #@param e the entry to be mapped
    #@return a positive integer, if the leaf entries were enumerated using finishedInsertingData(), otherwise -1
    def mapToClosestSubcluster(x):
        e=CFEntry(x)
        return self.root.mapToClosestSubcluster(e)
        
    #Computes an estimate of the cost of running an o(n^2) algorithm to split each subcluster in more fine-grained clusters
    #@return sqrt(sum_i[(n_i)^2]), where n_i is the number of members of the i-th subcluster
    def computeSumLambdaSquared(self):
        lambdaSS=0
        
        #l=CFNode()
        l=self.leafListStart.getNextLeaf()
        #print "self.leafListStart.getNextLeaf() is %s" %self.leafListStart.getNextLeaf()
        #e=CFEntry()
        while l is not None:
            if not l.isDummy():
                for e in l.getEntries():
                    #print l.getEntries()
                    #print e.getIndexList()
                    lambdaSS += math.pow(len(e.getIndexList()), 2)
                    #print "lambdaSS is %s" %lambdaSS
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
        n = self.root.size() #at least root has to be present
        n += self.root.countEntriesInChildrenNodes()
        
        return n
        
    #counts the number of leaf entries (i.e. the number of sub-clusters in the tree)
    #@return the number of leaf entries (i.e. the number of sub-clusters)
    def countLeafEntries(self):
        i=0
        #l=CFNode()
        l=self.leafListStart.getNextLeaf()
        while l is not None:
            if not l.isDummy():
                i += l.size()
                
            l=l.getNextLeaf()
            
        return i 
        
    #prints the index of all the pattern vectors that fall into the leaf nodes
    #This is only useful for debugging purposes
    def printLeafIndexes(self):
        indexes=list()
        #l=CFNode()
        l=self.leafListStart.getNextLeaf()
        #e=CFEntry()
        while l!=None:
            if not l.isDummy():
                print l
                for e in l.getEntries():
                    indexes.append(e.getIndexList())
            l=l.getNextLeaf()
        
        print "Num of Indexes=%d" %len(indexes)
        print str(indexes)
        
    #prints the index of the pattern vectors in each leaf entry (i.e. each subcluster)
    def printLeafEntries(self):
        i=0
        #l=CFNode()
        l=self.leafListStart.getNextLeaf()
        #print self.leafListStart
        #e=CFEntry()
        #print "self.leafListStart.getNextLeaf() is %s" %self.leafListStart.getNextLeaf()
        while l is not None:
            if not l.isDummy():
                for e in l.getEntries():
                    #print e
                    i=i+1
                    print "[[%d]]" %i
                    #v=np.array(e.getIndexList())
                    #sorted(v)
                    v=e.getIndexList()
                    print v


            l=l.getNextLeaf()
            

if __name__ == '__main__':
    maxNodeEntries = 400
    distThreshold = 0.5
    distFunction = 0
    applyMergingRefinement = False
        
    birchTree = CFTree(maxNodeEntries,distThreshold,distFunction,applyMergingRefinement)
    birchTree.setMemoryLimit(1*1024*1024)

    #print birchTree

    #pdb.set_trace()
    with open("KL20.txt") as dataFile:
        for line in dataFile:
            #line=dataFile.readline()
            tmp = line.split(",")
                        
            x = []
            for i in range(len(tmp)):
                
                x.append(float(tmp[i]))

            #print x
            inserted = birchTree.insertEntry(x)
            #print inserted
            if not inserted:
                print("NOT INSERTED!")
                exit()
        

    print("*************************************************")
    print("*************************************************")
    #pdb.set_trace()
    birchTree.printCFTree();
    print("*************************************************")
    print("*************************************************")

    
    print("****************** LEAVES ***********************")
    birchTree.printLeafEntries()
    print("******************* END *************************")
    #print("****************** INDEXES *******************")
    #birchTree.printLeafIndexes()
    #print("****************** END *******************")
    print "Total CF-Nodes = %d" %birchTree.countNodes()
    print "Total CF-Entries = %d" %birchTree.countEntries()
    print "Total CF-Leaf_Entries = %d" %birchTree.countLeafEntries()
    print "Total CF-Leaf_Entries lambdaSS = %d"%(birchTree.computeSumLambdaSquared())
        
    

    oldTree = birchTree

    newThreshold = distThreshold
    for i in range(10):
        newThreshold = oldTree.computeNewThreshold(oldTree.getLeafListStart(), distFunction, newThreshold)
        print("*************************************************")
        print "new Threshold [%d] = %d" %(i, newThreshold)
        newTree = oldTree.rebuildTree(maxNodeEntries, newThreshold, distFunction, applyMergingRefinement, False)
        print "Total CF-Nodes in new Tree[%d] = %d" %(i, newTree.countNodes())
        print "Total CF-Entries in new Tree[%d] = %d"%(i, newTree.countEntries())
        print "Total CF-Leaf_Entries lambdaSS in new Tree[%d] = %d"%(i, newTree.computeSumLambdaSquared())
        oldTree = newTree;
    
    members = newTree.getSubclusterMembers();
