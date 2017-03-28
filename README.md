# kdeployer

Very very early attempt at making a very simple deploy mechanism for kubernetes.

Command to deploy:

curl -i -H "Content-Type: application/json" -X POST  \
	-d '{"name":"foo", "image": "espenkm/kdeployer:latest"}' \ 
	http://localhost:5000/deploy