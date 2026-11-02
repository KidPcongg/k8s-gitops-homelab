# NetworkPolicy tests

| # | Source | Destination | Expected | Result |
|---|--------|-------------|----------|--------|
| 1 | User via Ingress (Traefik) | app:8000 | allow | ✓ 200 OK |
| 2 | Pod in `default` | postgres:5432 | deny | ✓ no response |
| 3 | Pod in `default` | app:8000 (bypass Ingress) | deny | ✓ connection refused |
| 4 | Unlabeled pod in `shortlink` | postgres:5432 | deny | ✓ no response |
| 5 | app | Internet | deny | ✓ network unreachable |
| 6 | Pod in `shortlink` with fake label `app=shortlink` | postgres:5432 | allow (by design) | ✓ accepting connections |

Note: test 6 shows that NetworkPolicy trusts pod labels. It must be combined with RBAC to restrict who can create pods in the namespace.