# k8s-gitops-homelab

## Overview

This project runs a local Kubernetes cluster, deploys an app using Helm, exposes it through an Ingress, secures it with NetworkPolicy, and uses ArgoCD to sync everything from GitHub.

## Learning goals

- Understand how Pods find each other through Services and DNS
- Understand how traffic from outside reaches the cluster through an Ingress
- Learn how to control traffic between Pods with NetworkPolicy
- Learn why GitOps makes deployments easier to track and roll back
- Get comfortable with Docker, Linux and Git

## Quick start

Create the local cluster:

```bash
colima start --cpu 2 --memory 4
k3d cluster create homelab --agents 1 -p "8080:80@loadbalancer"
```

Deploy infrastructure (namespace, PostgreSQL, NetworkPolicy):

```bash
kubectl apply -f k8s/namespace.yaml
kubectl create secret generic postgres-secret -n shortlink --from-literal=POSTGRES_PASSWORD=<your-password>
kubectl apply -f k8s/
```

Install ArgoCD and hand the app over to GitOps:

```bash
kubectl create namespace argocd
kubectl apply -n argocd --server-side -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl apply -f gitops/application.yaml
```

Open the app at http://shortlink.localhost:8080

Stop / start / delete:

```bash
k3d cluster stop homelab && colima stop
colima start && k3d cluster start homelab
k3d cluster delete homelab
```

## Progress

- [x] Phase 0: Setup
- [x] Phase 1: Containerize the app
- [x] Phase 2: Kubernetes basics
- [x] Phase 3: Ingress and database
- [x] Phase 4: Helm
- [x] Phase 5: NetworkPolicy
- [x] Phase 6: CI and GitOps
- [ ] Phase 7: Autoscaling and docs