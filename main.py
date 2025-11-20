from pypmml import Model, PMMLContext
import pandas as pd
from pathlib import Path

# 1. Inicializar pypmml usando JPype
PMMLContext.getOrCreate(gateway="jpype")

# 2. Ruta al PMML
BASE_DIR = Path(__file__).resolve().parent
model_path = BASE_DIR / "salary_model.pmml"

print("Model path:", model_path)
print("¿Existe el archivo?:", model_path.exists())

# 3. Cargar el modelo
model = Model.load(str(model_path))
print("✅ Modelo cargado correctamente")


# 4. DataFrame con TODAS las columnas posibles (relleno incluido)
data = pd.DataFrame([{
    # ✔ Necesarias para el PMML
    "company_location": "Germany",
    "company_size": "M",
    "experience_level": "SE",
    "remote_ratio": 100,
    "years_experience": 7.0,
    "job_description_length": 120,

    # ✔ Columnas adicionales (relleno harmless)
    "job_title": "Data Scientist",
    "employee_residence": "DE",
    "education_required": "Bachelor",
    "industry": "Software",
    "benefits_score": 3.7,
    "contract_type": "Full-Time"
}])

print("\n📦 Datos enviados al modelo:")
print(data)

# 5. Ejecutar predicción
prediction = model.predict(data)

print("\n🎯 Predicción:")
print(prediction)
