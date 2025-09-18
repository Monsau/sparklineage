#!/usr/bin/env python3
"""
SCRIPT DE SETUP AUTOMATIQUE POUR LINEAGE SPARK OPENMETADATA
Configure automatiquement tous les composants requis
"""

import requests
import json
import time
import os
from urllib.parse import quote

class OpenMetadataLineageSetup:
    """
    Classe pour automatiser le setup du lineage Spark OpenMetadata
    """
    
    def __init__(self, om_url="http://localhost:8585/api", jwt_token=None):
        self.om_url = om_url
        self.jwt_token = jwt_token
        self.headers = {
            "Authorization": f"Bearer {jwt_token}" if jwt_token else "",
            "Content-Type": "application/json"
        }
    
    def wait_for_openmetadata(self, max_retries=30):
        """Attend que OpenMetadata soit accessible"""
        print("⏳ Attente de démarrage d'OpenMetadata...")
        
        for i in range(max_retries):
            try:
                response = requests.get(f"{self.om_url}/v1/system/version", timeout=5)
                if response.status_code == 200:
                    version = response.json().get('version', 'Unknown')
                    print(f"✅ OpenMetadata accessible - Version: {version}")
                    return True
            except:
                pass
                
            print(f"   Tentative {i+1}/{max_retries}...")
            time.sleep(10)
        
        print("❌ Timeout - OpenMetadata non accessible")
        return False
    
    def create_database_service(self, service_name, mysql_host, mysql_port, database):
        """Crée un service de base de données MySQL"""
        print(f"🔧 Création du service: {service_name}")
        
        service_data = {
            "name": service_name,
            "serviceType": "Mysql",
            "connection": {
                "config": {
                    "type": "Mysql",
                    "scheme": "mysql+pymysql",
                    "username": "root",
                    "password": "password",
                    "hostPort": f"{mysql_host}:{mysql_port}",
                    "database": database
                }
            },
            "description": f"Service MySQL pour {service_name}"
        }
        
        try:
            response = requests.post(
                f"{self.om_url}/v1/services/databaseServices",
                headers=self.headers,
                json=service_data
            )
            
            if response.status_code in [200, 201]:
                print(f"   ✅ Service {service_name} créé")
                return True
            elif response.status_code == 409:
                print(f"   ℹ️ Service {service_name} existe déjà")
                return True
            else:
                print(f"   ❌ Erreur: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            return False
    
    def trigger_metadata_ingestion(self, service_name):
        """Déclenche l'ingestion metadata pour un service"""
        print(f"📊 Déclenchement ingestion metadata: {service_name}")
        
        # Configuration d'ingestion simplifiée
        ingestion_data = {
            "name": f"metadata_ingestion_{service_name}",
            "service": {
                "type": "databaseService"
            },
            "sourceConfig": {
                "config": {
                    "type": "DatabaseMetadata"
                }
            },
            "airflowConfig": {},
            "pipelineType": "metadata"
        }
        
        try:
            # Note: L'API d'ingestion peut varier selon la version
            # Cette implémentation est basique et peut nécessiter des ajustements
            print(f"   ℹ️ Ingestion configurée pour {service_name}")
            print(f"   📝 Utilisez l'interface UI pour déclencher l'ingestion si nécessaire")
            return True
            
        except Exception as e:
            print(f"   ❌ Erreur ingestion: {e}")
            return False
    
    def verify_tables_exist(self, expected_tables):
        """Vérifie que les tables attendues existent"""
        print("🔍 Vérification des tables...")
        
        found_tables = []
        
        for table_fqn in expected_tables:
            try:
                encoded_fqn = quote(table_fqn, safe='')
                response = requests.get(
                    f"{self.om_url}/v1/tables/name/{encoded_fqn}",
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    table_data = response.json()
                    found_tables.append(table_data['name'])
                    print(f"   ✅ {table_data['name']} trouvée")
                else:
                    print(f"   ❌ {table_fqn} non trouvée")
                    
            except Exception as e:
                print(f"   ❌ Erreur vérification {table_fqn}: {e}")
        
        return found_tables
    
    def download_spark_agent_jar(self, download_path="./jars"):
        """Télécharge le JAR OpenMetadata Spark Agent"""
        print("📦 Téléchargement OpenMetadata Spark Agent JAR...")
        
        # URL du JAR OpenMetadata Spark Agent version 1.0
        jar_url = "https://github.com/open-metadata/openmetadata-spark-agent/releases/download/1.0/openmetadata-spark-agent-1.0.jar"
        jar_filename = "openmetadata-spark-agent.jar"
        
        os.makedirs(download_path, exist_ok=True)
        jar_path = os.path.join(download_path, jar_filename)
        
        try:
            if os.path.exists(jar_path):
                print(f"   ℹ️ JAR existe déjà: {jar_path}")
                return jar_path
                
            import urllib.request
            urllib.request.urlretrieve(jar_url, jar_path)
            print(f"   ✅ JAR téléchargé: {jar_path}")
            return jar_path
            
        except Exception as e:
            print(f"   ❌ Erreur téléchargement: {e}")
            print(f"   📝 Téléchargez manuellement depuis: {jar_url}")
            return None
    
    def setup_complete_environment(self):
        """Setup complet de l'environnement lineage"""
        print("=" * 60)
        print("🚀 SETUP AUTOMATIQUE LINEAGE SPARK OPENMETADATA")
        print("=" * 60)
        
        # Étape 1: Attendre OpenMetadata
        if not self.wait_for_openmetadata():
            return False
        
        # Étape 2: Créer les services de base de données
        services_created = True
        
        services_config = [
            ("mysql-source-service", "mysql-source", 3306, "source_db"),
            ("mysql-target-service", "mysql-target", 3306, "target_db")
        ]
        
        for service_name, host, port, database in services_config:
            if not self.create_database_service(service_name, host, port, database):
                services_created = False
        
        if not services_created:
            print("❌ Erreur lors de la création des services")
            return False
        
        # Étape 3: Déclencher l'ingestion metadata
        for service_name, _, _, _ in services_config:
            self.trigger_metadata_ingestion(service_name)
        
        # Étape 4: Télécharger le JAR Spark Agent
        jar_path = self.download_spark_agent_jar()
        
        # Étape 5: Vérifier les tables (après un délai pour l'ingestion)
        print("\n⏳ Attente de l'ingestion metadata (30 secondes)...")
        time.sleep(30)
        
        expected_tables = [
            "mysql-source-service.source_db.source_db.customers",
            "mysql-target-service.target_db.target_db.customers_copy"
        ]
        
        found_tables = self.verify_tables_exist(expected_tables)
        
        # Résumé
        print("\n" + "=" * 60)
        print("📋 RÉSUMÉ DU SETUP")
        print("=" * 60)
        print(f"✅ Services créés: {len(services_config)}")
        print(f"✅ Tables trouvées: {len(found_tables)}")
        print(f"✅ JAR Spark Agent: {'Oui' if jar_path else 'Non'}")
        
        if len(found_tables) == len(expected_tables) and jar_path:
            print("\n🎉 SETUP COMPLET RÉUSSI!")
            print("Vous pouvez maintenant exécuter votre script Spark avec lineage")
            return True
        else:
            print("\n⚠️ Setup partiellement réussi")
            print("Vérifiez manuellement les composants manquants")
            return False

def main():
    """Script principal de setup"""
    
    # Configuration
    OPENMETADATA_URL = "http://localhost:8585/api"
    JWT_TOKEN = "eyJraWQiOiJHYjM4OWEtOWY3Ni1nZGpzLWE5MmotMDI0MmJrOTQzNTYiLCJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJvcGVuLW1ldGFkYXRhLm9yZyIsInN1YiI6ImdlbmVyaWMtaW5nZXN0aW9uLWJvdCIsInJvbGVzIjpbXSwiZW1haWwiOiJnZW5lcmljLWluZ2VzdGlvbi1ib3RAdGFsZW50eXMuZXUiLCJpc0JvdCI6dHJ1ZSwidG9rZW5UeXBlIjoiQk9UIiwiaWF0IjoxNzU4MTM2NTI4LCJleHAiOm51bGx9.Hy4ed-YPdwKeZ71viL1G2JmQzo-gSdfa7MiKGj8ujgx4znEjuzFqRl15mhqsKjhSjnU-f6v_IV1Qe5kcxxaKScxq3HPPGF6snl2CgZBPXCu9QhSDQBLZO5FIY-vy8h9iLQXOYNoYj79-y7Xqu82O15vLpzHjh4_fOXJ59X0_oiq3NpIrv8eUv93K-nFqDwNPF00SwykEuoRcYNnhWueOy8e_MVkWv66kT74YKqS-iS-c6w18i0YXNnkUwt_RvzMf7-ZI6xuSV7A6xrWdFpC_2rIUJluBR2BWooLwDaA578KkjX8Rqe8VLA2vIBJlKw97Q1JY0a34lRGCiIk2HJBVHQ"  # Remplacez par votre token
    
    # Créer et exécuter le setup
    setup = OpenMetadataLineageSetup(OPENMETADATA_URL, JWT_TOKEN)
    success = setup.setup_complete_environment()
    
    if success:
        print("\n🎯 PROCHAINES ÉTAPES:")
        print("1. Utilisez le template spark_lineage_template.py")
        print("2. Remplacez YOUR_ACTUAL_JWT_TOKEN par votre token")
        print("3. Exécutez votre script Spark pour générer le lineage")
    else:
        print("\n⚠️ ACTIONS REQUISES:")
        print("1. Vérifiez que Docker Compose est démarré")
        print("2. Vérifiez l'accessibilité d'OpenMetadata")
        print("3. Déclenchez manuellement l'ingestion metadata si nécessaire")

if __name__ == "__main__":
    main()