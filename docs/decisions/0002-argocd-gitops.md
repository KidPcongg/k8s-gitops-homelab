# 0002 – GitOps with ArgoCD instead of deploying from CI

**Status:** Accepted

## Context
After building images in GitHub Actions, the app still had to reach the cluster. Before this, I deployed with `kubectl apply` and `helm upgrade`, and hit drift three times: manual `kubectl` edits, a `helm rollback` that left the values file out of date, and a `--set` value that was never committed.

## Options
| Option | How it works | Problem |
|---|---|---|
| Push from CI | GitHub Actions runs `helm upgrade` | CI needs cluster credentials; nothing detects drift |
| **Pull with ArgoCD** | ArgoCD inside the cluster watches Git and syncs | Extra component (~0.5–1 GB RAM) |

## Decision
ArgoCD with `automated`, `prune: true` and `selfHeal: true`. CI only builds images; it has no access to the cluster.

## Consequences
- Every change to the cluster is a Git commit with an author and a message.
- Manual changes are reverted automatically (verified: `kubectl scale --replicas=5` returned to 2 within seconds).
- Rollback is `git revert`, so Git and the cluster never disagree.
- The HPA must own the replica count, so `replicas` is omitted from the Deployment when autoscaling is enabled, to avoid a fight between the HPA and self-heal.