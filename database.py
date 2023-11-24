import sqlite3


class Database:
    def __init__(self, db_name="ecommerce.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def criar_tabelas(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL
            )
        """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL
            )
        """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                descricao TEXT NOT NULL,
                preco REAL NOT NULL
            )
        """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS carrinho (
                id INTEGER PRIMARY KEY,
                id_cliente INTEGER,
                id_produto INTEGER,
                FOREIGN KEY (id_cliente) REFERENCES clientes (id),
                FOREIGN KEY (id_produto) REFERENCES produtos (id)
            )
        """
        )

        self.conn.commit()

    def close_connection(self):
        self.conn.close()


# Instanciando o objeto Database
db = Database()
