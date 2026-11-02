# crash_script.py
import json
import httpx

prompt = "Extrae los datos del cliente: Me llamo Laura García y mi correo es laura@empresa.com. Devuélveme exclusivamente un JSON."

response = httpx.post(
    "http://localhost:11434/api/generate",
    json={"model": "qwen2.5:0.5b", "prompt": prompt, "stream": False},
    timeout=30.0
)

raw_text = response.json()["response"]
print("--- RESPUESTA BRUTA DEL MODELO ---")
print(raw_text)

print("\n--- INTENTO DE PARSEO DIRECTO ---")
try:
    data = json.loads(raw_text)
    print("Datos procesados con éxito:", data)
except json.JSONDecodeError as e:
    print(f"FALLO DE PARSEO: {e}")