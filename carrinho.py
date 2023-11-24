class CarrinhoDeCompras:
    def __init__(self):
        self.items = []

    def adicionar_produto(self, produto):
        self.items.append(produto)

    def remover_produto(self, produto):
        self.items.remove(produto)

    def calcular_total(self):
        total = 0
        for item in self.items:
            total += item.preco
        return total
