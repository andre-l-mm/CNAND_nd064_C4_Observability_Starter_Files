# Useful Commands

## Get Grafana POD name

```
kubectl get pods -n monitoring | grep grafana
```

## Expose Grafana port using port forward

```
# Update pod name below and run
kubectl port-forward -n monitoring prometheus-grafana-cb4dcbb8f-4dr95 3000
```

## Access Grafana

URL: http://localhost:3000
User: admin
Password: prom-operator

## Expose Project App

```
kubectl port-forward svc/frontend-service 8080:8080
```
## Accessing the Project App

http://localhost:8080/


## Create Jaeger Instance

```
kubectl apply -f manifests/other/jaeger-instance.yaml
```

## Expose Jaeger

```
kubectl port-forward -n observability \
    $(kubectl get pods -n observability -l=app="jaeger" -o name) --address 0.0.0.0 16686:16686
```

## Building 

Frontend code has been modified so that metrics are exported using prometheus_flask_exporter library.

### Build Docker Images

```
# Frontend
cd reference-app/frontend
docker build -f ./Dockerfile -t frontend .

# Backend
cd reference-app/backend
docker build -f ./Dockerfile -t backend .
```

### Push Docker Images

```
docker tag frontend andremagalhaes/frontend
docker push andremagalhaes/frontend

docker tag backend andremagalhaes/backend
docker push andremagalhaes/backend
```
