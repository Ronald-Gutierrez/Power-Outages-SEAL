import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase
cred = credentials.Certificate('credentials/credentials.json')  # Ruta al archivo JSON que descargaste
firebase_admin.initialize_app(cred)

# Obtener referencia a la base de datos de Firestore
db = firestore.client()
