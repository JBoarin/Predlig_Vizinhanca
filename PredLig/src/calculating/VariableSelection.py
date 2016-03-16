'''
Created on Jul 1, 2015

@author: cptullio
'''
import networkx
import os.path
from formating.dblp.Formating import Formating
from datetime import datetime
from formating.FormatingDataSets import FormatingDataSets

#MAX_NUMBER_OF_PEOPLE_BETWEEN = 2;
#MAX_DISTANCE_NEIGHBORHOOD = 3;

class VariableSelection(object):

    @staticmethod
    def getItemFromLine(lineofFile):
        cols = lineofFile.strip().replace('\n','').split('\t')
        return [cols[0], eval(cols[1])]
    
    
    def get_all_pair_nodes(self, graph, file):
        
        nodesinGraph =set(n for n,d in graph.nodes(data=True) if d['node_type'] == 'N')
        nodesOrdered = sorted(nodesinGraph)
        for node1 in nodesOrdered:
            others =  set(n for n in nodesOrdered if n > node1)
            file.write(str(node1) + '\t' +  repr(others) + '\n')
       
            
        
        
    def get_pair_nodes_not_linked(self, graph, file, min_papers):
        print "Starting getting pair of nodes that is not liked", datetime.today()
        results = []
        nodesinGraph =set(n for n,d in graph.nodes(data=True) if d['node_type'] == 'N')
        currentNodes = set()
        for n in nodesinGraph:
            
            papers = set(networkx.all_neighbors(graph, n))
            print papers
            if (len(papers) >= min_papers):
                currentNodes.add(n)
        
        print 'qty of authors: ', len(currentNodes)
        nodesOrdered = sorted(currentNodes)
        element = 0
        totalnodesOrdered = len(nodesOrdered)
        for node1 in nodesOrdered:
            element = element+1
            FormatingDataSets.printProgressofEvents(element, totalnodesOrdered, "Checking Node not liked: ")
            
            others =  set(n for n in nodesOrdered if n > node1)
            notLinked = set()
            for other_node in others:
                if len(set(networkx.common_neighbors(graph, node1, other_node))) == 0:
                    #notLinked.add(other_node) # como estava antes
                    # esse if abaixo verifica se estao perto
                    if networkx.has_path(graph, node1, other_node):
                        tamanho_caminho = len(networkx.shortest_path(graph, node1, other_node)) - 2
                        #print "%s ate %s: %s" %(node1, other_node,tamanho_caminho)
                        #print repr(networkx.shortest_path(graph, node1, other_node));
                        if ( tamanho_caminho > 0 ) and (tamanho_caminho <= self.MAX_NUMBER_OF_PEOPLE_BETWEEN * 2 + 1 ): # -2 porque inclui o inicio e fim
                            print "adicionando %s - %s" %(node1, other_node)
                            notLinked.add(other_node)
            if len(notLinked) > 0:
                results.append([node1, notLinked])
            if element % 2000 == 0:
                for item in results:
                    file.write(str(item[0]) + '\t' +  repr(item[1]) + '\n')
                results = []
                
        for item in results:
            file.write(str(item[0]) + '\t' +  repr(item[1]) + '\n')
        results = []
            
        print "getting pair of nodes that is not liked finished", datetime.today()
        
    

    def __init__(self, graph,  filepathNodesToCalculate, min_papers = 1, allNodes = False, MAX_NUMBER_OF_PEOPLE_BETWEEN = 1000):
        self.MAX_NUMBER_OF_PEOPLE_BETWEEN = MAX_NUMBER_OF_PEOPLE_BETWEEN
        myfile = Formating.get_abs_file_path(filepathNodesToCalculate)
        if not os.path.exists(myfile):
            with open(myfile, 'w') as fnodes:
                if allNodes:
                    self.get_all_pair_nodes(graph, fnodes)
                else:
                    self.get_pair_nodes_not_linked(graph,fnodes, min_papers)
                fnodes.close()
        else:
            print "Nodes not linked file already generated. please delete if you want a new one.", datetime.today()
                 
            
        