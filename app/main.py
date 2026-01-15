from fastapi import FastAPI
app = FastAPI(
    title="Smart Translator API",
    version="0.1.0",
    description="Microservicio de traducción con caché inteligente."
)

# Endpoint de prueba (Health Check)
@app.get("/")
def read_root():
    return {"status": "online", "message": "Smart Translator API is running!"}

# Endpoint de prueba con parámetro
@app.get("/ping")
def pong():
    return {"ping": "pong!"}