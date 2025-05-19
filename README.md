# 🧠 InsightImporter — Importateur de modèles InsightMaker vers MongoDB

### 👨‍💻 Développeur

- [Anli-Yach Mohamed](https://github.com/YashLeBg)

## 📌 Description

**InsightImporter** est une application de bureau en **Python** avec interface graphique **Tkinter**, conçue pour importer des modèles **InsightMaker** au format JSON dans une base de données **MongoDB Atlas**.
L’objectif est de faciliter la collecte, la gestion et la pérennisation de modèles dynamiques, notamment pour des projets d’analyse ou d’entraînement de modèles d’intelligence artificielle (IA).

## ⚙️ Fonctionnalités

* Interface de connexion à MongoDB Atlas (nom d'utilisateur, mot de passe, cluster, base).
* Sélection multiple de fichiers JSON.
* Importation automatique des données dans deux collections MongoDB :

  * `models` : métadonnées du modèle
  * `elements` : composants du modèle
* Affichage des fichiers sélectionnés.
* Gestion des erreurs lors de l’import.
* Suppression de fichiers sélectionnés ou de toute la liste.

## 🛠️ Technologies utilisées

* **Langage** : Python 3
* **Librairies** :

  * `tkinter` pour l’interface graphique
  * `pymongo` pour la connexion à MongoDB
  * `json` pour le traitement des fichiers

## 🚀 Installation et exécution

### ✅ Prérequis

* Python 3.x installé
* Un cluster MongoDB Atlas
* Fichiers JSON exportés depuis [InsightMaker](https://insightmaker.com/)
* Le fichier python `insightimporter.py` disponible dans le dépôt

### 🔧 Installation des dépendances

```bash
pip3 install pymongo
```

> 📦 `tkinter` est inclus avec la plupart des distributions Python.

### ▶️ Exécution

```bash
python3 insightimporter.py
```

> L'interface de connexion s'ouvrira pour saisir les identifiants MongoDB.


## 💡 Exemple de fichiers attendus

Le fichier JSON doit suivre le format généré par InsightMaker, contenant une structure similaire à :

```json
{
  "name": "Model_name",
  "engine": "Simulation",
  "simulation": {
    "algorithm": "...",
    "time_start": ...,
    "time_length": ...,
    "time_step": ...,
    "time_units": "..."
  },
  "elements": [
    {
      "type": "Stock",
      "name": "Average life service capital 1",
      "description": "Default average life of service sector capital",
      "behavior": {
        "value": 20,
        "units": "year"
      }
    }
  ]
}
```

## 🧪 Cas d’usage

* Archivage de masse de modèles InsightMaker.
* Création d’un jeu de données pour entraîner un modèle d’IA.
* Visualisation ou traitement ultérieur via MongoDB ou autres outils.

## 🔥 Défis rencontrés

* Connexion sécurisée à MongoDB Atlas.
* Gestion d’erreurs lors de l’importation.

## ✅ Améliorations futures

* Visualisation des données importées.
* Export vers d’autres formats (CSV, YAML…).
* Intégration avec des frameworks de machine learning (TensorFlow, PyTorch…).

## 📝 Licence
Projet réalisé dans le cadre d'un stage de développement web.
