# 🧱 BlockchainIR4

Projet académique réalisé en 4ᵉ année à l’**ESAIP**, ayant pour objectif de **concevoir une blockchain en Python**.  
Ce programme illustre le fonctionnement d’une blockchain simple, avec gestion des transactions, des blocs et d’un mécanisme de **Proof of Work (PoW)**.

---

## 🚀 Fonctionnalités principales

Le programme permet de :

- ➕ **Ajouter une transaction** → `add(transaction)`
- ✅ **Vérifier une transaction** → `check(id_transaction)`
- 📜 **Afficher les 10 dernières transactions** → `show()`
- 🧩 **Altérer une transaction (tamper)** → `tamper(id_transaction)`
- 🔗 **Valider la blockchain** : un nouveau bloc est automatiquement créé toutes les 10 transactions

---

## ⚙️ Exécution en local

### 1️⃣ Prérequis

Assurez-vous d’avoir Python ≥ 3.8 et `pip` installés.

### 2️⃣ Installation des dépendances

```bash
pip install -U pycryptodome
````

> ⚠️ Si vous rencontrez l’erreur suivante :
>
> ```
> AttributeError: module 'time' has no attribute 'clock'
> ```
>
> alors :
>
> ```bash
> pip uninstall PyCrypto
> pip install -U PyCryptodome
> ```

### 3️⃣ Exécution du programme

```bash
python main.py
```

---

## 🐳 Exécution dans Docker (via GHCR)

Une image Docker est disponible sur le **GitHub Container Registry (GHCR)**.

### ▶️ Récupérer et exécuter l’image

```bash
docker pull ghcr.io/shaneosaure/blockchainir4:latest
docker run -it ghcr.io/shaneosaure/blockchainir4:latest
```

### 🏗️ Construire l’image en local (optionnel)

Si vous souhaitez builder l’image vous-même :

```bash
docker build -t ghcr.io/shaneosaure/blockchainir4:local .
docker run -it ghcr.io/shaneosaure/blockchainir4:local
```

---

## 🧩 Architecture technique

### Principales classes :

* **`Block`** → définit la structure d’un bloc et calcule son hash SHA-256
* **`Blockchain`** → gère la chaîne complète, les PoW et la validation
* **`Transaction`** → encapsule les transferts et signatures RSA

### Librairies utilisées :

* `hashlib` — calcul des hash SHA-256
* `datetime` — horodatage des blocs et transactions
* `json` — sérialisation des objets
* `pycryptodome` — génération et vérification des clés RSA

---

## 🧠 Exemple de menu

```text
--------------------------------------------------------------------
Bienvenue dans le programme Blockchain rédigé par :
Aymeric BOURDIN, Rémi JARDRET, Stéphane SIMON & Thomas PERRAULT
--------------------------------------------------------------------
 1. Créer une blockchain et 5 blocks
 2. Tester les transactions
 3. Détail de la Proof of Work
 4. Quitter
```

---

## 🧑‍💻 Auteurs

Projet réalisé par :

* [Aymeric BOURDIN](https://github.com/warzazate)
* [Rémi JARDRET](https://github.com/RemiESAIP)
* [Stéphane SIMON](https://github.com/Shaneosaure)
* [Thomas PERRAULT](https://github.com/BethGarion)

