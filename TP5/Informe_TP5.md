### **1) Reconocimiento de arquitectura**

**Firewall** 
* **a) Problema que resuelve:** Filtra y controla el tráfico entrante y saliente basándose en reglas de seguridad para prevenir accesos no autorizados y mitigar ataques.
* **b) Capa TCP/IP:** Capa de Internet (filtrado de IP) y Capa de Transporte (filtrado de puertos). Algunos modernos (como los WAF) operan también en la Capa de Aplicación.
* **c) Si falta:** La red y los servidores quedarían expuestos a todo el tráfico público, aumentando el riesgo de ataques DDoS, vulnerabilidades y brechas de seguridad.
 
**Load Balancer** 
* **a) Problema que resuelve:** Distribuye las peticiones entrantes entre múltiples servidores para asegurar que ningún nodo se sobrecargue, maximizando el *throughput* y garantizando alta disponibilidad.
* **b) Capa TCP/IP:** Capa de Transporte (Layer 4 - TCP/UDP) o Capa de Aplicación (Layer 7 - HTTP/HTTPS).
* **c) Si falta:** Todo el tráfico golpearía a un único servidor (o la distribución sería estática). Esto generaría cuellos de botella severos y un Punto Único de Falla (SPOF).
 
**Queue (Cola de mensajes)** 
* **a) Problema que resuelve:** Desacopla los servicios permitiendo el procesamiento asíncrono. Absorbe picos de tráfico reteniendo las tareas pesadas hasta que los *workers* tengan capacidad para procesarlas.
* **b) Capa TCP/IP:** Capa de Aplicación.
* **c) Si falta:** Las peticiones síncronas de alto costo bloquearían los hilos del servidor web, provocando *timeouts* y pérdida de datos durante picos de tráfico.
 
**Compute (Servidor / VM)** 
* **a) Problema que resuelve:** Proporciona los recursos de hardware subyacentes (CPU, RAM) para alojar el código persistente y la lógica de negocio principal de la aplicación.
* **b) Capa TCP/IP:** Capa de Aplicación (es el *host* donde se ejecutan los protocolos de aplicación).
* **c) Si falta:** No habría un entorno donde ejecutar el backend monolítico o los contenedores persistentes de la plataforma.
 
**Serverless Function** 
* **a) Problema que resuelve:** Permite ejecutar fragmentos de código bajo demanda en respuesta a eventos sin tener que provisionar, administrar ni mantener servidores. Escala automáticamente a cero.
* **b) Capa TCP/IP:** Capa de Aplicación.
* **c) Si falta:** Se consumirían recursos económicos y operativos manteniendo servidores encendidos incluso en momentos de inactividad, perdiendo flexibilidad de auto-escalado instántaneo.
 
**SQL DB** 
* **a) Problema que resuelve:** Almacena datos estructurados asegurando integridad relacional y cumplimiento de las propiedades ACID para transacciones seguras (ej. pagos, usuarios).
* **b) Capa TCP/IP:** Capa de Aplicación.
* **c) Si falta:** Resultaría imposible mantener la consistencia y la integridad en conjuntos de datos complejos y altamente interrelacionados.
 
**NoSQL** 
* **a) Problema que resuelve:** Almacena grandes volúmenes de datos no estructurados o semi-estructurados con esquemas flexibles, facilitando la escalabilidad horizontal y las escrituras rápidas.
* **b) Capa TCP/IP:** Capa de Aplicación.
* **c) Si falta:** Guardar *logs* masivos o documentos dinámicos en una base relacional saturaría sus tiempos de escritura y haría muy complejo el escalado del esquema.
 
**Cache** 
* **a) Problema que resuelve:** Almacena datos de acceso muy frecuente en memoria (RAM) para responder a las consultas con latencias de milisegundos y aliviar la carga de la base de datos.
* **b) Capa TCP/IP:** Capa de Aplicación.
* **c) Si falta:** Cada solicitud de lectura requeriría ir al disco de la base de datos principal, disparando la latencia de respuesta y saturando sus recursos rápidamente.
 
**CDN (Content Delivery Network)** 
* **a) Problema que resuelve:** Almacena copias de los archivos estáticos en nodos distribuidos geográficamente para entregarlos desde el punto más cercano al cliente, ahorrando ancho de banda.
* **b) Capa TCP/IP:** Capa de Aplicación (operan utilizando HTTP/HTTPS).
* **c) Si falta:** Todo el contenido estático viajaría desde el servidor origen, aumentando el tiempo de carga para usuarios lejanos y agotando la capacidad de red de tu infraestructura.
 
**Storage** 
* **a) Problema que resuelve:** Proporciona un repositorio altamente escalable y duradero para archivos binarios (imágenes, modelos, videos), como es el caso de un *bucket* de S3.
* **b) Capa TCP/IP:** Capa de Aplicación.
* **c) Si falta:** Habría que guardar los archivos en el disco local de los nodos de Compute, dificultando la sincronización de archivos si se escala horizontalmente y llenando el disco a gran velocidad.
 
