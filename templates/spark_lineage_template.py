#!/usr/bin/env python3
"""
TEMPLATE CODE SPARK LINEAGE OPENMETADATA - VERSION MINIMALE FONCTIONNELLE
Extrait de l'implémentation réussie
"""

from pyspark.sql import SparkSession

# =================================================================
# CONFIGURATION SPARK POUR LINEAGE OPENMETADATA
# =================================================================

def create_spark_session_with_lineage(
    app_name="SparkLineageDemo",
    openmetadata_host="http://host.docker.internal:8585/api",
    jwt_token="YOUR_JWT_TOKEN_HERE",
    pipeline_service_name="spark_lineage_service", 
    pipeline_name="spark_lineage_pipeline"
):
    """
    Crée une session Spark configurée pour le lineage OpenMetadata
    
    Args:
        app_name: Nom de l'application Spark
        openmetadata_host: URL de l'API OpenMetadata  
        jwt_token: Token JWT pour l'authentification
        pipeline_service_name: Nom du service pipeline dans OpenMetadata
        pipeline_name: Nom du pipeline dans OpenMetadata
    
    Returns:
        SparkSession configurée pour le lineage
    """
    
    spark = (
        SparkSession.builder
        .master("local")
        .appName(app_name)
        
        # ✅ CRITIQUE: JARs obligatoires
        .config(
            "spark.jars",
            "/opt/bitnami/spark/ivy/openmetadata-spark-agent.jar,"
            "/opt/bitnami/spark/ivy/mysql-connector-j-8.0.33.jar"
        )
        
        # ✅ CRITIQUE: Listener OpenLineage pour capturer les événements
        .config(
            "spark.extraListeners",
            "io.openlineage.spark.agent.OpenLineageSparkListener"
        )
        
        # ✅ CRITIQUE: Transport OpenMetadata
        .config("spark.openmetadata.transport.type", "openmetadata")
        .config("spark.openmetadata.transport.hostPort", openmetadata_host)
        .config("spark.openmetadata.transport.jwtToken", jwt_token)
        
        # ✅ CRITIQUE: Configuration du pipeline
        .config("spark.openmetadata.transport.pipelineServiceName", pipeline_service_name)
        .config("spark.openmetadata.transport.pipelineName", pipeline_name)
        
        # ✅ Optionnel: Configuration additionnelle
        .config("spark.openmetadata.transport.timeout", "30")
        .config(
            "spark.openmetadata.transport.databaseServiceNames",
            "mysql-source-service,mysql-target-service"
        )
        
        .getOrCreate()
    )
    
    return spark

# =================================================================
# FONCTIONS ETL GÉNÉRATEURS DE LINEAGE
# =================================================================

def read_mysql_table(spark, host, port, database, table, user="root", password="password"):
    """
    Lit une table MySQL - GÉNÈRE AUTOMATIQUEMENT LE LINEAGE INPUT
    
    Args:
        spark: Session Spark
        host: Host MySQL
        port: Port MySQL  
        database: Nom de la base
        table: Nom de la table
        user: Utilisateur MySQL
        password: Mot de passe MySQL
    
    Returns:
        DataFrame Spark
    """
    
    df = (
        spark.read.format("jdbc")
        .option("url", f"jdbc:mysql://{host}:{port}/{database}")
        .option("dbtable", table)
        .option("user", user)
        .option("password", password)
        .option("driver", "com.mysql.cj.jdbc.Driver")
        .load()
    )
    
    print(f"✅ Table lue: {host}:{port}/{database}.{table}")
    return df

def write_mysql_table(df, host, port, database, table, mode="overwrite", user="root", password="password"):
    """
    Écrit une table MySQL - GÉNÈRE AUTOMATIQUEMENT LE LINEAGE OUTPUT
    
    Args:
        df: DataFrame à écrire
        host: Host MySQL
        port: Port MySQL
        database: Nom de la base
        table: Nom de la table
        mode: Mode d'écriture (overwrite, append, etc.)
        user: Utilisateur MySQL
        password: Mot de passe MySQL
    """
    
    (
        df.write.format("jdbc")
        .option("url", f"jdbc:mysql://{host}:{port}/{database}")
        .option("dbtable", table)
        .option("user", user)
        .option("password", password)
        .option("driver", "com.mysql.cj.jdbc.Driver")
        .mode(mode)
        .save()
    )
    
    print(f"✅ Table écrite: {host}:{port}/{database}.{table}")

# =================================================================
# PIPELINE ETL COMPLET AVEC LINEAGE
# =================================================================

