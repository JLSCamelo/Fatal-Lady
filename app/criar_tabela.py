from app.database import Base, engine
#import as tabelas
from app.models import favorito_model

Base.metadata.create_all(bind=engine)