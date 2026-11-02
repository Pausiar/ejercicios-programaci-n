# experimento_memoria.py
import httpx

url = "http://localhost:11434/api/generate"

cache = ""

while True:
    prompt = input("\nUsuario: ")

    cache += f"Usuario: {prompt}\n"
    
    res = httpx.post(
        url,
        json={
            "model": "llama3.2:3b",
            "prompt": cache,
            "stream": False
        },
        timeout=30.0
    )
    respuesta = res.json()["response"].strip()
    cache += f"Modelo: {respuesta}\n"
    print("Modelo:", respuesta)
