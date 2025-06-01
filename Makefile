build:
	eval $$(minikube docker-env) && \
	docker build -t odoo-custom:latest ./odoo-community

apply:
	kubectl apply -f ./k8s

status:
	kubectl get pods

url:
	minikube service odoo-service --url
