# ============================================
# SERVICIO: Gestión del Menú
# CRUD de Platillos
# ============================================
import os
from modelos.platillo import Platillo


class MenuServicio:

    def __init__(self, ruta_archivo: str = None):
        base_dir = os.path.dirname(__file__)

        ruta_archivo = os.path.join(
            base_dir,
            "registros",
            "menu.txt"
        )

        self.ruta_archivo = ruta_archivo
        self.platillos = []
        self.cargar_desde_archivo()

    
    # ----------- CARGAR DESDE ARCHIVO -----------
    def asegurar_archivo(self):

        carpeta = os.path.dirname(self.ruta_archivo)

        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        if not os.path.exists(self.ruta_archivo):
            with open(self.ruta_archivo, "w", encoding="utf-8") as f:
                pass

    def cargar_desde_archivo(self) -> None:
        """
        Lee menu.txt y carga self.platillos.
        Si el archivo no existe, lo crea.
        """
        self.asegurar_archivo()
        self.platillos.clear()

        with open(self.ruta_archivo, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                platillo = self._linea_a_platillo(linea)
                if platillo:
                    self.platillos.append(platillo)
    
    def guardar_en_archivo(self) -> None:
        """
        Guarda la lista de platillos en menu.txt.
        """
        self.asegurar_archivo()
        with open(self.ruta_archivo, "w", encoding="utf-8") as f:
            for p in self.platillos:
                f.write(self._platillo_a_linea(p) + "\n")
    
    def _platillo_a_linea(self, platillo: Platillo) -> str:
        """
        Convierte un Platillo a una línea TXT: id|nombre|precio|categoria
        """
        # Reemplazos simples para no romper el separador |
        nombre = platillo.get_nombre().replace("|", "/")
        categoria = platillo.get_categoria().replace("|", "/")
        return f"{platillo.get_id()}|{nombre}|{platillo.get_precio()}|{categoria}"
    
    def _linea_a_platillo(self, linea: str):
        """
        Convierte una línea TXT a Platillo.
        Maneja errores sin romper el programa.
        """
        try:
            partes = linea.split("|")
            if len(partes) != 4:
                return None

            id_p = int(partes[0])
            nombre = partes[1]
            precio = float(partes[2])
            categoria = partes[3]

            return Platillo(id_p, nombre, precio, categoria)
        except Exception:
            return None

    # ----------- AGREGAR -----------
    def agregar_platillo_gui(self, id_p, nombre, precio, categoria):
        if self.buscar_por_id(id_p):
            return False, "Ya existe un platillo con ese ID."
        self.platillos.append(Platillo(id_p, nombre, precio, categoria))
        self.guardar_en_archivo()
        return True, "Platillo agregado."

    # ----------- LISTAR -----------
    def listar_platillos(self):

        if not self.platillos:
            print("📭 No hay platillos registrados")
            return

        print("\n📋 MENÚ DEL RESTAURANTE")
        for p in self.platillos:
            print(p)

    # ----------- BUSCAR -----------
    def buscar_por_id(self, id_platillo):

        for p in self.platillos:
            if p.get_id() == id_platillo:
                return p

        return None

    # ----------- ACTUALIZAR -----------
    def actualizar_platillo_gui(self, id_p, nombre, precio, categoria):
        p = self.buscar_por_id(id_p)
        if not p:
            return False, "Platillo no encontrado."
        p.set_nombre(nombre)
        p.set_precio(precio)
        p.set_categoria(categoria)
        self.guardar_en_archivo()
        return True, "Platillo actualizado."

    # ----------- ELIMINAR -----------
    def eliminar_platillo_gui(self, id_p):
        p = self.buscar_por_id(id_p)
        if not p:
            return False, "Platillo no encontrado."
        self.platillos.remove(p)
        self.guardar_en_archivo()
        return True, "Platillo eliminado."