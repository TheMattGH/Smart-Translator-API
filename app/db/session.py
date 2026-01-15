from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# Crear el motor asíncrono (el cable a la BD)
engine = create_async_engine(settings.DATABASE_URL, echo=True)
# echo=True nos mostrará las consultas SQL en la consola

# Fábrica de sesiones (para interactuar con la BD)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Clase base para los modelos
class Base(DeclarativeBase):
    pass

# Dependencia para inyectar la sesión en los endpoints
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session