import tkinter as tk
from tkinter import messagebox, simpledialog

productos = {
    "Camiseta": {"precio": 45000, "stock": 10, "almacen": 0, "vendidos": 0},
    "Pantalón": {"precio": 85000, "stock": 10, "almacen": 0, "vendidos": 0},
    "Zapatos": {"precio": 180000, "stock": 10, "almacen": 0, "vendidos": 0},
    "Gorra": {"precio": 35000, "stock": 10, "almacen": 0, "vendidos": 0},
    "Chaqueta": {"precio": 160000, "stock": 10, "almacen": 0, "vendidos": 0},
    "Sudadera": {"precio": 120000, "stock": 10, "almacen": 0, "vendidos": 0},
    "Bufanda": {"precio": 30000, "stock": 10, "almacen": 0, "vendidos": 0},
    "Calcetines": {"precio": 18000, "stock": 10, "almacen": 0, "vendidos": 0},
    "Cinturón": {"precio": 40000, "stock": 10, "almacen": 0, "vendidos": 0},
    "Vestido": {"precio": 140000, "stock": 10, "almacen": 0, "vendidos": 0},
    "Falda": {"precio": 70000, "stock": 10, "almacen": 0, "vendidos": 0},
    "Blusa": {"precio": 65000, "stock": 10, "almacen": 0, "vendidos": 0},
    "Short": {"precio": 55000, "stock": 10, "almacen": 0, "vendidos": 0},
    "Tenis": {"precio": 220000, "stock": 10, "almacen": 0, "vendidos": 0},
    "Sandalias": {"precio": 90000, "stock": 10, "almacen": 0, "vendidos": 0},
    "Bolso": {"precio": 130000, "stock": 10, "almacen": 0, "vendidos": 0},
    "Reloj": {"precio": 250000, "stock": 10, "almacen": 0, "vendidos": 0},
    "Pulsera": {"precio": 25000, "stock": 10, "almacen": 0, "vendidos": 0},
    "Lentes": {"precio": 95000, "stock": 10, "almacen": 0, "vendidos": 0},
    "Pijama": {"precio": 80000, "stock": 10, "almacen": 0, "vendidos": 0}
}

dinero_total = 0
carrito = []


def actualizar_lista():
    lista_productos.delete(0, tk.END)

    for nombre, datos in productos.items():
        lista_productos.insert(
            tk.END,
            f"{nombre} | ${datos['precio']} | Stock: {datos['stock']}"
        )


def comprar_producto():
    seleccion = lista_productos.curselection()

    if not seleccion:
        messagebox.showwarning("Error", "Seleccione un producto")
        return

    nombre = list(productos.keys())[seleccion[0]]
    stock = productos[nombre]["stock"]
    precio = productos[nombre]["precio"]

    if stock <= 0:
        messagebox.showerror("Sin stock", "Producto agotado")
        return

    cantidad = simpledialog.askinteger(
        "Cantidad",
        f"¿Cuántos {nombre}? (Stock: {stock})"
    )

    if cantidad is None:
        return

    if cantidad <= 0:
        messagebox.showerror("Error", "Cantidad inválida")
        return

    if cantidad > stock:
        messagebox.showerror("Error", "No hay suficiente stock")
        return

    subtotal = cantidad * precio

    if messagebox.askyesno(
        "Confirmar",
        f"{nombre} x{cantidad}\nTotal: ${subtotal}\n¿Agregar?"
    ):

        productos[nombre]["stock"] -= cantidad
        productos[nombre]["vendidos"] += cantidad

        carrito.append({
            "nombre": nombre,
            "cantidad": cantidad,
            "subtotal": subtotal
        })

        actualizar_lista()


def finalizar_compra():
    global dinero_total

    if not carrito:
        messagebox.showwarning("Carrito vacío", "No hay productos")
        return

    total = sum(i["subtotal"] for i in carrito)

    factura = "FACTURA\n\n"

    for item in carrito:
        factura += (
            f"{item['nombre']} x{item['cantidad']} "
            f"= ${item['subtotal']}\n"
        )

    factura += f"\nTOTAL: ${total}"

    dinero_total += total
    carrito.clear()

    messagebox.showinfo("Compra", factura)


