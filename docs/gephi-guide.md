# Guide d'utilisation avec Gephi

Ce guide explique comment visualiser votre graphe social dans Gephi.

## 1. Installation de Gephi

Téléchargez et installez Gephi: https://gephi.org/users/download/

## 2. Export du graphe

Générez le fichier GraphML avec les labels:

```bash
python main.py friends.csv --graphml friends.graphml --stats
```

Le fichier `.graphml` contient:
- Les **nœuds** (utilisateurs) avec leurs **labels** (noms)
- Les **arêtes** (relations d'amitié)
- Le type de graphe (bidirectionnel ou directionnel)

## 3. Import dans Gephi

1. Ouvrez Gephi
2. Cliquez sur **Fichier → Ouvrir** ou **File → Open**
3. Sélectionnez votre fichier `.graphml` (ex: `friends.graphml`)
4. Dans la fenêtre d'import:
   - **Type de graphe**: Choisir "Undirected" (Non dirigé) pour un graphe bidirectionnel
   - Cliquez sur **OK**

## 4. Visualisation

### A. Afficher les labels

1. Dans l'onglet **Apparence** (bottom left)
2. Cliquez sur l'icône **T** (texte)
3. Activez **Afficher les labels** ou **Show labels**
4. Les noms des utilisateurs s'affichent maintenant sur les nœuds

### B. Appliquer une mise en page

Dans l'onglet **Mise en page** (Layout):

1. Sélectionnez **Force Atlas 2** (recommandé) ou **Fruchterman Reingold**
2. Configurez les paramètres:
   - Force Atlas 2:
     - Gravity: 10-30
     - Scaling: 10-50
   - Fruchterman Reingold:
     - Area: 1000-5000
     - Gravity: 10
3. Cliquez sur **Exécuter** ou **Run**
4. Attendez que le graphe se stabilise
5. Cliquez sur **Arrêter** ou **Stop**

### C. Personnaliser l'apparence

#### Taille des nœuds (par degré)

1. Onglet **Apparence** → **Nœuds**
2. Sélectionnez **Taille** (Size)
3. Choisissez **Classement** (Ranking) → **Degree**
4. Définir min/max (ex: 10-50)
5. Cliquez sur **Appliquer**

Les utilisateurs avec plus d'amis apparaissent plus grands!

#### Couleur des nœuds

1. Onglet **Apparence** → **Nœuds**
2. Sélectionnez **Couleur**
3. Choisissez une couleur ou utilisez **Partition** pour colorer par communauté

## 5. Analyse du réseau

### Calculer les statistiques

1. Onglet **Statistiques** (Statistics)
2. Exécutez les analyses suivantes:
   - **Degré moyen** (Average Degree): Nombre moyen d'amis
   - **Diamètre du réseau** (Network Diameter): Distance maximale
   - **Modularité** (Modularity): Détection de communautés
   - **Centralité d'intermédiarité** (Betweenness Centrality): Utilisateurs "ponts"

### Interpréter les résultats

- **Degré élevé**: Utilisateurs très connectés (hubs)
- **Centralité élevée**: Utilisateurs importants pour connecter le réseau
- **Modularité**: Groupes d'amis distincts (communautés)

## 6. Export de la visualisation

1. Onglet **Aperçu** (Preview)
2. Configurez l'apparence finale
3. **Exporter** → Choisir le format:
   - **PNG**: Image
   - **PDF**: Document vectoriel
   - **SVG**: Pour édition ultérieure

## Exemple avec friends.csv

Pour votre fichier `friends.csv`:

```bash
python main.py friends.csv --graphml friends.graphml --stats
```

Résultats attendus dans Gephi:
- **9 nœuds** (Alice, Bob, Charlie, David, Eve, Frank, George, Helen, Ivan)
- **18 arêtes** (relations d'amitié)
- Les nœuds les mieux connectés apparaissent plus grands
- Visualisation claire du réseau social

## Astuces

- **Zoom**: Molette de la souris
- **Déplacer**: Clic droit + glisser
- **Sélectionner un nœud**: Clic gauche
- **Rafraîchir la mise en page**: Re-exécuter l'algorithme

## Dépannage

### Les labels ne s'affichent pas
- Vérifiez que vous avez activé "Afficher les labels" dans l'onglet Apparence
- Augmentez la taille de la police dans l'onglet Aperçu

### Le graphe est trop dense
- Augmentez le paramètre "Scaling" dans Force Atlas 2
- Utilisez une aire plus grande dans Fruchterman Reingold

### Erreur d'import
- Vérifiez que le fichier `.graphml` est bien formé
- Réexécutez l'export: `python main.py friends.csv --graphml friends.graphml`

## Ressources

- Documentation Gephi: https://gephi.org/users/
- Tutoriels vidéo: https://gephi.org/users/tutorial-visualization/
