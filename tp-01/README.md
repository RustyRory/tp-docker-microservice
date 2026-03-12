# Créer le dossier du projet

D’abord, crée un dossier pour le TP.

```
mkdir tp-docker-microservice
cd tp-docker-microservice
```

Ce dossier va contenir **3 fichiers** :

- `app.py`
- `Dockerfile`
- `requirements.txt`

# Créer le microservice Flask

Dans le dossier, crée le fichier **app.py**.

```
nano app.py
```

```python
from flask import Flask, jsonify
app = Flask(__name__)
@app.route("/", methods=["GET"])def home():    return jsonify({"message": "Hello from Dockerized Microservice!"})
if __name__ == "__main__":    app.run(host="0.0.0.0", port=5000)
```

### Explication

- `Flask` → framework pour créer une API.
  - https://flask.palletsprojects.com/en/stable/
- `@app.route("/")` → route accessible à l'adresse `/`
- `jsonify` → renvoie une réponse JSON.
- `host="0.0.0.0"` → permet à Docker d'accéder à l'application.

# Créer le fichier requirements.txt

Ce fichier contient les **dépendances Python**.

Crée le fichier :

```
nano requirements.txt
```

```
flask
```

Docker installera automatiquement Flask grâce à ce fichier.

# Créer le Dockerfile

Crée le fichier :

```
nano Dockerfile
```

**pas d’extension (.txt)**

```docker
FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python","app.py"]
```

### Explication

**FROM python:3.9**

utilise une image Docker contenant Python.

**WORKDIR /app**

crée un dossier `/app` dans le conteneur.

**COPY requirements.txt .**

copie `requirements.txt` dans le conteneur.

**RUN pip install -r requirements.txt**

installe Flask.

**COPY . .**

copie tous les fichiers du projet dans le conteneur.

**CMD ["python", "app.py"]**

lance l'application.

# Vérifier les fichiers

Le dossier doit contenir :

```
tp-docker-microservice
│
├── app.py
├── Dockerfile
└── requirements.txt
```

# 6️⃣ Construire l'image Docker

Dans le dossier du projet, lancer :

```
docker build-t microservice .
```

### Explication

- `docker build` → construit une image
- `t microservice` → nom de l'image
- `.` → dossier courant

Docker va :

1. télécharger l'image Python
2. installer Flask
3. copier le code

# Lancer le conteneur

Ensuite :

```
docker run-p 5000:5000 microservice
```

### Explication

- `docker run` → lance le conteneur
- `p 5000:5000`

relie

```
port PC → port conteneur
5000    → 5000
```

### Si le port est déjà utilisé

```
failed to bind host port 0.0.0.0:5000: address already in use
```

Cela veut dire que **le port 5000 est déjà utilisé sur la machine**.

il faut voir **quel service utilise le port 5000** puis le stopper.

**Vérifier quel service utilise le port 5000**

Taper :

```
sudo lsof-i :5000
```

Résultat du type :

```
COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3  12345 rusty  3u  IPv4  ...   TCP *:5000 (LISTEN)
```

Le **PID** est le numéro du processus.

**Arrêter le processus**

Supposons que le PID soit `12345`.

```
kill 12345
```

**Relancer le conteneur**

Ensuite :

```
docker run-p 5000:5000 microservice
```

```
Running on http://0.0.0.0:5000/
```

# Tester l'API

**Dans un terminal** :

```
curl http://localhost:5000
```

```
{"message":"Hello from Dockerized Microservice!"}
```

### Test avec navigateur

```
http://localhost:5000
```
