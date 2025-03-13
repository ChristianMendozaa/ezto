<<<<<<< HEAD
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Cargar las credenciales de Firebase
cred = credentials.Certificate("firebase_credentials.json")

# Inicializar la aplicación de Firebase si no está ya inicializada
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Crear una instancia de Firestore
=======
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Cargar las credenciales de Firebase
cred = credentials.Certificate("firebase_credentials.json")

# Inicializar la aplicación de Firebase si no está ya inicializada
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Crear una instancia de Firestore
>>>>>>> afb75bf933e10a27a8164a48c8899b5b816ddf92
db = firestore.client()