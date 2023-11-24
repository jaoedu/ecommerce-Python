class Produto:
    def __init__(self, id_produto, nome, descricao, preco):
        self.id_produto = id_produto
        self.nome = nome
        self.descricao = descricao
        self.preco = preco

    def __str__(self):
        return f"{self.nome} - R${self.preco}"
