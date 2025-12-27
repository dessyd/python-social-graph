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

### Exemple (`friends.csv`):

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
python main.py <fichier_csv> [options]
```

### Options

| Option | Description |
|--------|-------------|
| `--no-bidirectional` | Relations unidirectionnelles (défaut: bidirectionnelles) |
| `--output <fichier>` | Fichier JSON de sortie (défaut: `social_graph.json`) |
| `--foaf-report <fichier>` | Génère un rapport FOAF détaillé |
| `--graphml <fichier>` | Export GraphML pour visualisation (Gephi, yEd, Cytoscape) |
| `--stats` | Affiche les statistiques du graphe |
| `--query-user <nom>` | Affiche les amis et FOAF d'un utilisateur |

### Exemples

#### 1. Import basique avec export JSON

```bash
python main.py friends.csv
```

Sortie: `social_graph.json`

#### 2. Avec statistiques

```bash
python main.py friends.csv --stats
```

```
📈 Statistiques du graphe:
  - Nombre d'utilisateurs: 9
  - Nombre de relations: 18
  - Mode: bidirectionnel
  - Moyenne d'amis par utilisateur: 4.00
```

#### 3. Générer un rapport FOAF

```bash
python main.py friends.csv --foaf-report foaf_report.json --stats
```

#### 4. Requête pour un utilisateur spécifique

```bash
python main.py friends.csv --query-user Alice
```

```
👤 Informations pour 'Alice':
  - Amis directs (3): Bob, Charlie, David
  - Amis d'amis (5): Eve, Frank, George, Helen, Ivan
```

#### 5. Export GraphML pour visualisation

```bash
python main.py friends.csv --graphml friends.graphml --stats
```

Le fichier `.graphml` peut être ouvert avec:
- **Gephi** - Visualisation et analyse de graphes
- **yEd** - Éditeur de diagrammes
- **Cytoscape** - Analyse de réseaux biologiques et sociaux

#### 6. Mode unidirectionnel

```bash
python main.py friends.csv --no-bidirectional --output graph_unidirectional.json
```

## Utilisation programmatique

### Import de la classe

```python
from social_graph import SocialGraph

# Créer un graphe bidirectionnel
graph = SocialGraph(bidirectional=True)

# Charger depuis CSV
graph.load_from_csv('friends.csv')

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
graph.to_json('output.json')

# Export GraphML (pour visualisation)
graph.to_graphml('graph.graphml')

# Rapport FOAF
graph.export_foaf_report('foaf_report.json')
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
python test_social_graph.py
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
|---------|-------------|
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

```
.
├── .venv/                    # Environnement virtuel
├── social_graph.py           # Classe principale
├── main.py                   # Script CLI
├── test_social_graph.py      # Suite de tests
├── friends.csv               # Fichier CSV d'exemple
├── requirements.txt          # Dépendances Python
├── .gitignore               # Fichiers à ignorer
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
