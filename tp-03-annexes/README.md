# Création de la structure du projet

On organise le projet en trois parties :

```
project/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── index.html
│   └── Dockerfile
│
└── k8s/
    ├── backend-deployment.yaml
    ├── backend-service.yaml
    ├── frontend-deployment.yaml
    └── frontend-service.yaml
```

Objectif :

- séparer **application** et **infrastructure Kubernetes**

# Création du backend

Le backend expose une API :

```
GET /api/message
```

qui retourne :

```json
{
  "message": "Hello from backend"
}
```

Exemple avec **Flask** :

```python
from flask import Flask, jsonify
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

@app.route("/api/message")
defmessage():
  return jsonify({"message":"Hello from backend"})

app.run(host="0.0.0.0",port=5000)
```

# Dockerisation du backend

Dockerfile :

```docker
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

EXPOSE5000

CMD ["python","app.py"]
```

Construction de l'image :

```
docker build-t backend:latest .
```

# Création du frontend

Le frontend est une page HTML qui appelle l’API :

```html
<h1>Frontend</h1>
<pid="msg">Chargement...</p>

<script>
fetch("http://192.168.49.2:30080/api/message")
.then((response) =>response.json())
.then((data) => {
document.getElementById("msg").innerText=
"Message du backend : "+data.message;
  });
</script>
```

# Dockerisation du frontend

Dockerfile :

```docker
FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html
```

Construction de l'image :

```
docker build-t frontend:latest .
```

# Utilisation de Minikube

Minikube permet de lancer un **cluster Kubernetes local**.

Démarrage :

```
minikube start
```

Configuration Docker pour Minikube :

```
eval $(minikube docker-env)
```

Cela permet de **construire les images directement dans le cluster**.

# Création des manifestes Kubernetes

## Backend Deployment

Déploie le conteneur backend.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: backend
          image: backend:latest
          ports:
            - containerPort: 5000
```

## Backend Service

Expose le backend :

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  type: NodePort
  selector:
    app: backend
  ports:
    - port: 5000
      targetPort: 5000
      nodePort: 30080
```

## Frontend Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: frontend
          image: frontend:latest
          ports:
            - containerPort: 80
```

## Frontend Service

Expose l'application web :

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend
spec:
  type: NodePort
  selector:
    app: frontend
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30286
```

# Déploiement dans Kubernetes

Application des fichiers :

```
kubectl apply-f k8s/
```

Vérification :

```
kubectl get pods
kubectl get services
```

# Tester la communication

Backend accessible :

```
http://192.168.49.2:30080/api/message
```

Réponse :

```json
{
  "message": "Hello from backend"
}
```

Frontend accessible :

```
http://192.168.49.2:30286
```

Le frontend appelle le backend et affiche :

```
Message du backend : Hello from backend
```
