import copy
import operator

import flet as ft
import networkx as nx


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        # dd dei colori, che prendo tramite una query dal DAO
        self._listColor = copy.deepcopy(self._model._listaColori)
        self._listColor.sort()
        for color in self._listColor:
            self._view._ddcolor.options.append(ft.dropdown.Option(color))

    def handle_graph(self, e):
        self._view.txtOut.controls.clear()
        self._view.update_page()

        if self._view._ddyear.value is None or self._view._ddcolor.value is None:
            self._view.create_alert("Inserire anno e colore!")
            return

        self._model.creaGrafo(self._view._ddcolor.value, self._view._ddyear.value)

        self._view.txtOut.controls.append(ft.Text("Grafo correttamente creato!"))
        self._view.txtOut.controls.append(ft.Text(f"Il grafo ha {self._model.numNodes()} nodi."))
        self._view.txtOut.controls.append(ft.Text(f"Il grafo ha {self._model.numEdges()} archi."))

        # successivamente stampo i 3 archi con i costi maggiori
        # ordino la lista degli edges per peso con lambda
        #archi = nx.get_edge_attributes(self._model.grafo, "weight")
        # dizionario che ha come chiave la tupla edge e come valore il weight
        # archi.sort(key=operator.attrgetter("vendite"), reverse=True)
        # for i in range(3):
        # self._view.txtOut.controls.append(ft.Text(archi[i]))

        connessioni = self._model._connessioniGrafo # lista di oggetti Connessione ottenuta dal DAO
        # è già ordinata per numero di vendite decrescente, mi basta prendere i primi 3 da stampare

        lista_nodi = []
        contatore = 0
        for c in connessioni:
            if contatore > 2:
                break
            else:
                self._view.txtOut.controls.append(ft.Text(c))
                lista_nodi.extend([c.p1, c.p2])
                contatore += 1

        insieme_nodi = set(lista_nodi)
        da_stampare = []
        for nodo in insieme_nodi:
            if lista_nodi.count(nodo) > 1:
                da_stampare.append(nodo.Product_number)

        if len(da_stampare) != 0:
            self._view.txtOut.controls.append(ft.Text(f"I nodi ripetuti sono: {da_stampare}"))
        else:
            self._view.txtOut.controls.append(ft.Text("Non ci sono nodi ripetuti in più archi"))

        self.fillDDProduct()

        self._view.update_page()


    def fillDDProduct(self):
        # per riempire il dd dei prodotti, devo fare una query che prenda tutti i prodotti dalla tabella
        prodotti = self._model.getProdottiColore(self._view._ddcolor.value)

        for p in prodotti:
            self._view._ddnode.options.append(ft.dropdown.Option(p.Product_number))

    def handle_search(self, e):
        self._view.txtOut2.controls.clear()
        if self._view._ddnode.value is None:
            self._view.create_alert("Selezionare un prodotto!")
            self._view.update_page()
            return

        percorso, lunghezza = self._model.getPercorso(int(self._view._ddnode.value))
        self._view.txtOut2.controls.append(ft.Text(f"Numero archi percorso più lungo: {lunghezza}"))

        self._view.update_page()
