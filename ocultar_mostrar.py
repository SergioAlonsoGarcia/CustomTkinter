import tkinter as tk
import customtkinter as ctk

class VentanaLogin:
    def __init__(self):
        self.root = ctk.CTk()  # Crear la ventana de Login
        self.root.title("Login")
        self.root.geometry("400x300")

        # Crear un botón para mostrar la Ventana Principal
        self.boton_login = ctk.CTkButton(self.root, text="Ir a la ventana principal", command=self.mostrar_ventana_principal)
        self.boton_login.pack(pady=20)

        # Iniciar la ventana de Login
        self.root.mainloop()

    def mostrar_ventana_principal(self):
        # Ocultar la ventana de login
        self.root.withdraw()

        # Crear y mostrar la ventana principal
        self.ventana_principal = VentanaPrincipal(self)

class VentanaPrincipal:
    def __init__(self, ventana_login):
        self.root = ctk.CTk()  # Crear la ventana principal
        self.root.title("Ventana Principal")
        self.root.geometry("400x300")

        # Crear un botón para volver a la ventana de Login
        self.boton_principal = ctk.CTkButton(self.root, text="Volver al Login", command=self.volver_a_login)
        self.boton_principal.pack(pady=20)

        # Guardar referencia a la ventana de Login
        self.ventana_login = ventana_login

        # Iniciar la ventana principal
        self.root.mainloop()

    def volver_a_login(self):
        # Ocultar la ventana principal
        self.root.withdraw()

        # Volver a mostrar la ventana de Login
        self.ventana_login.root.deiconify()

# Iniciar la aplicación
if __name__ == "__main__":
    VentanaLogin()
