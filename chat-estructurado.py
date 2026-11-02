# chat_ingenuo.py
import httpx

url = "http://localhost:11434/api/generate"
contexto_texto = ""

print("Iniciando Chat Ingenuo (Escribe 'salir' para terminar)\n")

while True:
    mensaje = input("Usuario: ")
    if mensaje.lower() in ("salir", "exit"):
        break

    # Concatenamos la nueva pregunta al texto acumulado
    contexto_texto += f"\nUsuario: {mensaje}\nAsistente:"

    response = httpx.post(url, json={
        "model": "qwen2.5:0.5b",
        "prompt": contexto_texto,
        "stream": False
    }, timeout=30.0)

    respuesta = response.json()["response"].strip()
    contexto_texto += f" {respuesta}"

    print(f"Asistente: {respuesta}\n")