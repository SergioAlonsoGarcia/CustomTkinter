import os, json, re, pymysql
import customtkinter as ctk
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

carpeta_principal = os.path.dirname(__file__)
carpeta_imagenes = os.path.join(carpeta_principal, "imagenes")

archivo_sesion = "sesion.json"




def guardar_sesion(usuario):
    """Guardar la sesión en un archivo JSON."""
    with open(archivo_sesion, "w") as archivo:
        json.dump(usuario, archivo)

def cargar_sesion():
    """Cargar la sesión desde un archivo JSON."""
    try:
        with open(archivo_sesion, "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return None

def cerrar_sesion(self):
    """Cerrar sesión y eliminar el archivo JSON."""
    if os.path.exists(archivo_sesion):
        os.remove(archivo_sesion)
    self.root.destroy()
    messagebox.showinfo("Sesion cerrada","Sesion cerrada")
    Login()



class Login:
    def __init__(self):

        global conexion

        try:
            with open("base_de_datos.sql", "r", encoding="utf-8") as f:
                script = f.read()

            # Buscar nombre de base de datos
            match = re.search(r'CREATE DATABASE IF NOT EXISTS\s+[`"]?(\w+)[`"]?;', script, re.IGNORECASE)

            if not match: 
                messagebox.showerror(title="Error", message="No se encontró")
                return

            nombre_bd = match.group(1)

            # Conexión sin base de datos
            conexion = pymysql.connect(
                host="localhost",
                user="root",
                password="" 
            )

            with conexion.cursor() as cursor:
                comandos = script.split(';')
                for comando in comandos:
                    if comando.strip():
                        cursor.execute(comando)

            conexion.commit()
            cursor.close()

            with open("bd_actual.txt", "w") as f:
                f.write(nombre_bd)


        except Exception as e:
            messagebox.showerror(title="Error", message=f"Ocurrió un error:\n{e}")

        # except pymysql.MySQLError as e :
        #     messagebox.showerror("Error",f"¡Error! {e}")

        self.root = ctk.CTk()
        self.root.title("Login")
        self.root.iconbitmap(os.path.join(carpeta_imagenes, "logo.ico"))
        self.root.geometry("400x500+450+100")
        self.root.resizable(False, False)

        # Variables
        self.correo=ctk.StringVar()
        self.contraseña=ctk.StringVar()

        try:
            self.logo = ctk.CTkImage(
                light_image=Image.open(os.path.join(carpeta_imagenes, "logoClaro.png")), 
                dark_image=Image.open(os.path.join(carpeta_imagenes, "logoOscuro.png")), 
                size=(250, 250)
            )
        except Exception as e:
            print("Error al cargar la imagen:", e)
            self.logo = None
        try:
            etiqueta = ctk.CTkLabel(self.root, image=self.logo, text="")
            etiqueta.pack(pady=15)
        except KeyError as e:
            print(e)
        # Campos de texto 
        # Usuario
        self.correoDefecto = "Correo"
        ctk.CTkLabel(self.root, text="Correo").pack()
        self.correo = ctk.CTkEntry(self.root,textvariable=self.correo)
        self.correo.insert(0, "Usuario")
        self.correo.bind("<Button-1>", lambda e: self.correo.delete(0, "end"))
        self.correo.bind("<FocusOut>", lambda e: self.on_focus_out(e, self.correo, self.correoDefecto))
        self.correo.bind("<FocusIn>", lambda e: self.on_focus_in(e, self.correo, self.correoDefecto))
        self.correo.pack()

        # Contraseña
        self.contrasenaDefecto = "Contraseña"
        ctk.CTkLabel(self.root, text="Contraseña").pack()
        self.contrasena = ctk.CTkEntry(self.root,textvariable=self.contraseña)  # M
        self.contrasena.insert(0, self.contrasenaDefecto)
        self.contrasena.bind("<FocusOut>", lambda e: self.on_focus_out(e, self.contrasena, self.contrasenaDefecto))
        self.contrasena.bind("<FocusIn>", lambda e: self.on_focus_in(e, self.contrasena, self.contrasenaDefecto))
        self.contrasena.pack()

        ctk.CTkButton(self.root, text="Entrar",command=self.entrar).pack(pady=10)

        ctk.CTkButton(self.root,text="Crear cuenta",command=lambda: self.crearCuentaDef()).pack()

        self.root.mainloop()

    def crearCuentaDef(self):
        self.root.destroy()
        crearCuenta()

    def entrar(self):
        global conexion
        correo=self.correo.get()
        contraseña=self.contrasena.get()

        if correo==self.correoDefecto or contraseña ==self.contrasenaDefecto or correo== "" or contraseña == "":
            if hasattr (self,"error"):
                self.error.destroy()
                self.error=ctk.CTkLabel(self.root,text_color=("red","red"),text="Todos los campos deben estar llenos.")
                self.error.pack()
            else:
                self.error=ctk.CTkLabel(self.root,text_color=("red","red"),text="Todos los campos deben estar llenos.")
                self.error.pack()
            return
        sql="SELECT * FROM `usuarios` WHERE `correo` =%s AND `contraseña` = %s"
        cursor=conexion.cursor()
        cursor.execute(sql,(correo,contraseña))
        resultado=cursor.fetchone()
        if resultado:
            usuario_sesion = {"correo": resultado[0], "usuario": resultado[1]}
            guardar_sesion(usuario_sesion)
            messagebox.showinfo("Correcto", "Inicio de sesión correcto.")
            self.root.withdraw()
            principal()
        else:
            if hasattr (self,"error"):
                self.error.destroy()
                self.error=ctk.CTkLabel(self.root,text_color=("red","red"),text="Correo o contraseña incorrectas.")
                self.error.pack()
            else:
                self.error=ctk.CTkLabel(self.root,text_color=("red","red"),text="Correo o contraseña incorrectas.")
                self.error.pack()
            return






    def on_focus_in(self, event, entry, defecto):
        """Cuando el campo recibe el foco, elimina el texto predeterminado si está presente"""
        if entry.get() == defecto:
            entry.delete(0, "end")  
            if entry == self.contrasena:
                entry.configure(show="*") 

    def on_focus_out(self, event, entry, defecto):
        """Cuando el campo pierde el foco, muestra el texto predeterminado si está vacío"""

        if entry.get() == '':
            entry.insert(0, defecto)
            if entry == self.contrasena:
                entry.configure(show="") 

    def on_click_contrasena(self, event):
        """Cuando se hace clic en el campo de la contraseña, borrar texto predeterminado y permitir escribir"""
        if self.contrasena.get() == self.contrasenaDefecto:
            self.contrasena.delete(0, "end")
            self.contrasena.configure(show="*")


class crearCuenta:
    def __init__(self):


        self.root=ctk.CTk()
        self.root.title("Crear cuenta")
        self.root.iconbitmap(os.path.join(carpeta_imagenes, "logo.ico"))
        self.root.geometry("400x500+450+100")
        self.root.resizable(False, False)



        self.correo=ctk.StringVar()
        self.contraseña=ctk.StringVar()
        self.usuario=ctk.StringVar()

        ctk.CTkLabel(self.root,text="Crear Cuenta",font=("Cascadia Code",25)).pack(pady=40)

        ctk.CTkLabel(self.root,text="Correo",font=("Cascadia Code",15)).pack()
        ctk.CTkEntry(self.root,textvariable=self.correo).pack()

        ctk.CTkLabel(self.root,text="Contraseña",font=("Cascadia Code",15)).pack()
        ctk.CTkEntry(self.root,textvariable=self.contraseña).pack()

        ctk.CTkLabel(self.root,text="Usuario",font=("Cascadia Code",15)).pack()
        ctk.CTkEntry(self.root,textvariable=self.usuario).pack()


        ctk.CTkButton(self.root,text="Continuar",command=self.mandarDatos).pack(pady=20)


        self.root.mainloop()

    # def mandarDatos(self):
    #     sql="INSERT INTO `usuarios` VAlUES (%s,%s,%s)"
    #     cursor=conexion.cursor()
    #     cursor.execute(sql,(self.correo.get(),self.contraseña.get(),self.usuario.get()))
    #     conexion.commit()








    # def sleccionarIcono(self):
    #     """Permite seleccionar un ícono de usuario desde el sistema de archivos"""
    #     archivo = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp")])
    #     if archivo:
    #         self.icono_usuario = archivo  # Guardar la ruta del ícono seleccionado







    def validar_correo(self, correo):
        """Validar que el correo tenga una estructura válida"""
        expresion_regular = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(expresion_regular, correo):
            return True
        else:
            return False

    def verificar_existencia(self, correo, usuario):
        """Verificar si el correo o el usuario ya existen en la base de datos"""
        sql_correo = "SELECT * FROM `usuarios` WHERE `correo`=%s"
        sql_usuario = "SELECT * FROM `usuarios` WHERE `usuario`=%s"
        cursor = conexion.cursor()
        cursor.execute(sql_correo, (correo,))
        if cursor.fetchone():
            return "Correo"
        cursor.execute(sql_usuario, (usuario,))
        if cursor.fetchone():
            return "Usuario"
        return None



    def mandarDatos(self):
        global conexion
        correo = self.correo.get()
        usuario = self.usuario.get()
        contraseña=self.contraseña.get()

        if not correo or not usuario or not contraseña:
            if hasattr (self,"error"):
                self.error.destroy()
                self.error=ctk.CTkLabel(self.root,text_color=("red","red"),text="Todos los campos deben estar llenos.")
                self.error.pack()
            else:
                self.error=ctk.CTkLabel(self.root,text_color=("red","red"),text="Todos los campos deben estar llenos.")
                self.error.pack()
            return

        # Validar el correo
        if not self.validar_correo(correo):
            if hasattr (self,"error"):
                self.error.destroy()
                self.error=ctk.CTkLabel(self.root,text_color=("red","red"),text="Correo no valido.")
                self.error.pack()
            else:
                self.error.destroy()
                self.error=ctk.CTkLabel(self.root,text_color=("red","red"),text="Correo no valido.")
                self.error.pack()

            return  

        # if self.icono_usuario:
            # Puedes usar la ruta completa o mover la imagen a una carpeta específica para evitar problemas de rutas
        icono_ruta = os.path.join(carpeta_imagenes, f"iconoPerfil.jpg")
            # shutil.copy(self.icono_usuario, icono_ruta)  # Mover el archivo de imagen al directorio



        # Verificar la existencia del correo o usuario
        existe = self.verificar_existencia(correo, usuario)
        if existe:
            if hasattr (self,"error"):
                self.error.destroy()
                self.error=ctk.CTkLabel(self.root,text_color=("red","red"),text=f"El {existe} ya esta en uso")
                self.error.pack()
            else:
                self.error=ctk.CTkLabel(self.root,text_color=("red","red"),text=f"El {existe} ya esta en uso")
                self.error.pack()

            return  # Salir de la función si el correo o usuario ya existen

        sql = "INSERT INTO `usuarios` (`correo`, `usuario`, `contraseña`,`icono`) VALUES (%s, %s, %s, %s)"
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (self.correo.get(), self.usuario.get(), self.contraseña.get(),icono_ruta ))
            conexion.commit()
            cursor.close()

            messagebox.showinfo("Exito","Cuenta creada correctamente")
            self.root.destroy() 
            Login() 
        except pymysql.MySQLError as e:
            print(f"Error al insertar los datos: {e}")



