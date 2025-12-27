# Data Input

## Fichiers CSV Sources

Ce répertoire contient vos fichiers CSV d'entrée pour l'analyse de graphe social.

### Fichiers Versionnés

- **friends.csv** - Fichier d'exemple (versionné dans git)

### Fichiers Ignorés

Tous les autres fichiers CSV dans ce répertoire sont **ignorés par git** (voir `.gitignore`).

Vous pouvez ajouter vos propres fichiers CSV ici:
- `my_network.csv`
- `colleagues.csv`
- `team.csv`
- etc.

Ils seront automatiquement ignorés et ne seront pas committés.

## Format CSV

```csv
Utilisateur,Ami1,Ami2,Ami3
Alice,Bob,Charlie,David
Bob,Alice,Eve,Frank
Charlie,Alice,David,George
```

**Notes:**
- Première colonne: nom de l'utilisateur
- Colonnes suivantes: liste de ses amis (séparés par des virgules)
- Les espaces sont automatiquement supprimés
- Les doublons sont éliminés
- Les lignes vides sont ignorées

## Utilisation

```bash
# Analyser un fichier
./social-graph data/input/friends.csv --stats

# Ajouter votre propre fichier
# 1. Créez votre fichier CSV ici
# 2. Analysez-le
./social-graph data/input/mon_fichier.csv --stats
```
