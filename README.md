# K8S-GitOps-Homelab

## Overview
This project runs a local Kubernetes cluster, deploys an app using Helm, exposes it through an Ingress, secures it with NetworkPolicy and uses ArgoCD to sync everything from GitHub.
## Learning goals 
- Understand how Pods find each other through Services and DNS
- Understand how traffic from outside reaches the cluster through an Ingress
- Learn how to control traffic between Pods with NetworkPolicy
- Learn why GitOps makes deployments easier to track and roll back
- Get comfortable with Docker, Linux and Git
## Quick start

    colima start --cpu 2 --memory 4
    k3d cluster create homelab --agents 1 -p "8080:80@loadbalancer"
    kubectl get nodes

Stop / start / delete:

    k3d cluster stop homelab && colima stop
    colima start && k3d cluster start homelab
    k3d cluster delete homelab
## Progress
- [ ] Phase 0: Setup
- [ ] Phase 1: Containerize the app
- [ ] Phase 2: Kubernetes basics
- [ ] Phase 3: Ingress and database
- [ ] Phase 4: Helm
- [ ] Phase 5: NetworkPolicy
- [ ] Phase 6: CI and GitOps
- [ ] Phase 7: Autoscaling and docs
 