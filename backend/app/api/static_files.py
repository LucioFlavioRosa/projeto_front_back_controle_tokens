from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Caminho absoluto para pasta de arquivos estáticos do frontend
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../frontend/static')
INDEX_HTML = os.path.join(STATIC_DIR, '../index.html')

# Monta arquivos estáticos
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_index():
    """
    Retorna o arquivo index.html na raiz da aplicação.
    """
    return FileResponse(INDEX_HTML)
