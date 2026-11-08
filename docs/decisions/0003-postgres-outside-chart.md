# 0003 – PostgreSQL kept outside the Helm chart

**Status:** Accepted

## Context
When packaging the app with Helm, I had to decide whether the database belonged in the same chart.

## Options
| Option | Pros | Cons |
|---|---|---|
| Database inside the app chart | One command deploys everything | Deleting or reinstalling the release can remove the PersistentVolumeClaim and the data |
| **Database outside the chart** | App and data have separate lifecycles | One extra `kubectl apply` step |

## Decision
Keep PostgreSQL (StatefulSet, headless Service, PVC) in `k8s/`, outside the chart. The password is created as a Secret from the command line and never stored in Git.

## Consequences
- Migrating the app from `kubectl` to Helm and then to ArgoCD never touched the data (the same short link survived every phase).
- The app and the database can be upgraded independently.
- In production, a managed database (for example Amazon RDS) would be the natural next step.