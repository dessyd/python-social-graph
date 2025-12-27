"""
Social Graph Manager - Handles CSV ingestion and social network analysis.

Format CSV attendu: chaque ligne = utilisateur,ami1,ami2,ami3,...
Exemple: Alice,Bob,Charlie,David
"""

import csv
import json
from pathlib import Path
from typing import Dict, Set, List, Optional
from collections import defaultdict


class SocialGraph:
    """Gestion d'un graphe social avec import CSV et export JSON."""

    def __init__(self, bidirectional: bool = True):
        """
        Initialise le graphe social.

        Args:
            bidirectional: Si True, les relations sont bidirectionnelles
                          (si A est ami avec B, alors B est ami avec A)
        """
        self.graph: Dict[str, Set[str]] = defaultdict(set)
        self.bidirectional = bidirectional

    @staticmethod
    def _clean_name(name: str) -> str:
        """
        Nettoie un nom d'utilisateur.

        Args:
            name: Nom à nettoyer

        Returns:
            Nom nettoyé (espaces supprimés, capitalisation)
        """
        return name.strip()

    def add_friendship(self, user: str, friend: str) -> None:
        """
        Ajoute une relation d'amitié.

        Args:
            user: Nom de l'utilisateur
            friend: Nom de l'ami
        """
        user = self._clean_name(user)
        friend = self._clean_name(friend)

        # Éviter les auto-références
        if user == friend:
            return

        # Ajouter la relation
        self.graph[user].add(friend)

        # Si bidirectionnel, ajouter la relation inverse
        if self.bidirectional:
            self.graph[friend].add(user)

    def load_from_csv(self, filepath: str | Path) -> None:
        """
        Charge le graphe depuis un fichier CSV.

        Format: chaque ligne = utilisateur,ami1,ami2,ami3,...

        Args:
            filepath: Chemin vers le fichier CSV
        """
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(f"Le fichier {filepath} n'existe pas")

        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)

            for line_num, row in enumerate(reader, start=1):
                # Ignorer les lignes vides
                if not row or not any(row):
                    continue

                # Le premier élément est l'utilisateur
                if len(row) < 1:
                    continue

                user = self._clean_name(row[0])

                # Les éléments suivants sont les amis
                friends = [self._clean_name(friend) for friend in row[1:] if friend.strip()]

                # Ajouter chaque amitié (gère automatiquement les doublons via Set)
                for friend in friends:
                    self.add_friendship(user, friend)

    def get_friends(self, user: str) -> Set[str]:
        """
        Retourne les amis d'un utilisateur.

        Args:
            user: Nom de l'utilisateur

        Returns:
            Ensemble des amis de l'utilisateur
        """
        user = self._clean_name(user)
        return self.graph.get(user, set())

    def get_foaf(self, user: str, include_direct_friends: bool = False) -> Set[str]:
        """
        Retourne les amis d'amis (Friend of a Friend).

        Args:
            user: Nom de l'utilisateur
            include_direct_friends: Si True, inclut aussi les amis directs

        Returns:
            Ensemble des amis d'amis
        """
        user = self._clean_name(user)
        direct_friends = self.get_friends(user)
        foaf = set()

        # Pour chaque ami, récupérer ses amis
        for friend in direct_friends:
            friend_of_friend = self.get_friends(friend)
            foaf.update(friend_of_friend)

        # Retirer l'utilisateur lui-même
        foaf.discard(user)

        # Retirer les amis directs si demandé
        if not include_direct_friends:
            foaf -= direct_friends

        return foaf

    def get_all_users(self) -> Set[str]:
        """
        Retourne tous les utilisateurs du graphe.

        Returns:
            Ensemble de tous les utilisateurs
        """
        return set(self.graph.keys())

    def get_user_count(self) -> int:
        """
        Retourne le nombre d'utilisateurs.

        Returns:
            Nombre d'utilisateurs
        """
        return len(self.graph)

    def get_friendship_count(self) -> int:
        """
        Retourne le nombre total de relations d'amitié.

        Returns:
            Nombre de relations (divisé par 2 si bidirectionnel)
        """
        total = sum(len(friends) for friends in self.graph.values())
        return total // 2 if self.bidirectional else total

    def to_dict(self) -> Dict[str, List[str]]:
        """
        Convertit le graphe en dictionnaire.

        Returns:
            Dictionnaire {utilisateur: [liste d'amis]}
        """
        return {user: sorted(list(friends)) for user, friends in self.graph.items()}

    def to_json(self, filepath: str | Path, indent: int = 2) -> None:
        """
        Export le graphe en JSON.

        Args:
            filepath: Chemin du fichier de sortie
            indent: Indentation du JSON (par défaut: 2)
        """
        filepath = Path(filepath)
        data = self.to_dict()

        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=indent, ensure_ascii=False)

    def get_statistics(self) -> Dict[str, any]:
        """
        Retourne des statistiques sur le graphe.

        Returns:
            Dictionnaire avec les statistiques
        """
        friend_counts = [len(friends) for friends in self.graph.values()]

        return {
            'total_users': self.get_user_count(),
            'total_friendships': self.get_friendship_count(),
            'bidirectional': self.bidirectional,
            'avg_friends_per_user': sum(friend_counts) / len(friend_counts) if friend_counts else 0,
            'max_friends': max(friend_counts) if friend_counts else 0,
            'min_friends': min(friend_counts) if friend_counts else 0,
        }

    def export_foaf_report(self, filepath: str | Path) -> None:
        """
        Export un rapport FOAF pour tous les utilisateurs en JSON.

        Args:
            filepath: Chemin du fichier de sortie
        """
        filepath = Path(filepath)
        foaf_report = {}

        for user in self.get_all_users():
            foaf_report[user] = {
                'direct_friends': sorted(list(self.get_friends(user))),
                'friends_of_friends': sorted(list(self.get_foaf(user))),
                'total_foaf': len(self.get_foaf(user))
            }

        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(foaf_report, file, indent=2, ensure_ascii=False)

    def to_graphml(self, filepath: str | Path) -> None:
        """
        Export le graphe au format GraphML.

        GraphML est un format XML standard pour les graphes, compatible avec
        Gephi, yEd, Cytoscape, et autres outils de visualisation.

        Args:
            filepath: Chemin du fichier de sortie (.graphml)
        """
        filepath = Path(filepath)

        # Déterminer le type de graphe
        edge_default = "undirected" if self.bidirectional else "directed"

        # Créer le contenu GraphML
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<graphml xmlns="http://graphml.graphdrawing.org/xmlns"',
            '         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
            '         xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns',
            '         http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">',
            '  <!-- Définition des attributs -->',
            '  <key id="label" for="node" attr.name="label" attr.type="string"/>',
            f'  <graph id="SocialGraph" edgedefault="{edge_default}">',
        ]

        # Ajouter les nœuds (utilisateurs) avec labels
        for user in sorted(self.get_all_users()):
            # Échapper les caractères XML spéciaux
            user_escaped = user.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
            lines.append(f'    <node id="{user_escaped}">')
            lines.append(f'      <data key="label">{user_escaped}</data>')
            lines.append(f'    </node>')

        # Ajouter les arêtes (relations)
        added_edges = set()  # Pour éviter les doublons en mode bidirectionnel

        for user in sorted(self.get_all_users()):
            user_escaped = user.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

            for friend in sorted(self.get_friends(user)):
                friend_escaped = friend.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

                # En mode bidirectionnel, éviter les doublons
                if self.bidirectional:
                    edge_key = tuple(sorted([user, friend]))
                    if edge_key in added_edges:
                        continue
                    added_edges.add(edge_key)

                lines.append(f'    <edge source="{user_escaped}" target="{friend_escaped}"/>')

        # Fermer les balises
        lines.extend([
            '  </graph>',
            '</graphml>'
        ])

        # Écrire le fichier
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write('\n'.join(lines))

    def __repr__(self) -> str:
        """Représentation textuelle du graphe."""
        stats = self.get_statistics()
        return (f"SocialGraph(users={stats['total_users']}, "
                f"friendships={stats['total_friendships']}, "
                f"bidirectional={self.bidirectional})")
