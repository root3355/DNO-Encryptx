import os
import json
import hashlib
import base64
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import getpass
from pyfiglet import Figlet
import time

# Forzar codificación UTF-8
sys.stdout.reconfigure(encoding='utf-8')
os.system('chcp 65001 > nul')  # Cambiar a UTF-8 en CMD
# =============================================
# Configuración de Estilos y Colores
# =============================================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def print_banner():
    """Muestra el banner de la aplicación"""
    print("\n" + "="*60)
    print(Colors.BLUE + r"""
██████╗  █████╗ ██████╗ ██╗  ██╗    ███╗   ██╗███████╗████████╗     ██████╗ ██████╗ ███████╗██████╗  █████╗ ████████╗██╗██╗   ██╗███████╗███████╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝    ████╗  ██║██╔════╝╚══██╔══╝    ██╔═══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██║██║   ██║██╔════╝██╔════╝
██║  ██║███████║██████╔╝█████╔╝     ██╔██╗ ██║█████╗     ██║       ██║   ██║██████╔╝█████╗  ██████╔╝███████║   ██║   ██║██║   ██║█████╗  ███████╗
██║  ██║██╔══██║██╔══██╗██╔═██╗     ██║╚██╗██║██╔══╝     ██║       ██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗██╔══██║   ██║   ██║╚██╗ ██╔╝██╔══╝  ╚════██║
██████╔╝██║  ██║██║  ██║██║  ██╗    ██║ ╚████║███████╗   ██║       ╚██████╔╝██║     ███████╗██║  ██║██║  ██║   ██║   ██║ ╚████╔╝ ███████╗███████║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═══╝╚══════╝   ╚═╝        ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═══╝  ╚══════╝╚══════╝
          
▓█████  ███▄    █  ▄████▄   ██▀███  ▓██   ██▓ ██▓███  ▄▄▄█████▓▒██   ██▒
▓█   ▀  ██ ▀█   █ ▒██▀ ▀█  ▓██ ▒ ██▒ ▒██  ██▒▓██░  ██▒▓  ██▒ ▓▒▒▒ █ █ ▒░
▒███   ▓██  ▀█ ██▒▒▓█    ▄ ▓██ ░▄█ ▒  ▒██ ██░▓██░ ██▓▒▒ ▓██░ ▒░░░  █   ░
▒▓█  ▄ ▓██▒  ▐▌██▒▒▓▓▄ ▄██▒▒██▀▀█▄    ░ ▐██▓░▒██▄█▓▒ ▒░ ▓██▓ ░  ░ █ █ ▒ 
░▒████▒▒██░   ▓██░▒ ▓███▀ ░░██▓ ▒██▒  ░ ██▒▓░▒██▒ ░  ░  ▒██▒ ░ ▒██▒ ▒██▒
░░ ▒░ ░░ ▒░   ▒ ▒ ░ ░▒ ▒  ░░ ▒▓ ░▒▓░   ██▒▒▒ ▒▓▒░ ░  ░  ▒ ░░   ▒▒ ░ ░▓ ░
 ░ ░  ░░ ░░   ░ ▒░  ░  ▒     ░▒ ░ ▒░ ▓██ ░▒░ ░▒ ░         ░    ░░   ░▒ ░
   ░      ░   ░ ░ ░          ░░   ░  ▒ ▒ ░░  ░░         ░       ░    ░  
   ░  ░         ░ ░ ░         ░      ░ ░                        ░    ░  
                  ░                  ░ ░     """ + Colors.RESET)
    print("="*60 + "\n")

def print_menu_header(title):
    """Imprime un encabezado de menú estilizado"""
    print("\n" + Colors.CYAN + "═" * 50)
    print(f" {title.upper()} ".center(50, '▓'))
    print("═" * 50 + Colors.RESET)

def print_success(message):
    """Muestra un mensaje de éxito"""
    print(Colors.GREEN + f"[✓] {message}" + Colors.RESET)

