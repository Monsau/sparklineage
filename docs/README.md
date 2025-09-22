# 📚 Documentation Index | Index de Documentation

*Complete documentation for integrating OpenMetadata lineage into existing Spark environments*

---

## 🗂️ Available Documentation

### 🔧 [Integration Guide](./INTEGRATION_GUIDE.md)
**English** | **Français** | **Español**
- How to add automatic lineage to existing Spark jobs
- Configuration options for different deployment scenarios
- Code examples and troubleshooting

### ⚙️ [Spark Configuration Templates](./SPARK_CONFIGURATION_TEMPLATES.md)
- Ready-to-use configuration files for various Spark deployments
- Templates for Standalone, YARN, Kubernetes, EMR, and Databricks
- Docker Compose examples and validation scripts

### 🏗️ [Production Deployment Guide](./PRODUCTION_DEPLOYMENT.md)
- Security best practices and JWT token management
- Performance optimization and reliability patterns
- Monitoring, alerting, and deployment strategies
- Production checklist template

---

## 🚀 Quick Start

Choose your deployment scenario:

### 🐳 Docker Environment
```bash
# 1. Add JARs to your Docker image
COPY jars/openmetadata-spark-agent.jar /opt/spark/jars/
COPY jars/mysql-connector-j-8.0.33.jar /opt/spark/jars/

# 2. Configure Spark with lineage
--conf "spark.extraListeners=io.openlineage.spark.agent.OpenLineageSparkListener"
--conf "spark.openmetadata.transport.type=openMetadata"
--conf "spark.openmetadata.transport.hostPort=http://openmetadata:8585/api"
--conf "spark.openmetadata.transport.jwtToken=YOUR_JWT_TOKEN"
```

### ☸️ Kubernetes Environment
```yaml
# Add to your SparkApplication
sparkConf:
  "spark.extraListeners": "io.openlineage.spark.agent.OpenLineageSparkListener"
  "spark.openmetadata.transport.type": "openMetadata"
  "spark.openmetadata.transport.hostPort": "http://openmetadata:8585/api"
  "spark.openmetadata.transport.jwtToken": "${OPENMETADATA_JWT_TOKEN}"
```

### 🌩️ YARN/EMR Environment
```bash
spark-submit \
  --master yarn \
  --jars hdfs://namenode/jars/openmetadata-spark-agent.jar \
  --conf "spark.extraListeners=io.openlineage.spark.agent.OpenLineageSparkListener" \
  --conf "spark.openmetadata.transport.hostPort=https://your-openmetadata.com/api" \
  your_job.py
```

---

## 🔍 By Use Case

### 🆕 **New Spark Projects**
Start with [Integration Guide](./INTEGRATION_GUIDE.md) → [Docker Templates](./SPARK_CONFIGURATION_TEMPLATES.md#docker-compose)

### 🏢 **Existing Production Environments**
Begin with [Production Deployment](./PRODUCTION_DEPLOYMENT.md) → [Security Best Practices](./PRODUCTION_DEPLOYMENT.md#security-best-practices)

### ☸️ **Kubernetes Deployments**
Check [K8s Configuration](./SPARK_CONFIGURATION_TEMPLATES.md#kubernetes) → [Production Monitoring](./PRODUCTION_DEPLOYMENT.md#monitoring-and-alerting)

### 🌩️ **Cloud Platforms (EMR, Databricks)**
Review [Cloud Templates](./SPARK_CONFIGURATION_TEMPLATES.md#emrdatabricks) → [Deployment Strategies](./PRODUCTION_DEPLOYMENT.md#deployment-strategies)

---

## 🛠️ Common Integration Patterns

### Pattern 1: **Programmatic Integration**
Add lineage configuration directly in your Spark code:
```python
spark = SparkSession.builder \
    .config("spark.extraListeners", "io.openlineage.spark.agent.OpenLineageSparkListener") \
    .config("spark.openmetadata.transport.type", "openMetadata") \
    .getOrCreate()
```

### Pattern 2: **Infrastructure-Level Integration**
Configure lineage at the cluster level via `spark-defaults.conf`:
```properties
spark.extraListeners    io.openlineage.spark.agent.OpenLineageSparkListener
spark.openmetadata.transport.type    openMetadata
```

### Pattern 3: **Container-Based Integration**
Embed lineage configuration in Docker images or Kubernetes manifests.

---

## 📋 Implementation Checklist

### Phase 1: **Preparation**
- [ ] Download required JARs ([Integration Guide](./INTEGRATION_GUIDE.md#download-required-jars))
- [ ] Generate OpenMetadata JWT token
- [ ] Test network connectivity to OpenMetadata
- [ ] Choose integration pattern based on your environment

### Phase 2: **Configuration**
- [ ] Select appropriate configuration template ([Templates](./SPARK_CONFIGURATION_TEMPLATES.md))
- [ ] Adapt configuration to your environment
- [ ] Test configuration with validation script
- [ ] Implement security best practices ([Production Guide](./PRODUCTION_DEPLOYMENT.md#security-best-practices))

### Phase 3: **Deployment**
- [ ] Deploy to staging environment first
- [ ] Validate lineage capture in OpenMetadata UI
- [ ] Monitor performance impact
- [ ] Deploy to production using appropriate strategy

### Phase 4: **Production**
- [ ] Set up monitoring and alerting
- [ ] Implement circuit breakers for reliability
- [ ] Configure backup strategies
- [ ] Document your specific configuration

---

## 🔗 External Resources

- [OpenMetadata Documentation](https://docs.open-metadata.org/)
- [OpenLineage Spark Integration](https://openlineage.io/docs/integrations/spark/)
- [Apache Spark Configuration Reference](https://spark.apache.org/docs/latest/configuration.html)
- [Spark on Kubernetes Guide](https://spark.apache.org/docs/latest/running-on-kubernetes.html)

---

## 🤝 Contributing

Found an issue or want to improve the documentation?

1. **Issues**: Report problems or suggest improvements
2. **Pull Requests**: Submit documentation updates
3. **Examples**: Share your production configurations (anonymized)

---

## 📞 Support

### 🆘 Common Issues
- **JWT Token Issues**: Check token expiration and permissions
- **JAR Not Found**: Verify JAR paths and file permissions
- **Connection Refused**: Validate OpenMetadata connectivity and firewall rules
- **Performance Impact**: Review memory allocation and connection pooling settings

### 📚 Additional Help
- Check the troubleshooting sections in each guide
- Review configuration validation scripts
- Test with minimal examples before full deployment
- Monitor logs for OpenLineage and OpenMetadata specific messages

---

*This documentation covers integration of OpenMetadata lineage tracking into existing Spark environments. For new deployments, consider starting with the main project [README](../README.md).*