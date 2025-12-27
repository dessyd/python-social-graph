"""
Exemples avancés d'utilisation de SocialGraph.

Usage:
    python advanced_example.py [fichier_csv]

Arguments:
    fichier_csv: Chemin vers le fichier CSV (défaut: friends.csv)
"""

import sys
from pathlib import Path
from social_graph import SocialGraph


# Variable globale pour le fichier CSV
CSV_FILE = 'data/input/friends.csv'


def example_1_recommendations():
    """Exemple: Recommandations d'amis basées sur FOAF."""
    print("=" * 60)
    print("Exemple 1: Recommandations d'amis")
    print("=" * 60)

    graph = SocialGraph()
    graph.load_from_csv(CSV_FILE)

    # Utiliser le premier utilisateur du graphe
    all_users = sorted(graph.get_all_users())
    if not all_users:
        print("\n⚠️  Aucun utilisateur dans le graphe\n")
        return

    user = all_users[0]
    foaf = graph.get_foaf(user)

    print(f"\n👤 Suggestions d'amis pour {user}:")
    if foaf:
        print(f"Vous pourriez connaître: {', '.join(sorted(foaf))}")
    else:
        print(f"Aucune suggestion (tous les utilisateurs sont déjà amis ou amis d'amis)")
    print()


def example_2_network_analysis():
    """Exemple: Analyse du réseau social."""
    print("=" * 60)
    print("Exemple 2: Analyse du réseau")
    print("=" * 60)

    graph = SocialGraph()
    graph.load_from_csv(CSV_FILE)

    stats = graph.get_statistics()

    print(f"\n📊 Statistiques globales:")
    print(f"  - Total utilisateurs: {stats['total_users']}")
    print(f"  - Total relations: {stats['total_friendships']}")
    print(f"  - Moyenne d'amis: {stats['avg_friends_per_user']:.2f}")

    # Trouver les utilisateurs les plus connectés
    print(f"\n🌟 Utilisateurs les plus connectés:")
    user_connections = []
    for user in graph.get_all_users():
        friend_count = len(graph.get_friends(user))
        user_connections.append((user, friend_count))

    # Trier par nombre de connexions (décroissant)
    user_connections.sort(key=lambda x: x[1], reverse=True)

    for user, count in user_connections[:5]:
        print(f"  - {user}: {count} amis")
    print()


def example_3_network_reach():
    """Exemple: Portée du réseau (amis + FOAF)."""
    print("=" * 60)
    print("Exemple 3: Portée du réseau")
    print("=" * 60)

    graph = SocialGraph()
    graph.load_from_csv(CSV_FILE)

    print(f"\n🔍 Portée du réseau pour chaque utilisateur:")

    for user in sorted(graph.get_all_users()):
        direct_friends = len(graph.get_friends(user))
        foaf_count = len(graph.get_foaf(user))
        total_reach = direct_friends + foaf_count

        print(f"\n  {user}:")
        print(f"    - Amis directs: {direct_friends}")
        print(f"    - Amis d'amis: {foaf_count}")
        print(f"    - Portée totale: {total_reach} personnes")


def example_4_mutual_friends():
    """Exemple: Trouver les amis communs."""
    print("\n" + "=" * 60)
    print("Exemple 4: Amis communs")
    print("=" * 60)

    graph = SocialGraph()
    graph.load_from_csv(CSV_FILE)

    # Utiliser les deux premiers utilisateurs du graphe
    all_users = sorted(graph.get_all_users())
    if len(all_users) < 2:
        print("\n⚠️  Pas assez d'utilisateurs pour cette analyse\n")
        return

    user1 = all_users[0]
    user2 = all_users[1]

    friends1 = graph.get_friends(user1)
    friends2 = graph.get_friends(user2)

    mutual = friends1 & friends2  # Intersection

    print(f"\n👥 Amis communs entre {user1} et {user2}:")
    if mutual:
        print(f"  {', '.join(sorted(mutual))}")
    else:
        print(f"  Aucun ami commun")
    print()


def example_5_create_custom_graph():
    """Exemple: Créer un graphe personnalisé."""
    print("=" * 60)
    print("Exemple 5: Graphe personnalisé")
    print("=" * 60)

    # Créer un graphe de followers (unidirectionnel)
    graph = SocialGraph(bidirectional=False)

    # Alice suit Bob et Charlie
    graph.add_friendship("Alice", "Bob")
    graph.add_friendship("Alice", "Charlie")

    # Bob suit Alice
    graph.add_friendship("Bob", "Alice")

    # Charlie suit David
    graph.add_friendship("Charlie", "David")

    print(f"\n📱 Graphe de followers (unidirectionnel):")
    for user in sorted(graph.get_all_users()):
        following = graph.get_friends(user)
        print(f"  {user} suit: {', '.join(sorted(following)) if following else 'personne'}")

    # Export
    graph.to_json('data/output/custom_followers.json')
    print(f"\n💾 Graphe exporté vers 'data/output/custom_followers.json'\n")


def example_6_connection_strength():
    """Exemple: Force des connexions (nombre d'amis communs)."""
    print("=" * 60)
    print("Exemple 6: Force des connexions")
    print("=" * 60)

    graph = SocialGraph()
    graph.load_from_csv(CSV_FILE)

    # Utiliser le premier utilisateur du graphe
    all_users = sorted(graph.get_all_users())
    if not all_users:
        print("\n⚠️  Aucun utilisateur dans le graphe\n")
        return

    user = all_users[0]
    friends = graph.get_friends(user)

    print(f"\n💪 Force des connexions pour {user}:")

    if not friends:
        print(f"  {user} n'a aucun ami")
        print()
        return

    connection_strength = []
    for friend in friends:
        mutual = graph.get_friends(user) & graph.get_friends(friend)
        # Retirer user et friend des amis communs
        mutual.discard(user)
        mutual.discard(friend)
        connection_strength.append((friend, len(mutual)))

    # Trier par force de connexion (décroissant)
    connection_strength.sort(key=lambda x: x[1], reverse=True)

    for friend, strength in connection_strength:
        print(f"  - {friend}: {strength} amis communs")
    print()


def main():
    """Exécute tous les exemples."""
    global CSV_FILE

    # Gérer les arguments de ligne de commande
    if len(sys.argv) > 1:
        CSV_FILE = sys.argv[1]

    # Vérifier que le fichier existe
    csv_path = Path(CSV_FILE)
    if not csv_path.exists():
        print(f"❌ Erreur: Le fichier '{CSV_FILE}' n'existe pas")
        print(f"\nUsage: python {sys.argv[0]} [fichier_csv]")
        print(f"Exemple: python {sys.argv[0]} data/input/friends.csv")
        sys.exit(1)

    print("\n" + "🚀 " + "=" * 56 + " 🚀")
    print("   EXEMPLES AVANCÉS - Social Graph Manager")
    print("🚀 " + "=" * 56 + " 🚀")
    print(f"\n📂 Fichier CSV utilisé: {CSV_FILE}\n")

    example_1_recommendations()
    example_2_network_analysis()
    example_3_network_reach()
    example_4_mutual_friends()
    example_5_create_custom_graph()
    example_6_connection_strength()

    print("=" * 60)
    print("✨ Tous les exemples ont été exécutés!")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
