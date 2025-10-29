import psycopg2
from psycopg2 import sql

class DatabaseManager:
    def __init__(self, dbname, user, password, host="localhost", port="5432"):
        self.connection_params = {
            'dbname': dbname,
            'user': user,
            'password': password,
            'host': host,
            'port': port
        }
        self.connection = None
        self.connect()
        self.create_table_if_not_exists()
    
    def connect(self):
        try:
            self.connection = psycopg2.connect(**self.connection_params)
            print("✅ Sikeresen csatlakozva a PostgreSQL adatbázishoz")
        except Exception as e:
            print(f"❌ Hiba a csatlakozás során: {e}")
    
    def create_table_if_not_exists(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS guild_messages (
            guild_id BIGINT PRIMARY KEY,
            test_message VARCHAR(255)
        );
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(create_table_query)
                self.connection.commit()
                print("✅ Tábla ellenőrizve/létrehozva")
        except Exception as e:
            print(f"❌ Hiba a tábla létrehozása során: {e}")
    
    def get_guild_id(self, test_message):
        query = "SELECT guild_id FROM guild_messages WHERE test_message = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (test_message,))
                result = cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            print(f"❌ Hiba a guild_id lekérése során: {e}")
            return None
    
    def get_test_message(self, guild_id):
        query = "SELECT test_message FROM guild_messages WHERE guild_id = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (guild_id,))
                result = cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            print(f"❌ Hiba a test_message lekérése során: {e}")
            return None
    
    def insert_or_update_message(self, guild_id, test_message):
        query = """
        INSERT INTO guild_messages (guild_id, test_message) 
        VALUES (%s, %s)
        ON CONFLICT (guild_id) 
        DO UPDATE SET test_message = EXCLUDED.test_message
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (guild_id, test_message))
                self.connection.commit()
                print(f"✅ Adatok sikeresen mentve: guild_id={guild_id}, test_message='{test_message}'")
                return True
        except Exception as e:
            print(f"❌ Hiba az adatok mentése során: {e}")
            return False
    
    def close(self):
        if self.connection:
            self.connection.close()
            print("✅ Kapcsolat bezárva")