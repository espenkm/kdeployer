# kdeployer

Very very early attempt at making a very simple deploy mechanism for kubernetes.

##Command to deploy:

```bash
curl -i -H "Content-Type: application/json" -X POST -d '{"name":"foo", "image": "espenkm/kdeployer:latest"}' http://localhost:5000/deploy
```

## Bootstrap into cluster

### Minikube:

We need ingress:

```bash
minikube addons enable ingress
```

Add the dns entry to hosts
```bash
echo "$(minikube ip) kdeployer.minikube.local" | sudo tee -a /etc/hosts
```

Bootstrap the minikube cluster with the help of docker

```bash
docker run -a stdin -a stdout -i -v $HOME/.kube/:/root/.kube -v $HOME/.minikube:$HOME/.minikube -t espenkm/kdeployer python deploy.py
```

You should now ha a running instance of the service. Test that you can get to it with

```bash
minikube service kdeployer
```

And can deploy some other app with

```bash
curl -i -H "Content-Type: application/json" -X POST -d '{"name":"foo", "image": "espenkm/kdeployer:latest"}' http://kdeployer.local/deploy
```

### Clean up

```bash
kubectl delete deployment,ingress,service kdeployer
``
