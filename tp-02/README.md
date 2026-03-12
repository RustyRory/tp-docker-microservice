# Créer la structure du projet

Créer un dossier principal puis deux dossiers pour les services.

```
mkdir service-user
mkdir service-order
```

Structure :

```
tp-compose
│
├── service-user
│
├── service-order
│
└── docker-compose.yml
```

# Créer le microservice **service-user**

Dans le dossier `service-user`, créer le fichier :

```
service-user/app.py
```

Ce service expose une API :

```
GET /users
```

Il renvoie une liste d’utilisateurs :

```
Alice
Bob
```

Ensuite dans ce dossier il faut aussi créer :

### requirements.txt

Contient les dépendances Python.

```
flask
```

### Dockerfile

Permet de construire l'image Docker du service.

Il sert à :

- installer Python
- installer Flask
- copier le code
- lancer l'application.

# Créer le microservice **service-order**

Dans le dossier `service-order`, créer :

```
service-order/app.py
```

Ce service expose une API :

```
GET /orders
```

Ce qu'il fait :

1. il appelle l’API du service `service-user`
2. récupère la liste des utilisateurs
3. crée des commandes associées aux utilisateurs.

La communication se fait avec :

```
http://service-user:5001/users
```

**service-user est le nom du service Docker**, ce qui permet la communication dans le réseau Docker Compose.

Dans ce dossier il faut aussi créer :

### requirements.txt

```
flask
requests
```

### Dockerfile

Même principe que pour le premier service :

- installer Python
- installer les dépendances
- copier le code
- lancer l'application.

# Créer le fichier **docker-compose.yml**

Dans le dossier principal créer :

```
docker-compose.yml
```

Ce fichier permet de :

- définir les services
- construire leurs images
- lancer les conteneurs
- créer un réseau pour qu’ils communiquent.

Il définit deux services :

### service-user

- construit l’image depuis `./service-user`
- expose le port **5001**

### service-order

- construit l’image depuis `./service-order`
- expose le port **5002**
- dépend de `service-user`

Le champ :

```
depends_on
```

indique que **service-order doit démarrer après service-user**.

# Lancer les services

Dans le dossier principal exécuter :

```
docker compose up--build
```

Cette commande :

1. construit les images Docker
2. crée les conteneurs
3. crée un réseau Docker
4. lance les deux services.

# Tester la communication

Dans un nouveau terminal :

```
curl http://localhost:5002/orders
```

Le résultat attendu est :

```json
{
  "orders": ["Order 1 for Alice", "Order 2 for Bob"]
}
```
