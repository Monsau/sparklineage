# Guide de Configuration des Services MySQL dans OpenMetadata

## 🎯 Objectif
Créer les services de base de données MySQL dans OpenMetadata pour que le lineage Spark puisse être correctement affiché.

## 📋 Services à créer

### 1. Service MySQL Source
- **Nom**: `mysql-source-service`
- **Host**: `host.docker.internal`
- **Port**: `3308`
- **Utilisateur**: `root`
- **Mot de passe**: `password`
- **Base de données**: `source_db`
- **Tables**: `customers`, `orders`

### 2. Service MySQL Target  
- **Nom**: `mysql-target-service`
- **Host**: `host.docker.internal`
- **Port**: `3307`
- **Utilisateur**: `root`
- **Mot de passe**: `password`
- **Base de données**: `target_db`
- **Tables**: `customer_summary`, `order_analytics`

## 🌐 Étapes via l'interface web

1. **Ouvrir OpenMetadata**: http://localhost:8585

2. **Se connecter** (si nécessaire):
   - Email: `admin@open-metadata.org`
   - Mot de passe: `admin`

3. **Créer le service Source**:
   - Aller dans "Settings" > "Services" > "Databases"
   - Cliquer "Add New Service"
   - Sélectionner "MySQL"
   - Configuration:
     ```
     Service Name: mysql-source-service
     Host and Port: host.docker.internal:3308
     Username: root
     Password: password
     Database: source_db
     ```

4. **Créer le service Target**:
   - Répéter pour le service target avec le port 3307 et target_db
   - Configuration:
     ```
     Service Name: mysql-target-service
     Host and Port: host.docker.internal:3307
     Username: root
     Password: password
     Database: target_db
     ```

5. **Lancer l'ingestion**:
   - Pour chaque service, configurer un pipeline d'ingestion
   - Cela va découvrir automatiquement les tables

## 🔗 Correspondance avec OpenLineage

Les événements OpenLineage utilisent ces URLs:
- Source: `mysql://mysql-source:3306` → Doit correspondre au service créé
- Target: `mysql://mysql-target:3306` → Doit correspondre au service créé

## ✅ Vérification

Après création des services:
1. Vérifier que les tables sont découvertes
2. Exécuter le pipeline Spark avec OpenLineage
3. Vérifier le lineage dans "Data Lineage"

## 📝 Notes

- Les ports dans Docker (3308/3307) correspondent aux services MySQL
- OpenLineage utilise les noms des conteneurs (mysql-source/mysql-target)
- Le mapping se fait automatiquement si les noms correspondent