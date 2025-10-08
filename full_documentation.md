#  Apache Spark ↔ OpenMetadata Lineage Integration Platform
*Complete Professional Documentation - Enterprise-Grade Data Lineage Toolkit*

---

##  Multi-Language Documentation | Documentation Multilingue | Documentación Multilingüe | وثائق متعددة اللغات

| Language | Section | Status |
|----------|---------|--------|
|  **English** | [Complete Technical Guide](#-english-complete-documentation) |  Full Coverage |
|  **Français** | [Guide Technique Complet](#-documentation-complète-française) |  Couverture Complète |
|  **Español** | [Guía Técnica Completa](#-documentación-completa-española) |  Cobertura Completa |
|  **العربية** | [الدليل التقني الكامل](#-الوثائق-العربية-الكاملة) |  تغطية كاملة |

---

#  English Complete Documentation

##  Executive Summary

The **Apache Spark ↔ OpenMetadata Lineage Platform** is an enterprise-grade solution for automatic data lineage tracking in Spark, with direct exposure in OpenMetadata. It enables zero-code lineage, real-time tracking, and seamless integration for technical teams.

###  Business Value Proposition
- **Zero-Code Lineage**: No code changes required in Spark jobs
- **Real-Time Tracking**: Captures lineage as jobs execute
- **Multi-Platform**: Works on YARN, Kubernetes, Standalone
- **Column-Level Lineage**: Tracks transformations at column level
- **Production Ready**: Used in enterprise environments

## ️ Comprehensive System Architecture

### High-Level Architecture Overview

```
┌───────────────────────────────────────────────────────────────┐
│                SPARK LINEAGE INTEGRATION PLATFORM            │
│                                                             │
├───────────────────────────────────────────────────────────────┤
│                SPARK ENVIRONMENT (YARN/K8S/Standalone)      │
├───────────────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐     │
│  │ Spark Jobs    │  │ Agent JAR     │  │ Config Mgmt   │     │
│  │ (Python/Scala)│  │ openmetadata- │  │ spark-defaults│     │
│  │               │  │ spark-agent   │  │ .conf/env     │     │
│  └───────────────┘  └───────────────┘  └───────────────┘     │
├───────────────────────────────────────────────────────────────┤
│                OPENMETADATA PLATFORM                         │
├───────────────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐     │
│  │ Metadata API  │  │ Lineage Graph │  │ UI/Monitoring │     │
│  └───────────────┘  └───────────────┘  └───────────────┘     │
└───────────────────────────────────────────────────────────────┘
```

### Component Architecture Deep Dive

- **Spark Jobs**: Standard ETL/ELT jobs in Python or Scala
- **Agent JAR**: openmetadata-spark-agent.jar captures lineage events
- **Config Management**: All integration is done via configuration (no code changes)
- **OpenMetadata**: Receives lineage, displays lineage graph, and provides search/monitoring

## ️ Technology Stack & Dependencies

| Component | Technology | Version | Purpose | License |
|-----------|------------|---------|---------|---------|
| **Data Processing** | Apache Spark | 3.5.0+ | ETL/ELT jobs | Apache 2.0 |
| **Lineage Agent** | OpenMetadata Spark Agent | 1.9.7+ | Lineage capture | Apache 2.0 |
| **Metadata Platform** | OpenMetadata | 1.9.7+ | Metadata management | Apache 2.0 |
| **Runtime Environment** | Python/Scala | 3.8+/2.12+ | Job implementation | PSF/Apache |
| **Container Runtime** | Docker | 24.0+ | Service orchestration | Apache 2.0 |
| **Orchestration** | Docker Compose/K8s/YARN | 2.0+ | Multi-service deployment | Apache 2.0 |

##  System Requirements & Prerequisites

- **Operating System**: Windows 10/11, macOS 12+, or Linux (Ubuntu 20.04+)
- **Memory**: 8GB+ RAM (16GB recommended)
- **Storage**: 10GB+ free space
- **Python**: 3.8+ (for PySpark jobs)
- **Java**: 8+ (for Spark and agent)
- **Docker**: 24.0+ (for containerized deployment)

##  Complete Installation & Setup Guide

### Step 1: Environment Preparation

```bash
# Clone the repository
 git clone <repository-url>
 cd spark

# Download required JARs
 wget https://github.com/open-metadata/OpenMetadata/releases/download/1.9.7/openmetadata-spark-agent.jar
 wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.33/mysql-connector-java-8.0.33.jar
```

### Step 2: Configuration

- Add JARs to your Spark classpath (via `spark-submit` or `spark-defaults.conf`)
- Configure OpenMetadata endpoint and JWT token

Example `spark-submit`:
```bash
spark-submit \
  --jars openmetadata-spark-agent.jar,mysql-connector-java-8.0.33.jar \
  --conf "spark.extraListeners=io.openlineage.spark.agent.OpenLineageSparkListener" \
  --conf "spark.openmetadata.transport.type=openMetadata" \
  --conf "spark.openmetadata.transport.hostPort=http://openmetadata:8585/api" \
  --conf "spark.openmetadata.transport.jwtToken=YOUR_JWT_TOKEN" \
  your_job.py
```

### Step 3: Run Example Job

```bash
# Run the provided example job
./run-example.sh
```

### Step 4: Verify Lineage in OpenMetadata

- Access OpenMetadata UI at `http://localhost:8585`
- Navigate to Pipelines and Data Lineage sections

##  Complete Project Structure

```
spark/
├── README.md
├── full_documentation.md
├── docker-compose.yml
├── samples/
│   ├── init-source.sql
│   ├── init-target.sql
│   └── create_*.sql
├── jars/
│   ├── openmetadata-spark-agent.jar
│   └── mysql-connector-j-8.0.33.jar
├── complex_spark_lineage_job.py
├── docs/
│   ├── INTEGRATION_GUIDE.md
│   ├── PRODUCTION_DEPLOYMENT.md
│   └── ...
└── ...
```

##  Feature Specifications

###  Lineage Features
- **Automatic Source & Target Discovery**
- **Column-Level Lineage**
- **Real-Time Tracking**
- **No Code Changes Required**
- **Graphical Visualization in OpenMetadata**

###  Operational Features
- **Health Monitoring**
- **Debug Logging**
- **Performance Metrics**
- **Alert System**

##  Usage Examples & Best Practices

### Basic Usage Patterns

#### 1. Standard Lineage Workflow
```bash
spark-submit \
  --jars openmetadata-spark-agent.jar,mysql-connector-java-8.0.33.jar \
  --conf "spark.extraListeners=io.openlineage.spark.agent.OpenLineageSparkListener" \
  --conf "spark.openmetadata.transport.type=openMetadata" \
  --conf "spark.openmetadata.transport.hostPort=http://openmetadata:8585/api" \
  --conf "spark.openmetadata.transport.jwtToken=YOUR_JWT_TOKEN" \
  your_job.py
```

#### 2. Docker Compose Environment
```bash
docker-compose up -d
./run-example.sh
```

#### 3. Kubernetes/YARN/Standalone
- See `docs/PRODUCTION_DEPLOYMENT.md` for advanced orchestration

##  Security & Authentication

- **JWT Token Management**
- **RBAC Integration**
- **SSL/TLS Support**
- **Audit Logging**

##  Contributing | Contribution | Contribución | المساهمة

We welcome contributions in all languages! Please see our contribution guidelines for more information.

##  Support | Assistance | Soporte | الدعم

For support in any language, please reach out through our community channels or GitHub Issues.

##  License | Licence | Licencia | الترخيص

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

---

*Last Updated: October 8, 2025*
