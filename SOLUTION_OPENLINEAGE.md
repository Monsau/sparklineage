# [](https://)SOLUTION COMPLETE OPENLINEAGE

## 1. INSTALLATION JAVA (REQUIS)

### Option A - Chocolatey (Rapide):

```powershell
# Ouvrir PowerShell en administrateur
choco install openjdk11
```

### Option B - Manuel:

1. Téléchargez: https://adoptium.net/temurin/releases/
2. Installez OpenJDK 11
3. Ajoutez JAVA_HOME dans variables d'environnement

## 2. VERIFICATION JAVA

```powershell
java -version
echo $env:JAVA_HOME
```

## 3. CONFIGURATION OPENMETADATA BOT

1. Ouvrez http://localhost:8585
2. Login: admin/admin
3. Settings → Integrations → Bots → Add Bot
4. Name: spark-openlineage-bot
5. Email: spark-openlineage-bot@openmetadata.org
6. Copiez le JWT Token
7. Ajoutez dans .env: OPENMETADATA_JWT_TOKEN=votre_token

## 4. TEST OPENLINEAGE

```powershell
# Après installation Java
.venv\Scripts\activate
python test_java_complete.py
```

## 5. PIPELINE COMPLET

```powershell
python submit_with_openlineage.py
```

## RESULTAT ATTENDU:

- Lineage automatique dans OpenMetadata
- Traçabilité des transformations Spark
- Métadonnées des sources et destinations
- Visualisation graphique du pipeline
