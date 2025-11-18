from app.database import Base, engine
from app.models import favorito_model, ItemFavoritoDB
from app.models import pagamento_model
print("🔧 Criando tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas com sucesso!")
