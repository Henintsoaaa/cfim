"""
Parser pour les bulletins météorologiques marins au format WTIO20 (Madagascar)
"""
import re
from datetime import datetime
from typing import Dict, Optional, Tuple


class BulletinParser:
    """Parse les bulletins marins spéciaux BMS de Météo Madagascar"""
    
    def __init__(self):
        # Patterns regex pour extraire les informations
        self.date_pattern = r'(\d{2})/(\d{2})/(\d{4})\s+A\s+(\d{2})\s+TU'
        self.position_pattern = r'(\d+\.?\d*)\s*S\s*/\s*(\d+\.?\d*)\s*E'
        self.wind_pattern = r'(CALME|BRISE LEGERE|PETITE BRISE|JOLIE BRISE|BONNE BRISE|VENT FRAIS|GRAND FRAIS|COUP DE VENT|FORT COUP DE VENT|TEMPETE|VIOLENTE TEMPETE|OURAGAN)\s+(\d+)\s*KT'
        self.sea_state_pattern = r'MER\s+(CALME|BELLE|PEU AGITEE|AGITEE|FORTE|TRES FORTE|GROSSE|TRES GROSSE|GROSSE A TRES GROSSE|ENORME)'
        self.visibility_pattern = r'(CLAIR|BON|MOYEN|MEDIOCRE|MAUVAIS|TRES MAUVAIS|BROUILLARD|BRUME|BROUILLARD EPAIS)'
        
        # Mapping des descriptions vers valeurs numériques
        self.wind_scale = {
            'CALME': 0,
            'BRISE LEGERE': 10,
            'PETITE BRISE': 15,
            'JOLIE BRISE': 25,
            'BONNE BRISE': 35,
            'VENT FRAIS': 45,
            'GRAND FRAIS': 55,
            'COUP DE VENT': 65,
            'FORT COUP DE VENT': 75,
            'TEMPETE': 85,
            'VIOLENTE TEMPETE': 95,
            'OURAGAN': 120
        }
        
        self.sea_state_scale = {
            'CALME': (0, 0),           # (état mer 0-9, hauteur m)
            'BELLE': (1, 0.1),
            'PEU AGITEE': (2, 0.5),
            'AGITEE': (3, 1.25),
            'FORTE': (4, 2.5),
            'TRES FORTE': (5, 4),
            'GROSSE': (6, 6),
            'TRES GROSSE': (7, 9),
            'GROSSE A TRES GROSSE': (7, 8),
            'ENORME': (9, 14)
        }
        
        self.visibility_scale = {
            'CLAIR': 10,
            'BON': 8,
            'MOYEN': 6,
            'MEDIOCRE': 4,
            'MAUVAIS': 2,
            'TRES MAUVAIS': 1,
            'BROUILLARD': 0.5,
            'BRUME': 1,
            'BROUILLARD EPAIS': 0.2
        }
    
    def parse_bulletin(self, bulletin_text: str) -> Dict:
        """
        Extrait les données d'un bulletin BMS
        
        Args:
            bulletin_text: Texte du bulletin au format WTIO20
            
        Returns:
            Dictionnaire avec les données extraites
        """
        result = {
            'date': None,
            'heure': None,
            'latitude': None,
            'longitude': None,
            'vent_description': None,
            'vent_kt': None,
            'vent_kmh': None,
            'etat_mer_description': None,
            'etat_mer_score': None,
            'hauteur_mer': None,
            'visibilite_description': None,
            'visibilite_km': None,
            'raw_text': bulletin_text
        }
        
        # Extraction de la date
        date_match = re.search(self.date_pattern, bulletin_text, re.IGNORECASE)
        if date_match:
            jour, mois, annee, heure = date_match.groups()
            result['date'] = f"{annee}-{mois}-{jour}"
            result['heure'] = int(heure)
            result['jour'] = int(jour)
            result['mois'] = int(mois)
            result['annee'] = int(annee)
        
        # Extraction de la position (latitude/longitude)
        position_match = re.search(self.position_pattern, bulletin_text, re.IGNORECASE)
        if position_match:
            lat, lon = position_match.groups()
            result['latitude'] = -float(lat)  # Négatif pour Sud
            result['longitude'] = float(lon)
        
        # Extraction du vent
        wind_match = re.search(self.wind_pattern, bulletin_text, re.IGNORECASE)
        if wind_match:
            description, kt = wind_match.groups()
            result['vent_description'] = description
            result['vent_kt'] = int(kt)
            result['vent_kmh'] = int(kt) * 1.852  # Conversion noeuds -> km/h
        
        # Extraction de l'état de la mer
        sea_match = re.search(self.sea_state_pattern, bulletin_text, re.IGNORECASE)
        if sea_match:
            description = sea_match.group(1)
            result['etat_mer_description'] = description
            if description.upper() in self.sea_state_scale:
                score, hauteur = self.sea_state_scale[description.upper()]
                result['etat_mer_score'] = score
                result['hauteur_mer'] = hauteur
        
        # Extraction de la visibilité
        visibility_match = re.search(self.visibility_pattern, bulletin_text, re.IGNORECASE)
        if visibility_match:
            description = visibility_match.group(1)
            result['visibilite_description'] = description
            if description.upper() in self.visibility_scale:
                result['visibilite_km'] = self.visibility_scale[description.upper()]
        
        return result
    
    def to_model_input(self, parsed_data: Dict) -> Tuple:
        """
        Convertit les données parsées en entrées pour le modèle
        
        Returns:
            Tuple de 9 valeurs: (vent_vitesse, hauteur_mer, etat_mer, visibilite, 
                                 jour, mois, annee, latitude, longitude)
        """
        # Valeur par défaut pour visibilité si non trouvée
        visibilite = parsed_data.get('visibilite_km')
        if visibilite is None:
            # Si mer très grosse/énorme, assume mauvaise visibilité
            hauteur_mer = parsed_data.get('hauteur_mer', 0)
            if hauteur_mer > 6:
                visibilite = 2  # Mauvaise
            else:
                visibilite = 5  # Moyenne
        
        return (
            parsed_data.get('vent_kmh', 0),
            parsed_data.get('hauteur_mer', 0),
            parsed_data.get('etat_mer_score', 0),
            visibilite,
            parsed_data.get('jour', 1),
            parsed_data.get('mois', 1),
            parsed_data.get('annee', 2020),
            parsed_data.get('latitude', -18.0),  # Centre Madagascar
            parsed_data.get('longitude', 47.0)
        )


# Instance globale
bulletin_parser = BulletinParser()


def parse_and_prepare(bulletin_text: str) -> Tuple[Dict, Tuple]:
    """
    Fonction helper pour parser et préparer les données en une seule étape
    
    Args:
        bulletin_text: Texte du bulletin
        
    Returns:
        Tuple (parsed_data, model_inputs)
    """
    parsed = bulletin_parser.parse_bulletin(bulletin_text)
    model_inputs = bulletin_parser.to_model_input(parsed)
    return parsed, model_inputs
