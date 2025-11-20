from pathlib import Path
import pandas as pd
from pypmml import Model, PMMLContext
from gui import launch_gui  # importamos la GUI

# =========================
# CARGAR MODELO PMML
# =========================
PMMLContext.getOrCreate(gateway="jpype")
BASE_DIR = Path(__file__).resolve().parent
model_path = BASE_DIR / "salary_model.pmml"

if not model_path.exists():
    raise FileNotFoundError(f"No se encontró el archivo PMML en {model_path}")

model = Model.load(str(model_path))
print("✅ Modelo cargado correctamente")

# =========================
# FUNCIÓN DE PREDICCIÓN
# =========================
def predict_salary(input_dict):
    """
    input_dict: diccionario con los mismos nombres de columnas que tu PMML
    """
    data = pd.DataFrame([input_dict])
    prediction = model.predict(data)
    return prediction

# =========================
# LANZAR GUI
# =========================
launch_gui(predict_salary)
