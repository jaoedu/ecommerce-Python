import getpass
import sqlite3
import time
import os
from cliente import Cliente
from funcionario import Funcionario
from produto import Produto
from carrinho import CarrinhoDeCompras
from database import db


class Ecommerce:
    def __init__(self):
        self.cliente = None
        self.funcionario = None
        self.carrinho = CarrinhoDeCompras()

    def fazer_login_cliente(self, email_cliente=None, senha_cliente=None):
        if email_cliente is None:
            email_cliente = input("Digite seu email: ")
        if senha_cliente is None:
            senha_cliente = getpass.getpass("Digite sua senha: ")

        try:
            db.cursor.execute(
                "SELECT * FROM clientes WHERE email = ? AND senha = ?",
                (email_cliente, senha_cliente),
            )
            cliente_data = db.cursor.fetchone()

            if cliente_data:
                id_cliente, nome, email, senha, tipo = cliente_data
                self.cliente = Cliente(id_cliente, nome, email, senha)
                return True
            else:
                print("Credenciais inválidas.")
                return False
        except sqlite3.Error as e:
            print(f"Erro ao fazer login: {e}")
            return False

    def fazer_login_funcionario(self, email_funcionario=None, senha_funcionario=None):
        if email_funcionario is None:
            email_funcionario = input("Digite seu email: ")
        if senha_funcionario is None:
            senha_funcionario = getpass.getpass("Digite sua senha: ")

        try:
            db.cursor.execute(
                "SELECT id, nome, email, senha FROM funcionarios WHERE email = ? AND senha = ?",
                (email_funcionario, senha_funcionario),
            )
            funcionario_data = db.cursor.fetchone()

            if funcionario_data:
                id_funcionario, nome, email, senha = funcionario_data
                self.funcionario = Funcionario(id_funcionario, nome, email, senha)
                print("Acesso Permitido")
                return True
            else:
                print("Credenciais invalidas.")
                return False
        except sqlite3.Error as e:
            print(f"Erro ao fazer login: {e}")
            return False

    def exibir_opcoes_tenis(self):
        print("Produtos disponíveis:")
        db.cursor.execute("SELECT * FROM produtos")
        produtos_data = db.cursor.fetchall()

        for produto_data in produtos_data:
            id_produto, nome, descricao, preco = produto_data
            produto = Produto(id_produto, nome, descricao, preco)
            print(f"{id_produto}. {produto}")

    def escolher_produto(self):
        self.exibir_opcoes_tenis()
        escolha = input(
            "Escolha um produto para adicionar ao carrinho (digite o número do produto): "
        )

        try:
            id_produto = int(escolha)
            db.cursor.execute("SELECT * FROM produtos WHERE id = ?", (id_produto,))
            produto_data = db.cursor.fetchone()

            if produto_data:
                id_produto, nome, descricao, preco = produto_data
                produto = Produto(id_produto, nome, descricao, preco)
                self.carrinho.adicionar_produto(produto)
                print(f"{produto.nome} foi adicionado ao carrinho.")
            else:
                print("Produto não encontrado.")
        except ValueError:
            print("Escolha inválida. Por favor, escolha um número válido.")

    def remover_produto(self):
        if not self.carrinho.items:
            print("Seu carrinho está vazio.")
            return

        print("Seu carrinho:")
        for i, produto in enumerate(self.carrinho.items, start=1):
            print(f"{i}. {produto}")

        escolha = input(
            "Escolha um produto para remover do carrinho (digite o número do produto): "
        )

        try:
            index = int(escolha) - 1
            if 0 <= index < len(self.carrinho.items):
                produto_removido = self.carrinho.items.pop(index)
                print(f"{produto_removido.nome} foi removido do carrinho.")
            else:
                print("Escolha inválida. Por favor, escolha um número válido.")
        except ValueError:
            print("Escolha inválida. Por favor, escolha um número válido.")

    def finalizar_compra(self):
        if not self.carrinho.items:
            print("Seu carrinho está vazio. Nada para comprar.")
            return

        total = self.carrinho.calcular_total()

        for produto in self.carrinho.items:
            db.cursor.execute(
                "INSERT INTO carrinho (id_cliente, id_produto) VALUES (?, ?)",
                (self.cliente.id_cliente, produto.id_produto),
            )

        db.conn.commit()

        print(f"Compra realizada com sucesso! Total: R${total}")

    def alterar_informacoes_cadastro_cliente(self):
        novo_nome = input(
            "Digite o novo nome (ou pressione Enter para manter o atual): "
        )
        novo_email = input(
            "Digite o novo email (ou pressione Enter para manter o atual): "
        )
        nova_senha = getpass.getpass(
            "Digite a nova senha (ou pressione Enter para manter a atual): "
        )

        if not novo_nome:
            novo_nome = self.cliente.nome

        if not novo_email:
            novo_email = self.cliente.email

        if not nova_senha:
            nova_senha = self.cliente.senha

        self.cliente.alterar_informacoes(novo_nome, novo_email, nova_senha)
        db.cursor.execute(
            "UPDATE clientes SET nome = ?, email = ?, senha = ? WHERE id = ?",
            (novo_nome, novo_email, nova_senha, self.cliente.id_cliente),
        )
        db.conn.commit()
        print("Informações de cadastro atualizadas com sucesso.")

    def deletar_conta_como_cliente(self):
        if self.cliente is None:
            print("Você precisa fazer login como cliente para excluir uma conta.")
            return False

        confirmacao = input(
            "Tem certeza que deseja excluir a conta do cliente? (Digite 'sim' para confirmar): "
        )
        if confirmacao.lower() == "sim":
            try:
                db.cursor.execute(
                    "DELETE FROM clientes WHERE id = ?", (self.cliente.id_cliente,)
                )
                db.conn.commit()
                print("Conta do cliente excluída com sucesso.")
                input("Pressione Enter para voltar ao menu principal.")
                self.main_ecommerce()  # Adicionando esta linha para redirecionar ao menu principal
                return True
            except sqlite3.Error as e:
                print(f"Erro ao excluir conta do cliente: {e}")
                return False
        else:
            print("Exclusão de conta cancelada.")
            return False

    def exibir_carrinho(self):
        if not self.carrinho.items:
            print("Seu carrinho está vazio.")
        else:
            print("Seu carrinho:")
            for i, produto in enumerate(self.carrinho.items, start=1):
                print(f"{i}. {produto}")
            print(f"Total: R${self.carrinho.calcular_total()}")

    def main_ecommerce_cliente(self):
        while True:
            time.sleep(2)
            os.system("cls" if os.name == "nt" else "clear")
            print(f"Bem-vindo, {self.cliente.nome}!")

            opcoes = {
                "1": self.exibir_opcoes_tenis,
                "2": self.escolher_produto,
                "3": self.remover_produto,
                "4": self.finalizar_compra,
                "5": self.alterar_informacoes_cadastro_cliente,
                "6": self.deletar_conta_como_cliente,
                "7": self.exibir_carrinho,  # Adicionando a opção para exibir o carrinho
                "8": lambda: None,  # Sair
            }

            print("1. Exibir produtos")
            print("2. Adicionar produto ao carrinho")
            print("3. Remover produto do carrinho")
            print("4. Finalizar compra")
            print("5. Alterar informações de cadastro")
            print("6. Deletar conta")
            print("7. Exibir carrinho")
            print("8. Sair")

            escolha = input("Escolha uma opção: ")

            if escolha in opcoes:
                opcoes[escolha]()
                if escolha == "8":
                    print("Redirecionando para o menu principal...")
                    break  # corrigindo aqui para sair do loop
            else:
                print("Opção inválida. Tente novamente.")

    def main_ecommerce_funcionario(self):
        while True:
            time.sleep(2)
            os.system("cls" if os.name == "nt" else "clear")
            print(f"Bem-vindo, {self.funcionario.nome}!")

            opcoes = {
                "1": (
                    self.funcionario.cadastrar_produto,
                    "Digite o nome do produto: ",
                    "Digite a descrição do produto: ",
                    "Digite o preço do produto: ",
                ),
                "2": self.funcionario.alterar_informacoes_funcionario,
                "3": self.funcionario.deletar_conta_cliente,
                "4": lambda: None,  # Sair
            }

            print("1. Cadastrar produto")
            print("2. Alterar informações de cadastro")
            print("3. Deletar conta do cliente")
            print("4. Sair")

            escolha = input("Escolha uma opção: ")

            if escolha in opcoes:
                if escolha == "1":
                    # Se a escolha for cadastrar_produto, solicite os detalhes do produto
                    args = [input(msg) for msg in opcoes[escolha][1:]]
                    # Chama a função com os detalhes do produto como argumentos
                    opcoes[escolha][0](*args)
                else:
                    # Se não for a opção de cadastrar_produto, chama a função sem argumentos
                    opcoes[escolha]()

                if escolha == "4":
                    print("Redirecionando para o menu principal...")
                    break  # corrigindo aqui para sair do loop
            else:
                print("Opção inválida. Tente novamente.")

    def main_ecommerce(self):
        while True:
            time.sleep(2)
            os.system("cls" if os.name == "nt" else "clear")

            opcoes_login = {
                "1": self.cadastrar_cliente,
                "2": self.cadastrar_funcionario,
                "3": self.fazer_login_cliente,
                "4": self.fazer_login_funcionario,
                "5": lambda: exit(),  # Sair
            }

            print("1. Cadastrar como cliente")
            print("2. Cadastrar como funcionário")
            print("3. Fazer login como cliente")
            print("4. Fazer login como funcionário")
            print("5. Sair")

            escolha = input("Escolha uma opção: ")

            if escolha in opcoes_login:
                os.system("cls" if os.name == "nt" else "clear")
                if opcoes_login[escolha]():
                    break  # Se o login for bem-sucedido, sair do loop
            else:
                print("Opção inválida. Tente novamente.")

    def cadastrar_cliente(self):
        nome = input("Digite seu nome: ")
        email = input("Digite seu email: ")
        senha = getpass.getpass("Digite sua senha: ")

        db.cursor.execute(
            "INSERT INTO clientes (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
            (nome, email, senha, "cliente"),  # Adiciona 'cliente' como o valor do tipo
        )
        db.conn.commit()
        print("Cadastro realizado com sucesso!")
        time.sleep(2)

    def cadastrar_funcionario(self):
        nome = input("Digite seu nome: ")
        email = input("Digite seu email: ")
        senha = getpass.getpass("Digite sua senha: ")

        try:
            db.cursor.execute(
                "INSERT INTO funcionarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
                (nome, email, senha, "funcionario"),
            )
            db.conn.commit()
            print("Cadastro realizado com sucesso!")
            time.sleep(2)
        except db.sqlite3.IntegrityError as e:
            print(f"Erro ao cadastrar funcionário: {e}")


if __name__ == "__main__":
    db.criar_tabelas()

    ecommerce = Ecommerce()
    ecommerce.main_ecommerce()

    email = input("Digite seu email: ")
    senha = getpass.getpass("Digite sua senha: ")

    if ecommerce.fazer_login_cliente(email, senha):
        ecommerce.main_ecommerce_cliente()
    elif ecommerce.fazer_login_funcionario(email, senha):
        ecommerce.main_ecommerce_funcionario()
    else:
        print("Credenciais inválidas. Acesso negado.")

    db.close_connection()
