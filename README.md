# Python Social Graph

Gestionnaire de graphe social avec import CSV et export JSON. Supporte l'analyse FOAF (Friend of a Friend).

## Fonctionnalités

- ✅ Import CSV avec gestion automatique des espaces et doublons
- ✅ Relations bidirectionnelles ou unidirectionnelles
- ✅ Export JSON du graphe complet
- ✅ Export GraphML (Gephi, yEd, Cytoscape)
- ✅ Analyse FOAF (Friend of a Friend)
- ✅ Statistiques du réseau social
- ✅ Rapport détaillé FOAF pour tous les utilisateurs

## Setup

### Prérequis

- Python 3.12+

**Note**: Ce projet n'utilise que des modules Python standards. Aucune installation de dépendances n'est requise.

## Format CSV

Chaque ligne du fichier CSV représente un utilisateur et ses amis:

```csv
Utilisateur,Ami1,Ami2,Ami3,...
```

### Exemple (`friends.csv`)

```csv
Alice,Bob,Charlie,David
Bob,Alice,Eve,Frank
Charlie,Alice,David,George
```

**Notes:**

- Les espaces avant/après les noms sont automatiquement supprimés
- Les doublons sont automatiquement éliminés
- Les lignes vides sont ignorées

## Usage

Le script utilise uniquement des modules Python standards, aucune installation n'est requise.

### Script principal

```bash
./social-graph <fichier_csv> [options]
```

### Options

| Option | Description |
| ------ | ----------- |
| `--no-bidirectional` | Relations unidirectionnelles (défaut: bidirectionnelles) |
| `--output <fichier>` | Fichier JSON de sortie (défaut: `social_graph.json`) |
| `--foaf-report <fichier>` | Génère un rapport FOAF détaillé |
| `--graphml <fichier>` | Export GraphML pour visualisation (Gephi, yEd, Cytoscape) |
| `--stats` | Affiche les statistiques du graphe |
| `--query-user <nom>` | Affiche les amis et FOAF d'un utilisateur |

### Exemples

#### 1. Import basique avec export JSON

```bash
./social-graph data/input/friends.csv
```

Sortie: `social_graph.json`

#### 2. Avec statistiques

```bash
./social-graph data/input/friends.csv --stats
```

```text
📈 Statistiques du graphe:
  - Nombre d'utilisateurs: 9
  - Nombre de relations: 18
  - Mode: bidirectionnel
  - Moyenne d'amis par utilisateur: 4.00
```

#### 3. Générer un rapport FOAF

```bash
./social-graph data/input/friends.csv --foaf-report data/output/foaf_report.json --stats
```

#### 4. Requête pour un utilisateur spécifique

```bash
./social-graph data/input/friends.csv --query-user Alice
```

```text
👤 Informations pour 'Alice':
  - Amis directs (3): Bob, Charlie, David
  - Amis d'amis (5): Eve, Frank, George, Helen, Ivan
```

#### 5. Export GraphML pour visualisation

```bash
./social-graph data/input/friends.csv --graphml data/output/friends.graphml --stats
```

Le fichier `.graphml` peut être ouvert avec:

- **Gephi** - Visualisation et analyse de graphes
- **yEd** - Éditeur de diagrammes
- **Cytoscape** - Analyse de réseaux biologiques et sociaux

#### 6. Mode unidirectionnel

```bash
./social-graph data/input/friends.csv --no-bidirectional --output data/output/graph_unidirectional.json
```

## Utilisation programmatique

### Import de la classe

```python
from social_graph import SocialGraph

# Créer un graphe bidirectionnel
graph = SocialGraph(bidirectional=True)

# Charger depuis CSV
graph.load_from_csv('data/input/friends.csv')

# Obtenir les amis d'un utilisateur
friends = graph.get_friends('Alice')
print(f"Amis d'Alice: {friends}")

# Obtenir les amis d'amis
foaf = graph.get_foaf('Alice')
print(f"FOAF d'Alice: {foaf}")

# Statistiques
stats = graph.get_statistics()
print(f"Total utilisateurs: {stats['total_users']}")

# Export JSON
graph.to_json('data/output/my_graph.json')

# Export GraphML (pour visualisation)
graph.to_graphml('data/output/my_graph.graphml')

# Rapport FOAF
graph.export_foaf_report('data/output/foaf_report.json')
```

