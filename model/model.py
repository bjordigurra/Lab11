import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._listaColori = DAO.getColori()
        self._grafo = nx.Graph()
        self._allProducts = DAO.getAllProducts()
        self._idMap = {}
        for product in self._allProducts:
            self._idMap[product.Product_number] = product
        self._connessioniGrafo = []
        self._solBest = []
        self._lunghezzaBest = 0

    def creaGrafo(self, colore, anno):
        self._grafo.clear()
        self._connessioniGrafo = []
        # aggiungo i nodi
        listaNodi = DAO.getProductsColor(colore)
        self._grafo.add_nodes_from(listaNodi) # aggiungo i prodotti filtrati per colore come nodi del grafo

        # aggiungo gli archi nel grafo
        """
        # itero sui prodotti già filtrati per colore e faccio una query ogni volta per trovare le loro connessioni
        # faccio anche un controllo per verificare che l'arco esista già, in modo da evitare doppioni
        for nodo in listaNodi:
            print(f"nodo - {nodo}")
            connessioni = DAO.getConnessioni(anno, nodo.Product_number, self._idMap)
            for c in connessioni:  # connessione = tupla con 3 posti: (prodotto1, prodotto2, numero vendite)
                print(f"connessione - {c}")
                if self._grafo.has_edge(nodo, c.p2) or self._grafo.has_node(c.p2) is False:
                    continue
                else:
                    self._grafo.add_edge(nodo, c.p2, weight=c.vendite)
                    print(f"aggiunto nuovo arco")
        """

        # utilizzo una query unica per ottenere tutte le connessioni
        self._connessioniGrafo = DAO.getAllConnessioni(colore, anno, self._idMap)
        for c in self._connessioniGrafo:
            self._grafo.add_edge(c.p1, c.p2, weight=c.vendite)
            print(f"Aggiunto arco {c.p1} - {c.p2} con peso {c.vendite}")

    def getPercorso(self, source):
        self._solBest = []
        self._lunghezzaBest = 0
        partenza = self._idMap[source]
        #rimanenti = copy.deepcopy(list(self._grafo.nodes))
        # chiamo la ricorsione e quando finisco, ritorno la solbest
        parziale = [partenza] # inizializzo il parziale con il primo nodo, cioè quello di partenza
        for vicino in nx.neighbors(self._grafo, partenza):
            parziale.append(vicino)
            self._ricorsione(parziale, partenza)
            parziale.pop()

        return self._solBest, self._lunghezzaBest

    def _ricorsione(self, parziale, partenza): # non abbastanza buona
        print("sono qui")
        # condizione terminale, come faccio a capire che sono al limite? Quando l'ultimo nodo a cui arrivo
        # non ha più vicini che devono essere esplorati
        if len(parziale) == len(self._grafo.nodes) or parziale[0] != partenza:
            return

        # devo avere una lista copia dei nodi del grafo da cui tolgo i nodi già esplorati (rimanenti)
        # e ogni volta che entro nella ricorsione controllo i vicini dell'ultimo nodo per controllare
        # che ce ne siano ancora nei rimanenti

        # ottimalità: controllo il numero degli archi
        if len(parziale) - 1 > self._lunghezzaBest:
            self._solBest = copy.deepcopy(parziale)
            self._lunghezzaBest = len(parziale) - 1

        for vicino in self._grafo.neighbors(parziale[-1]):
            if vicino not in parziale and self._arcoAmmissibile(parziale, vicino):
                parziale.append(vicino)
                self._ricorsione(parziale, partenza)
                parziale.pop()

    def _arcoAmmissibile(self, parziale, successivo):
        # ritorna True se posso aggiungere il nodo al parziale, cioè se l'arco che unisce l'ultimo elemento
        # del parziale ha un peso maggiore di quello tra parziale[-2] e parziale[-1]
        if len(parziale) == 1:
            return True # qualsiasi arco ha un peso maggiore in questo caso, dato che non ce ne è ancora nessuno

        ultimoPeso = self._grafo[parziale[-2]][parziale[-1]]["weight"]
        nuovoPeso = self._grafo[parziale[-1]][successivo]["weight"]
        if nuovoPeso >= ultimoPeso:
            return True
        else:
            return False

    def numNodes(self):
        return len(self._grafo.nodes)

    def numEdges(self):
        return len(self._grafo.edges)

    def getProdottiColore(self, colore):
        return DAO.getProductsColor(colore)

    @property
    def grafo(self):
        return self._grafo


