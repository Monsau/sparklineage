#!/usr/bin/env python3
"""
OpenMetadata Spark Lineage Tutorial - Script Officiel
Suit exactement le tutoriel : https://docs.open-metadata.org/latest/connectors/ingestion/lineage/spark-lineage
"""

from pyspark.sql import SparkSession

# Configuration Spark selon le tutoriel officiel OpenMetadata
spark = (
    SparkSession.builder.master("local")
    .appName("localTestApp")
    .config(
        "spark.jars",
        "/opt/bitnami/spark/ivy/openmetadata-spark-agent.jar,/opt/bitnami/spark/ivy/mysql-connector-j-8.0.33.jar",
    )
    .config(
        "spark.extraListeners",
        "io.openlineage.spark.agent.OpenLineageSparkListener",
    )
    .config("spark.openmetadata.transport.hostPort", "http://host.docker.internal:8585/api")
    .config("spark.openmetadata.transport.type", "openmetadata")
    .config("spark.openmetadata.transport.jwtToken", "eyJraWQiOiJHYjM4OWEtOWY3Ni1nZGpzLWE5MmotMDI0MmJrOTQzNTYiLCJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJvcGVuLW1ldGFkYXRhLm9yZyIsInN1YiI6ImdlbmVyaWMtaW5nZXN0aW9uLWJvdCIsInJvbGVzIjpbXSwiZW1haWwiOiJnZW5lcmljLWluZ2VzdGlvbi1ib3RAdGFsZW50eXMuZXUiLCJpc0JvdCI6dHJ1ZSwidG9rZW5UeXBlIjoiQk9UIiwiaWF0IjoxNzU4MTM2NTI4LCJleHAiOm51bGx9.Hy4ed-YPdwKeZ71viL1G2JmQzo-gSdfa7MiKGj8ujgx4znEjuzFqRl15mhqsKjhSjnU-f6v_IV1Qe5kcxxaKScxq3HPPGF6snl2CgZBPXCu9QhSDQBLZO5FIY-vy8h9iLQXOYNoYj79-y7Xqu82O15vLpzHjh4_fOXJ59X0_oiq3NpIrv8eUv93K-nFqDwNPF00SwykEuoRcYNnhWueOy8e_MVkWv66kT74YKqS-iS-c6w18i0YXNnkUwt_RvzMf7-ZI6xuSV7A6xrWdFpC_2rIUJluBR2BWooLwDaA578KkjX8Rqe8VLA2vIBJlKw97Q1JY0a34lRGCiIk2HJBVHQ")
    .config(
        "spark.openmetadata.transport.pipelineServiceName", "spark_lineage_demo_service"
    )
    .config("spark.openmetadata.transport.pipelineName", "spark_lineage_demo_pipeline")
    .config(
        "spark.openmetadata.transport.pipelineSourceUrl",
        "http://localhost:8585/pipeline/spark_lineage_demo_pipeline",
    )
    .config(
        "spark.openmetadata.transport.pipelineDescription", "Demo Spark Lineage Pipeline suivant le tutoriel OpenMetadata"
    )
    .config(
        "spark.openmetadata.transport.databaseServiceNames",
        "mysql-source-service,mysql-target-service",
    )
    .config("spark.openmetadata.transport.timeout", "30")
    .getOrCreate()
)

print("=" * 60)
print("🚀 OpenMetadata Spark Lineage Tutorial - Script Officiel")
print("=" * 60)

try:
    # Lecture de la table source selon le tutoriel
    print("📥 Lecture des données depuis la table source...")
    
    employee_df = (
        spark.read.format("jdbc")
        .option("url", "jdbc:mysql://mysql-source:3306/source_db")
        .option("driver", "com.mysql.cj.jdbc.Driver")
        .option("dbtable", "customers")
        .option("user", "root")
        .option("password", "password")
        .load()
    )
    
    print(f"✅ Données chargées : {employee_df.count()} enregistrements")
    print("\n📋 Échantillon des données :")
    employee_df.show(5, truncate=False)
    
    # Écriture vers la table cible selon le tutoriel
    print("\n💾 Écriture des données vers la table cible...")
    
    (
        employee_df.write.format("jdbc")
        .option("url", "jdbc:mysql://mysql-target:3306/target_db")
        .option("driver", "com.mysql.cj.jdbc.Driver")
        .option("dbtable", "customers_copy")
        .option("user", "root")
        .option("password", "password")
        .mode("overwrite")
        .save()
    )
    
    print("✅ Données écrites avec succès !")
    
    # Vérification
    print("\n🔍 Vérification des données dans la table cible...")
    target_df = (
        spark.read.format("jdbc")
        .option("url", "jdbc:mysql://mysql-target:3306/target_db")
        .option("driver", "com.mysql.cj.jdbc.Driver")
        .option("dbtable", "customers_copy")
        .option("user", "root")
        .option("password", "password")
        .load()
    )
    
    print(f"✅ Vérification réussie : {target_df.count()} enregistrements dans la table cible")
    
    print("\n🎯 Pipeline terminé avec succès !")
    print("   Vérifiez dans OpenMetadata :")
    print("   - Service Pipeline : spark_lineage_demo_service")
    print("   - Pipeline : spark_lineage_demo_pipeline")
    print("   - Lineage : customers → customers_copy")
    
    print("\n" + "=" * 60)
    print("✅ Tutorial OpenMetadata Spark Lineage Terminé avec Succès !")
    print("=" * 60)

except Exception as e:
    print(f"❌ Erreur : {str(e)}")
    raise

finally:
    # Arrêt de la session Spark
    print("\n🔄 Arrêt de la session Spark...")
    spark.stop()