**Search Engine** 
* **a) Problema que resuelve:** Utiliza índices invertidos para permitir consultas complejas y búsquedas *full-text* ultrarrápidas sobre inmensas cantidades de datos.
* **b) Capa TCP/IP:** Capa de Aplicación.
* **c) Si falta:** Realizar búsquedas de texto parcial (como un simple `LIKE %texto%`) sobre una tabla SQL gigante provocaría escaneos completos (*table scans*), bloqueando la base de datos por completo.
 
**Réplica** 
* **a) Problema que resuelve:** Mantiene copias sincronizadas de la base de datos principal (generalmente de solo lectura) para distribuir la carga de consultas y permitir *failover* (redundancia).
* **b) Capa TCP/IP:** Capa de Aplicación.
* **c) Si falta:** El nodo principal se convertiría en un cuello de botella letal para las lecturas. Si ese nodo llega a caerse, todo el servicio de datos quedaría inaccesible instantáneamente.

---

### **2) Tipos de tráfico**.

El simulador categoriza las peticiones en seis tipos distintos: STATIC, READ, WRITE, UPLOAD, SEARCH y MALICIOUS. Aplicar el componente correcto a cada tipo es la clave para que la arquitectura no colapse.

Armé la tabla utilizando algunos ejemplos prácticos, orientados a escenarios que podrías cruzarte desarrollando plataformas reales (como sistemas de inferencia o procesamiento de imágenes médicas), para que los conceptos te resulten más tangibles:

| Tipo de tráfico | Ejemplo real | Componente recomendado para procesarlo | Riesgo si se procesa incorrectamente |
| --- | --- | --- | --- |
| **STATIC** | Imágenes, CSS o JavaScript de una interfaz web.| CDN o almacenamiento estático (Storage).| Desperdiciar capacidad de cómputo sirviendo archivos que no requieren procesamiento.|
| **READ** | Consultar un panel de métricas o el historial de resultados de un paciente. | Cache (para datos frecuentes) y Réplica de lectura (para datos persistentes). | Saturar el nodo principal de la base de datos, disparando los tiempos de respuesta y afectando a todos los usuarios. |
| **WRITE** | Registrar en la base de datos las clasificaciones y segmentaciones generadas por un modelo. | Queue (para encolar las peticiones de alta concurrencia) + SQL DB / NoSQL. | Bloquear la aplicación esperando que el disco termine de escribir los datos (cuello de botella de I/O), causando *timeouts*. |
| **UPLOAD** | Subir imágenes histológicas pesadas desde un cliente hacia el servidor. | Storage (almacenamiento de objetos tipo S3) para guardar el binario directo. | Llenar rápidamente el disco del servidor de aplicación web y agotar el ancho de banda del mismo, tumbando la API. |
| **SEARCH** | Buscar palabras clave específicas entre millones de registros o metadatos de muestras. | Search Engine (motor de búsqueda indexado). | Realizar la búsqueda sobre una tabla SQL gigante provocaría un *table scan* que consumiría toda la CPU y memoria de la base de datos. |
| **MALICIOUS (ATTACK)** | Peticiones masivas intentando explotar endpoints o hacer un ataque de denegación de servicio (DDoS). | Firewall. | Caída total del sistema por agotamiento de recursos o exposición de datos sensibles si vulneran una capa interna. |

---

### **3) Testeamos queues: Análisis de comportamiento**

![alt text](image.png)

**Al incrementar el rate de tráfico (Sobrecarga del sistema):**

* **Saturación del Buffer (Buffer Overflow):** La tasa de llegada de peticiones comienza a ser mucho mayor que la tasa de procesamiento (servicio) que tiene la instancia de computación. Como bien dedujiste, la *queue* no da abasto, agota la capacidad de su buffer y comienza a descartar paquetes.
* **Impacto en la Reputación:** Estos paquetes descartados se traducen en errores visibles para el usuario (como *Timeouts* o errores HTTP 503 Service Unavailable), lo que justifica la caída rápida y drástica en la métrica de reputación del simulador.
* **Protección del Nodo de Cómputo:** La función clave de la *queue* aquí es actuar como un amortiguador. Tiene el control del flujo y solo le entrega a la computadora los paquetes que esta es capaz de procesar concurrente. Si la *queue* no estuviera, la computadora recibiría todo el tráfico de golpe, saturando su memoria y CPU, y el nodo entero se caería (Crash).

**Al mantener el rate alto y luego llevarlo a cero rápidamente:**

* **Procesamiento del Backlog (Remanente):** Aunque la entrada de nuevas peticiones se detiene por completo (Rate = 0), después de la queue, la computadora sigue trabajando.
* **Desacople temporal:** Esto demuestra el principio de desacople de una cola de mensajes. La computadora continúa procesando de forma asíncrona todos los paquetes que quedaron almacenados en el buffer de la *queue* durante el pico de tráfico, hasta que la cola finalmente se vacía y el sistema vuelve al reposo.
