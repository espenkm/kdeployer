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
echo "$(minikube ip) kdeployer.local" | sudo tee -a /etc/hosts
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


Create cluster

gcloud container --project "nifty-yeti-164407" clusters create "dev-cluster-1" --zone "europe-west1-b" --machine-type "n1-standard-1" --image-type "COS" --disk-size "100" --scopes "https://www.googleapis.com/auth/compute","https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --num-nodes "1" --network "default" --no-enable-cloud-logging --no-enable-cloud-monitoring --preemptible --disable-addons HttpLoadBalancing 

and ip

gcloud compute addresses create kubernetes-ingress --global  --project nifty-yeti-164407