def quitar_producto():

    if not carrito:
        messagebox.showwarning(
            "Carrito vacío",
            "No hay productos en el carrito"
        )
        return

    ventana_quitar = tk.Toplevel()
    ventana_quitar.title("Quitar productos")
    ventana_quitar.geometry("400x400")
    ventana_quitar.config(bg="black")

    lista_carrito = tk.Listbox(
        ventana_quitar,
        width=40,
        height=10,
        font=("Calibri", 12)
    )

    lista_carrito.pack(pady=10)

    for item in carrito:
        lista_carrito.insert(
            tk.END,
            f"{item['nombre']} x{item['cantidad']}"
        )

    def quitar_cantidad():

        seleccion = lista_carrito.curselection()

        if not seleccion:
            messagebox.showwarning("Error", "Seleccione un producto")
            return

        indice = seleccion[0]
        item = carrito[indice]

        cantidad = simpledialog.askinteger(
            "Quitar",
            f"¿Cuántos {item['nombre']} desea quitar?\nTiene: {item['cantidad']}"
        )

        if cantidad is None:
            return

        if cantidad <= 0:
            messagebox.showerror("Error", "Cantidad inválida")
            return

        if cantidad > item['cantidad']:
            messagebox.showerror("Error", "Cantidad inválida")
            return

        productos[item['nombre']]['stock'] += cantidad
        productos[item['nombre']]['vendidos'] -= cantidad

        item['cantidad'] -= cantidad
        item['subtotal'] -= (
            cantidad * productos[item['nombre']]['precio']
        )

        if item['cantidad'] == 0:
            carrito.pop(indice)

        actualizar_lista()
        ventana_quitar.destroy()

    tk.Button(
        ventana_quitar,
        text="Quitar cantidad",
        bg="white",
        font=("Calibri", 14),
        command=quitar_cantidad
    ).pack(pady=10)


def ingresar_cliente():

    titulo.pack_forget()
    btn_cliente.pack_forget()
    btn_dueno.pack_forget()
    btn_salir.pack_forget()

    titulo_cliente.pack(pady=20)
    lista_productos.pack(pady=10)
    frame_cliente.pack(pady=10)


def volver_inicio():

    titulo_cliente.pack_forget()
    lista_productos.pack_forget()
    frame_cliente.pack_forget()

    titulo.pack(pady=100)
    btn_cliente.pack(pady=10)
    btn_dueno.pack(pady=10)
    btn_salir.pack(pady=20)


def abrir_panel_dueno():

    if simpledialog.askstring(
        "Contraseña",
        "Ingrese contraseña:",
        show="*"
    ) != "1234":

        messagebox.showerror(
            "Error",
            "Contraseña incorrecta"
        )
        return

    panel = tk.Toplevel()
    panel.title("Panel Dueño")
    panel.attributes("-fullscreen", True)
    panel.config(bg="black")

    # =========================
    # SCROLL PANEL DUEÑO
    # =========================

    canvas_panel = tk.Canvas(
        panel,
        bg="black",
        highlightthickness=0
    )

    scrollbar_panel = tk.Scrollbar(
        panel,
        orient="vertical",
        command=canvas_panel.yview
    )

    scrollable_panel = tk.Frame(
        canvas_panel,
        bg="black"
    )

    scrollable_panel.bind(
        "<Configure>",
        lambda e: canvas_panel.configure(
            scrollregion=canvas_panel.bbox("all")
        )
    )

    canvas_panel.create_window(
        (0, 0),
        window=scrollable_panel,
        anchor="nw"
    )

    canvas_panel.configure(
        yscrollcommand=scrollbar_panel.set
    )

    canvas_panel.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar_panel.pack(
        side="right",
        fill="y"
    )

    # RUEDA RATÓN PANEL

    def mover_rueda_panel(event):

        if event.delta:
            canvas_panel.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        elif event.num == 4:
            canvas_panel.yview_scroll(-1, "units")

        elif event.num == 5:
            canvas_panel.yview_scroll(1, "units")

    panel.bind_all("<MouseWheel>", mover_rueda_panel)
    panel.bind_all("<Button-4>", mover_rueda_panel)
    panel.bind_all("<Button-5>", mover_rueda_panel)

    tk.Label(
        scrollable_panel,
        text="Panel del Dueño",
        font=("Calibri", 50, "bold"),
        bg="black",
        fg="white"
    ).pack(pady=10)

    lista_info = tk.Listbox(
        scrollable_panel,
        width=80,
        height=22,
        font=("Calibri", 18)
    )

    lista_info.pack(pady=20)

    def mostrar_info():

        lista_info.delete(0, tk.END)

        lista_info.insert(
            tk.END,
            f"DINERO TOTAL: ${dinero_total}"
        )

        lista_info.insert(
            tk.END,
            "------------------------------------------"
        )

        for nombre, datos in productos.items():

            lista_info.insert(
                tk.END,
                f"{nombre} | "
                f"Tienda: {datos['stock']} | "
                f"Almacén: {datos['almacen']}"
            )

    def volver():
        panel.destroy()

    tk.Button(
        scrollable_panel,
        text="Volver",
        bg="gray",
        fg="white",
        width=20,
        font=("Calibri", 14),
        command=volver
    ).pack(pady=15)

    mostrar_info()


