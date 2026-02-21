import tkinter as tk
from tkinter import ttk, messagebox


class AppTk:
    def __init__(self, servicio):
        self.servicio = servicio

        # Ventana principal
        self.root = tk.Tk()
        self.root.title("Menú del Restaurante (Tkinter)")
        self.root.geometry("860x520")

        # ======= FORM =======
        frm = ttk.LabelFrame(self.root, text="Formulario Platillo")
        frm.pack(fill="x", padx=10, pady=10)

        self.var_id = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_precio = tk.StringVar()
        self.var_categoria = tk.StringVar()

        ttk.Label(frm, text="ID").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        ttk.Entry(frm, textvariable=self.var_id, width=15).grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(frm, text="Nombre").grid(row=0, column=2, padx=6, pady=6, sticky="w")
        ttk.Entry(frm, textvariable=self.var_nombre, width=30).grid(row=0, column=3, padx=6, pady=6)

        ttk.Label(frm, text="Precio").grid(row=1, column=0, padx=6, pady=6, sticky="w")
        ttk.Entry(frm, textvariable=self.var_precio, width=15).grid(row=1, column=1, padx=6, pady=6)

        ttk.Label(frm, text="Categoría").grid(row=1, column=2, padx=6, pady=6, sticky="w")
        ttk.Entry(frm, textvariable=self.var_categoria, width=30).grid(row=1, column=3, padx=6, pady=6)

        # ======= BOTONES =======
        btns = ttk.Frame(self.root)
        btns.pack(fill="x", padx=10, pady=5)

        ttk.Button(btns, text="Agregar", command=self.on_agregar).pack(side="left", padx=5)
        ttk.Button(btns, text="Actualizar", command=self.on_actualizar).pack(side="left", padx=5)
        ttk.Button(btns, text="Eliminar", command=self.on_eliminar).pack(side="left", padx=5)
        ttk.Button(btns, text="Limpiar", command=self.on_limpiar).pack(side="left", padx=5)
        ttk.Button(btns, text="Guardar", command=self.on_guardar).pack(side="left", padx=5)

        # ======= TABLA =======
        tabla_frame = ttk.LabelFrame(self.root, text="Listado")
        tabla_frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("id", "nombre", "precio", "categoria")
        self.tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=12)

        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("categoria", text="Categoría")

        self.tree.column("id", width=80, anchor="center")
        self.tree.column("nombre", width=280)
        self.tree.column("precio", width=120, anchor="e")
        self.tree.column("categoria", width=220)

        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

        # Evento: click en fila -> llena formulario
        self.tree.bind("<<TreeviewSelect>>", self.on_select_row)

        # Cargar datos iniciales desde el servicio
        self.refrescar_tabla()

        # Al cerrar ventana: guardar
        self.root.protocol("WM_DELETE_WINDOW", self.on_cerrar)

    # ========================
    # UTILIDADES UI
    # ========================
    def run(self):
        self.root.mainloop()

    def refrescar_tabla(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Pintar desde memoria
        for p in self.servicio.platillos:
            self.tree.insert("", "end", values=(
                p.get_id(),
                p.get_nombre(),
                f"{p.get_precio():.2f}",
                p.get_categoria()
            ))

    def leer_formulario(self):
        try:
            id_p = int(self.var_id.get().strip())
            nombre = self.var_nombre.get().strip()
            precio = float(self.var_precio.get().strip())
            categoria = self.var_categoria.get().strip()

            if not nombre or not categoria:
                raise ValueError("Nombre y Categoría no pueden estar vacíos")

            return id_p, nombre, precio, categoria
        except Exception as e:
            messagebox.showerror("Datos inválidos", f"Revisa el formulario.\nDetalle: {e}")
            return None

    def on_limpiar(self):
        self.var_id.set("")
        self.var_nombre.set("")
        self.var_precio.set("")
        self.var_categoria.set("")
        self.tree.selection_remove(self.tree.selection())

    def on_select_row(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0], "values")
        self.var_id.set(values[0])
        self.var_nombre.set(values[1])
        self.var_precio.set(values[2])
        self.var_categoria.set(values[3])

    # ========================
    # EVENTOS (CRUD)
    # ========================
    def on_agregar(self):
        datos = self.leer_formulario()
        if not datos:
            return
        id_p, nombre, precio, categoria = datos

        ok, msg = self.servicio.agregar_platillo_gui(id_p, nombre, precio, categoria)
        if ok:
            self.refrescar_tabla()
            self.on_limpiar()
            messagebox.showinfo("OK", msg)
        else:
            messagebox.showwarning("Atención", msg)

    def on_actualizar(self):
        datos = self.leer_formulario()
        if not datos:
            return
        id_p, nombre, precio, categoria = datos

        ok, msg = self.servicio.actualizar_platillo_gui(id_p, nombre, precio, categoria)
        if ok:
            self.refrescar_tabla()
            messagebox.showinfo("OK", msg)
        else:
            messagebox.showwarning("Atención", msg)

    def on_eliminar(self):
        try:
            id_p = int(self.var_id.get().strip())
        except Exception:
            messagebox.showwarning("Atención", "Selecciona un platillo (ID) para eliminar.")
            return

        if not messagebox.askyesno("Confirmar", f"¿Eliminar el platillo ID {id_p}?"):
            return

        ok, msg = self.servicio.eliminar_platillo_gui(id_p)
        if ok:
            self.refrescar_tabla()
            self.on_limpiar()
            messagebox.showinfo("OK", msg)
        else:
            messagebox.showwarning("Atención", msg)

    def on_guardar(self):
        self.servicio.guardar_en_archivo()
        messagebox.showinfo("Guardado", "Cambios guardados en el archivo.")

    def on_cerrar(self):
        # Guardado al salir
        self.servicio.guardar_en_archivo()
        self.root.destroy()