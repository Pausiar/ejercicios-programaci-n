import pytest
from pydantic import ValidationError

from ud01_contratos.contratos import ContactoCliente


def campos_y_tipos_de_error(raw_json: str) -> dict[str, list[str]]:
    with pytest.raises(ValidationError) as exc_info:
        ContactoCliente.model_validate_json(raw_json)

    errores: dict[str, list[str]] = {}
    for error in exc_info.value.errors():
        campo = str(error["loc"][0]) if error["loc"] else "<raíz del JSON>"
        errores.setdefault(campo, []).append(error["type"])
    return errores


def test_contrato_valido_nominal():
    raw_json = '{"nombre": "Laura García", "email": "laura@empresa.com", "intencion": "compra"}'
    obj = ContactoCliente.model_validate_json(raw_json)
    assert obj.nombre == "Laura García"
    assert obj.email == "laura@empresa.com"
    assert obj.intencion == "compra"


def test_contrato_rechaza_campos_faltantes():
    assert campos_y_tipos_de_error('{"nombre": "Laura García"}') == {
        "email": ["missing"],
        "intencion": ["missing"],
    }


def test_contrato_rechaza_tipo_incompatible():
    raw_json = '{"nombre": ["Laura", "García"], "email": "laura@empresa.com", "intencion": "compra"}'
    assert campos_y_tipos_de_error(raw_json) == {"nombre": ["string_type"]}


def test_contrato_rechaza_nombre_demasiado_corto():
    raw_json = '{"nombre": "L", "email": "laura@empresa.com", "intencion": "compra"}'
    assert campos_y_tipos_de_error(raw_json) == {"nombre": ["string_too_short"]}


def test_validador_rechaza_email_invalido():
    raw_json = '{"nombre": "Laura García", "email": "usuario@@correo", "intencion": "compra"}'
    with pytest.raises(ValidationError, match="email") as exc_info:
        ContactoCliente.model_validate_json(raw_json)

    errores = exc_info.value.errors()
    assert [(error["loc"], error["type"]) for error in errores] == [(("email",), "value_error")]
    assert "El email" in errores[0]["msg"]


def test_validador_rechaza_intencion_no_admitida():
    raw_json = '{"nombre": "Laura García", "email": "laura@empresa.com", "intencion": "reclamo"}'
    with pytest.raises(ValidationError, match="intencion") as exc_info:
        ContactoCliente.model_validate_json(raw_json)

    errores = exc_info.value.errors()
    assert [(error["loc"], error["type"]) for error in errores] == [(("intencion",), "value_error")]
    assert "consulta, compra, soporte" in errores[0]["msg"]


def test_contrato_rechaza_multiples_defectos():
    raw_json = '{"nombre": "L", "email": "usuario@@correo", "intencion": "reclamo"}'
    assert campos_y_tipos_de_error(raw_json) == {
        "nombre": ["string_too_short"],
        "email": ["value_error"],
        "intencion": ["value_error"],
    }


def test_contrato_rechaza_texto_libre_no_json():
    texto_libre = "¡Claro! Aquí tienes los datos: Laura García, laura@empresa.com"
    with pytest.raises(ValidationError, match="json_invalid") as exc_info:
        ContactoCliente.model_validate_json(texto_libre)

    errores = exc_info.value.errors()
    assert [error["type"] for error in errores] == ["json_invalid"]
    assert errores[0]["loc"] == ()