# =========================
# VENTANA PRINCIPAL
# =========================

ventana = tk.Tk()
ventana.title("Colombia Style")
ventana.attributes("-fullscreen", True)
ventana.config(bg="black")

# =========================
# SCROLL TODA LA APP
# =========================

canvas = tk.Canvas(
    ventana,
    bg="black",
    highlightthickness=0
)

scrollbar = tk.Scrollbar(
    ventana,
    orient="vertical",
    command=canvas.yview
)

scrollable_frame = tk.Frame(
    canvas,
    bg="black"
)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window(
    (0, 0),
    window=scrollable_frame,
    anchor="nw"
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)

# =========================
# RUEDA DEL RATÓN
# =========================

def mover_rueda(event):

    if event.delta:
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    elif event.num == 4:
        canvas.yview_scroll(-1, "units")

    elif event.num == 5:
        canvas.yview_scroll(1, "units")


ventana.bind_all("<MouseWheel>", mover_rueda)
ventana.bind_all("<Button-4>", mover_rueda)
ventana.bind_all("<Button-5>", mover_rueda)

# =========================
# WIDGETS
# =========================

titulo = tk.Label(
    scrollable_frame,
    text="Colombia Style",
    font=("Calibri", 80, "bold"),
    bg="black",
    fg="white"
)

titulo.pack(pady=100)

titulo_cliente = tk.Label(
    scrollable_frame,
    text="Panel del Comprador",
    font=("Calibri", 40, "bold"),
    bg="black",
    fg="white"
)

btn_cliente = tk.Button(
    scrollable_frame,
    text="Ingresar como Cliente",
    font=("Calibri", 25),
    bg="white",
    width=30,
    command=ingresar_cliente
)

btn_cliente.pack(pady=10)

btn_dueno = tk.Button(
    scrollable_frame,
    text="Ingresar como Dueño",
    font=("Calibri", 25),
    bg="white",
    width=30,
    command=abrir_panel_dueno
)

btn_dueno.pack(pady=10)

lista_productos = tk.Listbox(
    scrollable_frame,
    width=80,
    height=20,
    font=("Calibri", 18)
)

actualizar_lista()

frame_cliente = tk.Frame(
    scrollable_frame,
    bg="black"
)

tk.Button(
    frame_cliente,
    text="Agregar al carrito",
    bg="white",
    width=35,
    font=("Calibri", 20),
    command=comprar_producto
).pack(pady=5)

tk.Button(
    frame_cliente,
    text="Quitar producto",
    bg="white",
    width=35,
    font=("Calibri", 20),
    command=quitar_producto
).pack(pady=5)

tk.Button(
    frame_cliente,
    text="Finalizar compra",
    bg="white",
    width=35,
    font=("Calibri", 20),
    command=finalizar_compra
).pack(pady=5)

tk.Button(
    frame_cliente,
    text="Volver",
    bg="grey",
    width=20,
    font=("Calibri", 14),
    command=volver_inicio
).pack(pady=5)

btn_salir = tk.Button(
    scrollable_frame,
    text="Salir",
    bg="red",
    fg="white",
    font=("Calibri", 18),
    command=ventana.destroy
)

btn_salir.pack(pady=20)

ventana.mainloop()