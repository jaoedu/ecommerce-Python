from database import db
from produto import Produto


class Funcionario:
    def __init__(self, id_funcionario, nome, email, senha):
        self.id_funcionario = id_funcionario
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = "funcionario"

    def fazer_login(self, email, senha):
        try:
            db.cursor.execute(
                "SELECT * FROM funcionarios WHERE email = ? AND senha = ?",
                (email, senha),
            )
            funcionario_data = db.cursor.fetchone()

            if funcionario_data:
                id_funcionario, nome, email, senha, tipo = funcionario_data
                self.id_funcionario = id_funcionario
                self.nome = nome
                self.email = email
                self.senha = senha
                self.tipo = tipo
                return True

            return False
        except db.sqlite3.Error as e:
            print(f"Erro ao fazer login: {e}")
            return False

    def alterar_informacoes_funcionario(self, novo_nome, novo_email, nova_senha):
        self.nome = novo_nome
        self.email = novo_email
        self.senha = nova_senha

    def cadastrar_produto(self, nome, descricao, preco):
        db.cursor.execute(
            "INSERT INTO produtos (nome, descricao, preco) VALUES (?, ?, ?)",
            (nome, descricao, preco),
        )
        db.conn.commit()
        print("Produto cadastrado com sucesso.")

    def deletar_conta_cliente(self):
        try:
            print("Lista de clientes:")
            db.cursor.execute("SELECT id, nome, email FROM clientes")
            clientes_data = db.cursor.fetchall()

            for cliente_data in clientes_data:
                id_cliente, nome, email = cliente_data
                print(f"{id_cliente}. Nome: {nome}, Email: {email}")

            while True:
                id_cliente = input("Digite o ID do cliente que deseja excluir: ")

                try:
                    id_cliente = int(id_cliente)
                    # Verifica se o ID existe na base de dados
                    db.cursor.execute(
                        "SELECT * FROM clientes WHERE id = ?", (id_cliente,)
                    )
                    cliente_existente = db.cursor.fetchone()

                    if cliente_existente:
                        break  # ID válido, sai do loop
                    else:
                        print("ID não encontrado na base de dados. Tente novamente.")
                except ValueError:
                    print("Por favor, digite um número válido.")

            confirmacao = input(
                "Tem certeza que deseja excluir a conta do cliente? (Digite 'sim' para confirmar): "
            )

            if confirmacao.lower() == "sim":
                try:
                    db.cursor.execute(
                        "DELETE FROM clientes WHERE id = ?", (id_cliente,)
                    )
                    db.conn.commit()
                    print(f"Conta do cliente com ID {id_cliente} excluída com sucesso.")
                except db.sqlite3.Error as e:
                    print(f"Erro ao excluir conta do cliente: {e}")
            else:
                print("Exclusão de conta cancelada.")
        except db.sqlite3.Error as e:
            print(f"Erro ao recuperar lista de clientes: {e}")

    def exibir_produtos(self):
        print("Produtos disponíveis:")
        db.cursor.execute("SELECT * FROM produtos")
        produtos_data = db.cursor.fetchall()

        for produto_data in produtos_data:
            id_produto, nome, descricao, preco = produto_data
            produto = Produto(id_produto, nome, descricao, preco)
            print(f"{id_produto}. {produto}")
