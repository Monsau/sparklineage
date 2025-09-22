# 🚀 Spark OpenMetadata Lineage | Lineage Automático | نسب البيانات التلقائي

*Automatic data lineage tracking for Apache Spark with OpenMetadata integration*

---

## 🌍 Languages | Idiomas | اللغات
- [🇫🇷 Français](#français)
- [🇬🇧 English](#english)  
- [🇪🇸 Español](#español)
- [🇵🇹 Português](#português)
- [🇸🇦 العربية](#العربية)

---

## 🇫🇷 Français

### 📋 Description
Ce projet implémente un système de lineage automatique pour Apache Spark avec OpenMetadata. Il trace automatiquement les flux de données entre les tables MySQL via les transformations Spark ETL.

### ⚡ Fonctionnalités
- ✅ **Lineage automatique** - Capture automatique des relations entre tables
- ✅ **Multi-tables** - Support de transformations complexes (7 tables : 4 sources + 3 cibles)
- ✅ **OpenMetadata** - Integration native avec OpenMetadata 1.9.7
- ✅ **Docker** - Environment complet avec Docker Compose
- ✅ **Spark 3.5.0** - Dernière version stable d'Apache Spark

### 🛠️ Installation

1. **Cloner le repository**
```bash
git clone https://github.com/Monsau/sparklineage.git
cd sparklineage
```

2. **Lancer l'environnement Docker**
```bash
docker-compose up -d
```

3. **Exécuter le job Spark**
```bash
docker exec spark-master /opt/bitnami/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --conf "spark.driver.extraClassPath=/opt/bitnami/spark/jars/openmetadata-spark-agent.jar:/opt/bitnami/spark/jars/mysql-connector-j-8.0.33.jar" \
  --conf "spark.executor.extraClassPath=/opt/bitnami/spark/jars/openmetadata-spark-agent.jar:/opt/bitnami/spark/jars/mysql-connector-j-8.0.33.jar" \
  /opt/bitnami/spark/complex_spark_lineage_job.py
```

### 📊 Services
- **OpenMetadata UI**: http://localhost:8585
- **Spark Master UI**: http://localhost:8080
- **MySQL Source**: localhost:3308 (root/password)
- **MySQL Target**: localhost:3307 (root/password)

---

## 🇬🇧 English

### 📋 Description
This project implements an automatic lineage system for Apache Spark with OpenMetadata. It automatically tracks data flows between MySQL tables through Spark ETL transformations.

### ⚡ Features
- ✅ **Automatic lineage** - Automatic capture of table relationships
- ✅ **Multi-table** - Support for complex transformations (7 tables: 4 sources + 3 targets)
- ✅ **OpenMetadata** - Native integration with OpenMetadata 1.9.7
- ✅ **Docker** - Complete environment with Docker Compose
- ✅ **Spark 3.5.0** - Latest stable version of Apache Spark

### 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/Monsau/sparklineage.git
cd sparklineage
```

2. **Start Docker environment**
```bash
docker-compose up -d
```

3. **Run Spark job**
```bash
docker exec spark-master /opt/bitnami/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --conf "spark.driver.extraClassPath=/opt/bitnami/spark/jars/openmetadata-spark-agent.jar:/opt/bitnami/spark/jars/mysql-connector-j-8.0.33.jar" \
  --conf "spark.executor.extraClassPath=/opt/bitnami/spark/jars/openmetadata-spark-agent.jar:/opt/bitnami/spark/jars/mysql-connector-j-8.0.33.jar" \
  /opt/bitnami/spark/complex_spark_lineage_job.py
```

### 📊 Services
- **OpenMetadata UI**: http://localhost:8585
- **Spark Master UI**: http://localhost:8080
- **MySQL Source**: localhost:3308 (root/password)
- **MySQL Target**: localhost:3307 (root/password)

---

## 🇪🇸 Español

### 📋 Descripción
Este proyecto implementa un sistema de linaje automático para Apache Spark con OpenMetadata. Rastrea automáticamente los flujos de datos entre tablas MySQL a través de transformaciones ETL de Spark.

### ⚡ Características
- ✅ **Linaje automático** - Captura automática de relaciones entre tablas
- ✅ **Multi-tabla** - Soporte para transformaciones complejas (7 tablas: 4 fuentes + 3 objetivos)
- ✅ **OpenMetadata** - Integración nativa con OpenMetadata 1.9.7
- ✅ **Docker** - Entorno completo con Docker Compose
- ✅ **Spark 3.5.0** - Última versión estable de Apache Spark

### 🛠️ Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/Monsau/sparklineage.git
cd sparklineage
```

2. **Iniciar entorno Docker**
```bash
docker-compose up -d
```

3. **Ejecutar trabajo Spark**
```bash
docker exec spark-master /opt/bitnami/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --conf "spark.driver.extraClassPath=/opt/bitnami/spark/jars/openmetadata-spark-agent.jar:/opt/bitnami/spark/jars/mysql-connector-j-8.0.33.jar" \
  --conf "spark.executor.extraClassPath=/opt/bitnami/spark/jars/openmetadata-spark-agent.jar:/opt/bitnami/spark/jars/mysql-connector-j-8.0.33.jar" \
  /opt/bitnami/spark/complex_spark_lineage_job.py
```

### 📊 Servicios
- **OpenMetadata UI**: http://localhost:8585
- **Spark Master UI**: http://localhost:8080
- **MySQL Fuente**: localhost:3308 (root/password)
- **MySQL Objetivo**: localhost:3307 (root/password)

---

## 🇵🇹 Português

### 📋 Descrição
Este projeto implementa um sistema de linhagem automática para Apache Spark com OpenMetadata. Rastreia automaticamente os fluxos de dados entre tabelas MySQL através de transformações ETL do Spark.

### ⚡ Funcionalidades
- ✅ **Linhagem automática** - Captura automática de relacionamentos entre tabelas
- ✅ **Multi-tabela** - Suporte para transformações complexas (7 tabelas: 4 fontes + 3 destinos)
- ✅ **OpenMetadata** - Integração nativa com OpenMetadata 1.9.7
- ✅ **Docker** - Ambiente completo com Docker Compose
- ✅ **Spark 3.5.0** - Última versão estável do Apache Spark

### 🛠️ Instalação

1. **Clonar o repositório**
```bash
git clone https://github.com/Monsau/sparklineage.git
cd sparklineage
```

2. **Iniciar ambiente Docker**
```bash
docker-compose up -d
```

3. **Executar job Spark**
```bash
docker exec spark-master /opt/bitnami/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --conf "spark.driver.extraClassPath=/opt/bitnami/spark/jars/openmetadata-spark-agent.jar:/opt/bitnami/spark/jars/mysql-connector-j-8.0.33.jar" \
  --conf "spark.executor.extraClassPath=/opt/bitnami/spark/jars/openmetadata-spark-agent.jar:/opt/bitnami/spark/jars/mysql-connector-j-8.0.33.jar" \
  /opt/bitnami/spark/complex_spark_lineage_job.py
```

### 📊 Serviços
- **OpenMetadata UI**: http://localhost:8585
- **Spark Master UI**: http://localhost:8080
- **MySQL Fonte**: localhost:3308 (root/password)
- **MySQL Destino**: localhost:3307 (root/password)

---

## 🇸🇦 العربية

### 📋 الوصف
يطبق هذا المشروع نظام نسب البيانات التلقائي لـ Apache Spark مع OpenMetadata. يتتبع تلقائياً تدفقات البيانات بين جداول MySQL من خلال تحويلات Spark ETL.

### ⚡ الميزات
- ✅ **نسب تلقائي** - التقاط تلقائي لعلاقات الجداول
- ✅ **متعدد الجداول** - دعم للتحويلات المعقدة (7 جداول: 4 مصادر + 3 أهداف)
- ✅ **OpenMetadata** - التكامل الأصلي مع OpenMetadata 1.9.7
- ✅ **Docker** - بيئة كاملة مع Docker Compose
- ✅ **Spark 3.5.0** - أحدث إصدار مستقر من Apache Spark

### 🛠️ التثبيت

**1. استنساخ المستودع**
```bash
git clone https://github.com/Monsau/sparklineage.git
cd sparklineage
```

**2. بدء بيئة Docker**
```bash
docker-compose up -d
```

**3. تشغيل مهمة Spark**
```bash
docker exec spark-master /opt/bitnami/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --conf "spark.driver.extraClassPath=/opt/bitnami/spark/jars/openmetadata-spark-agent.jar:/opt/bitnami/spark/jars/mysql-connector-j-8.0.33.jar" \
  --conf "spark.executor.extraClassPath=/opt/bitnami/spark/jars/openmetadata-spark-agent.jar:/opt/bitnami/spark/jars/mysql-connector-j-8.0.33.jar" \
  /opt/bitnami/spark/complex_spark_lineage_job.py
```

### 📊 الخدمات
- **OpenMetadata UI**: http://localhost:8585
- **Spark Master UI**: http://localhost:8080
- **MySQL المصدر**: localhost:3308 (root/password)
- **MySQL الهدف**: localhost:3307 (root/password)

---

## 🏗️ Architecture | Arquitectura | Arquitetura | الهندسة المعمارية

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MySQL Source  │────│   Apache Spark  │────│  MySQL Target   │
│   (Port 3308)   │    │   ETL Process   │    │   (Port 3307)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  OpenMetadata   │
                    │   (Port 8585)   │
                    │ Lineage Tracking│
                    └─────────────────┘
```

## 📁 Project Structure | Estructura | Estrutura | هيكل المشروع

```
sparklineage/
├── complex_spark_lineage_job.py    # Main Spark ETL job
├── docker-compose.yml              # Docker services configuration
├── samples/                        # SQL initialization examples
│   ├── init-source.sql
│   ├── init-target.sql
│   └── create_*.sql
├── jars/                           # Required JAR files
│   ├── openmetadata-spark-agent.jar
│   └── mysql-connector-j-8.0.33.jar
└── README.md                       # This file
```

## 🤝 Contributing | Contribuir | Contribuindo | المساهمة

1. Fork the project | Haz fork del proyecto | Faça fork do projeto | قم بعمل fork للمشروع
2. Create your feature branch | Crea tu rama de características | Crie sua branch de feature | أنشئ فرع الميزة الخاص بك
3. Commit your changes | Haz commit de tus cambios | Faça commit das suas mudanças | قم بعمل commit لتغييراتك
4. Push to the branch | Haz push a la rama | Faça push para a branch | ادفع إلى الفرع
5. Open a Pull Request | Abre un Pull Request | Abra um Pull Request | افتح Pull Request

## 📝 License | Licencia | Licença | الترخيص

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Made with ❤️ for the data community | Hecho con ❤️ para la comunidad de datos | Feito com ❤️ para a comunidade de dados | صُنع بـ ❤️ لمجتمع البيانات**