def run_etl_pipeline_with_lineage():
    """
    Pipeline ETL complet qui génère automatiquement le lineage
    """
    
    print("=" * 60)
    print("🚀 Démarrage Pipeline ETL avec Lineage OpenMetadata")
    print("=" * 60)
    
    # ✅ Étape 1: Créer session Spark avec lineage
    spark = create_spark_session_with_lineage(
        app_name="ETLLineageDemo",
        openmetadata_host="http://host.docker.internal:8585/api",
        jwt_token="YOUR_ACTUAL_JWT_TOKEN",  # ⚠️ REMPLACER PAR VOTRE TOKEN
        pipeline_service_name="etl_lineage_service",
        pipeline_name="customers_etl_pipeline"
    )
    
    try:
        # ✅ Étape 2: Lecture source (génère INPUT lineage)
        print("\n📥 Lecture des données source...")
        source_df = read_mysql_table(
            spark=spark,
            host="mysql-source",
            port=3306,
            database="source_db", 
            table="customers"
        )
        
        print(f"   Nombre d'enregistrements: {source_df.count()}")
        
        # ✅ Étape 3: Transformations (génère PROCESSING lineage)
        print("\n🔄 Application des transformations...")
        
        # Exemple de transformations qui seront trackées
        transformed_df = (
            source_df
            .filter(source_df.country.isNotNull())  # Filtrage
            .select("customer_id", "customer_name", "email", "city", "country", "created_at")  # Sélection
            .withColumn("processed_at", spark.sql("SELECT current_timestamp()").collect()[0][0])  # Ajout colonne
        )
        
        print("   Transformations appliquées: filtrage + sélection + ajout colonne")
        
        # ✅ Étape 4: Écriture cible (génère OUTPUT lineage)
        print("\n💾 Écriture vers la cible...")
        write_mysql_table(
            df=transformed_df,
            host="mysql-target",
            port=3306,
            database="target_db",
            table="customers_copy",
            mode="overwrite"
        )
        
        # ✅ Étape 5: Vérification
        print("\n🔍 Vérification des données écrites...")
        verification_df = read_mysql_table(
            spark=spark,
            host="mysql-target", 
            port=3306,
            database="target_db",
            table="customers_copy"
        )
        
        print(f"   Nombre d'enregistrements écrits: {verification_df.count()}")
        
        print("\n✅ Pipeline ETL terminé avec succès!")
        print("🔗 Le lineage a été automatiquement généré par l'agent OpenMetadata")
        
    except Exception as e:
        print(f"❌ Erreur dans le pipeline: {e}")
        
    finally:
        print("\n🔄 Arrêt de la session Spark...")
        spark.stop()

# =================================================================
# CONFIGURATION ALTERNATIVE: TRANSPORT HTTP
# =================================================================

def create_spark_session_http_transport(
    app_name="SparkLineageHTTP",
    openmetadata_api_url="http://host.docker.internal:8585/api/v1/lineage",
    jwt_token="YOUR_JWT_TOKEN_HERE"
):
    """
    Version alternative avec transport HTTP direct
    """
    
    spark = (
        SparkSession.builder
        .master("local")
        .appName(app_name)
        .config("spark.jars", "/path/to/jars/openmetadata-spark-agent.jar,/path/to/jars/mysql-connector.jar")
        .config("spark.extraListeners", "io.openlineage.spark.agent.OpenLineageSparkListener")
        
        # Transport HTTP au lieu d'OpenMetadata
        .config("spark.openlineage.transport.type", "http")
        .config("spark.openlineage.transport.url", openmetadata_api_url)
        .config("spark.openlineage.transport.auth.type", "api_key")
        .config("spark.openlineage.transport.auth.apiKey", jwt_token)
        .config("spark.openlineage.namespace", "spark_demo")
        
        .getOrCreate()
    )
    
    return spark

# =================================================================
# SCRIPT PRINCIPAL
# =================================================================

if __name__ == "__main__":
    print("TEMPLATE CODE SPARK LINEAGE OPENMETADATA")
    print("=" * 50)
    print("Ce template contient:")
    print("1. ✅ Configuration Spark pour lineage OpenMetadata")
    print("2. ✅ Fonctions ETL générateurs de lineage")  
    print("3. ✅ Pipeline complet avec lecture → transformation → écriture")
    print("4. ✅ Configuration alternative transport HTTP")
    print("\nPour utiliser:")
    print("1. Remplacez YOUR_ACTUAL_JWT_TOKEN par votre token")
    print("2. Adaptez les hosts/ports à votre environnement")
    print("3. Exécutez: run_etl_pipeline_with_lineage()")
    
    # Décommentez pour exécuter:
    # run_etl_pipeline_with_lineage()