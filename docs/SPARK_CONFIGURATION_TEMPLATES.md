# ⚙️ Spark Configuration Templates | Modèles de Configuration

*Ready-to-use configuration templates for different Spark deployment scenarios*

---

## 📋 Table of Contents

1. [Standalone Spark](#standalone-spark)
2. [YARN Cluster](#yarn-cluster)
3. [Kubernetes](#kubernetes)
4. [EMR/Databricks](#emrdatabricks)
5. [Docker Compose](#docker-compose)

---

## 🔧 Standalone Spark

### spark-defaults.conf
```properties
# Basic Spark Configuration with OpenMetadata Lineage
spark.master                            spark://spark-master:7077
spark.eventLog.enabled                  true
spark.eventLog.dir                      /opt/spark/logs
spark.history.fs.logDirectory           /opt/spark/logs

# OpenMetadata Lineage Configuration
spark.jars                              /opt/spark/jars/openmetadata-spark-agent.jar,/opt/spark/jars/mysql-connector-j-8.0.33.jar
spark.extraListeners                    io.openlineage.spark.agent.OpenLineageSparkListener
spark.openmetadata.transport.type       openMetadata
spark.openmetadata.transport.hostPort   http://openmetadata:8585/api
spark.openmetadata.transport.jwtToken   ${OPENMETADATA_JWT_TOKEN}
spark.openmetadata.transport.pipelineServiceName spark_pipeline_service

# Database Configuration
spark.sql.adaptive.enabled              true
spark.sql.adaptive.coalescePartitions.enabled true
```

### spark-submit Command
```bash
#!/bin/bash
# standalone-submit.sh

export OPENMETADATA_JWT_TOKEN="your_jwt_token_here"

spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  --driver-memory 2g \
  --executor-memory 4g \
  --executor-cores 2 \
  --num-executors 3 \
  --jars /opt/spark/jars/openmetadata-spark-agent.jar,/opt/spark/jars/mysql-connector-j-8.0.33.jar \
  --conf "spark.extraListeners=io.openlineage.spark.agent.OpenLineageSparkListener" \
  --conf "spark.openmetadata.transport.type=openMetadata" \
  --conf "spark.openmetadata.transport.hostPort=http://openmetadata:8585/api" \
  --conf "spark.openmetadata.transport.jwtToken=${OPENMETADATA_JWT_TOKEN}" \
  --conf "spark.openmetadata.transport.pipelineServiceName=spark_pipeline_service" \
  --conf "spark.openmetadata.transport.pipelineName=my_etl_pipeline" \
  your_spark_job.py
```

---

## 🏗️ YARN Cluster

### yarn-site.xml Addition
```xml
<!-- Add to existing yarn-site.xml -->
<configuration>
  <!-- Existing YARN configuration -->
  
  <!-- Spark History Server for Lineage -->
  <property>
    <name>yarn.timeline-service.enabled</name>
    <value>true</value>
  </property>
  
  <property>
    <name>yarn.timeline-service.hostname</name>
    <value>yarn-timeline-server</value>
  </property>
</configuration>
```

### YARN spark-submit
```bash
#!/bin/bash
# yarn-submit.sh

export OPENMETADATA_JWT_TOKEN="your_jwt_token_here"

spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --driver-memory 4g \
  --executor-memory 8g \
  --executor-cores 4 \
  --num-executors 10 \
  --queue production \
  --files /etc/spark/conf/hive-site.xml \
  --jars hdfs://namenode:9000/jars/openmetadata-spark-agent.jar,hdfs://namenode:9000/jars/mysql-connector-j-8.0.33.jar \
  --conf "spark.extraListeners=io.openlineage.spark.agent.OpenLineageSparkListener" \
  --conf "spark.openmetadata.transport.type=openMetadata" \
  --conf "spark.openmetadata.transport.hostPort=http://openmetadata.company.com:8585/api" \
  --conf "spark.openmetadata.transport.jwtToken=${OPENMETADATA_JWT_TOKEN}" \
  --conf "spark.openmetadata.transport.pipelineServiceName=production_pipeline_service" \
  --conf "spark.openmetadata.transport.pipelineName=daily_etl" \
  --conf "spark.yarn.appMasterEnv.OPENMETADATA_JWT_TOKEN=${OPENMETADATA_JWT_TOKEN}" \
  --conf "spark.executorEnv.OPENMETADATA_JWT_TOKEN=${OPENMETADATA_JWT_TOKEN}" \
  hdfs://namenode:9000/jobs/your_spark_job.py
```

---

## ☸️ Kubernetes

### spark-operator.yaml
```yaml
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata:
  name: spark-lineage-job
  namespace: spark-jobs
spec:
  type: Python
  pythonVersion: "3"
  mode: cluster
  image: "bitnami/spark:3.5.0"
  imagePullPolicy: Always
  mainApplicationFile: "local:///opt/spark/jobs/your_spark_job.py"
  
  sparkConf:
    "spark.extraListeners": "io.openlineage.spark.agent.OpenLineageSparkListener"
    "spark.openmetadata.transport.type": "openMetadata"
    "spark.openmetadata.transport.hostPort": "http://openmetadata.default.svc.cluster.local:8585/api"
    "spark.openmetadata.transport.jwtToken": "${OPENMETADATA_JWT_TOKEN}"
    "spark.openmetadata.transport.pipelineServiceName": "k8s_pipeline_service"
    "spark.openmetadata.transport.pipelineName": "k8s_etl_job"
    
  deps:
    jars:
      - "local:///opt/spark/jars/openmetadata-spark-agent.jar"
      - "local:///opt/spark/jars/mysql-connector-j-8.0.33.jar"
      
  driver:
    cores: 1
    memory: "2g"
    labels:
      version: 3.5.0
    serviceAccount: spark-driver
    env:
      - name: OPENMETADATA_JWT_TOKEN
        valueFrom:
          secretKeyRef:
            name: openmetadata-secrets
            key: jwt-token
            
  executor:
    cores: 2
    instances: 3
    memory: "4g"
    labels:
      version: 3.5.0
    env:
      - name: OPENMETADATA_JWT_TOKEN
        valueFrom:
          secretKeyRef:
            name: openmetadata-secrets
            key: jwt-token

  restartPolicy:
    type: OnFailure
    onFailureRetries: 2
    onFailureRetryInterval: 10
    onSubmissionFailureRetries: 1
    onSubmissionFailureRetryInterval: 20
```

### Kubernetes Secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: openmetadata-secrets
  namespace: spark-jobs
type: Opaque
data:
  jwt-token: <base64-encoded-jwt-token>
```

---

## 🌩️ EMR/Databricks

### EMR Bootstrap Script
```bash
#!/bin/bash
# emr-bootstrap.sh

# Download JARs to EMR cluster
aws s3 cp s3://your-bucket/jars/openmetadata-spark-agent.jar /usr/lib/spark/jars/
aws s3 cp s3://your-bucket/jars/mysql-connector-j-8.0.33.jar /usr/lib/spark/jars/

# Set permissions
chmod 644 /usr/lib/spark/jars/openmetadata-spark-agent.jar
chmod 644 /usr/lib/spark/jars/mysql-connector-j-8.0.33.jar

# Add to Spark defaults
cat >> /etc/spark/conf/spark-defaults.conf << EOF
spark.extraListeners                    io.openlineage.spark.agent.OpenLineageSparkListener
spark.openmetadata.transport.type       openMetadata
spark.openmetadata.transport.hostPort   https://your-openmetadata.amazonaws.com/api
spark.openmetadata.transport.jwtToken   \${OPENMETADATA_JWT_TOKEN}
spark.openmetadata.transport.pipelineServiceName emr_pipeline_service
EOF
```

### Databricks Init Script
```bash
#!/bin/bash
# databricks-init.sh

# Create jars directory
mkdir -p /databricks/jars

# Download JARs
wget -O /databricks/jars/openmetadata-spark-agent.jar \
  https://github.com/open-metadata/OpenMetadata/releases/download/1.0.0/openmetadata-spark-agent.jar

wget -O /databricks/jars/mysql-connector-j-8.0.33.jar \
  https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.33/mysql-connector-java-8.0.33.jar

# Set permissions
chmod 644 /databricks/jars/*.jar
```

### Databricks Cluster Configuration
```json
{
  "spark_conf": {
    "spark.jars": "/databricks/jars/openmetadata-spark-agent.jar,/databricks/jars/mysql-connector-j-8.0.33.jar",
    "spark.extraListeners": "io.openlineage.spark.agent.OpenLineageSparkListener",
    "spark.openmetadata.transport.type": "openMetadata",
    "spark.openmetadata.transport.hostPort": "https://your-openmetadata.com/api",
    "spark.openmetadata.transport.jwtToken": "{{secrets/openmetadata/jwt-token}}",
    "spark.openmetadata.transport.pipelineServiceName": "databricks_pipeline_service"
  },
  "spark_env_vars": {
    "OPENMETADATA_JWT_TOKEN": "{{secrets/openmetadata/jwt-token}}"
  }
}
```

---

## 🐳 Docker Compose

### docker-compose.yml Extension
```yaml
version: '3.8'

services:
  # Your existing services...
  
  spark-master:
    image: bitnami/spark:3.5.0
    environment:
      - SPARK_MODE=master
      - SPARK_MASTER_PORT=7077
      - SPARK_MASTER_WEBUI_PORT=8080
      - OPENMETADATA_JWT_TOKEN=${OPENMETADATA_JWT_TOKEN}
    ports:
      - "8080:8080"
      - "7077:7077"
    volumes:
      - ./jars:/opt/bitnami/spark/jars
      - ./jobs:/opt/bitnami/spark/jobs
      - ./conf/spark-defaults.conf:/opt/bitnami/spark/conf/spark-defaults.conf
    networks:
      - spark-network

  spark-worker:
    image: bitnami/spark:3.5.0
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
      - SPARK_WORKER_MEMORY=4g
      - SPARK_WORKER_CORES=2
      - OPENMETADATA_JWT_TOKEN=${OPENMETADATA_JWT_TOKEN}
    depends_on:
      - spark-master
    volumes:
      - ./jars:/opt/bitnami/spark/jars
      - ./jobs:/opt/bitnami/spark/jobs
      - ./conf/spark-defaults.conf:/opt/bitnami/spark/conf/spark-defaults.conf
    networks:
      - spark-network

networks:
  spark-network:
    driver: bridge
```

### Environment Variables (.env)
```bash
# .env file for Docker Compose
OPENMETADATA_JWT_TOKEN=your_jwt_token_here
SPARK_MASTER_URL=spark://spark-master:7077
OPENMETADATA_HOST=http://openmetadata:8585/api
PIPELINE_SERVICE_NAME=docker_pipeline_service
```

---

## 🔍 Configuration Validation

### Test Script
```python
# test_lineage_config.py
from pyspark.sql import SparkSession
import os

def test_lineage_configuration():
    """Test if OpenMetadata lineage is properly configured"""
    
    try:
        spark = SparkSession.builder \
            .appName("LineageConfigTest") \
            .getOrCreate()
        
        # Check if OpenLineage listener is registered
        listeners = spark.sparkContext.getConf().get("spark.extraListeners", "")
        
        if "OpenLineageSparkListener" in listeners:
            print("✅ OpenLineage listener is configured")
        else:
            print("❌ OpenLineage listener is NOT configured")
            
        # Check OpenMetadata configuration
        transport_type = spark.sparkContext.getConf().get("spark.openmetadata.transport.type", "")
        host_port = spark.sparkContext.getConf().get("spark.openmetadata.transport.hostPort", "")
        jwt_token = spark.sparkContext.getConf().get("spark.openmetadata.transport.jwtToken", "")
        
        if transport_type == "openMetadata":
            print("✅ OpenMetadata transport is configured")
        else:
            print("❌ OpenMetadata transport is NOT configured")
            
        if host_port:
            print(f"✅ OpenMetadata host: {host_port}")
        else:
            print("❌ OpenMetadata host is NOT configured")
            
        if jwt_token and jwt_token != "":
            print("✅ JWT token is configured")
        else:
            print("❌ JWT token is NOT configured")
            
        spark.stop()
        
    except Exception as e:
        print(f"❌ Error testing configuration: {e}")

if __name__ == "__main__":
    test_lineage_configuration()
```

### Run Test
```bash
# Test your configuration
spark-submit test_lineage_config.py
```

---

## 📝 Notes

- **JWT Token**: Always use environment variables or secrets management for JWT tokens
- **JAR Paths**: Ensure JARs are accessible from all cluster nodes
- **Network**: Verify OpenMetadata is reachable from Spark executors
- **Permissions**: Check file permissions for JAR files
- **Versions**: Match Spark version with OpenLineage agent version