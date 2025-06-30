# 🧊 Apache Iceberg Lakehouse Architecture (Dockerized)

This project sets up a **local lakehouse architecture** using **Docker Compose** with the following components:

- 🧊 **Apache Iceberg** – Table format for huge analytic datasets
- 🗃 **MinIO** – S3-compatible object store
- 📚 **Project Nessie** – Catalog for versioned data
- 🔥 **Apache Spark** – For batch/streaming + Iceberg integration
- 🚀 **Trino** – Distributed SQL query engine

---

## 🏗️ Architecture Overview

        ┌─────────────┐
        │   Trino     │ ◄────────────┐
        └────┬────────┘              │
             │                       │
        ┌────▼────┐            ┌─────▼──────┐
        │ Spark   │ ─────┐     │  Nessie    │
        └────┬────┘      │     └────┬───────┘
             │           │          │
             │        Iceberg Tables (Catalog)
             │           │
        ┌────▼───────────▼─────┐
        │     MinIO (S3)       │
        └──────────────────────┘

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR-USERNAME/iceberg-lakehouse.git
cd iceberg-lakehouse
```

### 2. Create .env file

```bash
MINIO_ROOT_USER=minio
MINIO_ROOT_PASSWORD=supersecret
AWS_ACCESS_KEY_ID=minio
AWS_SECRET_ACCESS_KEY=supersecret
```

### 3. Download Required JARs


In jars/ folder place the following inside:

| File                                       | Source                                                                                                                                 |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| `iceberg-spark-runtime-3.5_2.12-1.6.0.jar` | [Maven Central – Iceberg Spark Runtime 1.6.0](https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/1.6.0/) |
| `aws-java-sdk-bundle-1.12.261.jar`         | [Maven Central – AWS SDK Bundle](https://repo1.maven.org/maven2/software/amazon/awssdk/bundle/1.12.261/)                               |


### 4. Start the Stack

```bash
docker-compose up --build
```

All services will be started:

```bash
MinIO: http://localhost:9000
Login: minio / supersecret
Nessie (REST API): http://localhost:19120/api/v1
Trino: localhost:8080
Spark Master UI: http://localhost:8088
```

### 5. Load Data into Iceberg (via Spark)
Place it in data/incoming/, then run:

```bash
docker exec -it spark bash
spark-submit /opt/spark/work-dir/validate_and_load.py
```

