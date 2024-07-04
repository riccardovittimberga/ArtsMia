import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._artObjectList=DAO.getAllObjects()
        self._grafo=nx.Graph()
        self._grafo.add_nodes_from(self._artObjectList)
        self._idMap={}
        for v in self._artObjectList:
            self._idMap[v.object_id]=v
        self._solBest=[]
        self._costBest=0

    def getBestPath(self,lun,v0):
        self._solBest = []
        self._costBest = 0

        parziale=[v0]
        for v in self._grafo.neighbors(v0):
            if v.classification==v0.classification:
                parziale.append(v)
                self.ricorsione(parziale,lun)
                parziale.pop()
        return self._solBest, self._costBest

    def ricorsione(self,parziale,lun):
        if len(parziale)==lun:
            if self.peso(parziale)>self._costBest:
                self._costBest=self.peso(parziale)
                self._solBest=copy.deepcopy(parziale)
            return
        for v in self._grafo.neighbors(parziale[-1]):
            if v.classification==parziale[-1].classification and v not in parziale:
                parziale.append(v)
                self.ricorsione(parziale,lun)
                parziale.pop()

    def peso(self,listObject):
        p=0

        for i in range(0, len(listObject)-1):#-1 perché conto gli archi
            p+=self._grafo[listObject[i]][listObject[i+1]]["weight"]
        return p

    def getConnessa(self,v0int):

        #Modo 1
        #non funziona perché alcuni dei successori non sono un unico valore ma si può avere più successori
        v0=self._idMap[v0int]
        successors=nx.dfs_successors(self._grafo,v0)
        #rimedio così
        allSucc=[]
        for v in successors.values():
            allSucc.extend(v)

        #Modo 2
        v0 = self._idMap[v0int]
        predecessors = nx.dfs_predecessors(self._grafo, v0)

        #Danno risultati diversi quindi modo3:
        #conto i nodi dell'albero di visita
        tree=nx.dfs_tree(self._grafo,v0)
        #Dà il risultato con un nodo in più del metodo 2 ma perché conta l'origine

        #modo 4:node_connected_component
        connComp=nx.node_connected_component(self._grafo,v0)
        #fa tutto lui ma ha anche il nodo sorgente
        return len(connComp)

    def creaGrafo(self):
        self.addEdges()

    def addEdges(self):
        self._grafo.clear_edges()

        allEdges = DAO.getAllConnessioni(self._idMap)
        for e in allEdges:
            self._grafo.add_edge(e.v1,e.v2,weight=e.peso)

    def checkExistence(self,idOggetto):
        return idOggetto in self._idMap

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    def getObjFromId(self, idOggetto):
        return self._idMap[idOggetto]
