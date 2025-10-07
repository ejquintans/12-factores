## Estructura del proyecto

```
note-app/
├── main.py                 # App principal (12f-compliant)
├── database.py             # Conexión a DB con URL desde env
├── models.py               # Modelo Pydantic
├── migrate.py              # Script de admin (Factor XII)
├── requirements.txt
├── Containerfile           # Para Podman/OpenShift
├── .gitlab-ci.yml          # Pipeline
├── .env.example            # Solo para desarrollo local (¡no commitear .env!)
└── README.md
```



### **Factor 1: Codebase**

*Una base de código, rastreada en control de versiones, que despliega múltiples veces.*

- Usa **Git**
- Crear .gitignore

```bash
# .gitignore
__pycache__/
*.pyc
app.log
.env
venv/
```



### **Factor 2: Dependencies**

*Declarar y aislar explícitamente las dependencias.* 

- Crear `requirements.txt` con todas las dependencias:

```tex
fastapi
uvicorn[standard]
psycopg2-binary
```



### **Factor III: Config**

*Almacenar la configuración en el entorno.*

- **Elimina todo hardcodeo** de credenciales, puertos, hosts.
- Usa `os.getenv()` para leer variables:

```python
import os
PORT = int(os.getenv("PORT", "8000"))
DATABASE_URL = os.getenv("DATABASE_URL")
```



### **Factor IV: Backing services**

*Tratar los servicios de soporte como recursos adjuntos.* 

- Conéctar a PostgreSQL mediante una URL (ej: `postgresql://user:pass@host:5432/db`).
- No asumir que está en `localhost`.
