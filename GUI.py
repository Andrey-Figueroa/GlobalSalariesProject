# gui_completa_con_imagen.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

def launch_gui(predict_function):
    # =====================
    # VENTANA PRINCIPAL DE PREDICCIÓN
    # =====================
    def main_window(user_fullname):
        root = tk.Tk()
        root.title(f"Predicción de Nivel Salarial - {user_fullname}")
        root.geometry("900x700")
        root.configure(bg="#0f172a")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Main.TFrame", background="#1e293b")
        style.configure("TLabel", background="#1e293b", foreground="#e5e7eb", font=("Segoe UI", 10))
        style.configure("Title.TLabel", background="#0f172a", foreground="#e5e7eb", font=("Segoe UI Semibold", 16))
        style.configure("TButton", background="#2563eb", foreground="white", font=("Segoe UI Semibold", 11), padding=6, borderwidth=0)
        style.map("TButton", background=[("active", "#1d4ed8")])
        style.configure("TCombobox", foreground="black", fieldbackground="white", background="white")
        style.map("TCombobox", fieldbackground=[("readonly", "white")], foreground=[("readonly", "black")])

        # Título y saludo
        title_label = ttk.Label(root, text=f"🤖 [QUANTUM-HR] Estimación de Compensación 💰", style="Title.TLabel")
        title_label.pack(pady=10)

        saludo_label = tk.Label(root, text=f"¡Saludos {user_fullname}! Soy QUANTUM-HR, tu Asistente Predictivo 📊",
                                background="#0f172a", foreground="white", font=("Segoe UI", 11))
        saludo_label.pack(pady=5)

        # Botón de Manual
        def abrir_manual():
            manual_window = tk.Toplevel(root)
            manual_window.title("Manual de Uso")
            manual_window.geometry("850x600")  # ventana más grande
            manual_window.configure(bg="#1e293b")

            texto_manual = """
Bienvenido al Manual de Uso de QUANTUM-HR:

A continuación se explica cada campo del formulario:

1. País de la empresa: Seleccione el país donde se encuentra la empresa.
2. Tamaño de empresa: S (Pequeña), M (Mediana), L (Grande).
3. Nivel de experiencia: EN (Entry), MI (Mid), SE (Senior), EX (Expert).
4. Trabajo remoto (%): Porcentaje de trabajo remoto permitido (0, 50, 100).
5. Años de experiencia: Cantidad de años que posee de experiencia profesional.
6. Largo descripción del puesto: Número aproximado de caracteres en la descripción del trabajo.
7. Puesto: El rol que desempeñará el empleado (Data Scientist, AI Software Engineer, ML Engineer).
8. Residencia del empleado: País de residencia del empleado (DE, US, IN).
9. Educación requerida: Nivel educativo requerido para el puesto (Bachelor, Master, PhD).
10. Industria: Sector al que pertenece la empresa (Software, Finance, Healthcare).
11. Tipo de contrato: Full-Time, Part-Time o Contract.

Recuerde:
- Complete todos los campos antes de presionar 'Predecir salario'.
- Ingrese su Nombre y Apellidos en la pantalla de bienvenida.
- Puede consultar este manual en cualquier momento presionando el botón 'Manual de Uso'.
            """
            label = tk.Label(manual_window, text=texto_manual, justify="left", background="#1e293b", foreground="white", font=("Segoe UI", 12))
            label.pack(padx=20, pady=20)
            ttk.Button(manual_window, text="Volver al Formulario", command=manual_window.destroy).pack(pady=15)

        ttk.Button(root, text="Manual de Uso", command=abrir_manual).pack(pady=5)

        # Marco principal del formulario
        main_frame = ttk.Frame(root, style="Main.TFrame", padding=20)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # =========================
        # VARIABLES DEL FORMULARIO
        # =========================
        var_company_location = tk.StringVar(value="Germany")
        var_company_size = tk.StringVar(value="M")
        var_experience_level = tk.StringVar(value="SE")
        var_remote_ratio = tk.StringVar(value="50")
        var_years_experience = tk.StringVar(value="5.0")
        var_job_description = tk.StringVar(value="1250")
        var_job_title = tk.StringVar(value="Data Scientist")
        var_employee_residence = tk.StringVar(value="DE")
        var_education_required = tk.StringVar(value="Bachelor")
        var_industry = tk.StringVar(value="Software")
        var_contract_type = tk.StringVar(value="Full-Time")

        company_location_opts = ["Germany", "United States", "Canada", "France", "India"]
        company_size_opts = ["S", "M", "L"]
        experience_level_opts = ["EN", "MI", "SE", "EX"]
        remote_ratio_opts = ["0", "50", "100"]
        job_title_opts = ["Data Scientist", "AI Software Engineer", "ML Engineer"]
        employee_residence_opts = ["DE", "US", "IN"]
        education_required_opts = ["Bachelor", "Master", "PhD"]
        industry_opts = ["Software", "Finance", "Healthcare"]
        contract_type_opts = ["Full-Time", "Part-Time", "Contract"]

        # Funciones de creación de campos
        def create_labeled_combobox(parent, text, row, var, values, col=0):
            ttk.Label(parent, text=text).grid(row=row, column=col, sticky="w", padx=5, pady=5)
            combo = ttk.Combobox(parent, textvariable=var, values=values, state="readonly")
            combo.grid(row=row, column=col + 1, sticky="ew", padx=5, pady=5)
            return combo

        def create_labeled_entry(parent, text, row, var, col=0, placeholder=""):
            ttk.Label(parent, text=text).grid(row=row, column=col, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(parent, textvariable=var)
            entry.grid(row=row, column=col + 1, sticky="ew", padx=5, pady=5)
            if placeholder:
                entry.insert(0, placeholder)
            return entry

        for i in range(4):
            main_frame.columnconfigure(i, weight=1)

        # =========================
        # CAMPOS DEL FORMULARIO
        # =========================
        # Lado izquierdo
        row = 0
        create_labeled_combobox(main_frame, "País de la empresa:", row, var_company_location, company_location_opts)
        row += 1
        create_labeled_combobox(main_frame, "Tamaño de empresa:", row, var_company_size, company_size_opts)
        row += 1
        create_labeled_combobox(main_frame, "Nivel de experiencia:", row, var_experience_level, experience_level_opts)
        row += 1
        create_labeled_combobox(main_frame, "Trabajo remoto (%):", row, var_remote_ratio, remote_ratio_opts)
        row += 1
        create_labeled_entry(main_frame, "Años de experiencia:", row, var_years_experience)
        row += 1
        create_labeled_entry(main_frame, "Largo descripción del puesto:", row, var_job_description)

        # Lado derecho
        row_r = 0
        create_labeled_combobox(main_frame, "Puesto:", row_r, var_job_title, job_title_opts, col=2)
        row_r += 1
        create_labeled_combobox(main_frame, "Residencia del empleado:", row_r, var_employee_residence, employee_residence_opts, col=2)
        row_r += 1
        create_labeled_combobox(main_frame, "Educación requerida:", row_r, var_education_required, education_required_opts, col=2)
        row_r += 1
        create_labeled_combobox(main_frame, "Industria:", row_r, var_industry, industry_opts, col=2)
        row_r += 1
        create_labeled_combobox(main_frame, "Tipo de contrato:", row_r, var_contract_type, contract_type_opts, col=2)

        # =========================
        # RESULTADO QUANTUM-HR
        # =========================
        resultado_label = tk.Label(root, text="", justify="left", background="#1e293b", foreground="white",
                                   font=("Segoe UI", 11), anchor="w")
        resultado_label.pack(fill="x", padx=20, pady=10)

        # Función de predicción
        def on_predict():
            input_dict = {
                "company_location": var_company_location.get(),
                "company_size": var_company_size.get(),
                "experience_level": var_experience_level.get(),
                "remote_ratio": int(var_remote_ratio.get()),
                "years_experience": float(var_years_experience.get()),
                "job_description_length": int(var_job_description.get()),
                "job_title": var_job_title.get(),
                "employee_residence": var_employee_residence.get(),
                "education_required": var_education_required.get(),
                "industry": var_industry.get(),
                "contract_type": var_contract_type.get()
            }
            try:
                pred_df = predict_function(input_dict)
                prediction_value = str(pred_df.iloc[0, 0]).strip().lower()  # conversión robusta

                if prediction_value in ["alta", "high", "premium"]:
                    texto = f"""
🚀 [QUANTUM-HR] Reporte de Valoración de Élite 💎
¡Felicidades {user_fullname}! Soy QUANTUM-HR, y mi análisis predictivo ha clasificado tu perfil en la banda,
 de talento más alta del sector de IA. Catalogada en: HIGH🧠

Compensación Anual Base: La cifra se ubicará por encima de los $120,000 USD 💰.
Clasificación de QUANTUM-HR: Este paquete salarial es "Excepcional".
                    """
                else:
                    texto = f"""
🤖 [QUANTUM-HR] Estimación de Compensación 💰
¡Saludos {user_fullname}! Soy QUANTUM-HR, tu Asistente Predictivo 📊

Mi análisis indica que la compensación base para este rol se sitúa en el rango "{pred_df.iloc[0,0]}" 🚀.

Compensación Anual Base: La cifra se encontrará por debajo de los $115,000 USD 🎯.
Clasificación de QUANTUM-HR: Hemos definido este paquete como "Estratégico" para tu trayectoria.
                    """

                resultado_label.config(text="")
                resultado_label.update()
                resultado_label.config(text=texto)

            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}")

        button_frame = ttk.Frame(root, style="Main.TFrame")
        button_frame.pack(fill="x", padx=20, pady=10)
        ttk.Button(button_frame, text="Predecir salario", command=on_predict).pack(pady=5)

        root.mainloop()

    # =====================
    # VENTANA DE BIENVENIDA CON IMAGEN
    # =====================
    welcome_window = tk.Tk()
    welcome_window.title("Bienvenido")
    welcome_window.geometry("800x800")
    welcome_window.configure(bg="#0f172a")

    ttk.Label(welcome_window, text="🤖 QUANTUM-HR te da la bienvenida al programa de predicción salarial", 
              font=("Segoe UI Semibold", 18), background="#0f172a", foreground="#e5e7eb").pack(pady=20)

   
    # Imagen de bienvenida
    image_path = r"C:\Users\andre\Documents\GlobalSalariesProject\GlobalSalariesProject\QUANTUM-HR.jpg"
    image = Image.open(image_path)
    image = image.resize((250, 250))  # ajustar tamaño
    photo = ImageTk.PhotoImage(image)
    img_label = tk.Label(welcome_window, image=photo, bg="#0f172a")
    img_label.image = photo
    img_label.pack(pady=10)


    # Campos Nombre y Apellidos
    name_var = tk.StringVar()
    surname_var = tk.StringVar()
    ttk.Label(welcome_window, text="Nombre:", background="#0f172a", foreground="#e5e7eb").pack(pady=5)
    ttk.Entry(welcome_window, textvariable=name_var, width=30).pack(pady=5)
    ttk.Label(welcome_window, text="Apellidos:", background="#0f172a", foreground="#e5e7eb").pack(pady=5)
    ttk.Entry(welcome_window, textvariable=surname_var, width=30).pack(pady=5)

    def start_program():
        name = name_var.get().strip()
        surname = surname_var.get().strip()
        if not name:
            messagebox.showwarning("Aviso", "Por favor ingrese su nombre.")
            return
        if not surname:
            messagebox.showwarning("Aviso", "Por favor ingrese sus apellidos.")
            return
        fullname = f"{name} {surname}"
        welcome_window.destroy()
        main_window(fullname)

    ttk.Button(welcome_window, text="Iniciar", command=start_program).pack(pady=20)

    welcome_window.mainloop()
