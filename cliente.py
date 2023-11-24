class Cliente:
    def __init__(self, id_cliente, nome, email, senha):
        self.id_cliente = id_cliente
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = "cliente"  # Adicionamos uma propriedade para indicar o tipo

    def fazer_login(self, email, senha):
        return email == self.email and senha == self.senha

    def alterar_informacoes(self, novo_nome, novo_email, nova_senha):
        self.nome = novo_nome
        self.email = novo_email
        self.senha = nova_senha
