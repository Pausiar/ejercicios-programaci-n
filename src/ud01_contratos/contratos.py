from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ContactoCliente(BaseModel):
    nombre: str = Field(description="Nombre completo del cliente", min_length=2)
    email: str = Field(description="Dirección de correo electrónico del cliente")
    intencion: str = Field(
        description="Intención del cliente. Valores habituales: consulta, compra, soporte"
    )

    @field_validator("email")
    @classmethod
    def validar_email(cls, email: str) -> str:
        if email.count("@") != 1:
            raise ValueError("El email debe contener exactamente un carácter '@'")

        _, dominio = email.split("@")
        if "." not in dominio:
            raise ValueError("El email debe contener al menos un punto después de '@'")

        return email

    @field_validator("intencion")
    @classmethod
    def validar_intencion(cls, intencion: str) -> str:
        intenciones_admitidas = {"consulta", "compra", "soporte"}
        if intencion not in intenciones_admitidas:
            raise ValueError(
                "La intención debe ser una de estas: consulta, compra, soporte"
            )

        return intencion


class ResultadoValido(BaseModel):
    valido: Literal[True] = True
    contacto: ContactoCliente
    raw_content: str


class ResultadoRechazado(BaseModel):
    valido: Literal[False] = False
    motivo: str
    raw_content: str


ResultadoExtraccion = ResultadoValido | ResultadoRechazado