class principal():
    def __init__(self):

        self.root = ctk.CTk()
        self.root.title("Login")
        self.root.iconbitmap(os.path.join(carpeta_imagenes, "logo.ico"))
        self.root.geometry("1000x600+280+80")
        self.root.resizable(False, False)
        
        self.usuario_sesion=cargar_sesion()

        self.frameDerecha=ctk.CTkFrame(self.root,border_color="black",width=150)
        self.frameDerecha.pack(side="left",fill="both")

        self.framePersona=ctk.CTkFrame(self.root,width=100,height=40,border_color="black")
        self.framePersona.pack(side="top",anchor="ne")
        self.usuarioPersona=ctk.CTkButton(self.framePersona,command=self.configuracionUsuario,fg_color=("gray77","gray21"),hover_color=("gray68","gray18"),hover=True)
        self.usuarioPersona.pack(expand=True)
        self.root.mainloop()
    def configuracionUsuario(self):
        self.frameConfiguracion=ctk.CTkFrame(self.root)
        self.frameConfiguracion.pack(expand=True)
        self.cerrraSesion=ctk.CTkButton(self.frameConfiguracion,command=lambda:cerrar_sesion(self))
        self.cerrraSesion.pack()


# Iniciar la aplicación
# if __name__ == "__main__":
#     Login()
# usuario_sesion=cargar_sesion()
# if usuario_sesion:
#     principal()
# else:
#     Login()

