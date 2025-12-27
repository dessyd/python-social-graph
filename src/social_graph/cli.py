#!/usr/bin/env python3
"""
Script principal pour gérer le graphe social.

Usage:
    python main.py <fichier_csv> [options]

Options:
    --no-bidirectional    Relations unidirectionnelles
    --output <fichier>    Fichier JSON de sortie (défaut: social_graph.json)
    --foaf-report         Génère un rapport FOAF
    --stats              Affiche les statistiques
"""

import sys
import argparse
from pathlib import Path
from social_graph.graph import SocialGraph


def main():
    """Point d'entrée principal du script."""
    parser = argparse.ArgumentParser(
        description='Gestionnaire de graphe social - Import CSV et export JSON'
    )

    parser.add_argument(
        'csv_file',
        type=str,
        help='Fichier CSV à importer (format: utilisateur,ami1,ami2,...)'
    )

    parser.add_argument(
        '--no-bidirectional',
        action='store_true',
        help='Relations unidirectionnelles (défaut: bidirectionnelles)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='data/output/social_graph.json',
        help='Fichier JSON de sortie (défaut: data/output/social_graph.json)'
    )

    parser.add_argument(
        '--foaf-report',
        type=str,
        help='Génère un rapport FOAF dans le fichier spécifié'
    )

    parser.add_argument(
        '--graphml',
        type=str,
        help='Export au format GraphML (pour Gephi, yEd, Cytoscape)'
    )

    parser.add_argument(
        '--stats',
        action='store_true',
        help='Affiche les statistiques du graphe'
    )

    parser.add_argument(
        '--query-user',
        type=str,
        help='Affiche les amis et FOAF pour un utilisateur spécifique'
    )

    args = parser.parse_args()

    # Vérifier que le fichier CSV existe
    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        print(f"❌ Erreur: Le fichier '{args.csv_file}' n'existe pas")
        sys.exit(1)

    # Créer le graphe social
    print(f"📊 Création du graphe social...")
    graph = SocialGraph(bidirectional=not args.no_bidirectional)

    # Charger les données
    print(f"📂 Chargement du fichier '{args.csv_file}'...")
    try:
        graph.load_from_csv(csv_path)
        print(f"✅ Données chargées avec succès!")
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        sys.exit(1)

    # Afficher les statistiques si demandé
    if args.stats:
        print("\n📈 Statistiques du graphe:")
        stats = graph.get_statistics()
        print(f"  - Nombre d'utilisateurs: {stats['total_users']}")
        print(f"  - Nombre de relations: {stats['total_friendships']}")
        print(f"  - Mode: {'bidirectionnel' if stats['bidirectional'] else 'unidirectionnel'}")
        print(f"  - Moyenne d'amis par utilisateur: {stats['avg_friends_per_user']:.2f}")
        print(f"  - Maximum d'amis: {stats['max_friends']}")
        print(f"  - Minimum d'amis: {stats['min_friends']}")

    # Requête pour un utilisateur spécifique
    if args.query_user:
        user = args.query_user
        friends = graph.get_friends(user)
        foaf = graph.get_foaf(user)

        print(f"\n👤 Informations pour '{user}':")
        print(f"  - Amis directs ({len(friends)}): {', '.join(sorted(friends)) if friends else 'Aucun'}")
        print(f"  - Amis d'amis ({len(foaf)}): {', '.join(sorted(foaf)) if foaf else 'Aucun'}")

    # Export JSON
    output_path = Path(args.output)
    print(f"\n💾 Export vers '{output_path}'...")
    try:
        graph.to_json(output_path)
        print(f"✅ Export réussi!")
    except Exception as e:
        print(f"❌ Erreur lors de l'export: {e}")
        sys.exit(1)

    # Rapport FOAF si demandé
    if args.foaf_report:
        foaf_path = Path(args.foaf_report)
        print(f"\n📋 Génération du rapport FOAF vers '{foaf_path}'...")
        try:
            graph.export_foaf_report(foaf_path)
            print(f"✅ Rapport FOAF généré!")
        except Exception as e:
            print(f"❌ Erreur lors de la génération du rapport: {e}")
            sys.exit(1)

    # Export GraphML si demandé
    if args.graphml:
        graphml_path = Path(args.graphml)
        print(f"\n🔗 Export GraphML vers '{graphml_path}'...")
        try:
            graph.to_graphml(graphml_path)
            print(f"✅ GraphML généré! (Compatible Gephi, yEd, Cytoscape)")
        except Exception as e:
            print(f"❌ Erreur lors de l'export GraphML: {e}")
            sys.exit(1)

    print(f"\n✨ Traitement terminé!")


if __name__ == '__main__':
    main()
