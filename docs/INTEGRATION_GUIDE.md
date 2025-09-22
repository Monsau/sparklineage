# 🔧 Integration Guide | Guide d'Intégration | Guía de Integración

*How to integrate automatic lineage tracking into your existing Spark environment*

---

## 🌍 Languages
- [🇫🇷 Français](#français)
- [🇬🇧 English](#english)  
- [🇪🇸 Español](#español)
- [🇸🇦 العربية](#العربية)

---

## 🇫🇷 Français

### 🎯 Intégration dans un Spark Existant

#### 1. **Ajouter les JARs nécessaires**

```bash
# Télécharger les JARs requis
wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.33/mysql-connector-java-8.0.33.jar
wget https://github.com/OpenLineage/OpenLineage/releases/download/1.13.1/openlineage-spark_2.12-1.13.1.jar
wget https://github.com/open-metadata/OpenMetadata/releases/download/1.0.0/openmetadata-spark-agent.jar
```

#### 2. **Configuration Spark pour Lineage Automatique**

**Option A: Via spark-submit**
```bash
spark-submit \
  --master yarn \
  --jars openmetadata-spark-agent.jar,mysql-connector-j-8.0.33.jar \
  --conf "spark.extraListeners=io.openlineage.spark.agent.OpenLineageSparkListener" \
  --conf "spark.openmetadata.transport.type=openMetadata" \
  --conf "spark.openmetadata.transport.hostPort=http://your-openmetadata:8585/api" \
  --conf "spark.openmetadata.transport.jwtToken=YOUR_JWT_TOKEN" \
  --conf "spark.openmetadata.transport.pipelineServiceName=your_pipeline_service" \
  your_spark_job.py
```

**Option B: Via spark-defaults.conf**
```properties
# /path/to/spark/conf/spark-defaults.conf
spark.jars                              /path/to/jars/openmetadata-spark-agent.jar,/path/to/jars/mysql-connector-j-8.0.33.jar
spark.extraListeners                    io.openlineage.spark.agent.OpenLineageSparkListener
spark.openmetadata.transport.type       openMetadata
spark.openmetadata.transport.hostPort   http://your-openmetadata:8585/api
spark.openmetadata.transport.jwtToken   YOUR_JWT_TOKEN
spark.openmetadata.transport.pipelineServiceName your_pipeline_service
```

**Option C: Dans votre code Spark**
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("YourAppWithLineage") \
    .config("spark.extraListeners", "io.openlineage.spark.agent.OpenLineageSparkListener") \
    .config("spark.openmetadata.transport.type", "openMetadata") \
    .config("spark.openmetadata.transport.hostPort", "http://your-openmetadata:8585/api") \
    .config("spark.openmetadata.transport.jwtToken", "YOUR_JWT_TOKEN") \
    .config("spark.openmetadata.transport.pipelineServiceName", "your_pipeline_service") \
    .getOrCreate()
```

#### 3. **Configuration OpenMetadata**

1. **Créer un Bot Token**
```bash
# Dans OpenMetadata UI
Settings → Bots → Add Bot → Generate JWT Token
```

2. **Configurer les Services de Données**
```bash
# Créer les services MySQL source et target
Settings → Services → Databases → Add MySQL Service
```

3. **Configurer le Pipeline Service**
```bash
# Créer le service pipeline
Settings → Services → Pipelines → Add Pipeline Service
```

#### 4. **Variables d'Environnement**

```bash
# Variables optionnelles pour simplifier la configuration
export OPENMETADATA_HOST="http://your-openmetadata:8585/api"
export OPENMETADATA_JWT_TOKEN="your_jwt_token"
export PIPELINE_SERVICE_NAME="your_pipeline_service"
```

#### 5. **Exemple d'Intégration Complète**

```python
# your_existing_job.py avec lineage automatique
from pyspark.sql import SparkSession
import os

def create_spark_session_with_lineage():
    """Créer une session Spark avec lineage automatique"""
    
    # Configuration OpenMetadata
    jwt_token = os.getenv('OPENMETADATA_JWT_TOKEN', 'your_default_token')
    openmetadata_host = os.getenv('OPENMETADATA_HOST', 'http://localhost:8585/api')
    pipeline_service = os.getenv('PIPELINE_SERVICE_NAME', 'spark_pipeline_service')
    
    # Chemins des JARs
    jar_path = "/path/to/your/jars"
    mysql_jar = f"{jar_path}/mysql-connector-j-8.0.33.jar"
    openmetadata_jar = f"{jar_path}/openmetadata-spark-agent.jar"
    
    return SparkSession.builder \
        .appName("ExistingJobWithLineage") \
        .config("spark.jars", f"{openmetadata_jar},{mysql_jar}") \
        .config("spark.extraListeners", "io.openlineage.spark.agent.OpenLineageSparkListener") \
        .config("spark.openmetadata.transport.type", "openMetadata") \
        .config("spark.openmetadata.transport.hostPort", openmetadata_host) \
        .config("spark.openmetadata.transport.jwtToken", jwt_token) \
        .config("spark.openmetadata.transport.pipelineServiceName", pipeline_service) \
        .config("spark.openmetadata.transport.pipelineName", "existing_etl_pipeline") \
        .getOrCreate()

# Votre code ETL existant
def your_existing_etl():
    spark = create_spark_session_with_lineage()
    
    # Vos transformations existantes - le lineage sera automatique !
    df_source = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:mysql://source:3306/database") \
        .option("dbtable", "your_table") \
        .option("user", "user") \
        .option("password", "password") \
        .load()
    
    # Transformations
    df_transformed = df_source.select("col1", "col2").filter("col1 > 10")
    
    # Écriture - lineage automatiquement capturé
    df_transformed.write \
        .format("jdbc") \
        .option("url", "jdbc:mysql://target:3306/database") \
        .option("dbtable", "target_table") \
        .option("user", "user") \
        .option("password", "password") \
        .mode("overwrite") \
        .save()
    
    spark.stop()

if __name__ == "__main__":
    your_existing_etl()
```

---

## 🇬🇧 English

### 🎯 Integration into Existing Spark

#### 1. **Add Required JARs**

```bash
# Download required JARs
wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.33/mysql-connector-java-8.0.33.jar
wget https://github.com/OpenLineage/OpenLineage/releases/download/1.13.1/openlineage-spark_2.12-1.13.1.jar
wget https://github.com/open-metadata/OpenMetadata/releases/download/1.0.0/openmetadata-spark-agent.jar
```

#### 2. **Spark Configuration for Automatic Lineage**

**Option A: Via spark-submit**
```bash
spark-submit \
  --master yarn \
  --jars openmetadata-spark-agent.jar,mysql-connector-j-8.0.33.jar \
  --conf "spark.extraListeners=io.openlineage.spark.agent.OpenLineageSparkListener" \
  --conf "spark.openmetadata.transport.type=openMetadata" \
  --conf "spark.openmetadata.transport.hostPort=http://your-openmetadata:8585/api" \
  --conf "spark.openmetadata.transport.jwtToken=YOUR_JWT_TOKEN" \
  --conf "spark.openmetadata.transport.pipelineServiceName=your_pipeline_service" \
  your_spark_job.py
```

**Option B: Via spark-defaults.conf**
```properties
# /path/to/spark/conf/spark-defaults.conf
spark.jars                              /path/to/jars/openmetadata-spark-agent.jar,/path/to/jars/mysql-connector-j-8.0.33.jar
spark.extraListeners                    io.openlineage.spark.agent.OpenLineageSparkListener
spark.openmetadata.transport.type       openMetadata
spark.openmetadata.transport.hostPort   http://your-openmetadata:8585/api
spark.openmetadata.transport.jwtToken   YOUR_JWT_TOKEN
spark.openmetadata.transport.pipelineServiceName your_pipeline_service
```

**Option C: In your Spark code**
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("YourAppWithLineage") \
    .config("spark.extraListeners", "io.openlineage.spark.agent.OpenLineageSparkListener") \
    .config("spark.openmetadata.transport.type", "openMetadata") \
    .config("spark.openmetadata.transport.hostPort", "http://your-openmetadata:8585/api") \
    .config("spark.openmetadata.transport.jwtToken", "YOUR_JWT_TOKEN") \
    .config("spark.openmetadata.transport.pipelineServiceName", "your_pipeline_service") \
    .getOrCreate()
```

---

## 🇪🇸 Español

### 🎯 Integración en Spark Existente

#### 1. **Agregar JARs Requeridos**

```bash
# Descargar JARs requeridos
wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.33/mysql-connector-java-8.0.33.jar
wget https://github.com/OpenLineage/OpenLineage/releases/download/1.13.1/openlineage-spark_2.12-1.13.1.jar
wget https://github.com/open-metadata/OpenMetadata/releases/download/1.0.0/openmetadata-spark-agent.jar
```

#### 2. **Configuración Spark para Linaje Automático**

**Opción A: Via spark-submit**
```bash
spark-submit \
  --master yarn \
  --jars openmetadata-spark-agent.jar,mysql-connector-j-8.0.33.jar \
  --conf "spark.extraListeners=io.openlineage.spark.agent.OpenLineageSparkListener" \
  --conf "spark.openmetadata.transport.type=openMetadata" \
  --conf "spark.openmetadata.transport.hostPort=http://your-openmetadata:8585/api" \
  --conf "spark.openmetadata.transport.jwtToken=YOUR_JWT_TOKEN" \
  --conf "spark.openmetadata.transport.pipelineServiceName=your_pipeline_service" \
  your_spark_job.py
```

---

## 🇸🇦 العربية

### 🎯 التكامل مع Spark الموجود

#### 1. **إضافة ملفات JAR المطلوبة**

```bash
# تحميل ملفات JAR المطلوبة
wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.33/mysql-connector-java-8.0.33.jar
wget https://github.com/OpenLineage/OpenLineage/releases/download/1.13.1/openlineage-spark_2.12-1.13.1.jar
wget https://github.com/open-metadata/OpenMetadata/releases/download/1.0.0/openmetadata-spark-agent.jar
```

#### 2. **تكوين Spark لتتبع النسب التلقائي**

**الخيار أ: عبر spark-submit**
```bash
spark-submit \
  --master yarn \
  --jars openmetadata-spark-agent.jar,mysql-connector-j-8.0.33.jar \
  --conf "spark.extraListeners=io.openlineage.spark.agent.OpenLineageSparkListener" \
  --conf "spark.openmetadata.transport.type=openMetadata" \
  --conf "spark.openmetadata.transport.hostPort=http://your-openmetadata:8585/api" \
  --conf "spark.openmetadata.transport.jwtToken=YOUR_JWT_TOKEN" \
  --conf "spark.openmetadata.transport.pipelineServiceName=your_pipeline_service" \
  your_spark_job.py
```

**الخيار ب: عبر spark-defaults.conf**
```properties
# /path/to/spark/conf/spark-defaults.conf
spark.jars                              /path/to/jars/openmetadata-spark-agent.jar,/path/to/jars/mysql-connector-j-8.0.33.jar
spark.extraListeners                    io.openlineage.spark.agent.OpenLineageSparkListener
spark.openmetadata.transport.type       openMetadata
spark.openmetadata.transport.hostPort   http://your-openmetadata:8585/api
spark.openmetadata.transport.jwtToken   YOUR_JWT_TOKEN
spark.openmetadata.transport.pipelineServiceName your_pipeline_service
```

**الخيار ج: في كود Spark الخاص بك**
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("YourAppWithLineage") \
    .config("spark.extraListeners", "io.openlineage.spark.agent.OpenLineageSparkListener") \
    .config("spark.openmetadata.transport.type", "openMetadata") \
    .config("spark.openmetadata.transport.hostPort", "http://your-openmetadata:8585/api") \
    .config("spark.openmetadata.transport.jwtToken", "YOUR_JWT_TOKEN") \
    .config("spark.openmetadata.transport.pipelineServiceName", "your_pipeline_service") \
    .getOrCreate()
```

#### 3. **تكوين OpenMetadata**

1. **إنشاء رمز Bot Token**
```bash
# في واجهة OpenMetadata
Settings → Bots → Add Bot → Generate JWT Token
```

2. **تكوين خدمات البيانات**
```bash
# إنشاء خدمات MySQL للمصدر والهدف
Settings → Services → Databases → Add MySQL Service
```

3. **تكوين خدمة Pipeline**
```bash
# إنشاء خدمة pipeline
Settings → Services → Pipelines → Add Pipeline Service
```

#### 4. **متغيرات البيئة**

```bash
# متغيرات اختيارية لتبسيط التكوين
export OPENMETADATA_HOST="http://your-openmetadata:8585/api"
export OPENMETADATA_JWT_TOKEN="your_jwt_token"
export PIPELINE_SERVICE_NAME="your_pipeline_service"
```

#### 5. **مثال على التكامل الكامل**

```python
# your_existing_job.py مع تتبع النسب التلقائي
from pyspark.sql import SparkSession
import os

def create_spark_session_with_lineage():
    """إنشاء جلسة Spark مع تتبع النسب التلقائي"""
    
    # تكوين OpenMetadata
    jwt_token = os.getenv('OPENMETADATA_JWT_TOKEN', 'your_default_token')
    openmetadata_host = os.getenv('OPENMETADATA_HOST', 'http://localhost:8585/api')
    pipeline_service = os.getenv('PIPELINE_SERVICE_NAME', 'spark_pipeline_service')
    
    # مسارات ملفات JAR
    jar_path = "/path/to/your/jars"
    mysql_jar = f"{jar_path}/mysql-connector-j-8.0.33.jar"
    openmetadata_jar = f"{jar_path}/openmetadata-spark-agent.jar"
    
    return SparkSession.builder \
        .appName("ExistingJobWithLineage") \
        .config("spark.jars", f"{openmetadata_jar},{mysql_jar}") \
        .config("spark.extraListeners", "io.openlineage.spark.agent.OpenLineageSparkListener") \
        .config("spark.openmetadata.transport.type", "openMetadata") \
        .config("spark.openmetadata.transport.hostPort", openmetadata_host) \
        .config("spark.openmetadata.transport.jwtToken", jwt_token) \
        .config("spark.openmetadata.transport.pipelineServiceName", pipeline_service) \
        .config("spark.openmetadata.transport.pipelineName", "existing_etl_pipeline") \
        .getOrCreate()

# كود ETL الموجود لديك
def your_existing_etl():
    spark = create_spark_session_with_lineage()
    
    # التحويلات الموجودة لديك - سيتم تتبع النسب تلقائياً!
    df_source = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:mysql://source:3306/database") \
        .option("dbtable", "your_table") \
        .option("user", "user") \
        .option("password", "password") \
        .load()
    
    # التحويلات
    df_transformed = df_source.select("col1", "col2").filter("col1 > 10")
    
    # الكتابة - يتم تسجيل النسب تلقائياً
    df_transformed.write \
        .format("jdbc") \
        .option("url", "jdbc:mysql://target:3306/database") \
        .option("dbtable", "target_table") \
        .option("user", "user") \
        .option("password", "password") \
        .mode("overwrite") \
        .save()
    
    spark.stop()

if __name__ == "__main__":
    your_existing_etl()
```

---

## 🔍 Troubleshooting | Dépannage | Solución de Problemas | استكشاف الأخطاء

### Erreurs Communes / Common Errors / Errores Comunes / الأخطاء الشائعة

**1. JWT Token Invalide / رمز JWT غير صالح**
```
Error: 401 Unauthorized - Token verification failed
Solution: Régénérer le token dans OpenMetadata UI / إعادة توليد الرمز في واجهة OpenMetadata
```

**2. JAR non trouvé / ملف JAR غير موجود**
```
Error: ClassNotFoundException: io.openlineage.spark.agent.OpenLineageSparkListener
Solution: Vérifier le chemin des JARs et les permissions / التحقق من مسار ملفات JAR والصلاحيات
```

**3. Connexion OpenMetadata / اتصال OpenMetadata**
```
Error: Connection refused to OpenMetadata
Solution: Vérifier que OpenMetadata est démarré et accessible / التحقق من تشغيل OpenMetadata وإمكانية الوصول إليه
```

## 📚 Resources | Ressources | Recursos

- [OpenMetadata Documentation](https://docs.open-metadata.org/)
- [OpenLineage Spark Integration](https://openlineage.io/docs/integrations/spark/)
- [Apache Spark Configuration](https://spark.apache.org/docs/latest/configuration.html)