def print_error(message):
    """Muestra un mensaje de error"""
    print(Colors.RED + f"[✗] {message}" + Colors.RESET)

def print_warning(message):
    """Muestra un mensaje de advertencia"""
    print(Colors.YELLOW + f"[!] {message}" + Colors.RESET)

def print_info(message):
    """Muestra un mensaje informativo"""
    print(Colors.BLUE + f"[i] {message}" + Colors.RESET)

def loading_animation(message, duration=2):
    """Muestra una animación de carga"""
    print(Colors.YELLOW + f"\n{message}", end="", flush=True)
    for _ in range(duration*2):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print(Colors.RESET + "\n")

# =============================================
# Configuración de la Aplicación
# =============================================
SALT_FILE = "salt.bin"
KEY_FILE = "key.bin"
DB_FILE = "passwords.db"
USERS_FILE = "users.db"
ITERATIONS = 480000
ROLES = {"admin": 2, "user": 1}  # Niveles de permiso

class PasswordManager:
    def __init__(self):
        self.current_user = None
        self.user_key = None  # Nueva: clave para credenciales del usuario
        self.master_key = None  # Nueva: clave maestra para el archivo
        self.cipher = None  # Lo mantenemos por compatibilidad

    def generate_salt(self):
        return os.urandom(16)

    def derive_key(self, master_password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=ITERATIONS,
        )
        return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

    def initialize_manager(self):
        if os.path.exists(DB_FILE):
            print_error("El gestor ya está inicializado.")
            return False

        print_menu_header("Inicialización del Gestor")
        master_pwd = getpass.getpass(Colors.YELLOW + "Crea una contraseña maestra para el administrador: " + Colors.RESET)
        verify_pwd = getpass.getpass(Colors.YELLOW + "Confirma la contraseña maestra: " + Colors.RESET)

        if master_pwd != verify_pwd:
            print_error("Las contraseñas no coinciden.")
            return False

        loading_animation("Generando claves de seguridad")
        
        salt = self.generate_salt()
        key = self.derive_key(master_pwd, salt)
        self.master_key = key  # Almacenamos la clave maestra

        with open(SALT_FILE, "wb") as f:
            f.write(salt)
        with open(KEY_FILE, "wb") as f:
            f.write(key)

        # Crear usuario admin inicial
        users = {
            "admin": {
                "password_hash": hashlib.sha256(master_pwd.encode()).hexdigest(),
                "role": "admin",
                "salt": salt.hex()
            }
        }

        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

        with open(DB_FILE, "wb") as f:
            f.write(Fernet(key).encrypt(b"{}"))

        print_success("Gestor inicializado con éxito. Usuario 'admin' creado.")
        return True

    def authenticate(self, username, password):
        try:
            with open(USERS_FILE, "r") as f:
                users = json.load(f)
        except FileNotFoundError:
            print_error("Sistema no inicializado.")
            return False

        if username not in users:
            print_error("Usuario no encontrado.")
            return False

        loading_animation("Verificando credenciales")
        
        stored_hash = users[username]["password_hash"]
        input_hash = hashlib.sha256(password.encode()).hexdigest()

        if input_hash == stored_hash:
            self.current_user = username
            salt = bytes.fromhex(users[username]["salt"])
            
            # Cargar clave maestra
            with open(KEY_FILE, "rb") as f:
                self.master_key = f.read()
            
            # Crear clave de usuario
            self.user_key = self.derive_key(password, salt)
            self.cipher = Fernet(self.user_key)  # Mantenemos por compatibilidad
            
            print_success(f"Bienvenido, {username}!")
            return True
        else:
            print_error("Contraseña incorrecta.")
            return False

    def create_user(self, username, password, role):
        if self.current_user is None or not self.check_permission(2):
            print_error("Permiso denegado.")
            return False

        with open(USERS_FILE, "r") as f:
            users = json.load(f)

        if username in users:
            print_error("Usuario ya existe.")
            return False

        loading_animation("Creando nuevo usuario")
        
        salt = self.generate_salt()
        users[username] = {
            "password_hash": hashlib.sha256(password.encode()).hexdigest(),
            "role": role,
            "salt": salt.hex()
        }

        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

        print_success(f"Usuario '{username}' creado con rol '{role}'.")
        return True

    def check_permission(self, required_level):
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
        
        user_role = users[self.current_user]["role"]
        return ROLES.get(user_role, 0) >= required_level

    def add_password(self, site, username, password):
        if not self.master_key:
            print_error("No autenticado.")
            return False

        master_cipher = Fernet(self.master_key)
        user_cipher = Fernet(self.user_key)

        try:
            with open(DB_FILE, "rb") as f:
                encrypted_data = f.read()
            passwords = json.loads(master_cipher.decrypt(encrypted_data).decode())
        except:
            passwords = {}

        if site in passwords and not self.check_permission(2):
            print_error("No tienes permisos para modificar este sitio.")
            return False

        loading_animation("Encriptando y almacenando credenciales")
        
        passwords[site] = {
            "username": user_cipher.encrypt(username.encode()).decode(),
            "password": user_cipher.encrypt(password.encode()).decode(),
            "created_by": self.current_user,
            "user_key": self.user_key.decode()  # Almacenamos referencia a la clave
        }

        with open(DB_FILE, "wb") as f:
            f.write(master_cipher.encrypt(json.dumps(passwords).encode()))

        print_success("Contraseña guardada/actualizada con éxito.")
        return True

    def edit_password(self, site, new_password):
        if not self.master_key:
            print_error("No autenticado.")
            return False

        master_cipher = Fernet(self.master_key)

        try:
            with open(DB_FILE, "rb") as f:
                encrypted_data = f.read()
            passwords = json.loads(master_cipher.decrypt(encrypted_data).decode())
        except:
            print_error("Error al leer las contraseñas.")
            return False

        if site not in passwords:
            print_error("Sitio no encontrado.")
            return False

        if passwords[site]["created_by"] != self.current_user and not self.check_permission(2):
            print_error("No tienes permisos para editar esta contraseña.")
            return False

        loading_animation("Actualizando contraseña")
        
        # Usamos la clave original con la que se cifró
        original_user_key = passwords[site]["user_key"]
        user_cipher = Fernet(original_user_key.encode())
        passwords[site]["password"] = user_cipher.encrypt(new_password.encode()).decode()

        with open(DB_FILE, "wb") as f:
            f.write(master_cipher.encrypt(json.dumps(passwords).encode()))

        print_success("Contraseña actualizada con éxito.")
        return True

    def delete_password(self, master_key, site):
        if not master_key:
            print_error("No autenticado.")
            return False

        try:
            with open(DB_FILE, "rb") as f:
                encrypted_data = f.read()
            passwords = json.loads(self.cipher.decrypt(encrypted_data).decode())
        except:
            print_error("Error al leer las contraseñas.")
            return False

        if site not in passwords:
            print_error("Sitio no encontrado.")
            return False

        if passwords[site]["created_by"] != self.current_user and not self.check_permission(2):
            print_error("No tienes permisos para borrar esta contraseña.")
            return False

        loading_animation("Eliminando contraseña")
        
        del passwords[site]

        with open(DB_FILE, "wb") as f:
            f.write(self.cipher.encrypt(json.dumps(passwords).encode()))

        print_success("Contraseña eliminada con éxito.")
        return True

    def list_passwords(self):
        if not self.master_key:
            print_error("No autenticado.")
            return

        master_cipher = Fernet(self.master_key)

        try:
            with open(DB_FILE, "rb") as f:
                encrypted_data = f.read()
            all_passwords = json.loads(master_cipher.decrypt(encrypted_data).decode())
        except:
            print_error("Error al leer las contraseñas.")
            return

        print_menu_header("Contraseñas Almacenadas")
        
        for site, data in all_passwords.items():
            try:
                # Solo mostramos las que podemos descifrar con nuestras claves
                if data["created_by"] == self.current_user or self.check_permission(2):
                    user_cipher = Fernet(self.user_key)
                    username = user_cipher.decrypt(data["username"].encode()).decode()
                    password = user_cipher.decrypt(data["password"].encode()).decode()
                    
                    print(f"\n{Colors.BOLD}Sitio:{Colors.RESET} {Colors.CYAN}{site}{Colors.RESET}")
                    print(f"{Colors.BOLD}Usuario:{Colors.RESET} {username}")
                    print(f"{Colors.BOLD}Contraseña:{Colors.RESET} {'*' * len(password)}")
                    print(f"{Colors.BOLD}Creado por:{Colors.RESET} {data['created_by']}")
                    print(f"{Colors.GREEN}Contraseña real (copiar):{Colors.RESET} {password}")
            except:
                continue

    def logout(self):
        self.current_user = None
        self.cipher = None
        print_success("Sesión cerrada con éxito.")

