import logging

import httpx
from pydantic import ValidationError

from ud01_contratos.contratos import (
    ContactoCliente,
    ResultadoExtraccion,
    ResultadoRechazado,
    ResultadoValido,
)

logger = logging.getLogger(__name__)


def extraer_contacto(texto_usuario: str) -> ResultadoExtraccion:
    url = "http://localhost:11434/api/chat"
    
    messages = [
        {
            "role": "system",
            "content": (
                "Eres un extractor de datos de clientes. Analiza el mensaje del usuario y extrae "
                "los datos solicitados cumpliendo estrictamente con el esquema esperado."
            )
        },
        {
            "role": "user",
            "content": texto_usuario
        }
    ]
    
    # 1. Llamada HTTP: captura de errores de comunicación de infraestructura
    try:
        response = httpx.post(
            url,
            json={
                "model": "qwen2.5:0.5b",
                "messages": messages,
                "format": ContactoCliente.model_json_schema(), # Indicación de esquema para orientar la generación
                "stream": False
            },
            timeout=30.0
        )
        response.raise_for_status()
    except httpx.HTTPError as e:
        # Error de comunicación con la infraestructura
        raise ConnectionError(f"Error de comunicación con Ollama: {e}") from e

    raw_content = response.json()["message"]["content"]
    
    try:
        contacto = ContactoCliente.model_validate_json(raw_content)
    except ValidationError as error:
        motivo = str(error)
        logger.warning("Propuesta de contacto rechazada: %s", motivo)
        return ResultadoRechazado(motivo=motivo, raw_content=raw_content)

    return ResultadoValido(contacto=contacto, raw_content=raw_content)