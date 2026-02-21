# ============================================
# SISTEMA PRINCIPAL
# Restaurante App
# ============================================

from servicios.menu_servicio import MenuServicio


def mostrar_menu():
    print("""
=============================
 🍽️  SISTEMA RESTAURANTE
=============================
1. Agregar platillo
2. Listar platillos
3. Buscar platillo
4. Actualizar platillo
5. Eliminar platillo
0. Salir
=============================
""")


def main():

    servicio = MenuServicio()

    while True:

        mostrar_menu()

        try:
            opcion = int(input("Seleccione opción: "))

            if opcion == 1:
                servicio.agregar_platillo()

            elif opcion == 2:
                servicio.listar_platillos()

            elif opcion == 3:
                id_p = int(input("ID a buscar: "))
                p = servicio.buscar_por_id(id_p)

                if p:
                    print("🔎 Encontrado:", p)
                else:
                    print("❌ No existe")

            elif opcion == 4:
                servicio.actualizar_platillo()

            elif opcion == 5:
                servicio.eliminar_platillo()

            elif opcion == 0:
                servicio.guardar_en_archivo()
                print("💾 Cambios guardados en menu.txt")
                print("👋 Saliendo del sistema...")
                break

            else:
                print("⚠️ Opción inválida")

        except ValueError:
            print("⚠️ Debe ingresar números")


if __name__ == "__main__":
    main()