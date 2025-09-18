#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=====================================================================
JOB SPARK COMPLEXE POUR LINEAGE MULTI-TABLES
=====================================================================
Ce script Spark crée un pipeline ETL complexe qui:
1. Lit plusieurs tables sources (customers, products, orders, order_items)
2. Effectue des transformations et agrégations
3. Écrit vers plusieurs tables target agrégées
4. Génère automatiquement le lineage OpenMetadata
"""

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

def create_spark_session():
    """Création de la session Spark avec configuration lineage"""
    
    # JWT Token pour OpenMetadata (à remplacer par un token valide)
    jwt_token = "eyJraWQiOiJHYjM4OWEtOWY3Ni1nZGpzLWE5MmotMDI0MmJrOTQzNTYiLCJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJvcGVuLW1ldGFkYXRhLm9yZyIsInN1YiI6ImluZ2VzdGlvbi1ib3QiLCJlbWFpbCI6ImluZ2VzdGlvbi1ib3RAb3Blbm1ldGFkYXRhLm9yZyIsImlzQm90Ijp0cnVlLCJ0b2tlblR5cGUiOiJCT1QiLCJpYXQiOjE3MjY2ODI4MDksImV4cCI6bnVsbH0.F67yNlDp7SIpJJTgCgXlvWWl2nqt_Q8gvAv3E-VBtGJKP1mAJ2sVs1YTmYHqwNHlm5P8_-AKj1X4Hpv_BpYU2EwF7nZP_QJ6vY2H3LW4Jp5_-vF9n_1pM8ZH_J4kF2WV7B"
    
    # Configuration des JARs
    jar_path = "/opt/spark/jars"
    mysql_jar = f"{jar_path}/mysql-connector-j-8.0.33.jar"
    openmetadata_jar = f"{jar_path}/openmetadata-spark-agent.jar"
    
    spark = SparkSession.builder \
        .appName("ComplexLineageETL") \
        .master("local[*]") \
        .config("spark.jars", f"{openmetadata_jar},{mysql_jar}") \
        .config("spark.extraListeners", "io.openlineage.spark.agent.OpenLineageSparkListener") \
        .config("spark.openmetadata.transport.type", "openmetadata") \
        .config("spark.openmetadata.transport.hostPort", "http://host.docker.internal:8585/api") \
        .config("spark.openmetadata.transport.jwtToken", jwt_token) \
        .config("spark.openmetadata.transport.pipelineServiceName", "spark_lineage_demo_service") \
        .config("spark.openmetadata.transport.pipelineName", "complex_etl_pipeline") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("INFO")
    return spark

def load_source_tables(spark):
    """Chargement de toutes les tables sources"""
    
    source_config = {
        "url": "jdbc:mysql://host.docker.internal:3308/source_db",
        "driver": "com.mysql.cj.jdbc.Driver",
        "user": "openmetadata_user",
        "password": "openmetadata_password"
    }
    
    # Lecture des tables sources
    customers_df = spark.read.format("jdbc") \
        .options(**source_config) \
        .option("dbtable", "customers") \
        .load()
    
    products_df = spark.read.format("jdbc") \
        .options(**source_config) \
        .option("dbtable", "products") \
        .load()
    
    orders_df = spark.read.format("jdbc") \
        .options(**source_config) \
        .option("dbtable", "orders") \
        .load()
    
    order_items_df = spark.read.format("jdbc") \
        .options(**source_config) \
        .option("dbtable", "order_items") \
        .load()
    
    print("✅ Tables sources chargées:")
    print(f"   - Customers: {customers_df.count()} lignes")
    print(f"   - Products: {products_df.count()} lignes")
    print(f"   - Orders: {orders_df.count()} lignes")
    print(f"   - Order Items: {order_items_df.count()} lignes")
    
    return customers_df, products_df, orders_df, order_items_df

def transform_customer_sales_summary(customers_df, orders_df, order_items_df, products_df):
    """Transformation 1: Résumé des ventes par client"""
    
    # Jointure des données de commandes
    order_details = orders_df.join(order_items_df, "order_id") \
        .join(products_df, "product_id")
    
    # Agrégation par client
    customer_summary = order_details.groupBy("customer_id") \
        .agg(
            count("order_id").alias("total_orders"),
            sum("total_amount").alias("total_amount"),
            avg("total_amount").alias("avg_order_value"),
            max("order_date").alias("last_order_date")
        )
    
    # Enrichissement avec les données client
    customer_sales_summary = customers_df.join(customer_summary, "customer_id") \
        .withColumn("customer_tier", 
            when(col("total_amount") > 1000, "Premium")
            .when(col("total_amount") > 500, "Gold")
            .otherwise("Standard")
        ) \
        .select(
            "customer_id", "customer_name", "email",
            "total_orders", "total_amount", "avg_order_value",
            "last_order_date", "customer_tier"
        )
    
    print(f"✅ Customer Sales Summary: {customer_sales_summary.count()} lignes")
    return customer_sales_summary

def transform_product_sales_summary(products_df, order_items_df):
    """Transformation 2: Résumé des ventes par produit"""
    
    # Agrégation des ventes par produit
    product_sales = order_items_df.groupBy("product_id") \
        .agg(
            sum("quantity").alias("total_sold"),
            sum(col("quantity") * col("unit_price")).alias("total_revenue"),
            avg("unit_price").alias("avg_price")
        )
    
    # Enrichissement avec les données produit
    product_sales_summary = products_df.join(product_sales, "product_id") \
        .withColumn("stock_status",
            when(col("stock_quantity") > 50, "High")
            .when(col("stock_quantity") > 20, "Medium")
            .otherwise("Low")
        ) \
        .select(
            "product_id", "product_name", "category",
            "total_sold", "total_revenue", "avg_price", "stock_status"
        )
    
    print(f"✅ Product Sales Summary: {product_sales_summary.count()} lignes")
    return product_sales_summary

def transform_business_metrics(customers_df, orders_df, order_items_df, products_df):
    """Transformation 3: Métriques business globales"""
    
    # Calculs de métriques
    total_customers = customers_df.count()
    total_orders = orders_df.count()
    total_revenue = order_items_df.agg(sum(col("quantity") * col("unit_price"))).collect()[0][0]
    avg_order_value = orders_df.agg(avg("total_amount")).collect()[0][0]
    
    # Top catégorie
    top_category = order_items_df.join(products_df, "product_id") \
        .groupBy("category") \
        .agg(sum(col("quantity") * col("unit_price")).alias("revenue")) \
        .orderBy(desc("revenue")) \
        .select("category") \
        .first()[0]
    
    # Top produit
    top_product = order_items_df.join(products_df, "product_id") \
        .groupBy("product_name") \
        .agg(sum("quantity").alias("qty_sold")) \
        .orderBy(desc("qty_sold")) \
        .select("product_name") \
        .first()[0]
    
    # Récupération de la session Spark depuis le contexte
    from pyspark.sql import SparkSession
    spark = SparkSession.getActiveSession()
    
    # Création du DataFrame métrique
    business_metrics = spark.createDataFrame([{
        "metric_date": "2024-01-19",
        "total_customers": total_customers,
        "total_orders": total_orders,
        "total_revenue": float(total_revenue),
        "avg_order_value": float(avg_order_value),
        "top_category": top_category,
        "top_product": top_product
    }])
    
    print(f"✅ Business Metrics: {business_metrics.count()} ligne")
    return business_metrics

def save_to_target(df, table_name):
    """Sauvegarde vers la base target"""
    
    target_config = {
        "url": "jdbc:mysql://host.docker.internal:3307/target_db",
        "driver": "com.mysql.cj.jdbc.Driver",
        "user": "openmetadata_user",
        "password": "openmetadata_password",
        "dbtable": table_name
    }
    
    df.write.format("jdbc") \
        .options(**target_config) \
        .mode("overwrite") \
        .save()
    
    print(f"✅ Table {table_name} sauvegardée")

def main():
    """Pipeline ETL principal"""
    
    print("🚀 DÉMARRAGE DU JOB SPARK COMPLEXE AVEC LINEAGE")
    print("=" * 60)
    
    # Création session Spark
    spark = create_spark_session()
    
    try:
        # 1. Chargement des tables sources
        print("\n📥 CHARGEMENT DES TABLES SOURCES")
        print("-" * 40)
        customers_df, products_df, orders_df, order_items_df = load_source_tables(spark)
        
        # 2. Transformations
        print("\n🔄 TRANSFORMATIONS ET AGRÉGATIONS")
        print("-" * 40)
        
        # Transformation 1: Customer Sales Summary
        customer_sales_summary = transform_customer_sales_summary(
            customers_df, orders_df, order_items_df, products_df
        )
        
        # Transformation 2: Product Sales Summary  
        product_sales_summary = transform_product_sales_summary(
            products_df, order_items_df
        )
        
        # Transformation 3: Business Metrics
        business_metrics = transform_business_metrics(
            customers_df, orders_df, order_items_df, products_df
        )
        
        # 3. Sauvegarde vers target
        print("\n📤 SAUVEGARDE VERS TARGET")
        print("-" * 40)
        
        save_to_target(customer_sales_summary, "customer_sales_summary")
        save_to_target(product_sales_summary, "product_sales_summary")
        save_to_target(business_metrics, "business_metrics")
        
        print("\n✅ JOB SPARK TERMINÉ AVEC SUCCÈS!")
        print("=" * 60)
        print("🔗 LINEAGE GÉNÉRÉ:")
        print("   📊 Sources: customers, products, orders, order_items")
        print("   🎯 Targets: customer_sales_summary, product_sales_summary, business_metrics")
        print("   🔄 Transformations: Jointures, agrégations, enrichissements")
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    main()