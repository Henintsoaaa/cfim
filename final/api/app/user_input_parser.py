# app/user_input_parser.py
"""
Parser pour les inputs utilisateur simplifiés
Convertit les descriptions naturelles en valeurs numériques pour le modèle
"""
from datetime import datetime
from typing import Dict, Optional, Tuple


class UserInputParser:
    """
    Convertit les inputs familiers des utilisateurs en données pour le modèle
    """
    
    # Mapping des descriptions de vent vers vitesse en km/h
    VENT_DESCRIPTIONS = {
        'calme': 5.0,
        'légère brise': 10.0,
        'petite brise': 15.0,
        'jolie brise': 20.0,
        'bonne brise': 25.0,
        'vent frais': 30.0,
        'grand frais': 35.0,
        'coup de vent': 45.0,
        'fort coup de vent': 55.0,
        'tempête': 65.0,
        'forte tempête': 75.0,
        'ouragan': 85.0
    }
    
    # Mapping des états de mer (échelle Douglas)
    ETAT_MER_DESCRIPTIONS = {
        'calme': {'score': 0, 'hauteur': 0.1},
        'ridée': {'score': 1, 'hauteur': 0.2},
        'belle': {'score': 2, 'hauteur': 0.5},
        'peu agitée': {'score': 3, 'hauteur': 1.0},
        'agitée': {'score': 4, 'hauteur': 2.0},
        'forte': {'score': 5, 'hauteur': 3.0},
        'très forte': {'score': 6, 'hauteur': 4.5},
        'grosse': {'score': 7, 'hauteur': 7.0},
        'très grosse': {'score': 8, 'hauteur': 10.0},
        'énorme': {'score': 9, 'hauteur': 14.0}
    }
    
    # Mapping des conditions météo vers visibilité (0=nulle, 10=excellente)
    TEMPS_DESCRIPTIONS = {
        'clair': 10.0,
        'beau temps': 10.0,
        'peu nuageux': 9.0,
        'nuageux': 7.5,
        'couvert': 6.5,
        'averses': 5.0,
        'pluie légère': 5.5,
        'pluie': 4.0,
        'pluie forte': 2.5,
        'brume': 2.0,
        'orage': 3.0,
        'grains': 3.5,
        'brouillard': 1.0,
        'brouillard épais': 0.2
    }
    
    # Coordonnées GPS des principales zones maritimes de Madagascar
    LIEUX_MADAGASCAR = {
        # Côte Est
        'cap d\'ambre': {'lat': -12.0, 'lon': 49.3},
        'antsiranana': {'lat': -12.3, 'lon': 49.3},
        'diego suarez': {'lat': -12.3, 'lon': 49.3},
        'antalaha': {'lat': -14.9, 'lon': 50.3},
        'sambava': {'lat': -14.3, 'lon': 50.2},
        'sainte marie': {'lat': -17.0, 'lon': 49.8},
        'île sainte marie': {'lat': -17.0, 'lon': 49.8},
        'toamasina': {'lat': -18.2, 'lon': 49.4},
        'tamatave': {'lat': -18.2, 'lon': 49.4},
        'mahanoro': {'lat': -19.9, 'lon': 48.8},
        'manakara': {'lat': -22.1, 'lon': 48.0},
        'farafangana': {'lat': -22.8, 'lon': 47.8},
        'taolagnaro': {'lat': -25.0, 'lon': 47.0},
        'fort dauphin': {'lat': -25.0, 'lon': 47.0},
        'cap est': {'lat': -15.3, 'lon': 50.5},
        
        # Côte Ouest
        'morombe': {'lat': -21.8, 'lon': 43.4},
        'morondava': {'lat': -20.3, 'lon': 44.3},
        'maintirano': {'lat': -18.1, 'lon': 44.0},
        'besalampy': {'lat': -16.8, 'lon': 44.5},
        'mahajanga': {'lat': -15.7, 'lon': 46.3},
        'majunga': {'lat': -15.7, 'lon': 46.3},
        
        # Côte Sud
        'cap sainte marie': {'lat': -25.6, 'lon': 45.2},
        'tuléar': {'lat': -23.4, 'lon': 43.7},
        'toliara': {'lat': -23.4, 'lon': 43.7},
        
        # Centre (par défaut)
        'madagascar': {'lat': -18.9, 'lon': 47.5},
        'antananarivo': {'lat': -18.9, 'lon': 47.5}
    }
    
    def __init__(self):
        pass
    
    def parse_date(self, date_str: str) -> Tuple[int, int, int]:
        """
        Parse une date au format DD/MM/YYYY ou YYYY-MM-DD
        
        Args:
            date_str: Date au format texte
            
        Returns:
            Tuple (jour, mois, année)
        """
        # Essayer format DD/MM/YYYY
        for fmt in ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d']:
            try:
                date_obj = datetime.strptime(date_str.strip(), fmt)
                return (date_obj.day, date_obj.month, date_obj.year)
            except ValueError:
                continue
        
        # Si échec, retourner date du jour
        now = datetime.now()
        return (now.day, now.month, now.year)
    
    def parse_vent(self, vent_input: str) -> float:
        """
        Convertit description ou vitesse en noeuds vers km/h
        
        Args:
            vent_input: Description ("grand frais") ou valeur ("35 kt" ou "35")
            
        Returns:
            Vitesse en km/h
        """
        vent_lower = vent_input.lower().strip()
        
        # 1. Chercher correspondance EXACTE
        if vent_lower in self.VENT_DESCRIPTIONS:
            return self.VENT_DESCRIPTIONS[vent_lower]
        
        # 2. Chercher correspondance partielle (trier par longueur décroissante)
        sorted_descriptions = sorted(self.VENT_DESCRIPTIONS.items(), key=lambda x: len(x[0]), reverse=True)
        for desc, vitesse in sorted_descriptions:
            if desc in vent_lower:
                return vitesse
        
        # Extraire valeur numérique si présente
        import re
        match = re.search(r'(\d+(?:\.\d+)?)', vent_input)
        if match:
            valeur = float(match.group(1))
            
            # Si l'unité est en noeuds (kt, kts, noeuds)
            if any(unit in vent_lower for unit in ['kt', 'noeud', 'knot']):
                return round(valeur * 1.852, 1)  # Convertir kt vers km/h
            
            # Si valeur entre 0-100, supposer que c'est des noeuds
            if valeur <= 100:
                return round(valeur * 1.852, 1)
            
            # Sinon, supposer km/h
            return valeur
        
        # Valeur par défaut
        return 20.0
    
    def parse_etat_mer(self, etat_input: str) -> Tuple[float, float]:
        """
        Convertit description d'état de mer en score (0-9) et hauteur (m)
        
        Args:
            etat_input: Description ("grosse", "très forte", etc.)
            
        Returns:
            Tuple (score 0-9, hauteur en mètres)
        """
        etat_lower = etat_input.lower().strip()
        
        # 1. Chercher correspondance EXACTE d'abord
        if etat_lower in self.ETAT_MER_DESCRIPTIONS:
            valeurs = self.ETAT_MER_DESCRIPTIONS[etat_lower]
            return (float(valeurs['score']), valeurs['hauteur'])
        
        # 2. Chercher correspondance partielle (trier par longueur décroissante pour éviter faux positifs)
        sorted_descriptions = sorted(self.ETAT_MER_DESCRIPTIONS.items(), key=lambda x: len(x[0]), reverse=True)
        for desc, valeurs in sorted_descriptions:
            if desc in etat_lower:
                return (float(valeurs['score']), valeurs['hauteur'])
        
        # Si valeur numérique fournie directement
        import re
        match = re.search(r'(\d+)', etat_input)
        if match:
            score = min(9, max(0, int(match.group(1))))
            # Estimer hauteur basée sur score
            hauteurs = [0.1, 0.2, 0.5, 1.0, 2.0, 3.0, 4.5, 7.0, 10.0, 14.0]
            hauteur = hauteurs[score] if score < len(hauteurs) else 14.0
            return (float(score), hauteur)
        
        # Valeur par défaut (agitée)
        return (4.0, 2.0)
    
    def parse_temps(self, temps_input: str) -> float:
        """
        Convertit description météo en indice de visibilité (0-10)
        
        Args:
            temps_input: Description ("clair", "pluie", "brouillard", etc.)
            
        Returns:
            Indice de visibilité 0-10
        """
        temps_lower = temps_input.lower().strip()
        
        # 1. Chercher correspondance EXACTE
        if temps_lower in self.TEMPS_DESCRIPTIONS:
            return self.TEMPS_DESCRIPTIONS[temps_lower]
        
        # 2. Chercher correspondance partielle (trier par longueur décroissante)
        sorted_descriptions = sorted(self.TEMPS_DESCRIPTIONS.items(), key=lambda x: len(x[0]), reverse=True)
        for desc, visibilite in sorted_descriptions:
            if desc in temps_lower:
                return visibilite
        
        # Si valeur numérique
        import re
        match = re.search(r'(\d+(?:\.\d+)?)', temps_input)
        if match:
            valeur = float(match.group(1))
            return min(10.0, max(0.0, valeur))
        
        # Valeur par défaut (nuageux)
        return 7.0
    
    def parse_lieu(self, lieu_input: str) -> Tuple[float, float]:
        """
        Convertit nom de lieu en coordonnées GPS
        
        Args:
            lieu_input: Nom du lieu ("Toamasina", "Cap d'Ambre", etc.)
            
        Returns:
            Tuple (latitude, longitude)
        """
        lieu_lower = lieu_input.lower().strip()
        
        # Chercher correspondance
        for nom, coords in self.LIEUX_MADAGASCAR.items():
            if nom in lieu_lower or lieu_lower in nom:
                return (coords['lat'], coords['lon'])
        
        # Si coordonnées GPS fournies directement
        import re
        # Format: "-18.9, 47.5" ou "-18.9 / 47.5"
        match = re.search(r'(-?\d+(?:\.\d+)?)[,/\s]+(-?\d+(?:\.\d+)?)', lieu_input)
        if match:
            lat = float(match.group(1))
            lon = float(match.group(2))
            return (lat, lon)
        
        # Par défaut : centre de Madagascar
        return (-18.9, 47.5)
    
    def parse_user_input(self, 
                        date_input: str,
                        vent_input: str,
                        etat_mer_input: str,
                        temps_input: str,
                        lieu_input: str) -> Dict:
        """
        Parse tous les inputs utilisateur et retourne les données pour le modèle
        
        Args:
            date_input: Date (DD/MM/YYYY)
            vent_input: Description ou vitesse du vent
            etat_mer_input: Description de l'état de la mer
            temps_input: Description météo/visibilité
            lieu_input: Nom du lieu ou coordonnées
            
        Returns:
            Dict avec toutes les features pour le modèle
        """
        # Parser chaque input
        jour, mois, annee = self.parse_date(date_input)
        vent_vitesse = self.parse_vent(vent_input)
        etat_mer_score, hauteur_mer = self.parse_etat_mer(etat_mer_input)
        visibilite = self.parse_temps(temps_input)
        latitude, longitude = self.parse_lieu(lieu_input)
        
        return {
            'jour': jour,
            'mois': mois,
            'annee': annee,
            'vent_vitesse': vent_vitesse,
            'hauteur_mer': hauteur_mer,
            'etat_mer': etat_mer_score,
            'visibilite': visibilite,
            'latitude': latitude,
            'longitude': longitude,
            # Informations supplémentaires pour affichage
            'parsed_info': {
                'date_str': f"{jour:02d}/{mois:02d}/{annee}",
                'vent_desc': vent_input,
                'etat_mer_desc': etat_mer_input,
                'temps_desc': temps_input,
                'lieu_desc': lieu_input
            }
        }


# Instance globale
user_input_parser = UserInputParser()
