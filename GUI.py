import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

import pandas as pd
from pypmml import Model, PMMLContext

# =========================
#  CARGA DEL MODELO PMML
# =========================
PMMLContext.getOrCreate(gateway="jpype")

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "salary_model.pmml"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"No se encontró el archivo PMML en: {MODEL_PATH}")

model = Model.load(str(MODEL_PATH))

# Nombre de la columna objetivo en el resultado del modelo
TARGET_COLUMN = "salary_level"   # <-- cámbialo si tu PMML usa otro nombre


# Mapeo de nivel salarial -> texto y rango (ajusta a tu proyecto real)
SALARY_RANGES = {
    "low": ("Salario bajo", "≈ 0 – 40 000 USD"),
    "medium": ("Salario medio", "≈ 40 001 – 80 000 USD"),
    "high": ("Salario alto", "≈ 80 001 USD o más"),
}


# =========================
#  FUNCIÓN DE PREDICCIÓN
# =========================
def predict_salary():
    try:
        # Obtener valores desde la GUI
        data_dict = {
            "company_location": var_company_location.get(),
            "company_size": var_company_size.get(),
            "experience_level": var_experience_level.get(),
            "remote_ratio": int(var_remote_ratio.get()),
            "years_experience": float(var_years_experience.get()),
            "job_description_length": float(var_job_description.get()),
            "job_title": var_job_title.get(),
            "employee_residence": var_employee_residence.get(),
            "education_required": var_education_required.get(),
            "industry": var_industry.get(),
            "benefits_score": float(var_benefits_score.get()),
            "contract_type": var_contract_type.get(),
        }

        # Validar que no haya campos vacíos
        for key, value in data_dict.items():
            if isinstance(value, str) and value.strip() == "":
                messagebox.showerror(
                    "Datos incompletos",
                    f"El campo '{key}' no puede estar vacío."
                )
                return

        # Crear DataFrame con una sola fila
        df = pd.DataFrame([data_dict])

        # Llamar al modelo
        prediction = model.predict(df)

        # Obtener la clase predicha
        if TARGET_COLUMN not in prediction.columns:
            # Si el nombre no coincide, mostrar todo el resultado
            messagebox.showinfo(
                "Resultado",
                "No se encontró la columna objetivo en la predicción.\n\n"
                f"Salida completa del modelo:\n{prediction.to_string(index=False)}"
            )
            return

        salary_class = str(prediction[TARGET_COLUMN].iloc[0])
        key = salary_class.lower()

        if key in SALARY_RANGES:
            label_esp, rango = SALARY_RANGES[key]
            msg = (
                f"Nivel salarial predicho: {label_esp} ({salary_class})\n\n"
                f"Rango estimado de salario:\n{rango}"
            )
        else:
            msg = f"Nivel salarial predicho por el modelo: {salary_class}"

        messagebox.showinfo("Predicción de salario", msg)

    except ValueError:
        messagebox.showerror(
            "Error en los datos",
            "Verifica que los campos numéricos tengan valores válidos.\n"
            "Ejemplos: años de experiencia = 5, descripción = 120, beneficios = 7.5"
        )
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al predecir:\n{e}")


# =========================
#  CONFIGURACIÓN DE LA GUI
# =========================
root = tk.Tk()
root.title("Predicción de Nivel Salarial - Mercado TI")
root.geometry("900x600")
root.configure(bg="#0f172a")  # azul oscuro

# Estilos modernos con ttk
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Main.TFrame",
    background="#1e293b"
)
style.configure(
    "TLabel",
    background="#1e293b",
    foreground="#e5e7eb",
    font=("Segoe UI", 10)
)
style.configure(
    "Title.TLabel",
    background="#0f172a",
    foreground="#e5e7eb",
    font=("Segoe UI Semibold", 16)
)
style.configure(
    "TButton",
    background="#2563eb",
    foreground="white",
    font=("Segoe UI Semibold", 11),
    padding=6,
    borderwidth=0
)
style.map(
    "TButton",
    background=[("active", "#1d4ed8")]
)
style.configure(
    "TCombobox",
    fieldbackground="#111827",
    background="#111827",
    foreground="#e5e7eb"
)

title_label = ttk.Label(
    root,
    text="Formulario de Predicción de Nivel Salarial",
    style="Title.TLabel",
    anchor="center"
)
title_label.pack(pady=15)

main_frame = ttk.Frame(root, style="Main.TFrame", padding=20)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

# =========================
#  VARIABLES Y OPCIONES
# =========================

var_company_location = tk.StringVar()
var_company_size = tk.StringVar()
var_experience_level = tk.StringVar()
var_remote_ratio = tk.StringVar()
var_years_experience = tk.StringVar()
var_job_description = tk.StringVar()
var_job_title = tk.StringVar()
var_employee_residence = tk.StringVar()
var_education_required = tk.StringVar()
var_industry = tk.StringVar()
var_benefits_score = tk.StringVar()
var_contract_type = tk.StringVar()

