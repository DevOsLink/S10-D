from servicios.menu_servicio import MenuServicio
from ui.app_tk import AppTk

def main():
    servicio = MenuServicio()
    app = AppTk(servicio)
    app.run()

if __name__ == "__main__":
    main()