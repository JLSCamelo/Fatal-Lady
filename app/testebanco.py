import sqlite3
import random

# Conexão com SQLite (arquivo produtos.db)
conexao = sqlite3.connect("produtos.db")
cursor = conexao.cursor()

# Criar tabela (se não existir)
cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    estoque INTEGER NOT NULL,
    marca TEXT NOT NULL,
    tamanho TEXT NOT NULL,
    categoria TEXT NOT NULL,
    imagem TEXT NOT NULL
)
""")
conexao.commit()

marcas_ficticias = [
    "Luna Bella", "Estilo Chic", "Passarela Dourada", "Encanto Urbano", "Divina Walk",
    "Pérola Shoes", "Glamour & Cia", "Vitta Calçados", "Lux Feet", "Bella Stilo"
]

valores = [
    ("Scarpin Clássico Preto", 189.90, 25, random.choice(marcas_ficticias), "36/39", "Salto Alto","sem foto"),
    ("Sandália Salto Alto Nude", 159.99, 30, random.choice(marcas_ficticias), "36/38", "Salto Alto","sem foto"),
    ("Sapatilha Verniz Vermelha", 99.90, 40, random.choice(marcas_ficticias), "35/39", "Salto Alto", "sem foto"),
    ("Bota Cano Curto Couro", 249.90, 15, random.choice(marcas_ficticias), "37/40", "Salto Alto","sem foto"),
    ("Tênis Casual Branco", 179.90, 50, random.choice(marcas_ficticias), "36/39", "Salto Alto", "sem foto"),
    # ... seus outros produtos iniciais
]

modelos = [
    "Scarpin", "Sandália", "Sapatilha", "Bota", "Tênis", "Anabela", "Rasteira", "Mule",
    "Oxford", "Tamanco", "Chinelo", "Peep Toe", "Slip On", "Coturno", "Montaria", "Gladiadora"
]
cores = ["Preto", "Branco", "Nude", "Vermelho", "Marrom", "Bege", "Cinza", "Dourado", "Prata"]
categorias = ["Sandália", "Scarpin", "Botas", "Salto Alto"]
tamanhos = ["35/38", "37/40", "38/41", "39/42"]
quantidades = list(range(10, 61))
imagem="sem foto"

# Gerar produtos aleatórios
for _ in range(1000):
    modelo = random.choice(modelos)
    cor = random.choice(cores)
    nome = f"{modelo} {cor}"
    preco = round(random.uniform(69.9, 329.9), 2)
    quantidade = random.choice(quantidades)
    marca = random.choice(marcas_ficticias)
    tamanho = random.choice(tamanhos)
    categoria = random.choice(categorias)
    imagem = imagem
    valores.append((nome, preco, quantidade, marca, tamanho, categoria, imagem))

# Inserir dados
sql = """
INSERT INTO PRODUTOS (nome, preco, estoque, marca, tamanho, categoria, imagem)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

cursor.executemany(sql, valores)
conexao.commit()

# Fechar conexão
cursor.close()
conexao.close()
