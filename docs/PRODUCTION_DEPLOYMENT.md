# 🏗️ Production Deployment Guide | Guide de Déploiement Production

*Best practices for deploying OpenMetadata lineage in production environments*

---

## 🎯 Production Checklist

### ✅ Security
- [ ] JWT tokens stored in secrets management (Vault, K8s secrets, etc.)
- [ ] HTTPS enabled for OpenMetadata communication
- [ ] Network segmentation and firewall rules configured
- [ ] Service accounts with minimal permissions
- [ ] Audit logging enabled

### ✅ Performance
- [ ] JAR files distributed on all cluster nodes
- [ ] Connection pooling configured
- [ ] Lineage batching optimized
- [ ] Memory allocation tuned for lineage overhead

### ✅ Reliability
- [ ] Health checks implemented
- [ ] Retry mechanisms configured
- [ ] Circuit breakers for OpenMetadata connectivity
- [ ] Graceful degradation when lineage is unavailable

### ✅ Monitoring
- [ ] Lineage capture metrics
- [ ] OpenMetadata connectivity monitoring
- [ ] Job performance impact assessment
- [ ] Error rate tracking

---

## 🔐 Security Best Practices

### 1. JWT Token Management

**Kubernetes Secrets**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: openmetadata-credentials
  namespace: production
type: Opaque
stringData:
  jwt-token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  api-endpoint: "https://openmetadata.company.com/api"
```

**HashiCorp Vault Integration**
```python
import hvac

def get_openmetadata_token():
    """Retrieve JWT token from Vault"""
    client = hvac.Client(url='https://vault.company.com')
    client.token = os.environ['VAULT_TOKEN']
    
    secret = client.secrets.kv.v2.read_secret_version(
        path='openmetadata/production'
    )
    
    return secret['data']['data']['jwt_token']
```

### 2. Network Security

**Firewall Rules Example**
```bash
# Allow Spark cluster to OpenMetadata
iptables -A OUTPUT -p tcp --dport 8585 -d openmetadata.company.com -j ACCEPT

# Allow OpenMetadata to databases for validation
iptables -A OUTPUT -p tcp --dport 3306 -d mysql.company.com -j ACCEPT
```

**TLS Configuration**
```properties
# spark-defaults.conf with TLS
spark.openmetadata.transport.hostPort    https://openmetadata.company.com/api
spark.openmetadata.transport.sslEnabled  true
spark.openmetadata.transport.trustStore  /etc/ssl/certs/company-truststore.jks
spark.openmetadata.transport.trustStorePassword ${TRUSTSTORE_PASSWORD}
```

---

## ⚡ Performance Optimization

### 1. JAR Distribution Strategy

**Pre-distribute on HDFS (for YARN)**
```bash
# Upload JARs to HDFS for cluster-wide access
hdfs dfs -mkdir /shared/spark/jars
hdfs dfs -put openmetadata-spark-agent.jar /shared/spark/jars/
hdfs dfs -put mysql-connector-j-8.0.33.jar /shared/spark/jars/

# Reference in spark-submit
--jars hdfs://namenode:9000/shared/spark/jars/openmetadata-spark-agent.jar,hdfs://namenode:9000/shared/spark/jars/mysql-connector-j-8.0.33.jar
```

**Pre-install on all nodes**
```bash
# Ansible playbook example
- name: Install OpenMetadata JARs on all Spark nodes
  copy:
    src: "{{ item }}"
    dest: /opt/spark/jars/
    mode: '0644'
  with_items:
    - openmetadata-spark-agent.jar
    - mysql-connector-j-8.0.33.jar
  when: inventory_hostname in groups['spark_nodes']
```

### 2. Connection Pooling

```python
# Enhanced Spark session with connection pooling
from pyspark.sql import SparkSession

def create_optimized_spark_session():
    return SparkSession.builder \
        .appName("ProductionETLWithLineage") \
        .config("spark.extraListeners", "io.openlineage.spark.agent.OpenLineageSparkListener") \
        .config("spark.openmetadata.transport.type", "openMetadata") \
        .config("spark.openmetadata.transport.hostPort", "https://openmetadata.company.com/api") \
        .config("spark.openmetadata.transport.jwtToken", get_jwt_token()) \
        .config("spark.openmetadata.transport.pipelineServiceName", "production_pipeline_service") \
        .config("spark.openmetadata.transport.connectionPoolSize", "10") \
        .config("spark.openmetadata.transport.connectionTimeout", "30000") \
        .config("spark.openmetadata.transport.readTimeout", "60000") \
        .config("spark.openmetadata.transport.retryAttempts", "3") \
        .config("spark.openmetadata.transport.retryDelay", "5000") \
        .getOrCreate()
