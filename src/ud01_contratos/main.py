from ud01_contratos.cliente_ollama import extraer_contacto

mensajes = [
    (
        "Caso 1",
        "Hola, quiero comprar pavimentos cerámicos. Mi correo es usuario@@correo.",
    ),
    (
        "Caso 2",
        "Hola, solo quiero presentar una reclamación por un pedido roto. "
        "Mi correo es laura@empresa.com.",
    ),
]

try:
    for caso, mensaje in mensajes:
        print(f"--- {caso} ---")
        resultado = extraer_contacto(mensaje)
        print(f"Propuesta del modelo (raw_content): {resultado.raw_content}")
        if resultado.valido:
            cliente = resultado.contacto
            print("--- CONTRATO VALIDADO CON ÉXITO ---")
            print(f"Tipo devuelto: {type(cliente)}")
            print(f"Nombre:        {cliente.nombre}")
            print(f"Email:         {cliente.email}")
            print(f"Intención:     {cliente.intencion}")
        else:
            print(f"Propuesta rechazada por el contrato de datos: {resultado.motivo}")
except ConnectionError as e:
    # Error de infraestructura: fallo de red o caída del servicio Ollama
    print(f"Error de infraestructura: {e}")