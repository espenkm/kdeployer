# kdeployer

Very very early attempt at making a very simple deploy mechanism for kubernetes.

##Command to deploy:

curl -i -H "Content-Type: application/json" -X POST -d '{"name":"foo", "image": "espenkm/kdeployer:latest"}' http://localhost:5000/deploy

##Bootstrap into cluster

###Minikube:

We need ingress:

minikube addons enable ingress

echo "$(minikube ip) kdeployer.minikube.local" | sudo tee -a /etc/hosts

docker run -a stdin -a stdout -i -v $HOME/.kube/:/root/.kube -v $HOME/.minikube:$HOME/.minikube -t espenkm/kdeployer python deploy.py

You should now ha a running instance of the service. Test that you can get to it with

minikube service kdeployer

Clean up

kubectl delete deployment,ingress,service kdeployer

