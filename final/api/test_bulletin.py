#!/usr/bin/env python3
"""Script de test pour parser un bulletin météo"""

import sys
sys.path.insert(0, '/home/henintsoa/CFIM/final/api')

from app.bulletin_parser import parse_and_prepare

# Bulletin de test
bulletin_text = """WTIO20 FMMD 010600
BULLETIN MARINE SPECIAL
BMS N°07/04 DE FMMDYMYP A 06 TU
EMIS PAR METEO MADAGASCAR LE 01/01/2020 A 06 TU
1. AVIS D'OURAGAN
2. PHENOMENE: CYCLONE TROPICAL 4 (CALVINIA) 976 HPA
POSITION A 06 TU : DANS UN RAYON DE 10 MN AUTOUR DU POINT 26.9 S / 60.6 E
(VINGT SIX DEGRES NEUF SUD ET SOIXANTE DEGRES SIX EST)
DEPLACEMENT: SUD-SUD-EST 17 KT
3. ZONE MENACEE :
TEMPS A GRAINS DANS UN RAYON DE 100 MN AUTOUR DU CENTRE S'ETENDANT
JUSQU'A 350 MN DANS LE DEMI-CERCLE SUD.
OURAGAN 65 KT ET MER TRES GROSSE A ENORME S'ETENDANT JUSQUE 40 MN
DANS LE DEMI-CERCLE EST.
TEMPETE 50/60 KT ET MER GROSSE A TRES GROSSE DANS UN RAYON DE 55 MN
AUTOUR DU CENTRE, S'ETENDANT JUSQUE 80 MN DANS LE DEMI-CERCLE EST."""

# Parser le bulletin
print("=" * 60)
print("TEST DU PARSING DU BULLETIN MÉTÉO")
print("=" * 60)

parsed_data, model_input = parse_and_prepare(bulletin_text)

print("\n📋 DONNÉES EXTRAITES DU BULLETIN:")
print("-" * 60)
for key, value in parsed_data.items():
    if key != 'raw_text':
        print(f"  {key:25s}: {value}")

print("\n🤖 ENTRÉES POUR LE MODÈLE ML:")
print("-" * 60)
labels = ['vent_vitesse', 'hauteur_mer', 'etat_mer', 'visibilite', 
          'jour', 'mois', 'annee', 'latitude', 'longitude']
for label, value in zip(labels, model_input):
    print(f"  {label:15s}: {value}")

# Faire la prédiction
from app.predict import make_prediction

pred, proba = make_prediction(*model_input)

print("\n🎯 PRÉDICTION:")
print("-" * 60)
print(f"  Incident prédit: {'OUI ⚠️' if pred == 1 else 'NON ✓'}")
print(f"  Probabilité: {proba*100:.1f}%")

if proba >= 0.70:
    niveau = "CRITIQUE 🔴"
elif proba >= 0.50:
    niveau = "ÉLEVÉ 🟠"
elif proba >= 0.30:
    niveau = "MODÉRÉ 🟡"
else:
    niveau = "FAIBLE 🟢"

print(f"  Niveau de risque: {niveau}")
print("=" * 60)
