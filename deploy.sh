#!/bin/bash

APP_NAME=odoo-custom
IMAGE_TAG=latest
KUBE_MANIFESTS=./k8s
DOCKER_CONTEXT=./odoo-community

echo "🔧 Activando entorno Docker de Minikube..."
eval $(minikube docker-env)

echo "📦 Construyendo imagen: $APP_NAME:$IMAGE_TAG"
docker build -t $APP_NAME:$IMAGE_TAG $DOCKER_CONTEXT

echo "🚀 Aplicando manifiestos Kubernetes..."
kubectl apply -f $KUBE_MANIFESTS

echo "🌐 Espera unos segundos y luego accede a:"
minikube service odoo-service --url
