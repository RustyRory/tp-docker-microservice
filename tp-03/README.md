# Installation de Minikube sur Linux

## Installer un hyperviseur ou utiliser Docker

Minikube a besoin d’un moteur pour exécuter Kubernetes. Sur Linux Mint, tu as plusieurs options :

1. **Docker** (déjà installé)
2. **KVM**
3. **VirtualBox**

## Installer kubectl

- Téléchargez la dernière release avec la commande :
  ```
  curl -LO https://dl.k8s.io/release/$(curl -Ls https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl
  ```
  Pour télécharger une version spécifique, remplacez `$(curl -s https://dl.k8s.io/release/stable.txt)` avec la version spécifique.
  Par exemple, pour télécharger la version 1.35.0 sur Linux, tapez :
  ```
  curl -LO https://dl.k8s.io/release/v1.35.0/bin/linux/amd64/kubectl
  ```
- Rendez le binaire kubectl exécutable.
  ```
  chmod +x ./kubectl
  ```
- Déplacez le binaire dans votre PATH.
  ```
  sudo mv ./kubectl /usr/local/bin/kubectl
  ```
- Testez pour vous assurer que la version que vous avez installée est à jour:
  ```
  kubectl version --client
  ```

## Télécharger et installer Minikube

### Installez Minikube par téléchargement direct

Si vous n'installez pas via un package, vous pouvez télécharger
un binaire autonome et l'utiliser.

```bash
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
  && chmod +x minikube
```

Voici un moyen simple d'ajouter l'exécutable Minikube à votre path :

```bash
sudo mkdir -p /usr/local/bin/
sudo install minikube /usr/local/bin/
```

Vérifie l’installation :

```
minikube version
```

## Confirmer l'installation

Pour confirmer la réussite de l'installation d'un hyperviseur et d'un mini-cube, vous pouvez exécuter la commande suivante pour démarrer un cluster Kubernetes local :

**Note:** Pour définir le `--driver` avec `minikube start`, entrez le nom de l'hyperviseur que vous avez installé en minuscules où `<driver_name>` est mentionné ci-dessous. Une liste complète des valeurs `--driver` est disponible dans [la documentation spécifiant le pilote VM](https://kubernetes.io/docs/setup/learning-environment/minikube/#specifying-the-vm-driver).

```bash
minikube start --driver=docker
```

Une fois `minikube start` terminé, exécutez la commande ci-dessous pour vérifier l'état du cluster :

```bash
minikube status
```

Si votre cluster est en cours d'exécution, la sortie de `minikube status` devrait être similaire à :

```
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

Après avoir vérifié si Minikube fonctionne avec l'hyperviseur choisi, vous pouvez continuer à utiliser Minikube ou arrêter votre cluster. Pour arrêter votre cluster, exécutez :

```bash
minikube stop
```

## Tout nettoyer pour recommencer à zéro

Si vous avez déjà installé minikube, exécutez :

```bash
minikube start
```

Si cette commande renvoie une erreur :

`machine does not exist`

Vous devez supprimer les fichiers de configuration :

```bash
rm -rf ~/.minikube
```

## Préparer tes images Docker pour Minikube

Minikube utilise son propre moteur Docker, donc il faut construire les images **dans Minikube** :

```
eval $(minikube docker-env)
docker build-t service-user:latest ./service-user
docker build-t service-order:latest ./service-order
```

> Ici, `service-order` pourra appeler `service-user` via `http://service-user:5001/users`.

## Créer les fichiers Kubernetes

1. `user-deployment.yaml` et `user-service.yaml`
2. `order-deployment.yaml` et `order-service.yaml`

Avec les configurations que je t’ai données dans mon message précédent.

- `Deployment` → crée le pod avec l’image Docker.
- `Service` → expose le pod sur le réseau du cluster (ClusterIP pour interne, LoadBalancer pour accéder depuis Minikube).

## Déployer sur Kubernetes

```bash
kubectl apply-f user-deployment.yaml
kubectl apply-f user-service.yaml
kubectl apply-f order-deployment.yaml
kubectl apply-f order-service.yaml
```

Pour vérifier que tout tourne :

```bash
kubectlget pods
kubectlget services
```

## Accéder au service-order depuis navigateur ou curl

Minikube peut exposer le LoadBalancer avec :

```bash
minikubeservice service-order--url
```

sortie :

```
http://192.168.49.2:31711/
```

Test avec curl :

```bash
curl http://192.168.49.2:31711/orders
```

Réponse attendue :

```json
{
  "orders": ["Order 1 for Alice", "Order 2 for Bob"]
}
```
