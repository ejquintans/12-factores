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

Probar código: 

```bash
curl -X POST "http://localhost:8000/notes/" -H "Content-Type: application/json" -d '{"content":"Primera nota"}'
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

- Conectar a PostgreSQL mediante una URL (ej: `postgresql://postgres:postgres@localhost:5432/postgres`).

```python
# database.py
import psycopg2
def get_db_connection(db_url: str):
    return psycopg2.connect(db_url)
```

- Instalar python-dotenv

```bash
pip install python-dotenv
```

- Lo incorporo al código:

```python
from dotenv import load_dotenv # <-- Importar la biblioteca

# Cargar variables del archivo .env
load_dotenv() 
```



### **Factor V: Build, release, run**

*Separar estrictamente las fases de build y run.* 

- Generar el dockerfile:

  ```dockerfile
  FROM python:3.11
  COPY requirements.txt .
  RUN pip install -r requirements.txt
  COPY . .
  CMD ["python", "main.py"]
  ```

- .gitlab-ci.yml: automatiza build → release → run.

  ```bash
  # Definimos las etapas en orden
  stages:
    - test
    - build
    - deploy
  
  # === ETAPA 1: Test ===
  test:
    stage: test
    image: python:3.11
    script:
      - pip install -r requirements.txt
      - python -c "import main; print('✅ App importable')"
  
  # === ETAPA 2: Build (Construir la imagen) ===
  build:
    stage: build
    image: registry.redhat.io/openshift4/ose-podman
    script:
      # Construye la imagen usando Containerfile
      - podman build -f Containerfile -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA .
  
      # Inicia sesión en el registry de GitLab
      - podman login -u gitlab-ci-token -p $CI_JOB_TOKEN $CI_REGISTRY
  
      # Sube la imagen al registry
      - podman push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
  
  # === ETAPA 3: Deploy (Desplegar en OpenShift) ===
  deploy-to-openshift:
    stage: deploy
    image: registry.redhat.io/openshift4/ose-cli
    script:
      # Conectarse a OpenShift
      - oc login $OPENSHIFT_SERVER --token=$OPENSHIFT_TOKEN
  
      # Actualizar el deployment con la nueva imagen
      - oc set image deployment/note-app note-app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA -n $OPENSHIFT_PROJECT
  ```



### **Factor VI: Processes**

*Ejecutar la app como procesos stateless.* 

- Se elimina cualquier escritura a archivos

	Se modifica:

	```python
    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
  ```

    Por:

    ```python
    import sys
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    ```

- Asegurate de que la DB no esté en localhost

  ```python
  DATABASE_URL = os.getenv("DATABASE_URL")
  ```

- Se sacaron las variables globales con estado.

| Pregunta                             | Respuesta                                        |
| ------------------------------------ | ------------------------------------------------ |
| ¿Guarda archivos en disco?           | ❌ (si usás`app.log`) → ✅ si usás`stdout`         |
| ¿Usa variables globales para estado? | ❌ (no lo hacés) → ✅                              |
| ¿Se conecta a la DB vía URL externa? | ❌ (si usás`localhost`) → ✅ si usás`DATABASE_URL` |
| ¿Cada request es independiente?      | ✅ (sí)                                           |