def main_menu():
    manager = PasswordManager()
    print_banner()
    
    while True:
        print_menu_header("Menú Principal")
        
        if manager.current_user:
            print(f"\n{Colors.BOLD}● Usuario actual:{Colors.RESET} {Colors.YELLOW}{manager.current_user}{Colors.RESET}")
            print(f"{Colors.GREEN}1. Añadir contraseña")
            print(f"2. Editar contraseña")
            print(f"3. Borrar contraseña")
            print(f"4. Listar contraseñas{Colors.RESET}")
            if manager.check_permission(2):
                print(f"{Colors.YELLOW}5. Crear usuario (admin){Colors.RESET}")
            print(f"{Colors.BLUE}6. Cerrar sesión{Colors.RESET}")
            print(f"{Colors.RED}7. Salir{Colors.RESET}")
        else:
            print(f"\n{Colors.GREEN}1. Iniciar sesión")
            print(f"2. Inicializar gestor (solo primera vez){Colors.RESET}")
            print(f"{Colors.RED}3. Salir{Colors.RESET}")
        
        print("\n" + "─" * 50)
        choice = input(f"{Colors.BOLD}» Selecciona una opción:{Colors.RESET} ")
        
        if manager.current_user:
            if choice == "1":
                print_menu_header("Añadir Contraseña")
                site = input("Sitio/web: ")
                username = input("Usuario: ")
                password = getpass.getpass("Contraseña: ")
                manager.add_password(site, username, password)
            elif choice == "2":
                print_menu_header("Editar Contraseña")
                site = input("Sitio a editar: ")
                new_password = getpass.getpass("Nueva contraseña: ")
                manager.edit_password(site, new_password)
            elif choice == "3":
                print_menu_header("Borrar Contraseña")
                site = input("Sitio a borrar: ")
                manager.delete_password(site)
            elif choice == "4":
                manager.list_passwords()
            elif choice == "5" and manager.check_permission(2):
                print_menu_header("Crear Nuevo Usuario")
                username = input("Nuevo nombre de usuario: ")
                password = getpass.getpass("Contraseña: ")
                role = input("Rol (admin/user): ").lower()
                if role not in ROLES:
                    role = "user"
                manager.create_user(username, password, role)
            elif choice == "6":
                manager.logout()
            elif choice == "7":
                print_info("Saliendo del gestor...")
                break
            else:
                print_error("Opción no válida.")
        else:
            if choice == "1":
                print_menu_header("Iniciar Sesión")
                username = input("Usuario: ")
                password = getpass.getpass("Contraseña: ")
                manager.authenticate(username, password)
            elif choice == "2":
                manager.initialize_manager()
            elif choice == "3":
                print_info("Saliendo del gestor...")
                break
            else:
                print_error("Opción no válida.")

if __name__ == "__main__":
    try:
        from cryptography.fernet import Fernet
        main_menu()
    except ImportError:
        print_error("Error: Necesitas instalar cryptography. Ejecuta: pip install cryptography")
