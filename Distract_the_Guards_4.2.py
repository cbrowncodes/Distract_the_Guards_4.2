import collections
import itertools

def answer(banana_list):
    numGuards=len(banana_list)
    guards=[Node(banana_list[i]) for i in range(numGuards)]
    #basically a crude graph implementation. Guards that loop when paired
    #are added to each others' loop list, functioning as edges on a graph.
    #Guards that don't loop are added to the exit list.
    for i in range(0,numGuards-1):
        for j in range(i+1,numGuards):
            if infiniteLoop(banana_list[i],banana_list[j]):
                guards[i].loop.append(guards[j])
                guards[j].loop.append(guards[i])
            else:
                guards[i].exit.append(guards[j])
                guards[j].exit.append(guards[i])
    counter=0
    #If there happens to be an odd number of guards. It's probably safe
    #to guess there are always an even number, but that isn't specified
    #and it shouldn't be assumed.
    if numGuards%2==1:
        single=Node(-1)
        for guard in guards:
            single.exit.append(guard)
            guard.exit.append(single)
        guards.append(single)
        counter-=1
    #I was unable to fully implement the Edmonds' blossom algorithm,
    #this solution isn't as thorough but it works for this situation.
    #Iterates through the graph and finds optimal pairings. Also
    #disconnects bad pairings.
    while len(guards)>0:
        guards.sort(key=lambda x: len(x.exit),reverse=True)
        currentGuard=guards[0]
        good=False
        for currentPair in guards[1:]:
            if currentPair in currentGuard.loop:
                removePair(guards, currentGuard,currentPair)
                good=True
                break
        if not good:
            counter+=2
            removePair(guards,currentGuard,guards[1])
    return counter
                
def disconnect(nodeList,node):
    for n in node.exit:
        n.exit.remove(node)
    for n in node.loop:
        n.loop.remove(node)
    nodeList.remove(node)

def removePair(nodeList,node1,node2):
    disconnect(nodeList,node1)
    disconnect(nodeList,node2)

#Most pairings are infinite loops. I determined that they do not loop
#when y/x=(2^n)-1 (assuming y>x), or y=(x*[power of 2])+1
def infiniteLoop(x,y):
    if x==y:
        return False
    if x>y:
        return infiniteLoop(y,x)
    val=(y/x)
    val+=1
    return not(val !=0 and ((val & (val-1))==0))
 
#Each Guard is a node. This class contains the number of bananas,
#a list of nodes sharing edges, and a list of nodes not sharing edges.
class Node:
    def __init__(self,bananas):
        self.bananas=bananas
        self.exit=[]
        self.loop=[]