company_location_opts = [
    "China", "Canada", "Switzerland", "India", "France", "Germany",
    "United Kingdom", "Singapore", "Austria", "Sweden", "South Korea",
    "Norway", "Netherlands", "United States", "Israel", "Australia",
    "Ireland", "Denmark", "Finland", "Japan"
]

company_size_opts = ["S", "M", "L"]
experience_level_opts = ["EN", "MI", "SE", "EX"]
remote_ratio_opts = ["0", "50", "100"]

job_title_opts = [
    "AI Research Scientist", "AI Software Engineer", "AI Specialist",
    "NLP Engineer", "AI Consultant", "AI Architect", "Principal Data Scientist",
    "Data Analyst", "Autonomous Systems Engineer", "AI Product Manager",
    "Machine Learning Engineer", "Data Engineer", "Research Scientist",
    "ML Ops Engineer", "Robotics Engineer", "Head of AI",
    "Deep Learning Engineer", "Data Scientist", "Machine Learning Researcher",
    "Computer Vision Engineer"
]

employee_residence_opts = [
    "China", "Ireland", "South Korea", "India", "Singapore", "Germany",
    "United Kingdom", "France", "Austria", "Sweden", "Norway", "Israel",
    "United States", "Netherlands", "Denmark", "Switzerland", "Finland",
    "Japan", "Canada", "Australia"
]

education_required_opts = ["Bachelor", "Master", "Associate", "PhD"]

industry_opts = [
    "Automotive", "Media", "Education", "Consulting", "Healthcare", "Gaming",
    "Government", "Telecommunications", "Manufacturing", "Energy",
    "Technology", "Real Estate", "Finance", "Transportation", "Retail"
]

contract_type_opts = ["CT", "FL", "PT", "FT"]


# =========================
#  CREACIÓN DE CAMPOS
# =========================

def create_labeled_combobox(parent, text, row, var, values, col=0):
    label = ttk.Label(parent, text=text)
    label.grid(row=row, column=col, sticky="w", padx=5, pady=5)
    combo = ttk.Combobox(parent, textvariable=var, values=values, state="readonly")
    combo.grid(row=row, column=col + 1, sticky="ew", padx=5, pady=5)
    return combo


def create_labeled_entry(parent, text, row, var, col=0, placeholder=""):
    label = ttk.Label(parent, text=text)
    label.grid(row=row, column=col, sticky="w", padx=5, pady=5)
    entry = ttk.Entry(parent, textvariable=var)
    entry.grid(row=row, column=col + 1, sticky="ew", padx=5, pady=5)
    if placeholder:
        entry.insert(0, placeholder)
    return entry


# Configurar grid
for i in range(4):
    main_frame.columnconfigure(i, weight=1)

row = 0

# Columna izquierda (0,1)
create_labeled_combobox(main_frame, "País de la empresa (company_location):",
                        row, var_company_location, company_location_opts, col=0)
row += 1
create_labeled_combobox(main_frame, "Tamaño de empresa (company_size):",
                        row, var_company_size, company_size_opts, col=0)
row += 1
create_labeled_combobox(main_frame, "Nivel de experiencia (experience_level):",
                        row, var_experience_level, experience_level_opts, col=0)
row += 1
create_labeled_combobox(main_frame, "Porcentaje remoto (remote_ratio):",
                        row, var_remote_ratio, remote_ratio_opts, col=0)
row += 1
create_labeled_entry(main_frame, "Años de experiencia (years_experience):",
                     row, var_years_experience, col=0, placeholder="Ej: 5")
row += 1
create_labeled_entry(main_frame, "Largo descripción puesto (job_description_length):",
                     row, var_job_description, col=0, placeholder="Ej: 120")

# Columna derecha (2,3)
row_right = 0
create_labeled_combobox(main_frame, "Puesto (job_title):",
                        row_right, var_job_title, job_title_opts, col=2)
row_right += 1
create_labeled_combobox(main_frame, "Residencia empleado (employee_residence):",
                        row_right, var_employee_residence, employee_residence_opts, col=2)
row_right += 1
create_labeled_combobox(main_frame, "Educación requerida (education_required):",
                        row_right, var_education_required, education_required_opts, col=2)
row_right += 1
create_labeled_combobox(main_frame, "Industria (industry):",
                        row_right, var_industry, industry_opts, col=2)
row_right += 1
create_labeled_entry(main_frame, "Beneficios (benefits_score 1–10):",
                     row_right, var_benefits_score, col=2, placeholder="Ej: 7.5")
row_right += 1
create_labeled_combobox(main_frame, "Tipo de contrato (contract_type):",
                        row_right, var_contract_type, contract_type_opts, col=2)

# Botón de enviar
button_frame = ttk.Frame(root, style="Main.TFrame")
button_frame.pack(fill="x", padx=20, pady=10)

predict_btn = ttk.Button(
    button_frame,
    text="Predecir salario",
    command=predict_salary
)
predict_btn.pack(pady=5)

root.mainloop()