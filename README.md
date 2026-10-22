# Supervision de la plateforme de données LoméMarket

Couche de supervision d'une plateforme de données qui combine MySQL, MongoDB et un entrepôt de données PostgreSQL. Elle collecte les métriques de chaque base, les affiche dans Grafana, centralise les journaux et planifie les sauvegardes.

## Architecture

```
MySQL ──── mysqld-exporter ───┐
PostgreSQL ─ postgres-exporter ┼──▶ Prometheus ──▶ Grafana (tableaux « DWH Overview », « DWH Counts »)
MongoDB ── exportateur maison ┘        │
Airflow ──────────────────────────────┘        └──▶ Alertmanager

Journaux des conteneurs ── Promtail ──▶ Loki ──▶ Grafana
Tâche cron : sauvegardes MySQL (3 h), PostgreSQL (3 h 30), MongoDB (4 h)
```

- **Prometheus** interroge les exportateurs de PostgreSQL, MySQL et MongoDB, ainsi qu'Airflow.
- **L'exportateur MongoDB** (`mongo_exporter/`) est écrit en Python avec `prometheus_client`. Il publie la disponibilité de la base et son nombre de collections.
- **Grafana** est configuré entièrement par fichiers : sources de données et tableaux de bord sont chargés au démarrage.
- **Loki et Promtail** collectent les journaux de tous les conteneurs Docker.
- **Un conteneur cron** lance chaque nuit les scripts de sauvegarde des trois bases.

## Prérequis

Ce dépôt ne contient que la supervision. Il suppose que les bases tournent déjà sur le réseau Docker externe `lomemarket-network`, et que les scripts de sauvegarde sont dans le dossier voisin `../couche2-replication/scripts-backup`.

## Lancement

```bash
cp .env.example .env                       # renseigner les mots de passe
cp mysql/.my.cnf.example mysql/.my.cnf     # idem pour l'exportateur MySQL
docker compose up -d
```

| Service | Adresse |
|---|---|
| Grafana | http://localhost:3001 |
| Prometheus | http://localhost:9091 |
| Alertmanager | http://localhost:9093 |
| Loki | http://localhost:3100 |

## Stack

Docker Compose · Prometheus · Grafana · Loki · Promtail · Alertmanager · Python (`prometheus_client`, `pymongo`)

## Limites

- Alertmanager n'a pas encore de destinataire configuré : les alertes ne sont envoyées nulle part.
- Plusieurs images utilisent l'étiquette `latest` : épingler les versions rendrait le déploiement reproductible.
