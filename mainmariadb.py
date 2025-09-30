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

marcas_ficticias = [
    "Luna Bella", "Estilo Chic", "Passarela Dourada", "Encanto Urbano", "Divina Walk",
    "Pérola Shoes", "Glamour & Cia", "Vitta Calçados", "Lux Feet", "Bella Stilo"
]

valores = [
    ("Scarpin Clássico Preto", 189.90, 25, random.choice(marcas_ficticias), "36/39", "Salto Alto"),
    ("Sandália Salto Alto Nude", 159.99, 30, random.choice(marcas_ficticias), "36/38", "Salto Alto"),
    ("Sapatilha Verniz Vermelha", 99.90, 40, random.choice(marcas_ficticias), "35/39", "Salto Alto"),
    ("Bota Cano Curto Couro", 249.90, 15, random.choice(marcas_ficticias), "37/40", "Salto Alto"),
    ("Tênis Casual Branco", 179.90, 50, random.choice(marcas_ficticias), "36/39", "Salto Alto"),
    ("Anabela Espadrille Bege", 139.90, 20, random.choice(marcas_ficticias), "37/38", "Salto Alto"),
    ("Sandália Rasteira Dourada", 89.90, 60, random.choice(marcas_ficticias), "35/40", "Salto Alto"),
    ("Bota Over The Knee Preta", 329.90, 10, random.choice(marcas_ficticias), "36/39", "Salto Alto"),
    ("Mule Salto Bloco Caramelo", 149.90, 18, random.choice(marcas_ficticias), "35/39", "Salto Alto"),
    ("Oxford Feminino Verniz Preto", 169.90, 22, random.choice(marcas_ficticias), "36/39", "Sandália"),
    ("Sandália Gladiadora Preta", 129.90, 15, random.choice(marcas_ficticias), "38/39", "Sandália"),
    ("Tamanco Plataforma Preto", 119.90, 25, random.choice(marcas_ficticias), "37/39", "Sandália"),
    ("Bota Coturno Feminina Marrom", 219.90, 20, random.choice(marcas_ficticias), "37/40", "Sandália"),
    ("Sapatilha Bico Fino Nude", 109.90, 35, random.choice(marcas_ficticias), "37/38", "Botas"),
    ("Chinelo Slide Preto", 69.90, 50, random.choice(marcas_ficticias), "38/39", "Botas"),
    ("Sandália Meia Pata Vermelha", 189.90, 12, random.choice(marcas_ficticias), "35/36", "Botas"),
    ("Peep Toe Preto Verniz", 159.90, 18, random.choice(marcas_ficticias), "37/38", "Botas"),
    ("Tênis Slip On Bege", 139.90, 28, random.choice(marcas_ficticias), "37/38", "Botas"),
    ("Bota Montaria Marrom", 289.90, 14, random.choice(marcas_ficticias), "38/39", "Botas"),
    ("Sandália Salto Fino Prata", 199.90, 16, random.choice(marcas_ficticias), "37/38", "Botas"),
]

modelos = [
    "Scarpin", "Sandália", "Sapatilha", "Bota", "Tênis", "Anabela", "Rasteira", "Mule",
    "Oxford", "Tamanco", "Chinelo", "Peep Toe", "Slip On", "Coturno", "Montaria", "Gladiadora"
]
cores = ["Preto", "Branco", "Nude", "Vermelho", "Marrom", "Bege", "Cinza", "Dourado", "Prata"]
categorias = ["Sandália", "Scarpin", "Botas", "Salto Alto"]
tamanho = ["35/38", "37/40", " 38/41", "38/41", "39/42"]
quantidades = list(range(10, 61))

for _ in range(1000):
    modelo = random.choice(modelos)
    cor = random.choice(cores)
    nome = f"{modelo} {cor}"
    preco = round(random.uniform(69.9, 329.9), 2)
    quantidade = random.choice(quantidades)
    marca = random.choice(marcas_ficticias)
    tamanhos = random.choice(tamanho)
    categoria = random.choice(categorias)
    valores.append((nome, preco, quantidade, marca, tamanhos, categoria))

sql = """
INSERT INTO PRODUTOS (Nome, Preco, Estoque, Marca, Tamanhos, Categoria)
VALUES (%s, %s, %s, %s, %s, %s)
"""

cursor.executemany(sql, valores)
conexao.commit()
cursor.close()
conexao.close()
