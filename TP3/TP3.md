## Punto 1

1\) Investigación conceptual (respuestas breves). Responder en forma concisa.  
a) ¿Qué es SSH y qué problema resuelve?

SSH (Secure Shell) es un protocolo de red que permite acceder y administrar computadoras de forma remota y segura. Un ejemplo de uso puede ser una maquina virtual corriendo en un servidor remoto. Para conectarnos de forma segura y sin importar la distancia física entre nosotros y la misma utilizamos el protocolo SSH. Como permite esa conexión segura? a través de la criptografía que autentica y encripta la conexión entre los dispositivos.

b) Diferencia entre autenticación y cifrado

**Autenticación**: Es el proceso de verificar la identidad de un usuario o dispositivo. Prueba que alguien o algo es quien dice ser.

**Cifrado**: Es el proceso de ocultar o alterar los datos mediante algoritmos para que sean ilegibles durante su transmisión, protegiendo la información de terceros. 

c) ¿Qué es una clave pública y una clave privada?

Son un par de claves matemáticas vinculadas entre sí que se usan en la criptografía asimétrica.

**Clave Pública:** Es el componente visible o identificador público del sistema. Se distribuye libremente a cualquier cliente o servidor. Cumple dos funciones: permite que terceros cifren datos dirigidos exclusivamente al que posee de la clave privada correspondiente, y sirve para verificar matemáticamente las firmas digitales emitidas por este.

**Clave Privada:** Es el componente secreto y nunca debe salir del entorno local donde fue generado. Se utiliza para descifrar la información confidencial recibida y para firmar digitalmente transacciones, documentos o código. Esto garantiza la autenticación.

d) ¿Por qué la clave privada no debe compartirse?

Porque es la única prueba criptográfica de nuestra identidad. Si un atacante la consigue puede suplantar completamente al usuario o sistema dueño de la clave. Significa que tendría vía libre a entrar a cualquier servidor que confíe en la clave pública asociada y podría leer toda la información confidencial.

e) ¿Qué ventajas tienen las claves SSH frente a contraseñas?

Las claves SSH no se pueden adivinar por fuerza bruta (prácticamente). No son susceptibles a phishing y keyloggers ya que el usuario no tiene que tipear la clave en el teclada ni ingresarla en un formulario web. Facilitan la automatización: permiten que dos máquinas se conecten entre sí de forma segura por su cuenta. Es clave para que los servidores ejecuten tareas programadas, copias de seguridad u otros scripts sin que una persona tenga que estar escribiendo la contraseña cada vez

## Punto 2

Se realizó la conexión a la máquina virtual 4:

| PC4 | 34.130.32.165 | 5000-6000 | pc-alumnos-4 | en el drive | Google | Canadá |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |

![][image1]

Luego se creó la carpeta “kayne-web” con el nombre del grupo:

![][image2]

## Punto 3

El tráfico capturado de wireshark:

![][image3]  
Podemos analizar un paquete. El cual no se puede descifrar. El paquete está cifrado con ChaCha20-Poly1305 y el contenido es a nuestros ojos carácteres inentendibles.

## Punto 4

Servidor (Máquina virtual)  
![][image4]

Cliente  
![][image5]

Luego de la conexión con netcat pudimos capturar el handshake:

Luego se envió el mensaje “test3” y se capturó con wireshark:

El mensaje se puede leer claramente captado en el paquete TCP “test3”. Ya que TCP no cifra nada. Solo se encarga de establecer la conexión, garantizar que los bytes lleguen en orden, reenviar si se pierde algo y confirmar recepción. 

b) Mismo experimento utilizando UDP:

![][image6]

Se realizaron envío de mensajes entre el cliente y servidor.

![][image7]

![][image8]

Podemos observar ambos paquetes UDP con el mensaje. A diferencia de TCP no tenemos el handshake.

c) Hacemos el mismo ejercicio pero utilizando la PC4 y PC5. Dos maquinas virtuales distintas. Establecemos la conexión cliente servidor:

PC4:  
![][image9]

PC5:  
![][image10]

Las dos VMs se conectan directo entre sí por la internet pública, sin pasar por nuestra computadora personal.

## Punto 5

Se creó el archivo “index.html” dentro de la carpeta del grupo “kayne-web”. Y se sirvio el servidor http en el puerto 5050

![][image11]

![][image12]

Captura wireshark

![][image13]

1. Pueden descifrar el contenido?  
     
   Si completamente. En la captura de wireshark se puede ver el contenido completo de la pagina html como la metadata y contenido. Http no cifra nada, cualquiera con acceso al medio puede leer todo lo que viaja.

2. Podrían intervenir el contenido?

	Si. Esto se llama ataque “man in the middle”. Como el contenido no va cifrado, alguien que se coloque en el medio de la conexión podría:

 1\. Modificar la respuesta: cambiar el HTML antes de que llegue al navegador.

 2\. Modificar el request: cambiar lo que el cliente pide.

 3\. Suplantar al servidor: responder él mismo haciéndose pasar por la VM

 4\. Robar cookies/tokens: capturar credenciales de sesión y reusarlas.

## Punto 6

a)

El video muestra exactamente el escenario de “Man in the Middle”. Lo mismo que pudimos reproducir en el TP donde capturamos tráfico TCP, UDP y HTTP con Wireshark y pudimos leer el contenido y modificarlo (si quisiéramos). En el video los investigadores hacen lo mismo pero con NFC entre el Iphone y la terminal de pago. Pueden hacerlo porque el protocolo no se defiende contra un actor intermedio.

Con SSH vimos que se cifra todo y no es posible ser leído por alguien en el medio. En el caso del video si Apple Pay con Visa hubiese usado autenticación criptográfica robusta de la terminal (como hace SSH al verificar el host con su clave pública) el ataque no sería posible.

Se puede ver también el concepto de clave pública y privada. Es lo que falta en el caso del video. Si la terminal legítima firma su identidad con una clave privada y el Iphone lo verifica con la clave pública no sería posible que un dispositivo NFC cualquiera pueda hacerse pasar por la terminal de transporte.

Y otro tema importante es que como TCP no es seguro por si solo porque no cifra ni autentica, con NFC sucede lo mismo. Mueve bytes de un lado al otro pero no garantiza nada sobre quien los manda ni si fueron leídos por alguien en el camino. La seguridad se construye en una capa superior (TLS sobre TCP y autenticación criptográfica sobre NFC)

b)

Lo que demostramos en el laboratorio es que por defecto las redes no garantizan la confidencialidad. Transmitir información por el medio no es confiable. Lo pudimos ver interceptando los paquetes y leyendo su contenido. Necesitamos capas adicionales que aseguren la autenticación y el cifrado. Tanto la autenticación como el cifrado son igual de importantes. No sirve de nada cifrar si tenemos un atacante haciendose pasar por el destinatario y tampoco saber que el destinatario es legítimo pero el contenido viaja en texto plano y puede ser interceptado y leído.

[image1]: image-1.png
[image2]: image-2.png
[image3]: image-3.png
[image4]: image-4.png
[image5]: image-5.png
[image6]: image-6.png
[image7]: image-7.png
[image8]: image-8.png
[image9]: image-9.png
[image10]: image-10.png
[image11]: image-11.png
[image12]: image-12.png
[image13]: image-13.png
