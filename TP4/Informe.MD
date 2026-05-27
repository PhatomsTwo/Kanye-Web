# Informe Técnico de Desarrollo: Serialización, Contenerización y Cifrado de Mensajes (Protocolo TCP)

**Grupo:** Kanye Web
**Fecha:** 27 de Mayo de 2026  

---

## 1) Serializacion en redes

**a) Que es la serializacion en redes de computadoras?**

Es el proceso de transformar una estructura de datos (objetos, listas o campos) en una secuencia de bytes para poder enviarla por la red y luego reconstruirla en el receptor. Garantiza que el significado de la informacion se conserve entre distintos sistemas, lenguajes y plataformas.

**b) Diferencia entre serializacion binaria y no binaria (ejemplos, ventajas y desventajas)**

- **No binaria (texto):** JSON, XML, YAML.
	- Ventajas: legible por humanos, facil de depurar, compatible con herramientas comunes.
	- Desventajas: mayor tamano, parsing mas lento, tipado mas ambiguo.
- **Binaria:** Protocol Buffers, MessagePack, Avro.
	- Ventajas: menor tamano, mas eficiente en red y CPU, estructuras mas estrictas.
	- Desventajas: menos legible, requiere herramientas/esquemas, depuracion mas compleja.

## 2) Servidor TCP multi-hilo y prueba con PacketSender

Se desplego el servidor TCP multi-hilo y se verifico el envio de mensajes usando PacketSender en formato JSON.

![PacketSender con payload JSON](assets/Screenshot%20from%202026-05-27%2013-19-17.png)
![Envio de JSON por TCP](assets/Screenshot%20from%202026-05-27%2013-19-24.png)
![Servidor recibiendo mensaje](assets/Screenshot%20from%202026-05-27%2013-19-35.png)

## 3) Cliente por consola

Se ejecuto un cliente que se conecta al servidor por IP y puerto, serializa el contenido en JSON con la morfologia solicitada y confirma que el servidor recibe el mensaje correctamente.

![Ejecucion cliente y servidor en contenedores](assets/Screenshot%20from%202026-05-27%2013-31-57.png)

Durante las pruebas se observo que, si la estructura no respeta las claves esperadas, el servidor rechaza el mensaje.

![Estructura incorrecta en el cliente](assets/Screenshot%20from%202026-05-27%2013-33-34.png)
![Servidor rechaza mensaje mal formado](assets/Screenshot%20from%202026-05-27%2013-33-49.png)

## 4) Cifrado de la payload

Se implemento cifrado XOR aplicado solo a la `payload`, y luego se codifico en Base64 para que sea transportable en JSON. El resultado es que la carga util llega cifrada al servidor.

![Payload cifrada en el servidor](assets/Screenshot%20from%202026-05-27%2013-39-57.png)

**Caracteristicas principales del cifrado usado (XOR + Base64):**

- Simple y rapido de implementar.
- No requiere librerias externas.
- No es criptograficamente seguro para uso real; sirve como ejercicio didactico.
- Base64 solo codifica para transporte, no agrega seguridad.

## 5) Opcional

Se realizo una prueba con descifrado en el servidor. El codigo que esta en el repo es el utilizado para esta ultima prueba.

![Corrida con descifrado en el servidor](assets/Screenshot%20from%202026-05-27%2013-42-23.png)

