# scripts/seed_usuarios.py

from app.database import SessionLocal, Base, engine
from app.models.usuario_model import UsuarioDB
from app.auth import gerar_hash_senha

def popular_usuarios():
    # 🔹 Garante que as tabelas existam antes de inserir dados
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    usuarios = [
        UsuarioDB(
            nome="Ana Souza",
            email="ana.souza@email.com",
            senha=gerar_hash_senha("senha123"),
            cep=1001000,
            rua="Av. Paulista, 1000",
            cidade="São Paulo",
            telefone="(11) 98888-1111"
        ),
        UsuarioDB(
            nome="Beatriz Lima",
            email="beatriz.lima@email.com",
            senha=gerar_hash_senha("senha456"),
            cep=20040001,
            rua="Rua das Flores, 200",
            cidade="Rio de Janeiro",
            telefone="(21) 97777-2222"
        ),
        UsuarioDB(
            nome="Carla Mendes",
            email="carla.mendes@email.com",
            senha=gerar_hash_senha("senha789"),
            cep=30130000,
            rua="Av. Afonso Pena, 50",
            cidade="Belo Horizonte",
            telefone="(31) 96666-3333"
        ),
        UsuarioDB(
            nome="Daniela Alves",
            email="daniela.alves@email.com",
            senha=gerar_hash_senha("abc123"),
            cep=40000000,
            rua="Rua das Palmeiras, 120",
            cidade="Salvador",
            telefone="(71) 95555-4444"
        ),
        UsuarioDB(
            nome="Elaine Costa",
            email="elaine.costa@email.com",
            senha=gerar_hash_senha("123abc"),
            cep=60060000,
            rua="Av. Beira Mar, 55",
            cidade="Fortaleza",
            telefone="(85) 94444-5555"
        ),
        UsuarioDB(
            nome="Fernanda Rocha",
            email="fernanda.rocha@email.com",
            senha=gerar_hash_senha("minhaSenha"),
            cep=70040010,
            rua="SQS 308, Bloco A",
            cidade="Brasília",
            telefone="(61) 93333-6666"
        ),
        UsuarioDB(
            nome="Gabriela Martins",
            email="gabriela.martins@email.com",
            senha=gerar_hash_senha("senhaSegura"),
            cep=80010000,
            rua="Rua XV de Novembro, 10",
            cidade="Curitiba",
            telefone="(41) 92222-7777"
        ),
        UsuarioDB(
            nome="Helena Barbosa",
            email="helena.barbosa@email.com",
            senha=gerar_hash_senha("pass1234"),
            cep=88015000,
            rua="Rua Felipe Schmidt, 90",
            cidade="Florianópolis",
            telefone="(48) 91111-8888"
        ),
        UsuarioDB(
            nome="Isabela Torres",
            email="isabela.torres@email.com",
            senha=gerar_hash_senha("qwerty"),
            cep=64000000,
            rua="Av. Frei Serafim, 70",
            cidade="Teresina",
            telefone="(86) 98888-9999"
        ),
        UsuarioDB(
            nome="Juliana Freitas",
            email="juliana.freitas@email.com",
            senha=gerar_hash_senha("asdfgh"),
            cep=49010000,
            rua="Rua Itabaiana, 33",
            cidade="Aracaju",
            telefone="(79) 97777-0000"
        ),
        UsuarioDB(
            nome="Karina Nogueira",
            email="karina.nogueira@email.com",
            senha=gerar_hash_senha("zxcvbn"),
            cep=66010000,
            rua="Av. Presidente Vargas, 123",
            cidade="Belém",
            telefone="(91) 96666-1111"
        ),
        UsuarioDB(
            nome="Laura Ribeiro",
            email="laura.ribeiro@email.com",
            senha=gerar_hash_senha("senhaLaura"),
            cep=59010000,
            rua="Rua Mossoró, 45",
            cidade="Natal",
            telefone="(84) 95555-2222"
        ),
    ]

    try:
        db.add_all(usuarios)
        db.commit()
        print(f"{len(usuarios)} usuárias adicionadas com sucesso! (senhas criptografadas com bcrypt)")
    except Exception as e:
        db.rollback()
        print("❌ Erro ao inserir usuárias:", e)
    finally:
        db.close()


if __name__ == "__main__":
    popular_usuarios()
