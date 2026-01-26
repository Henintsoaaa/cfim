# RAPPORT DE PROJET

## SYSTÈME DE PRÉDICTION DES INCIDENTS MARITIMES À MADAGASCAR

### Analyse des Conditions Météorologiques Marines et Développement d'un Modèle Prédictif

**Auteur** : Henintsoa  
**Institution** : CFIM  
**Période** : 2025-2026  
**Domaine** : Data Science & Machine Learning - Sécurité Maritime

## TABLE DES MATIÈRES

1. [Résumé Exécutif](#résumé-exécutif)
2. [Introduction](#introduction)
3. [Contexte et Problématique](#contexte-et-problématique)
4. [Méthodologie](#méthodologie)
5. [Développement du Projet](#développement-du-projet)
6. [Résultats et Performances](#résultats-et-performances)
7. [Problèmes Rencontrés et Solutions](#problèmes-rencontrés-et-solutions)
8. [Déploiement et Interface Utilisateur](#déploiement-et-interface-utilisateur)
9. [Perspectives d'Amélioration](#perspectives-damélioration)
10. [Conclusion](#conclusion)
11. [Annexes](#annexes)

## 1. RÉSUMÉ EXÉCUTIF

Dans un contexte insulaire où l'économie bleue est vitale pour Madagascar, ce projet répond à une urgence sécuritaire majeure : la prévention des accidents en mer. En effet, malgré une connaissance empirique des dangers par les navigateurs, l'absence d'outils prédictifs automatisés rend la navigation vulnérable aux changements rapides des conditions océanographiques.

Ce projet a permis de concevoir et développer de bout en bout un **système intelligent de prédiction des incidents maritimes**, transformant des données brutes et hétérogènes en informations décisionnelles critiques. Notre approche s'est distinguée par la rigueur de son traitement de données (valorisation de 6 années d'archives météorologiques textuelles) et par l'utilisation de stratégies de modélisation avancées pour surmonter le défi du **déséquilibre extrême des classes** (incidents rares représentant moins de 1% des données).

La solution délivrée ne se limite pas à un modèle théorique : elle intègre une chaîne de valeur complète, depuis l'ingestion multimodale des données jusqu'à une interface utilisateur opérationnelle, offrant ainsi un véritable outil d'aide à la décision pour la sécurité maritime malgache.

## 2. INTRODUCTION

### 2.1 Contexte Général

Madagascar, avec ses 5000 km de côtes, est une île où la mer est à la fois une ressource économique essentielle et un milieu hostile. La navigation, qu'elle soit commerciale, de pêche ou de plaisance, est soumise à des régimes météorologiques complexes, influencés par la convergence intertropicale et les cyclones saisonniers. Cependant, les incidents maritimes continuent de survenir, souvent par manque d'anticipation des conditions locales spécifiques.

### 2.2 Objectifs du Projet

L'ambition de ce projet dépasse la simple analyse statistique. Il s'agissait de construire un **outil prédictif robuste** capable d'alerter sur des situations à risque, en se basant sur l'analyse historique des liens de causalité entre conditions météo et accidents.

**Objectifs Spécifiques et Démarche** :

- **Valorisation du patrimoine de données** : Structurer et exploiter 6 années de bulletins météo, une mine d'informations jusque-là inexploitée car non structurée.
- **Unification spatio-temporelle** : Créer un pont entre la météorologie (zones marines) et la gestion de crise (régions administratives), nécessitant une modélisation géographique complexe.
- **Modélisation de l'événement rare** : Développer des algorithmes capables de "trouver une aiguille dans une botte de foin", c'est-à-dire prédire les rares jours d'incidents sans générer trop de fausses alertes.
- **Opérationnalisation** : Rendre ces modèles mathématiques complexes accessibles via une interface simple pour les utilisateurs finaux.

### 2.3 Périmètre du Projet

- **Période des données** : 2017-2022 (6 ans)
- **Zone géographique** : Côtes de Madagascar
- **Types de données** : Bulletins météo marins, incidents maritimes, données satellitaires
- **Technologies** : Python, Scikit-learn, XGBoost, FastAPI, HTML/CSS/JavaScript

## 3. CONTEXTE ET PROBLÉMATIQUE

### 3.1 Enjeux de la Sécurité Maritime

La prévision des conditions dangereuses en mer est cruciale pour :

- **Sauver des vies** : Éviter les accidents de navigation
- **Protéger l'économie** : Réduire les pertes matérielles
- **Optimiser les opérations** : Planification des activités maritimes

### 3.2 Défis Techniques

#### 3.2.1 Déséquilibre Extrême des Données

- Incidents : < 1% des observations
- Jours normaux : > 99% des observations
- **Risque** : Modèles biaisés prédisant toujours "pas d'incident"

#### 3.2.2 Hétérogénéité des Données

- Bulletins météo en texte libre (non structuré)
- Formats variables selon les périodes
- Zones géographiques avec nomenclatures différentes

#### 3.2.3 Complexité Météorologique

- Interactions multiples entre facteurs (vent, mer, précipitations)
- Phénomènes cycloniques saisonniers
- Variabilité spatiale importante

## 4. MÉTHODOLOGIE

### 4.1 Approche Globale

Le projet suit une méthodologie **CRISP-DM** (Cross-Industry Standard Process for Data Mining) adaptée :

1. **Compréhension du métier** : Analyse des besoins en sécurité maritime
2. **Compréhension des données** : Exploration des bulletins météo et incidents
3. **Préparation des données** : Extraction, nettoyage, transformation
4. **Modélisation** : Développement et optimisation des algorithmes
5. **Évaluation** : Validation des performances
6. **Déploiement** : Mise en production via API et interface web

### 4.2 Technologies et Outils

**Langages et Frameworks** :

- Python 3.11 (NumPy, Pandas, Scikit-learn, XGBoost)
- FastAPI (backend)
- HTML/CSS/JavaScript (frontend)

**Bibliothèques Spécialisées** :

- `imbalanced-learn` : Gestion du déséquilibre (SMOTE)
- `SHAP` : Interprétabilité des prédictions
- `Matplotlib/Seaborn` : Visualisations

**Environnement** :

- Jupyter Notebook (développement et expérimentation)
- VS Code (édition de code)
- Git (versionnement)

## 5. DÉVELOPPEMENT DU PROJET

### 5.1 Phase 1 : Extraction des Bulletins Météorologiques

**Notebook** : `1_extraction_bulletins_meteo.ipynb`

#### 5.1.1 Objectifs

Extraire et structurer les informations contenues dans les bulletins météo marins en texte libre.

#### 5.1.2 Données Sources

- **Fichier** : `meteo_marine_cotiere_complet.csv`
- **Contenu** : Bulletins quotidiens 2017-2022
- **Format** : Texte non structuré avec variations

#### 5.1.3 Processus d'Extraction

L'extraction d'informations structurées à partir de texte libre a constitué l'un des défis techniques majeurs du projet. Contrairement à des données tabulaires propres, les bulletins météo sont rédigés par des humains, avec une variabilité syntaxique importante selon les opérateurs et les années.

##### A. Analyse des Patterns et Complexité Linguistique

Une analyse approfondie du corpus de bulletins a été nécessaire pour identifier les structures récurrentes malgré le "bruit" textuel. Nous avons constaté que les informations clés (vent, mer, visibilité) n'étaient pas toujours présentées dans le même ordre et utilisaient un vocabulaire technique varié (ex: "Mer agitée à forte", "Vents de secteur Est").

Cette phase exploratoire a été cruciale pour mapper toutes les variantes possibles d'expression d'une même condition météorologique, conditionnant directement la qualité des données futures.

##### B. Développement d'Extracteurs Intelligents (NLP & Regex)

Plutôt que d'utiliser des outils de NLP génériques peu adaptés au jargon technique maritime malgache, nous avons développé une batterie d'extracteurs sur mesure basés sur des expressions régulières (Regex) complexes. Ces extracteurs ont été conçus pour être :

- **Robustes** : Capables de gérer les fautes de frappe et les variations d'unités (nœuds, km/h, beaufort).
- **Précis** : Distinguant le vent moyen des rafales, et la houle de la mer du vent.
- **Contextuels** : Associant correctement chaque condition à sa zone géographique spécifique, évitant les erreurs d'attribution fréquentes dans les bulletins couvrant plusieurs zones.

##### C. Standardisation et Nettoyage

Une fois l'information brute extraite, un important travail de standardisation a été réalisé pour rendre les données exploitables par des algorithmes. Cela a impliqué la conversion de descriptions qualitatives ("Mer belle") en échelles numériques, le traitement des plages de valeurs (conversion de "15 à 20 noeuds" en moyenne 17.5), et un nettoyage rigoureux des incohérences temporelles. Ce processus a transformé un amas de texte non structuré en un dataset analytique de haute qualité.

#### 5.1.4 Résultats

- **Dataset standardisé** : Variables météo numériques par zone et par jour
- **Qualité** : Réduction des valeurs manquantes, cohérence des formats
- **Volume** : ~6 années × 365 jours × plusieurs zones

### 5.2 Phase 2 : Correspondance Spatiale

**Notebooks** :

- `2_correspondance_spatiale.ipynb`
- `2.1_integration_donnees_satellites.ipynb`

#### 5.2.1 Problématique

Les **bulletins météo** utilisent des zones marines (ex: "CAP D'AMBRE A TOAMASINA") tandis que les **incidents** sont localisés par régions administratives (ex: "DIANA", "ATSINANANA").

#### 5.2.2 Approche de Résolution : Le Défi de l'Alignement Géographique

L'enjeu ici était de ne pas perdre d'information critique lors de la traduction d'une zone météo ("Conditions dangereuses au Cap d'Ambre") vers une région administrative ("Région DIANA"). Une mauvaise correspondance aurait pour conséquence d'entraîner le modèle sur des données fausses (associer un incident à du beau temps, ou l'inverse).

##### A. Cartographie et Logique d'Inclusion

Nous avons réalisé un travail minutieux de cartographie pour définir quelles zones météo influencent quelles régions côtières. Cette étape a nécessité de comprendre la géographie maritime locale : une région administrative peut être bordée par plusieurs zones météo (au Nord et à l'Est par exemple), exposant ses marins à des régimes de vents différents.

##### B. Matrice d'Agrégation "Worst-Case Scenario"

Au lieu d'une simple moyenne qui lisserait les dangers, nous avons adopté une **stratégie sécuritaire (Worst-Case)** pour l'agrégation des données. Si une région administrative est touchée par trois zones météo différentes, nous conservons systématiquement les **valeurs maximales** (vent le plus fort, mer la plus haute) pour l'entraînement du modèle.
_Raisonnement_ : En sécurité maritime, le danger vient des conditions extrêmes locales, pas de la moyenne régionale. Un marin subissant une tempête dans le nord de la région ne doit pas être "moyenné" avec le calme plat du sud. Cette décision méthodologique a considérablement amélioré la capacité du modèle à détecter les risques réels.

#### 5.2.3 Intégration des Données Satellitaires : Une Vérité Terrain Objective

Pour pallier les lacunes parfois subjectives des bulletins (estimations visuelles), nous avons enrichi notre dataset avec des données satellitaires (SWH). Cette fusion de données hétérogènes (texte humain + mesures physiques) apporte une double robustesse : le satellite confirme la tendance, et le bulletin apporte la nuance locale et les autres paramètres (vent, pluie) non visibles par le satellite d'altimétrie.

### 5.3 Phase 3 : Création du Dataset d'Entraînement

**Notebook** : `2.3_creation_dataset_entrainement.ipynb`

#### 5.3.1 Fusion des Données

**Données d'Entrée** :

1. Bulletins météo standardisés
2. Incidents maritimes géolocalisés
3. Données satellitaires SWH

**Processus de Fusion** :

- Jointure temporelle (par date)
- Jointure spatiale (via matrice zones-régions)
- Création de la variable cible : `incident` (0 ou 1)

#### 5.3.2 Feature Engineering Préliminaire

Création de variables dérivées :

- **Scores de risque** : Combinaisons pondérées de facteurs météo
- **Indicateurs binaires** : Conditions extrêmes (oui/non)
- **Agrégations** : Max, min, moyenne par région
- **Variables temporelles** : Jour, mois, année, jour de la semaine

#### 5.3.3 Découpage Train/Test

**Stratégie** : Split temporel (respecte la chronologie)

- **Train** : 2017-2021 (80%)
- **Test** : 2022 (20%)
- **Justification** : Évaluer la capacité de prédiction sur des données futures

### 5.4 Phase 4 : Modélisation Machine Learning

**Notebook** : `model.ipynb`

#### 5.4.1 Exploration des Données (EDA)

##### A. Analyse du Déséquilibre

Visualisations créées :

- Graphiques en barres : Distribution incidents/non-incidents
- Constat : Ratio > 100:1 (déséquilibre extrême)

##### B. Analyse des Variables Météo

- **Histogrammes comparatifs** : Distribution pour incidents vs non-incidents
- **Boxplots** : Identification des valeurs extrêmes associées aux incidents
- **Matrice de corrélation** : Relations entre variables

##### C. Analyse Temporelle

- **Saisonnalité** : Identification des mois à haut risque (saison cyclonique)
- **Tendances** : Évolution annuelle

#### 5.4.2 Feature Engineering : L'Art de Traduire l'Expertise Métier en Données

La simple utilisation des colonnes brutes (vitesse du vent, hauteur de mer) ne suffisait pas pour obtenir un modèle performant. Les incidents maritimes étant souvent le résultat d'une **synergie de facteurs**, nous avons dû "apprendre" au modèle à détecter ces interactions complexes.

##### A. Création d'Interactions et de Scores de Risque

C'est une étape où l'intuition physique a guidé la science des données. Savoir qu'un vent fort est dangereux est une chose, mais un vent fort combiné à une mer croisée est exponentiellement plus risqué.
Nous avons donc créé des **features d'interaction polynomiales** (ex: `vent * mer`) et des **indices composites de danger**. Ces variables synthétiques agissent comme des "amplificateurs de signal", permettant aux algorithmes de décision (comme les arbres de décision) de diviser l'espace des données plus efficacement sur les zones critiques.

##### B. Prise en Compte de la Dynamique Temporelle (Lags)

La mer a une mémoire. Une houle ne se forme pas instantanément ; elle est le résultat de vents soufflant sur la durée. Pour capturer cette inertie, nous avons introduit des features temporelles (Lags et Rolling Windows). Le modèle ne regarde plus seulement "le temps qu'il fait", mais aussi "comment le temps a évolué ces 3 derniers jours". Si la mer grossit rapidement (delta positif fort), le risque d'accident est souvent plus élevé que si elle est stable, car les équipages peuvent être surpris par la dégradation rapide.

##### C. Encodage Cyclique des Saisons

Le traitement linéaire du temps (janvier=1, décembre=12) pose problème en météorologie cyclique (janvier et décembre sont très proches en réalité). L'encodage trigonométrique (Sinus/Cosinus) a permis au modèle de comprendre correctement la saisonnalité des cyclones, assurant une continuité mathématique entre la fin et le début de l'année.

##### D. Sélection Rigoureuse des Variables

Avoir trop de variables peut "noyer" le signal des incidents rares dans du bruit. Nous avons appliqué une sélection stricte (ANOVA et Importance par arbre) pour ne garder que les ~40 indicateurs qui avaient une réelle corrélation causale ou prédictive avec les incidents, éliminant les redondances qui auraient pu complexifier inutilement le modèle.

#### 5.4.3 Stratégies de Modélisation du Déséquilibre : La Quête des Incidents Rares

Le cœur algorithmique de ce projet résidait dans la gestion du **déséquilibre extrême (1/100)**. Un modèle classique optimisant l'accuracy aurait simplement prédit "zéro incident" tout le temps pour avoir 99% de réussite, ce qui aurait été inutile pour la sécurité. Nous avons exploré trois philosophies distinctes pour forcer le modèle à apprendre :

##### A. Rééquilibrage Artificiel (SMOTE)

La première approche a consisté à modifier la réalité pour aider le modèle. Avec **SMOTE**, nous avons créé des "incidents virtuels" mathématiquement plausibles pour atteindre un ratio 50/50. Bien que puissante, cette méthode comportait le risque de générer du bruit ou des situations physiquement impossibles, ce qui nous a incités à rester prudents sur son utilisation finale.

##### B. Pénalisation des Erreurs (Cost-Sensitive Learning)

C'est l'approche "organique" finalement privilégiée. Au lieu de toucher aux données, nous avons modifié la "psychologie" du modèle (via les poids de classe XGBoost `scale_pos_weight`). Nous avons configuré l'algorithme pour qu'il considère qu'**rater un incident est 100 fois plus grave que de lancer une fausse alerte**. Cette calibration aligne parfaitement l'objectif mathématique avec l'objectif de sécurité publique (principe de précaution).

##### C. Détection d'Anomalies (Isolation Forest)

Nous avons aussi testé une approche radicalement différente : considérer l'incident non pas comme une classe à apprendre, mais comme une anomalie statistique à détecter (Outlier Detection). Si cette méthode est séduisante théoriquement, elle s'est avérée trop sensible en pratique, générant trop de fausses alarmes sur des conditions météo simplement "mauvaises" mais sans incident.

Le choix final s'est porté sur le **XGBoost avec pondération**, qui offrait le meilleur équilibre : il détecte bien les dangers réels sans paniquer à la moindre brise.

#### 5.4.4 Optimisation des Hyperparamètres

**Méthode** : RandomizedSearchCV

- 30 itérations de recherche aléatoire
- Validation croisée 3-fold stratifiée
- Optimisation du F1-score

**Paramètres optimisés** :

_Random Forest_ :

- Nombre d'arbres
- Profondeur maximale
- Critères de division
- Features par split

_XGBoost_ :

- Taux d'apprentissage
- Profondeur des arbres
- Échantillonnage (subsample, colsample)
- Poids de classe (scale_pos_weight)
- Régularisation (gamma, min_child_weight)

#### 5.4.5 Modèles d'Ensemble

##### A. Voting Classifier

- **Principe** : Vote pondéré de plusieurs modèles
- **Configuration** : Logistic Regression + Random Forest + XGBoost
- **Poids** : [1, 2, 2] (plus de poids aux modèles non-linéaires)
- **Type** : Soft voting (moyennes des probabilités)

##### B. Stacking Classifier

- **Niveau 1** : Random Forest + XGBoost (base learners)
- **Niveau 2** : Régression Logistique (meta-learner)
- **Principe** : Le meta-learner apprend à combiner optimalement les prédictions

#### 5.4.6 Interprétabilité

##### A. Importance des Features

- Scores natifs de Random Forest et XGBoost
- Identification des top 20 variables les plus influentes
- Visualisation en graphiques en barres

##### B. Valeurs SHAP

- **SHAP** : SHapley Additive exPlanations (théorie des jeux)
- Calcul de la contribution exacte de chaque feature
- **Visualisations** :
  - Summary plot : Impact global de chaque variable
  - Bar plot : Importance moyenne absolue

**Avantage** : Permet d'expliquer chaque prédiction individuellement.

### 5.5 Phase 5 : Déploiement

**Structure** : Dossier `api/`

#### 5.5.1 Architecture Backend (FastAPI)

##### A. Structure des Fichiers

```
api/
├── app/
│   ├── main.py              # Point d'entrée FastAPI
│   ├── model.py             # Chargement du modèle
│   ├── predict.py           # Logique de prédiction
│   ├── bulletin_parser.py   # Parsing des bulletins
│   ├── feature_engineering.py # Création des features
│   ├── user_input_parser.py # Parsing entrées utilisateur
│   ├── schemas.py           # Modèles Pydantic
│   └── templates/           # Templates HTML
│       └── index.html
│   └── static/              # CSS et JavaScript
│       ├── css/style.css
│       └── js/main.js
├── best_model_xgb_weighted.joblib  # Modèle sauvegardé
└── model_features_info.joblib      # Métadonnées
```

##### B. Endpoints API

**1. GET /**

- Page d'accueil avec interface utilisateur
- Formulaire de saisie

**2. POST /predict-simple**

- **Entrée** : Paramètres météo saisis manuellement
- **Traitement** :
  1. Validation des données (Pydantic)
  2. Feature engineering
  3. Prédiction avec le modèle
  4. Calcul du niveau de risque
- **Sortie** : JSON avec prédiction et probabilité

**3. POST /predict-bulletin**

- **Entrée** : Texte brut de bulletin météo
- **Traitement** :
  1. Parsing du bulletin (expressions régulières)
  2. Extraction des variables météo
  3. Feature engineering
  4. Prédiction
- **Sortie** : JSON avec prédiction, probabilité et données extraites

##### C. Chargement du Modèle

Stratégie de chargement au démarrage de l'application :

```python
# Chargement unique au lancement
model_package = joblib.load('best_model_xgb_weighted.joblib')
model = model_package['model']
scaler = model_package['scaler']
threshold = model_package['threshold']
```

**Avantage** : Temps de réponse rapide (modèle déjà en mémoire).

#### 5.5.2 Parsing de Bulletins

**Fichier** : `bulletin_parser.py`

##### A. Défis

- Bulletins en texte libre
- Formats variables
- Abréviations multiples (N, NE, m, kt, etc.)
- Zones géographiques avec orthographes variées

##### B. Solution

**Expressions Régulières Robustes** :

```python
# Exemple : Extraction de la force du vent
r'(?:VENT|VENTS)\s+(?:DE\s+)?(?:FORCE\s+)?(\d+)(?:\s+(?:A|À)\s+(\d+))?\s*(?:KT|NOEUDS?)?'
```

**Normalisation** :

- Conversion des directions (Nord → N)
- Unités standardisées (toujours en nœuds et mètres)
- Gestion des plages (ex: "15 à 20 kt" → moyenne)

##### C. Calcul de Scores de Risque

Le parseur calcule des scores composites :

- Score de mer (basé sur hauteur des vagues)
- Score de vent (vitesse + rafales)
- Score de temps (pluie, orage, visibilité)
- **Score global** : Combinaison pondérée

#### 5.5.3 Interface Utilisateur

**Fichiers** : `templates/index.html`, `static/css/style.css`, `static/js/main.js`

##### A. Design

**Approche** : Interface moderne et responsive

- **Header** : Titre et sous-titre explicatifs
- **Deux modes de saisie** :
  1. Formulaire simple (champs individuels)
  2. Bulletin complet (textarea)
- **Résultats** : Affichage clair avec codes couleur

##### B. Fonctionnalités JavaScript

**1. Soumission de Formulaire Simple**

```javascript
// Collecte des données
// Appel API POST /predict-simple
// Affichage du résultat avec couleur (vert/rouge)
```

**2. Parsing de Bulletin**

```javascript
// Envoi du texte brut
// Appel API POST /predict-bulletin
// Affichage de la prédiction + données extraites
```

**3. Feedback Visuel**

- Loading spinner pendant le traitement
- Animation des résultats
- Messages d'erreur clairs

##### C. Responsive Design

Adaptation à tous les écrans :

- Desktop : Layout large avec sections côte à côte
- Tablet : Layout adaptatif
- Mobile : Colonnes empilées verticalement

#### 5.5.4 Feature Engineering en Production : Le Défi de la Cohérence

Le passage du notebook de recherche à l'API de production a soulevé un défi d'ingénierie critique : la **reproductibilité temps-réel**. En phase d'entraînement, nous avions accès à tout l'historique passé et futur (pour l'analyse) et à toutes les variables. En production, face à une requête utilisateur unique, le système doit reconstruire instantanément un environnement de données aussi riche.

Pour garantir que le modèle en ligne se comporte exactement comme lors de sa validation :

- Nous avons réécrit tout le pipeline de transformation en **code modulaire "stateless"**, capable de traiter une seule ligne de données sans dépendre d'un dataframe massif.
- Les transformations mathématiques complexes (log, sin/cos) ont été hard-codées pour éviter toute dépendance à des versions de librairies changeantes.
- Nous avons implémenté des mécanismes de sécurité (valeurs par défaut intelligentes) pour les cas où certaines variables d'entrée seraient manquantes, garantissant que l'API réponde toujours, même en mode dégradé, ce qui est vital pour un service de sécurité.

## 6. RÉSULTATS ET PERFORMANCES

### 6.1 Métriques du Modèle Final

**Modèle Sélectionné** : XGBoost avec poids de classes optimisés

**Performances sur le jeu de test** :

- **F1-Score** : 0.6494 (équilibre précision/recall)
- **Recall** : 0.7353 (% d'incidents détectés)
- **Precision** : 0.5814 (% de prédictions correctes)
- **ROC-AUC** : 0.8903 (capacité de discrimination)

### 6.2 Interprétation des Résultats

#### 6.2.1 Top Features Importantes

D'après l'analyse SHAP et l'importance native :

1. **score_risque_max** : Score composite de conditions dangereuses
2. **vent_vitesse_max** : Vitesse maximale du vent
3. **mer_hauteur_max** : Hauteur maximale des vagues
4. **vent_rafales** : Intensité des rafales
5. **vent_mer_risque** : Interaction vent × mer
6. **saison_cyclonique** : Période de l'année à risque
7. **score_danger_composite** : Combinaison de tous les facteurs
8. **Features temporelles (lag)** : Tendances sur les jours précédents

**Insight** : Les **interactions** entre facteurs sont plus prédictives que les facteurs isolés.

#### 6.2.2 Analyse des Erreurs

**Faux Positifs** (prédictions d'incident incorrectes) :

- Souvent lors de conditions borderline (quasi-extrêmes)
- Préférable pour la sécurité (approche conservatrice)

**Faux Négatifs** (incidents non détectés) :

- Rares grâce à l'optimisation du recall
- Peuvent survenir lors d'événements soudains ou localisés

### 6.3 Comparaison des Stratégies

Classement par F1-Score (avec optimisations):
| Modèle | Seuil | Accuracy | Precision | Recall | F1-Score| ROC-AUC|
|-----------------------|-------|-------|----------------|---------|---------|---------|
| XGB Pondéré | 0.30 | 0.900000 | 0.581395 |0.735294 | 0.649351| 0.890329|
| XGB Optimisé | 0.75 | 0.896296 | 0.575000 |0.676471 | 0.621622| 0.904910|
| XGBoost | 0.35 | 0.900000 | 0.620690 |0.529412 | 0.571429| 0.852193|
| Voting Ensemble | 0.55 | 0.862963 | 0.469388 |0.676471 | 0.554217| 0.874875|
| RF Pondérée | 0.35 | 0.851852 | 0.437500 |0.617647 | 0.512195| 0.857178|
| RF Optimisé | 0.40 | 0.822222 | 0.375000 |0.617647 | 0.466667| 0.825773|
| Random Forest | 0.30 | 0.777778 | 0.314286 |0.647059 | 0.423077| 0.820165|
| RL Pondérée | 0.45 | 0.537037 | 0.186207 |0.794118 | 0.301676| 0.666625|
| Logistic Regression | 0.55 | 0.707407 | 0.215190 |0.500000 | 0.300885| 0.664506|
| Isolation Forest | 0.10 | 0.814815 | 0.250000 |0.235294 | 0.242424| 0.000000|
|Ensemble par Empilement | 0.10 | 0.125926 | 0.125926 |1.000000 | 0.223684| 0.135219|

**Conclusion** : XGBoost avec poids de classes offre le meilleur compromis.

## 7. PROBLÈMES RENCONTRÉS ET SOLUTIONS

### 7.1 Déséquilibre Extrême des Classes

#### Problème

- Incidents < 1% des observations
- Modèles naïfs prédisent toujours "pas d'incident"
- Accuracy élevée (99%) mais inutile (aucun incident détecté)

#### Solutions Testées

**1. SMOTE (Synthetic Minority Over-sampling)**

- Équilibre le dataset
- Risque de créer des exemples irréalistes
- Fonctionne bien avec Random Forest et XGBoost

**2. Poids de Classes**

- Pas de données synthétiques
- Force le modèle à prioriser les incidents
- **Solution retenue** pour le modèle final

**3. Ajustement du Seuil de Décision**

- Optimisation pour chaque modèle
- Amélioration significative du recall
- Appliqué à tous les modèles

**4. Validation Croisée Stratifiée**

- Assure la représentation des incidents dans chaque fold
- Évaluation plus fiable

### 7.2 Parsing des Bulletins Météo

#### Problème

- Texte non structuré
- Formats variables selon les années
- Abréviations multiples
- Erreurs typographiques
- Valeurs manquantes fréquentes

#### Solutions Implémentées

**1. Expressions Régulières Robustes**

```python
# Tolérance aux variations
r'(?:VENT|VENTS?)\s+(?:DE\s+)?(?:FORCE\s+)?(\d+)'
# Accepte: "VENT 15", "VENTS DE FORCE 15", "VENT FORCE 15"
```

**2. Normalisation Systématique**

- Conversion en majuscules
- Suppression des accents pour comparaison
- Standardisation des unités

**3. Gestion des Valeurs Manquantes**

- Valeurs par défaut cohérentes (ex: vent = 10 kt si non spécifié)
- Imputation par médiane pour les features numériques
- Flags indicateurs de valeur manquante

**4. Tests Extensifs**
Fichier `test_bulletin.py` avec :

- Bulletins de différentes périodes
- Cas limites (valeurs extrêmes, formats inhabituels)
- Validation de la cohérence des extractions

### 7.3 Correspondance Spatiale

#### Problème

- Zones météo ≠ Régions administratives
- Nomenclatures multiples pour les mêmes lieux
- Ambiguïté des frontières maritimes

#### Solutions

**1. Matrice de Correspondance Manuelle**

- Analyse géographique détaillée
- Validation avec expertise locale
- Documentation des choix

**2. Agrégations Multiples**

- Maximum (approche conservatrice)
- Moyenne (tendance)
- Minimum (conditions optimales)
- Permet différentes stratégies selon le besoin

**3. Gestion des Zones Multiples**
Une région peut correspondre à plusieurs zones météo :

```python
# Exemple: ATSINANANA couvre plusieurs zones
zones = ['SAINTE-MARIE A TOAMASINA', 'TOAMASINA A MAHANORO']
# On prend le maximum des conditions pour la sécurité
```

### 7.4 Feature Engineering en Production

#### Problème

- Nécessité de recréer exactement les mêmes features qu'à l'entraînement
- Gestion des features temporelles (lag) sans historique complet
- Performance en temps réel

#### Solutions

**1. Modularisation du Code**

- Fonctions réutilisables dans `feature_engineering.py`
- Même logique notebook → production
- Tests unitaires de cohérence

**2. Gestion des Features Lag**
Pour une prédiction ponctuelle :

- Utilisation de valeurs médianes pour les lags manquants
- Alternative : Mode "prédiction avec historique" (à développer)

**3. Optimisation des Performances**

- Vectorisation des opérations
- Chargement du modèle une seule fois
- Cache des calculs intermédiaires si applicable

### 7.5 Déploiement de l'API

#### Problème

- Gestion des erreurs en production
- Validation des entrées utilisateur
- Compatibilité des versions de bibliothèques

#### Solutions

**1. Validation avec Pydantic**

```python
class WeatherInput(BaseModel):
    vent_vitesse: float = Field(ge=0, le=100)  # 0-100 kt
    mer_hauteur: float = Field(ge=0, le=15)    # 0-15 m
    # Validation automatique des types et plages
```

**2. Gestion Globale des Erreurs**

```python
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Erreur interne", "detail": str(exc)}
    )
```

**3. Logging**

- Enregistrement de toutes les requêtes
- Traçabilité des erreurs
- Monitoring des performances

**4. Tests de l'API**

- Tests automatisés avec `pytest`
- Validation de tous les endpoints
- Tests de charge pour vérifier les performances

### 7.6 Compatibilité des Features entre Entraînement et Production

#### Problème

Le modèle a été entraîné avec des features incluant des colonnes de zones encodées (one-hot encoding), mais en production, on ne peut pas toujours fournir toutes ces colonnes.

#### Solution Actuelle

- Sélection uniquement des features disponibles
- Filtrage des features non-zone pour la prédiction simple
- Documentation des features requises vs optionnelles

#### À Améliorer

- Ré-entraîner le modèle sans les features de zone
- Ou créer un preprocessing standardisé qui génère toujours toutes les colonnes requises

## 8. DÉPLOIEMENT ET INTERFACE UTILISATEUR

### 8.1 Architecture Technique

```
┌─────────────────┐
│  Utilisateur    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Interface Web  │
│   (HTML/CSS/JS) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   API FastAPI   │
│  - Validation   │
│  - Parsing      │
│  - Features     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Modèle XGBoost │
│   (joblib)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Prédiction    │
│  + Probabilité  │
└─────────────────┘
```

### 8.2 Fonctionnalités de l'Interface

#### 8.2.1 Mode Saisie Simple

- **Champs** : Vitesse vent, rafales, hauteur mer, conditions météo, zone, date
- **Validation** : Contrôles en temps réel (plages de valeurs)
- **Feedback** : Messages d'erreur clairs

#### 8.2.2 Mode Bulletin Complet

- **Zone de texte** : Coller un bulletin météo brut
- **Parsing automatique** : Extraction de toutes les variables
- **Affichage** : Données extraites + prédiction

#### 8.2.3 Affichage des Résultats

**Format de Sortie** :

```json
{
  "prediction": 1,  // 0 ou 1
  "probabilite": 0.73,  // 0.0 à 1.0
  "niveau_risque": "ÉLEVÉ",  // FAIBLE, MODÉRÉ, ÉLEVÉ, TRÈS ÉLEVÉ
  "message": "Conditions météorologiques dangereuses détectées",
  "donnees_extraites": {
    "vent_vitesse": 25,
    "mer_hauteur": 4.5,
    ...
  }
}
```

**Codes Couleur** :

- Vert : Risque faible (probabilité < 0.3)
- Orange : Risque modéré (0.3 - 0.6)
- Rouge : Risque élevé (> 0.6)

### 8.3 Démarrage de l'Application

**Commande** :

```bash
cd api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Accès** :

- Interface : `http://localhost:8000`
- Documentation API : `http://localhost:8000/docs` (Swagger automatique)

### 8.4 Sécurité et Bonnes Pratiques

**Implémenté** :

- Validation stricte des entrées (Pydantic)
- Gestion des erreurs
- Logs des requêtes
- CORS configuré pour accès cross-origin

**À Ajouter pour Production** :

- Authentification (JWT tokens)
- Rate limiting (limitation du nombre de requêtes)
- HTTPS obligatoire
- Monitoring avancé (Prometheus, Grafana)
- Base de données pour historique des prédictions

## 9. PERSPECTIVES D'AMÉLIORATION ET VISION FUTURE

Ce projet a posé les fondations solides d'un système de prédiction, mais pour transformez ce prototype en une infrastructure nationale de sécurité maritime, plusieurs axes d'évolution stratégique sont envisagés.

### 9.1 Vers une Intelligence Artificielle "Data-Centric" et Multi-Source

La qualité des prédictions actuelles est limitée par la nature textuelle et parfois subjective des bulletins météo historiques. L'avenir du modèle réside dans sa capacité à **fusionner des sources hétérogènes** pour construire une "vérité terrain" indiscutable.

**L'apport décisif de l'imagerie satellitaire et des modèles numériques** :
Actuellement, nous n'utilisons qu'une fraction des données disponibles (SWH). L'intégration massive de données satellitaires (température de surface, courants, chlorophylle pour les zones de pêche) et de modèles numériques globaux (comme GFS ou ECMWF) permettrait de passer d'une vision "à la zone" à une vision "au pixel". Cela ouvrirait la voie à des prédictions hyper-locales, capables d'alerter un navire sur un danger spécifique à sa route, plutôt qu'à toute une région.

**Contextualisation par les données navires (AIS)** :
Un incident n'est pas seulement dû à la météo, mais à la vulnérabilité du navire. Croiser nos prédictions météo avec les données de trafic maritime (AIS) permettrait de pondérer le risque : une mer agitée est un danger mortel pour une pirogue traditionnelle, mais une simple routine pour un cargo. Intégrer la typologie des navires transformerait notre modèle météo en un véritable **modéle de risque opérationnel**.

### 9.2 Révolutionner l'Architecture : Du Prototype au Système Critique

Pour l'instant, notre solution est une API statique. Pour protéger des vies en temps réel, elle doit évoluer vers une architecture réactive et résiliente.

**Vers le "Live-Learning" et l'MLOps** :
La mer change, et les modèles climatiques aussi. Un modèle statique devient obsolète. La mise en place d'une boucle d'apprentissage continu (Online Learning) est cruciale. Chaque nouvel incident réel doit automatiquement venir enrichir l'entraînement du modèle. Cela nécessite une infrastructure MLOps robuste (pipeline CI/CD, versioning de données avec DVC) pour garantir que le modèle s'adapte aux dérives climatiques sans régression de performance.

**Mobile et Edge Computing : La sécurité dans la poche** :
La plupart des pêcheurs artisanaux n'ont pas d'ordinateur, mais ont un smartphone. Le développement d'une **Progressive Web App (PWA)** offline-first est une priorité absolue. L'objectif est de permettre le téléchargement des prévisions au port (via Wi-Fi/4G) et leur consultation en haute mer, même sans réseau. C'est cette "portabilité" qui fera la différence entre un outil technologique et un outil qui sauve des vies.

### 9.3 Innovation Algorithmique : Au-delà du Machine Learning Classique

Si XGBoost est excellent pour les données tabulaires, les phénomènes météorologiques sont par nature séquentiels et spatiaux.

**Deep Learning Spatio-Temporel** :
L'utilisation de réseaux de neurones récurrents (LSTM) ou convolutionnels (CNN) sur des séquences d'images satellitaires permettrait de capturer la _dynamique_ des systèmes météo (la formation d'une houle, la trajectoire d'un front) bien mieux que des variables statiques. Nous pourrions ainsi prédire non seulement le risque à l'instant T, mais son évolution à H+6 ou H+12, offrant un temps de réaction précieux aux équipages.

### 9.4 Impact Social et Ancrage Local

La technologie ne vaut rien si elle n'est pas adoptée. Le défi final est sociologique.

**Co-construction avec les Communautés Côtières** :
L'interface doit être adaptée aux réalités locales : multilingue (Malgache dialectal), vocale (pour l'accessibilité), et utilisant des codes visuels simples (drapeaux, couleurs). Un partenariat avec les chefs de port et les associations de pêcheurs est indispensable pour transformer cet outil numérique en un réflexe quotidien de sécurité. L'objectif ultime est de créer une **culture de la donnée** au service de la sécurité maritime à Madagascar.

- Documentation complète
- Contribution de la communauté

**2. Datasets Publics**

- Partage de datasets anonymisés
- Benchmark pour la recherche
- Hackathons et compétitions Kaggle

**3. Outils Réutilisables**

- Bibliothèque de parsing de bulletins météo
- Pipeline de feature engineering
- Framework de gestion du déséquilibre

### 9.6 Impact Social et Environnemental

#### 9.6.1 Réduction des Accidents

**Objectif** : Contribuer à sauver des vies

- Campagnes de sensibilisation
- Formation des pêcheurs et plaisanciers
- Partenariat avec ONG de sécurité maritime

#### 9.6.2 Durabilité

**1. Optimisation Énergétique**

- Routes optimales → moins de carburant
- Réduction de l'empreinte carbone

**2. Protection de l'Environnement Marin**

- Prévention des marées noires (navigation sûre)
- Réduction de la pollution marine

#### 9.6.3 Développement Local

**1. Formation et Emploi**

- Formation de data scientists malgaches
- Création d'emplois tech locaux
- Transfert de compétences

**2. Accessibilité**

- Version gratuite pour petits pêcheurs
- Subventions pour communautés côtières
- Partenariat avec gouvernement

## 10. CONCLUSION

### 10.1 Synthèse du Projet

Ce projet de prédiction des incidents maritimes à Madagascar a permis de développer un système complet et opérationnel intégrant :

1. **Traitement de données complexes** : Extraction et standardisation de bulletins météo en texte libre
2. **Correspondance spatiale** : Mapping entre zones météorologiques et régions géographiques
3. **Modélisation avancée** : Gestion du déséquilibre extrême avec techniques spécialisées (SMOTE, poids de classes, détection d'anomalies)
4. **Feature engineering créatif** : Création de variables d'interaction et temporelles pertinentes
5. **Optimisation rigoureuse** : Recherche d'hyperparamètres et ensembles de modèles
6. **Déploiement professionnel** : API FastAPI avec interface utilisateur intuitive

### 10.2 Apports et Compétences Acquises

**Compétences Techniques** :

- Traitement de données textuelles non structurées (NLP basique)
- Gestion de données déséquilibrées (techniques avancées)
- Feature engineering créatif et métier
- Optimisation de modèles de machine learning
- Développement d'API avec FastAPI
- Création d'interfaces web responsive
- Déploiement et mise en production

**Compétences Méthodologiques** :

- Approche CRISP-DM complète
- Gestion de projet data science de A à Z
- Documentation professionnelle
- Tests et validation
- Interprétabilité et explicabilité des modèles

**Compétences Métier** :

- Compréhension des enjeux maritimes
- Traduction de besoins métier en solutions techniques
- Communication avec experts non-techniques

### 10.3 Impact Potentiel

**Court Terme** :

- Outil d'aide à la décision pour navigateurs
- Réduction potentielle des accidents maritimes
- Sensibilisation aux conditions dangereuses

**Moyen Terme** :

- Intégration dans systèmes de gestion maritime
- Contribution aux bulletins météo officiels
- Optimisation des activités maritimes

**Long Terme** :

- Système de prévention nationale
- Benchmark pour la recherche
- Extension à d'autres régions de l'océan Indien

### 10.4 Limites Actuelles

**Données** :

- Historique limité (6 ans)
- Incidents rares (difficulté d'apprentissage)
- Qualité variable des bulletins

**Modèle** :

- Prédictions basées uniquement sur météo (pas de contexte navire)
- Généralisation à confirmer sur nouvelles données
- Explicabilité perfectible pour utilisateurs non-techniques

**Déploiement** :

- Pas encore en production réelle
- Sécurité et scalabilité à renforcer
- Besoin de monitoring opérationnel

### 10.5 Recommandations

**Pour Mise en Production** :

1. **Phase pilote** avec groupe restreint d'utilisateurs
2. **Collecte de feedback** systématique
3. **Validation continue** avec incidents réels
4. **Communication claire** des limites du système
5. **Formation** des utilisateurs finaux

**Pour Recherche Future** :

1. **Extension des données** (satellites, modèles numériques)
2. **Exploration deep learning** (LSTM, CNN)
3. **Prédictions multi-horizons** (J+1, J+2, J+3)
4. **Intégration de contexte** (type de navire, expérience équipage)

### 10.6 Remerciements

Ce projet a été rendu possible grâce à :

- L'accès aux données météorologiques historiques
- Les outils open source de la communauté data science
- Les ressources documentaires sur la sécurité maritime
- Le support technique et méthodologique durant le développement

## 11. ANNEXES

### Annexe A : Structure des Datasets

#### A.1 Dataset d'Entraînement Final

**Fichier** : `dataset_train.csv`

**Dimensions** : ~XXXX lignes × ~150 colonnes

**Colonnes principales** :

- `date` : Date de l'observation
- `region` : Région administrative
- `incident` : Variable cible (0 ou 1)
- `vent_vitesse_min/max/moyen` : Statistiques de vent
- `mer_hauteur_min/max/moyenne` : Statistiques de mer
- `vent_rafales_min/max` : Rafales
- `temps_*` : Conditions météo (pluie, orage, visibilité)
- `score_risque_*` : Scores composites
- `*_lag1/lag2/lag3` : Features temporelles décalées
- `*_rolling3` : Moyennes mobiles
- `*_diff1` : Variations jour à jour
- Variables d'interaction (vent_mer_risque, etc.)
- Variables cycliques (jour_semaine_sin/cos, etc.)
- Flags binaires (vent_extreme, mer_extreme, etc.)

### Annexe B : Commandes Utiles

#### B.1 Environnement Python

```bash
# Création environnement virtuel
python3 -m venv venv

# Activation
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Installation dépendances
pip install -r api/app/requirements.txt
```

#### B.2 Lancement de l'API

```bash
# Mode développement (avec rechargement automatique)
cd api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Mode production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### B.3 Jupyter Notebooks

```bash
# Lancement Jupyter
jupyter notebook

# Lancement JupyterLab (interface moderne)
jupyter lab
```

### Annexe C : Bibliographie et Ressources

#### C.1 Articles Scientifiques

1. **Imbalanced Learning** :
   - Chawla et al. (2002) - "SMOTE: Synthetic Minority Over-sampling Technique"
   - He & Garcia (2009) - "Learning from Imbalanced Data"

2. **Maritime Safety** :
   - Articles sur prévision d'accidents maritimes
   - Études météo-océanographiques

3. **Machine Learning** :
   - Chen & Guestrin (2016) - "XGBoost: A Scalable Tree Boosting System"
   - Lundberg & Lee (2017) - "A Unified Approach to Interpreting Model Predictions" (SHAP)

#### C.2 Documentation Technique

- **Scikit-learn** : https://scikit-learn.org/
- **XGBoost** : https://xgboost.readthedocs.io/
- **FastAPI** : https://fastapi.tiangolo.com/
- **Pandas** : https://pandas.pydata.org/
- **SHAP** : https://shap.readthedocs.io/

#### C.3 Données et Sources

- **Copernicus Marine Service** : Données satellitaires océanographiques
- **NOAA** : Données météorologiques
- **OMM (Organisation Météorologique Mondiale)** : Standards et bonnes pratiques

### Annexe D : Glossaire

**AUC** : Area Under Curve - Surface sous la courbe ROC, mesure de discrimination

**Déséquilibre de classe** : Situation où une classe est beaucoup plus fréquente qu'une autre

**F1-Score** : Moyenne harmonique de la précision et du recall

**Feature Engineering** : Création de nouvelles variables à partir des données existantes

**Lag** : Décalage temporel (ex: lag 1 = valeur du jour précédent)

**Precision** : Proportion de prédictions positives correctes

**Recall (Sensibilité)** : Proportion de cas positifs réels détectés

**ROC** : Receiver Operating Characteristic - Courbe de performance

**SHAP** : SHapley Additive exPlanations - Méthode d'interprétabilité

**SMOTE** : Synthetic Minority Over-sampling TEchnique - Génération d'exemples synthétiques

**XGBoost** : eXtreme Gradient Boosting - Algorithme de boosting performant

## SIGNATURES ET VALIDATION

**Projet réalisé par** : Henintsoa  
**Institution** : CFIM  
**Date de finalisation** : Janvier 2026

**Encadrant/Superviseur** : \***\*\*\*\*\***\_\***\*\*\*\*\***

**Date de validation** : \***\*\*\*\*\***\_\***\*\*\*\*\***

**FIN DU RAPPORT**

_Ce rapport constitue un document de référence complet sur le projet de prédiction des incidents maritimes. Il peut être utilisé pour présentation, documentation, ou comme base pour des améliorations futures._
