from database import Base, engine
#import as tabelas
from models import usuario_model, EnderecoDB

Base.metadata.create_all(bind=engine)