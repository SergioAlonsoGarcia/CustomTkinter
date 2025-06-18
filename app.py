import Interfaz.interfaz_grafica as gui
import sys
sys.path.append(r"H:/Nomas/CTkinter/Interfaz")
from Interfaz.interfaz_grafica import principal, Login,cargar_sesion

if __name__ == "__main__":
    usuario_sesion = cargar_sesion()
    if usuario_sesion:
        principal()
    else:
        Login()
