# =====================================================================
# GUIDE COMPLET : CODE ESSENTIEL LINEAGE SPARK OPENMETADATA
# =====================================================================

## 🎯 OBJECTIF
Ce guide identifie exactement le code minimal nécessaire pour implémenter 
le lineage Spark avec OpenMetadata, basé sur notre implémentation réussie.

## 📁 STRUCTURE DES FICHIERS FOURNIS

```
templates/
├── docker-compose-lineage.yml     # Infrastructure Docker minimale
├── spark_lineage_template.py      # Code Spark avec lineage  
├── setup_lineage_environment.py   # Script de setup automatique
└── README-guide.md                # Ce guide
```

## 🔧 COMPOSANTS CRITIQUES IDENTIFIÉS

### 1. INFRASTRUCTURE DOCKER OBLIGATOIRE

**Services essentiels dans docker-compose.yml :**
- ✅ `openmetadata-server:1.9.7` - Service principal
- ✅ `postgresql` - Base métadata OpenMetadata  
- ✅ `elasticsearch:8.10.2` - Indexation/recherche (OBLIGATOIRE)
- ✅ `mysql-source` et `mysql-target` - Bases de données
- ✅ `spark-master:3.5.0` - Cluster Spark

### 2. JARS CRITIQUES REQUIS

**Fichiers JAR obligatoires :**
```bash
# À télécharger et placer dans ./jars/
openmetadata-spark-agent-1.0.jar    # Agent principal lineage
mysql-connector-j-8.0.33.jar        # Driver JDBC MySQL
```

**Source officielle JAR :**
```
https://github.com/open-metadata/openmetadata-spark-agent/releases/download/1.0/openmetadata-spark-agent-1.0.jar
```

### 3. CONFIGURATION SPARK MINIMALE

**Code Spark essentiel :**
```python
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .master("local")
    .appName("SparkLineageDemo")
    
    # ✅ CRITIQUE: JARs obligatoires
    .config("spark.jars", "/path/openmetadata-spark-agent.jar,/path/mysql-connector.jar")
    
    # ✅ CRITIQUE: Listener OpenLineage
    .config("spark.extraListeners", "io.openlineage.spark.agent.OpenLineageSparkListener")
    
    # ✅ CRITIQUE: Transport OpenMetadata
    .config("spark.openmetadata.transport.type", "openmetadata")
    .config("spark.openmetadata.transport.hostPort", "http://localhost:8585/api")
    .config("spark.openmetadata.transport.jwtToken", "YOUR_JWT_TOKEN")
    
    # ✅ CRITIQUE: Configuration pipeline
    .config("spark.openmetadata.transport.pipelineServiceName", "your_service")
    .config("spark.openmetadata.transport.pipelineName", "your_pipeline")
    
    .getOrCreate()
)
```

### 4. CODE ETL GÉNÉRATEUR DE LINEAGE

**Opérations qui génèrent automatiquement le lineage :**
```python
# LECTURE (génère INPUT lineage)
source_df = spark.read.format("jdbc").option("url", "jdbc:mysql://...").load()

# TRANSFORMATIONS (génère PROCESSING lineage)  
transformed_df = source_df.select("*").filter(...)

# ÉCRITURE (génère OUTPUT lineage)
transformed_df.write.format("jdbc").option("url", "jdbc:mysql://...").save()
```

## 🚀 UTILISATION DES TEMPLATES

### ÉTAPE 1: Setup de l'infrastructure
```bash
# 1. Copier docker-compose-lineage.yml vers votre projet
cp templates/docker-compose-lineage.yml ./docker-compose.yml

# 2. Démarrer l'infrastructure
docker-compose up -d

# 3. Attendre que OpenMetadata soit accessible
# Vérifier: http://localhost:8585
```

### ÉTAPE 2: Setup automatique des services
```bash
# 1. Modifier le JWT_TOKEN dans setup_lineage_environment.py
# 2. Exécuter le setup automatique
python templates/setup_lineage_environment.py
```

### ÉTAPE 3: Exécution du lineage Spark
```bash
# 1. Modifier YOUR_ACTUAL_JWT_TOKEN dans spark_lineage_template.py
# 2. Adapter les configurations host/port si nécessaire
# 3. Exécuter le script Spark
python templates/spark_lineage_template.py
```

## 🔍 POINTS CRITIQUES POUR LE SUCCÈS

### ✅ Configuration obligatoire
1. **JAR Agent** : `openmetadata-spark-agent-1.0.jar` version exacte
2. **Listener** : `io.openlineage.spark.agent.OpenLineageSparkListener`
3. **Transport** : `type=openmetadata` + `hostPort` + `jwtToken`
4. **Services** : Database services créés dans OpenMetadata
5. **Tables** : Découvertes via ingestion metadata

### ⚠️ Pièges courants évités
1. **Version JAR** : Utiliser exactement la version 1.0 de l'agent
2. **Network** : Host `host.docker.internal` dans Docker
3. **Driver JDBC** : Spécifier `com.mysql.cj.jdbc.Driver`
4. **FQN Tables** : Format `service.database.schema.table`
5. **JWT Token** : Token valide avec permissions appropriées

### 🔧 Configuration réseau Docker
```yaml
# Dans docker-compose.yml
networks:
  app_net:
    driver: bridge

# Tous les services doivent être sur le même réseau
services:
  service_name:
    networks:
      - app_net
```

## 📊 VÉRIFICATION DU SUCCÈS

### Logs Spark à rechercher :
```
✅ "Registered listener io.openlineage.spark.agent.OpenLineageSparkListener"
✅ "Emitting lineage completed successfully with run id"
✅ "OpenMetadataTransport: ES fieldQuery REQUEST"
```

### Interface OpenMetadata :
1. **Services** → Pipeline Services → Votre service pipeline
2. **Pipelines** → Votre pipeline → Onglet Lineage
3. **Tables** → mysql-source-service → customers → Onglet Lineage
4. **Tables** → mysql-target-service → customers_copy → Onglet Lineage

## 🎯 RÉSUMÉ EXÉCUTIF

**Le lineage Spark OpenMetadata nécessite exactement :**

1. **Infrastructure** : OpenMetadata + ElasticSearch + MySQL + Spark
2. **Agent** : `openmetadata-spark-agent-1.0.jar`
3. **Configuration** : Listener + Transport + JWT Token
4. **Services** : Database services créés dans OpenMetadata
5. **ETL** : Opérations Spark JDBC (read/write)

**Le lineage est généré automatiquement** quand ces composants sont correctement configurés.

**En cas d'échec**, le lineage peut être créé manuellement via l'API OpenMetadata comme solution de fallback.

## 📞 SUPPORT

Ce guide est basé sur une implémentation réussie et testée.
Tous les templates fournis contiennent le code exact qui fonctionne.

Pour toute question, référez-vous aux scripts de diagnostic inclus
qui permettent de vérifier chaque composant individuellement.