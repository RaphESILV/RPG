import sqlite3
import os
from typing import Dict, List, Optional

class DatabaseManager:
    def __init__(self, db_name: str = "race.db"):
        """Initialise la connexion à la base de données"""
        # Créer le dossier data s'il n'existe pas
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
        os.makedirs(data_dir, exist_ok=True)
        
        # Définir le chemin complet de la base de données
        self.db_path = os.path.join(data_dir, db_name)
        self.conn = None
        self.cursor = None

    def connect(self):
        """Établit la connexion à la base de données"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        """Ferme la connexion à la base de données"""
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """Crée la table des races"""
        # Supprime la table si elle existe
        self.cursor.execute('DROP TABLE IF EXISTS races')
        
        # Crée la nouvelle table
        self.cursor.execute('''
            CREATE TABLE races (
                race_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) NOT NULL,
                race_code VARCHAR(10) UNIQUE NOT NULL,
                category VARCHAR(50) NOT NULL,  -- 'Nocturne' ou 'Non-Nocturne'
                hp INTEGER DEFAULT 0,
                mp INTEGER DEFAULT 0,
                force INTEGER DEFAULT 0,
                defense INTEGER DEFAULT 0,
                magie INTEGER DEFAULT 0,
                resistance INTEGER DEFAULT 0,
                agilite INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def initialize_data(self):
        """Initialise les données de base"""
        races = [
            # Non-Nocturnes
            ('Humain', 'HUM', 'Non-Nocturne', 20, 20, 12, 12, 12, 12, 12),
            ('Elfe', 'ELF', 'Non-Nocturne', 15, 25, 10, 8, 15, 15, 15),
            ('Nain', 'NAI', 'Non-Nocturne', 30, 5, 25, 25, 5, 5, 5),
            ('Argoniens', 'ARG', 'Non-Nocturne', 20, 10, 15, 15, 5, 10, 25),
            # Nocturnes
            ('Vampire', 'VAM', 'Nocturne', 20, 20, 12, 12, 12, 12, 12),
            ('Loup-Garou', 'LOU', 'Nocturne', 15, 10, 25, 15, 5, 25, 25),
            ('Youkai', 'YOU', 'Nocturne', 10, 25, 5, 5, 25, 25, 5),
            ('Squelette', 'SQU', 'Nocturne', 10, 30, 5, 5, 20, 20, 10)
        ]
        self.cursor.executemany('''
            INSERT OR IGNORE INTO races 
            (name, race_code, category, hp, mp, force, defense, magie, resistance, agilite)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', races)
        self.conn.commit()

    def get_all_races(self) -> List[Dict]:
        """Récupère toutes les races avec leurs statistiques"""
        self.cursor.execute('SELECT * FROM races')
        columns = [description[0] for description in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def get_race_by_code(self, race_code: str) -> Optional[Dict]:
        """Récupère une race par son code"""
        self.cursor.execute('SELECT * FROM races WHERE race_code = ?', (race_code,))
        columns = [description[0] for description in self.cursor.description]
        row = self.cursor.fetchone()
        return dict(zip(columns, row)) if row else None

    def get_races_by_category(self, category: str) -> List[Dict]:
        """Récupère toutes les races d'une catégorie"""
        self.cursor.execute('SELECT * FROM races WHERE category = ?', (category,))
        columns = [description[0] for description in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

# Exemple d'utilisation
if __name__ == "__main__":
    db = DatabaseManager()
    db.connect()
    
    # Création des tables et initialisation des données
    db.create_tables()
    db.initialize_data()
    
    # Exemple de récupération des données
    print("\nToutes les races :")
    all_races = db.get_all_races()
    for race in all_races:
        print(f"\n{race['name']} ({race['race_code']}) - {race['category']}")
        print(f"HP: {race['hp']}, MP: {race['mp']}")
        print(f"Force: {race['force']}, Défense: {race['defense']}")
        print(f"Magie: {race['magie']}, Résistance: {race['resistance']}")
        print(f"Agilité: {race['agilite']}")
    
    # Exemple de recherche par code de race
    print("\nRecherche d'une race spécifique :")
    human = db.get_race_by_code('HUM')
    if human:
        print(f"Race trouvée : {human['name']}")
    
    db.disconnect()
