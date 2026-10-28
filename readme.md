**1. Variabilidad Estocástica bajo un Contrato Sintáctico: Al ejecutar varias veces main.py en el Paso 4, habrás observado que el programa siempre devuelve un objeto ContactoCliente válido, pero el texto de cliente.intencion cambia entre ejecuciones. ¿Por qué tener un contrato tipado (str) no impide que los valores varíen semánticamente y qué implicaciones tiene esto si otro módulo de tu aplicación espera hacer un if cliente.intencion == "compra":?**

El formato es estrito por lo que los datos que ponga de forma general estarán bien pero cada dato será random, por lo que en el campo nombre habrá numbre pero el nombre será random
Puede dar error al no coincidir, garantiza que hay texto, no que el texto tenga el significado que el código.


**2. Anatomía del Esquema (model_json_schema()): Al inspeccionar la salida de ContactoCliente.model_json_schema(), ¿qué información de la clase Pydantic (Field, tipos, min_length, description) viaja dentro de ese diccionario JSON y cómo influyen los nombres de las propiedades y description durante la inferencia?**

El esquema lleva los tipos, las restricciones y las descripciones, y los nombres de los campos guían lo que escribe el modelo.

**3. Generación Restringida vs system prompt: En el experimento del Paso 5.2, cuando pusiste un system prompt que contradecía la tarea (pedir un poema y prohibir JSON) pero mantuviste format, el modelo siguió devolviendo un JSON acorde al esquema. ¿Qué es la generación restringida (constrained decoding) y por qué tiene más peso sobre la forma de la salida que las instrucciones escritas en el system prompt?**

Es un filtro del motor que solo deja generar tokens válidos según el esquema, y pesa más que el prompt

**4. Semántica del Nombre del Campo y Reglas de Dominio (email vs contacto): En el Paso 5.3 (Caso A), comprobaste que mientras el campo se llamaba email el modelo se resistía a poner un teléfono, pero al renombrarlo a contacto e indicarlo en el system prompt, devolvió "+34 654654654" y el contrato lo dio por válido. ¿Por qué el nombre del campo influye en los tokens que genera el modelo y por qué el tipo str por sí solo no basta para proteger las reglas de negocio?**

Sin format la respuesta es texto libre, no es JSON válido, y la validación en Python lo bloquea

**5. El Efecto de Retirar format: ¿Qué ocurrió exactamente cuando eliminaste el parámetro format de la llamada a Ollama (Paso 5.4) y qué componente de tu código impidió que esa respuesta no estructurada continuase hacia el resto del programa?**

El nombre del campo empuja al modelo a escribir cierto tipo de dato, y str no comprueba reglas de negocio

**6. La Gran Pregunta de Arquitectura: ¿Pero si Ollama ya aplica generación restringida al recibir el esquema en format, para qué necesitamos validar otra vez con ContactoCliente.model_validate_json() en Python?
(Apóyate en lo ocurrido en el Paso 5.3 Caso B con min_length=2 y en la diferencia entre un parámetro del motor de inferencia externo y la frontera de confianza determinista de tu aplicación).**

El modelo puede cambiar la estructura que hemos hecho a una que tiene los mismos campos montada de diferente forma y no validar

**7. Taxonomía de Errores y Resiliencia: ¿Qué diferencia conceptual existe entre un error de comunicación con la infraestructura, un incumplimiento del contrato de datos y un incumplimiento de una regla de dominio? ¿Qué excepciones expone nuestra función extraer_contacto() para discriminar estos escenarios frente a la excepción interna httpx.HTTPError, y cómo evita main.py mostrar trazas internas al usuario?**

Un error de infraestructura es de conexión, uno de contrato es de forma de los datos y uno de dominio es de valor no admitido; main.py muestra solo mensajes propios, sin trazas