```

### 3. Memory Allocation

```properties
# Optimized memory settings with lineage overhead
spark.driver.memory                     8g
spark.driver.memoryFraction             0.8
spark.executor.memory                   16g
spark.executor.memoryFraction           0.8

# Reserve memory for lineage processing
spark.executor.memoryOverhead           2g
spark.driver.memoryOverhead             1g

# Optimize serialization for lineage events
spark.serializer                        org.apache.spark.serializer.KryoSerializer
spark.kryo.registrationRequired         false
```

---

## 🛡️ Reliability Patterns

### 1. Circuit Breaker Pattern

```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class OpenMetadataCircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        
    def call_openmetadata(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN - skipping OpenMetadata call")
                
        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
            
        except Exception as e:
            self.on_failure()
            raise e
    
    def on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        
    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Usage in Spark application
circuit_breaker = OpenMetadataCircuitBreaker()

def create_resilient_spark_session():
    """Create Spark session with circuit breaker protection"""
    try:
        return circuit_breaker.call_openmetadata(
            SparkSession.builder.appName("ResilientApp").getOrCreate
        )
    except Exception as e:
        print(f"OpenMetadata unavailable, running without lineage: {e}")
        # Fallback to Spark session without lineage
        return SparkSession.builder.appName("ResilientApp").getOrCreate()
```

### 2. Graceful Degradation

```python
import os
import logging

def create_spark_with_optional_lineage():
    """Create Spark session with optional lineage based on environment"""
    
    builder = SparkSession.builder.appName("ProductionETL")
    
    # Check if lineage is enabled and OpenMetadata is available
    lineage_enabled = os.getenv('LINEAGE_ENABLED', 'true').lower() == 'true'
    openmetadata_host = os.getenv('OPENMETADATA_HOST')
    jwt_token = os.getenv('OPENMETADATA_JWT_TOKEN')
    
    if lineage_enabled and openmetadata_host and jwt_token:
        try:
            # Test OpenMetadata connectivity
            response = requests.get(f"{openmetadata_host}/health", timeout=5)
            if response.status_code == 200:
                # Configure lineage
                builder = builder \
                    .config("spark.extraListeners", "io.openlineage.spark.agent.OpenLineageSparkListener") \
                    .config("spark.openmetadata.transport.type", "openMetadata") \
                    .config("spark.openmetadata.transport.hostPort", openmetadata_host) \
                    .config("spark.openmetadata.transport.jwtToken", jwt_token)
                
                logging.info("✅ Lineage enabled - OpenMetadata available")
            else:
                logging.warning("⚠️ OpenMetadata unhealthy - running without lineage")
                
        except Exception as e:
            logging.warning(f"⚠️ OpenMetadata unavailable - running without lineage: {e}")
    else:
        logging.info("ℹ️ Lineage disabled by configuration")
    
    return builder.getOrCreate()
```

---

## 📊 Monitoring and Alerting

### 1. Custom Metrics

```python
from prometheus_client import Counter, Histogram, Gauge
import time

# Define metrics
lineage_events_sent = Counter('openmetadata_lineage_events_sent_total', 
                             'Total lineage events sent to OpenMetadata')
lineage_send_duration = Histogram('openmetadata_lineage_send_duration_seconds',
                                 'Time spent sending lineage events')
openmetadata_connection_status = Gauge('openmetadata_connection_status',
                                      'OpenMetadata connection status (1=up, 0=down)')

class LineageMetrics:
    @staticmethod
    def record_lineage_event():
        lineage_events_sent.inc()
    
    @staticmethod
    def record_send_duration(duration):
        lineage_send_duration.observe(duration)
    
    @staticmethod
    def update_connection_status(status):
        openmetadata_connection_status.set(1 if status else 0)

# Enhanced Spark listener with metrics
class MetricsAwareSparkListener:
    def __init__(self):
        self.metrics = LineageMetrics()
    
    def on_application_start(self, application_started):
        start_time = time.time()
        try:
            # Send lineage event
            self.send_lineage_event(application_started)
            self.metrics.record_lineage_event()
            self.metrics.update_connection_status(True)
        except Exception as e:
            self.metrics.update_connection_status(False)
            logging.error(f"Failed to send lineage: {e}")
        finally:
            duration = time.time() - start_time
            self.metrics.record_send_duration(duration)
```

### 2. Health Check Endpoint

```python
from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring systems"""
    
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "components": {}
    }
    
    # Check OpenMetadata connectivity
    try:
        om_host = os.getenv('OPENMETADATA_HOST')
        response = requests.get(f"{om_host}/health", timeout=5)
        health_status["components"]["openmetadata"] = {
            "status": "healthy" if response.status_code == 200 else "unhealthy",
            "response_time_ms": response.elapsed.total_seconds() * 1000
        }
    except Exception as e:
        health_status["components"]["openmetadata"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # Check Spark cluster connectivity
    try:
        spark_master = os.getenv('SPARK_MASTER_URL')
        response = requests.get(f"{spark_master.replace('spark://', 'http://').replace(':7077', ':8080')}", timeout=5)
        health_status["components"]["spark"] = {
            "status": "healthy" if response.status_code == 200 else "unhealthy"
        }
    except Exception as e:
        health_status["components"]["spark"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    status_code = 200 if health_status["status"] == "healthy" else 503
    return jsonify(health_status), status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
```

### 3. Alerting Rules (Prometheus)

```yaml
# alerting_rules.yml
groups:
  - name: openmetadata_lineage
    rules:
      - alert: OpenMetadataDown
        expr: openmetadata_connection_status == 0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "OpenMetadata is unavailable"
          description: "OpenMetadata has been down for more than 5 minutes"
          
      - alert: LineageEventsSendingFailed
        expr: rate(openmetadata_lineage_events_sent_total[5m]) == 0
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "No lineage events being sent"
          description: "No lineage events have been sent in the last 10 minutes"
          
      - alert: HighLineageSendLatency
        expr: histogram_quantile(0.95, rate(openmetadata_lineage_send_duration_seconds_bucket[5m])) > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High lineage send latency"
          description: "95th percentile lineage send latency is above 5 seconds"
```

---

## 🔄 Deployment Strategies

### 1. Blue-Green Deployment

```bash
#!/bin/bash
# blue-green-deploy.sh

# Deploy to green environment
kubectl apply -f spark-lineage-green.yaml

# Wait for green environment to be ready
kubectl wait --for=condition=ready pod -l app=spark-lineage,env=green --timeout=300s

# Run smoke tests on green
./smoke-test.sh green

if [ $? -eq 0 ]; then
    echo "Green environment tests passed, switching traffic..."
    
    # Switch traffic to green
    kubectl patch service spark-lineage -p '{"spec":{"selector":{"env":"green"}}}'
    
    # Wait for traffic switch
    sleep 30
    
    # Run production tests
    ./production-test.sh
    
    if [ $? -eq 0 ]; then
        echo "Production tests passed, cleaning up blue environment..."
        kubectl delete -f spark-lineage-blue.yaml
    else
        echo "Production tests failed, rolling back to blue..."
        kubectl patch service spark-lineage -p '{"spec":{"selector":{"env":"blue"}}}'
    fi
else
    echo "Green environment tests failed, keeping blue environment"
    kubectl delete -f spark-lineage-green.yaml
fi
```

### 2. Canary Deployment

```yaml
# canary-deployment.yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: spark-lineage-rollout
spec:
  replicas: 10
  selector:
    matchLabels:
      app: spark-lineage
  template:
    metadata:
      labels:
        app: spark-lineage
    spec:
      containers:
      - name: spark-lineage
        image: your-registry/spark-lineage:v2.0.0
        env:
        - name: OPENMETADATA_JWT_TOKEN
          valueFrom:
            secretKeyRef:
              name: openmetadata-secrets
              key: jwt-token
  strategy:
    canary:
      steps:
      - setWeight: 10
      - pause: {duration: 5m}
      - setWeight: 25
      - pause: {duration: 10m}
      - setWeight: 50
      - pause: {duration: 15m}
      - setWeight: 75
      - pause: {duration: 10m}
      analysis:
        templates:
        - templateName: success-rate
        args:
        - name: service-name
          value: spark-lineage
```

---

## 📋 Production Checklist Template

```markdown
# Production Deployment Checklist for OpenMetadata Lineage

## Pre-deployment
- [ ] JWT tokens generated and stored securely
- [ ] Network connectivity tested between Spark and OpenMetadata
- [ ] JAR files distributed to all cluster nodes
- [ ] Configuration validated in staging environment
- [ ] Performance baseline established
- [ ] Monitoring and alerting configured

## Deployment
- [ ] Blue-green or canary deployment strategy selected
- [ ] Rollback plan prepared
- [ ] Smoke tests defined and automated
- [ ] Production traffic gradually shifted
- [ ] Real-time monitoring during deployment

## Post-deployment
- [ ] Lineage events appearing in OpenMetadata UI
- [ ] No significant performance degradation observed
- [ ] Error rates within acceptable limits
- [ ] Alerting rules triggered and verified
- [ ] Documentation updated with production configuration

## Sign-off
- [ ] Technical Lead: _________________ Date: _________
- [ ] DevOps Lead: __________________ Date: _________
- [ ] Product Owner: ________________ Date: _________
```