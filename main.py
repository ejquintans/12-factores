import logging
import psycopg2
import os
from fastapi import FastAPI
from pydantic import BaseModel
from database import get_db_connection
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

PORT = int(os.getenv("PORT", "8000"))
DATABASE_URL = os.getenv("DATABASE_URL")

# Rompe Factor 11 Logs a archivo
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# Modelo para FastAPI (esto está bien, no es una mala práctica)
class NoteCreate(BaseModel):
    content: str

app = FastAPI()

@app.on_event("startup")
def create_table():
    conn = get_db_connection(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    logger.info("Tabla 'notes' verificada/creada")

@app.post("/notes/")
def create_note(note: NoteCreate):
    """Crea una nota. ¡Guarda estado en DB externa, pero con config fija!"""
    conn = get_db_connection(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("INSERT INTO notes (content) VALUES (%s)", (note.content,))
    conn.commit()
    cur.close()
    conn.close()
    logger.info(f"Nota creada: {note.content}")
    return {"status": "ok", "content": note.content}

app.get("/notes/")
def list_notes():
    """Lista todas las notas."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, content FROM notes")
    notes = [{"id": row[0], "content": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    logger.info("Notas listadas")
    return notes

@app.get("/health")
def health():
    """Endpoint de salud (aunque no se usa en esta versión)."""
    return {"status": "ok"}

# rompe Factor 7: Puerto y host fijos
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)  # ¡localhost! → inaccesible en contenedor