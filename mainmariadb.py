import mysql.connector
import random

CONFIG_BANCO = {
    'host': 'localhost',
    'user': 'root',
    'password': 'dev1t@24',
    'database': 'fatallady_bd',
}
conexao = mysql.connector.connect(**CONFIG_BANCO)
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS PRODUTOS (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Preco DECIMAL(10,2) NOT NULL,
    Estoque INT NOT NULL,
    Marca VARCHAR(50) NOT NULL,
    Tamanhos VARCHAR(10) NOT NULL,
    Categoria VARCHAR(50) NOT NULL
)
""")
conexao.commit()

valores = [
    ("Scarpin Clássico Preto", 189.90, 25, "Fatal Lady", "36/39", "Salto Alto"),
    ("Sandália Salto Alto Nude", 159.99, 30, "Fatal Lady", "36/38", "Sandália"),
    ("Sapatilha Verniz Vermelha", 99.90, 40, "Fatal Lady", "35/39", "Sapatilha"),
    ("Bota Cano Curto Couro", 249.90, 15, "Fatal Lady", "37/40", "Bota"),
    ("Sandália Rasteira Dourada", 89.90, 60, "Fatal Lady", "35/40", "Rasteirinha"),
    ("Bota Over The Knee Preta", 329.90, 10, "Fatal Lady", "36/39", "Bota"),
    ("Sandália Gladiadora Preta", 129.90, 15, "Fatal Lady", "38/39", "Sandália"),
    ("Bota Coturno Feminina Marrom", 219.90, 20, "Fatal Lady", "37/40", "Bota"),
    ("Sapatilha Bico Fino Nude", 109.90, 35, "Fatal Lady", "37/38", "Sapatilha"),
    ("Sandália Meia Pata Vermelha", 189.90, 12, "Fatal Lady", "35/36", "Sandália"),
    ("Peep Toe Preto Verniz", 159.90, 18, "Fatal Lady", "37/38", "Salto Alto"),
    ("Bota Montaria Marrom", 289.90, 14, "Fatal Lady", "38/39", "Bota"),
    ("Sandália Salto Fino Prata", 199.90, 16, "Fatal Lady", "37/38", "Sandália")
]


marca = "Fatal Lady"
cores = ["Preto", "Branco", "Nude", "Vermelho", "Marrom", "Bege", "Cinza", "Dourado", "Prata"]
categorias = ["Sandália", "Bota", "Salto Alto", "Rasteirinha", "Sapatilha"]
tamanhos = ["35/38", "37/40", "38/41", "39/42"]
quantidades = list(range(10, 61))

# Gerar mais 1000 produtos aleatórios
for _ in range(1000):
    categoria = random.choice(categorias)
    cor = random.choice(cores)
    nome = f"{categoria} {cor}"
    preco = round(random.uniform(69.9, 329.9), 2)
    quantidade = random.choice(quantidades)
    tamanho = random.choice(tamanhos)
    valores.append((nome, preco, quantidade, marca, tamanho, categoria))

sql = """
INSERT INTO PRODUTOS (Nome, Preco, Estoque, Marca, Tamanhos, Categoria)
VALUES (%s, %s, %s, %s, %s, %s)
"""

cursor.executemany(sql, valores)
conexao.commit()
cursor.close()
conexao.close()
