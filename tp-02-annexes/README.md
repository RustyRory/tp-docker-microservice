# Créer la structure du projet

Créer le dossier principal avec **frontend + backend**.

```
mkdir project
cd project

mkdir frontend
mkdir backend
```

Structure :

```
project
│
├── frontend
│
├── backend
│
└── docker-compose.yml
```

# Créer le backend (API)

Le backend doit exposer une API :

```
GET /api/message
```

qui retourne :

```json
{
  "message": "Hello from backend"
}
```

Exemple simple avec **Python + Flask**.

Créer :

```
backend/app.py
```

```python
from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # permet à tous les frontends d’accéder à l’API
@app.route("/api/message")
def message():
    return jsonify({"message": "Hello from backend"})
app.run(host="0.0.0.0", port=5000)
```

# Dockeriser le backend

Dans `backend/` créer :

### requirements.txt

```
flask
```

### Dockerfile

```docker
FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python","app.py"]
```

Dockerfile va :

1. installer Python
2. installer Flask
3. copier le code
4. lancer l’API

# Créer le frontend

Le frontend doit :

- afficher une page web
- appeler l’API backend
- afficher la réponse

Créer :

```
frontend/index.html
```

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Frontend</title>
  </head>

  <body>
    <h1>Frontend</h1>

    <p id="msg">Chargement...</p>

    <script>
      fetch("http://localhost:5000/api/message")
        .then((response) => response.json())
        .then((data) => {
          document.getElementById("msg").innerText =
            "Message du backend : " + data.message;
        });
    </script>
  </body>
</html>
```

# Dockeriser le frontend

Dans `frontend/` créer :

```
frontend/Dockerfile
```

```docker
FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html
```

Cela :

1. utilise un serveur web nginx
2. copie la page HTML
3. sert la page web

# Créer le docker-compose.yml

Dans le dossier `project` :

```
docker-compose.yml
```

```yaml
version:"3"

services:

  backend:
    build: ./backend
    ports:
      -"5000:5000"

  frontend:
    build: ./frontend
    ports:
      -"8080:80"
    depends_on:
      - backend
```

Ce fichier :

- lance **2 conteneurs**
- les met dans **le même réseau**
- permet au frontend d’appeler le backend.

# Lancer l’application

Dans le dossier `project` :

```
docker compose up--build
```

Docker va :

1. construire les images
2. lancer les conteneurs
3. créer un réseau entre eux

# Tester l'application

Ouvrir dans le navigateur :

```
http://localhost:8080
```

```
Frontend

Message du backend : Hello from backend
```
