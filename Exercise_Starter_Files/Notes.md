# Commands Used

## Port Forward for Grafana

To access Grafana on `http://localhost:3000`.

```
kubectl --namespace monitoring port-forward svc/prometheus-grafana --address 0.0.0.0 3000:80
```

