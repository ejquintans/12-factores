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



### **Factor I: Codebase**

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

