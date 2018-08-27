#kubectl create serviceaccount -n kube-system tiller
#kubectl create clusterrolebinding tiller-binding --clusterrole=cluster-admin --serviceaccount kube-system:tiller
#helm init --service-account tiller
#helm repo update
#helm install --name cert-manager --version v0.3.1 --namespace
helm install --name cert-manager --namespace cert-manager stable/cert-manager
kubectl create -f scripts/certificate.yaml
python deploy.py
#docker run -a stdin -a stdout -i -v $HOME/.kube/:/root/.kube -v $HOME/.minikube:$HOME/.minikube -t espenkm/kdeployer python deploy.py