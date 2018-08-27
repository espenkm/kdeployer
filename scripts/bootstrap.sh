kubectl create serviceaccount -n kube-system tiller
kubectl create clusterrolebinding tiller-binding --clusterrole=cluster-admin --serviceaccount kube-system:tiller
helm init --service-account tiller
helm repo update
helm install --name cert-manager --version v0.3.1 --namespace

docker run -a stdin -a stdout -i -v $HOME/.kube/:/root/.kube -v $HOME/.minikube:$HOME/.minikube -t espenkm/kdeployer python deploy.py