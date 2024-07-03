from dataclasses import dataclass
from model.product import Product


@dataclass
class Connessione:
    p1: Product
    p2: Product
    vendite: int

    def __hash__(self):
        return hash((self.p1, self.p2))

    def __str__(self):
        return f"Arco da {self.p1.Product_number} a {self.p2.Product_number}, peso={self.vendite}"