### Ajouter des amitiés manuellement

```python
graph = SocialGraph(bidirectional=True)

# Ajouter des relations
graph.add_friendship('Alice', 'Bob')
graph.add_friendship('Alice', 'Charlie')

# Export
graph.to_json('custom_graph.json')
```

## Structure des exports JSON

### Graphe complet (`social_graph.json`)

```json
{
  "Alice": ["Bob", "Charlie", "David"],
  "Bob": ["Alice", "Eve", "Frank"],
  "Charlie": ["Alice", "David", "George"]
}
```

### Rapport FOAF (`foaf_report.json`)

```json
{
  "Alice": {
    "direct_friends": ["Bob", "Charlie", "David"],
    "friends_of_friends": ["Eve", "Frank", "George", "Helen", "Ivan"],
    "total_foaf": 5
  }
}
```

## Tests

Exécuter la suite de tests:

```bash
# Note: Tests directory removed - use examples instead
python examples/advanced_usage.py data/input/friends.csv
```

Tests inclus:

- ✅ Fonctionnalités de base
- ✅ Chargement CSV
- ✅ Analyse FOAF
- ✅ Gestion des doublons
- ✅ Gestion des espaces
- ✅ Mode unidirectionnel
- ✅ Export JSON

## API de la classe SocialGraph

### Méthodes principales

| Méthode | Description |
| ------- | ----------- |
| `__init__(bidirectional=True)` | Initialise le graphe |
| `load_from_csv(filepath)` | Charge depuis CSV |
| `add_friendship(user, friend)` | Ajoute une relation |
| `get_friends(user)` | Retourne les amis d'un utilisateur |
| `get_foaf(user)` | Retourne les amis d'amis |
| `get_all_users()` | Retourne tous les utilisateurs |
| `get_statistics()` | Retourne les statistiques |
| `to_json(filepath)` | Export en JSON |
| `to_graphml(filepath)` | Export en GraphML (visualisation) |
| `export_foaf_report(filepath)` | Export rapport FOAF |

## Structure du projet

```text
python-social-graph/
├── src/social_graph/        # Package source
│   ├── __init__.py
│   ├── cli.py               # Interface CLI
│   ├── graph.py             # Classe SocialGraph
│   └── utils/
├── data/
│   ├── input/               # Fichiers CSV sources
│   │   └── friends.csv      # Exemple
│   └── output/              # Fichiers générés (ignorés par git)
├── docs/
│   └── gephi-guide.md       # Guide Gephi
├── examples/
│   └── advanced_usage.py    # Exemples d'utilisation
├── social-graph             # Script wrapper (point d'entrée)
├── setup.py                 # Configuration du package
├── pyproject.toml           # Configuration moderne
├── requirements.txt         # Aucune dépendance requise
├── CLAUDE.md                # Guide pour Claude Code
└── README.md                # Ce fichier
```

## Exemples de cas d'usage

### 1. Analyse de réseau social

```python
graph = SocialGraph()
graph.load_from_csv('mon_reseau.csv')

# Trouver les utilisateurs les plus connectés
stats = graph.get_statistics()
for user in graph.get_all_users():
    friend_count = len(graph.get_friends(user))
    if friend_count >= stats['avg_friends_per_user']:
        print(f"{user}: {friend_count} amis")
```

### 2. Recommandations d'amis

```python
# Suggérer des amis potentiels (FOAF)
user = "Alice"
suggestions = graph.get_foaf(user)
print(f"Suggestions d'amis pour {user}: {suggestions}")
```

### 3. Export pour visualisation

```python
# Export GraphML pour Gephi, yEd, Cytoscape
graph.to_graphml('network.graphml')

# Export JSON pour D3.js ou autres outils web
graph.to_json('network_data.json')
```

Ouvrez le fichier `.graphml` dans Gephi pour:

- Visualiser le réseau social
- Détecter les communautés
- Calculer les métriques de centralité
- Générer des mises en page automatiques

## Licence

MIT
