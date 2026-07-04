# Requerimientos No Funcionales
## Iniciativa: Automatización Administrativa y Facturación

---

## Punto 1: Integrar portales de aseguradoras mediante API

**RNF-01** (asociado a RF-01)
Como facturador de SanaRed
Quiero que el ERP de facturación envíe el expediente a la API de la aseguradora en un máximo de 5 segundos por transacción
Para garantizar que el cierre de episodios no se vea interrumpido por demoras en la transmisión

**RNF-02** (asociado a RF-01)
Como facturador de SanaRed
Quiero que la transmisión del expediente a la aseguradora se realice mediante HTTPS con autenticación OAuth 2.0
Para garantizar que los datos clínicos y financieros del paciente se transmitan de forma segura y cumpliendo estándares de seguridad

**RNF-16** (asociado a RF-01)
Como facturador de SanaRed
Quiero que el expediente digital generado se almacene automáticamente en un bucket de almacenamiento en la nube antes de ser enviado
Para garantizar su durabilidad y permitir que el ERP lo descargue y lo envíe a la aseguradora mediante API sin depender de almacenamiento local

**RNF-17** (asociado a RF-01)
Como facturador de SanaRed
Quiero que el envío del expediente a la aseguradora pase por un encolador de mensajes que gestione reintentos automáticos ante fallos
Para garantizar que ningún expediente se pierda por caídas temporales de la API de la aseguradora y que el reintento sea automático sin intervención manual

**RNF-18** (asociado a RF-01)
Como facturador de SanaRed
Quiero que el ERP registre logs de cada intento de envío del expediente con los estados: enviado, no enviado y enviado con error
Para tener trazabilidad completa de cada transacción y facilitar la identificación y resolución de fallos en el proceso de envío

**RNF-19** (asociado a RF-01)
Como facturador de SanaRed
Quiero que el ERP de facturación tenga capacidad de escalar automáticamente generando nuevas instancias ante picos de demanda
Para garantizar que el proceso de envío de expedientes no se degrade ni se interrumpa durante campañas preventivas o cierres masivos de episodios

**RNF-03** (asociado a RF-02)
Como facturador de SanaRed
Quiero que el ERP procese y registre la notificación de liquidación recibida por webhook en un máximo de 5 segundos con timestamp y código de respuesta
Para tener trazabilidad completa de cada notificación recibida de la aseguradora y detectar demoras en el ciclo de cobro

**RNF-04** (asociado a RF-02)
Como facturador de SanaRed
Quiero que el ERP exponga un endpoint seguro mediante HTTPS para recibir los webhooks de las aseguradoras con autenticación por token
Para garantizar que solo las aseguradoras autorizadas puedan notificar resultados de liquidación al ERP

**RNF-04b** (asociado a RF-02b)
Como facturador de SanaRed
Quiero que el ERP consulte periódicamente la API de la aseguradora en intervalos configurables y reintente automáticamente hasta 3 veces ante fallo de conexión
Para garantizar resiliencia ante caídas temporales de los portales externos sin requerir intervención manual

**RNF-04c** (asociado a RF-02b)
Como facturador de SanaRed
Quiero que el ERP registre cada consulta periódica a la API de la aseguradora con su resultado: respuesta obtenida, sin respuesta o error de conexión
Para tener trazabilidad del historial de consultas y detectar aseguradoras con baja disponibilidad en sus APIs

**RNF-05** (asociado a RF-03)
Como facturador de SanaRed
Quiero que las notificaciones de expedientes observados o rechazados lleguen al equipo en un máximo de 1 minuto desde la respuesta de la aseguradora
Para que la corrección y reenvío sea inmediata y no impacte el ciclo de cobro

**RNF-06** (asociado a RF-03)
Como facturador de SanaRed
Quiero que solo usuarios con rol de facturación tengan acceso a la gestión de expedientes observados o rechazados
Para proteger la integridad del proceso de cobro y cumplir con controles de acceso por rol


**RNF-20** (asociado a RF-07)
Como admisionista de SanaRed
Quiero que el bus de eventos que conecta la HCE, los portales y el ERP procese las consultas de elegibilidad de forma asíncrona con un tiempo de respuesta máximo de 2 segundos
Para soportar picos de demanda durante campañas masivas sin degradar la velocidad de ingreso del paciente

**RNF-21** (asociado a RF-07)
Como admisionista de SanaRed
Quiero que la infraestructura escale automáticamente de forma horizontal ante ráfagas de validaciones simultáneas de cobertura
Para garantizar una disponibilidad del 99.9% del servicio de consulta a aseguradoras sin intervención manual

**RNF-22** (asociado a RF-07)
Como admisionista de SanaRed
Quiero que las peticiones de validación de cobertura que no puedan procesarse en tiempo real sean retenidas en colas distribuidas asíncronas para su reintento
Para garantizar que ninguna consulta se pierda ante picos de carga o indisponibilidad temporal de la API de la aseguradora

**RNF-23** (asociado a RF-08)
Como admisionista de SanaRed
Quiero que todos los expedientes digitales compilados viajen cifrados con TLS en tránsito y cifrado en reposo gestionado por un servicio de llaves en la nube
Para prevenir accesos indebidos a datos clínicos y financieros sensibles del paciente durante su transmisión

**RNF-24** (asociado a RF-08)
Como admisionista de SanaRed
Quiero que cada acceso al expediente digital genere un log de auditoría centralizado e inmutable que registre la identidad del usuario, el ID del paciente, la fecha, hora y módulo de origen
Para garantizar trazabilidad completa de quién accedió a qué información y cumplir con las regulaciones de privacidad de datos de salud

**RNF-25** (asociado a RF-08)
Como admisionista de SanaRed
Quiero que el acceso al expediente digital esté controlado por roles diferenciando permisos entre admisión, facturación y auditoría médica mediante SSO
Para garantizar que cada perfil acceda únicamente a la información que le corresponde según su función


---

## Punto 2: Integrar ERP con HCE y Auditoría Médica

**RNF-07** (asociado a RF-04)
Como facturador de SanaRed
Quiero que la transferencia de prestaciones desde la HCE al ERP se complete en un máximo de 10 segundos por episodio cerrado
Para que las prestaciones estén disponibles en el ERP sin demoras que retrasen el inicio del ciclo de facturación

**RNF-08** (asociado a RF-04)
Como facturador de SanaRed
Quiero que el ERP valide que el 100% de las prestaciones transferidas cuenten con código CIE-10 antes de registrarlas
Para garantizar la integridad de la codificación y reducir los expedientes observados por las aseguradoras

**RNF-09** (asociado a RF-05)
Como auditor médico de SanaRed
Quiero que la consolidación de documentos clínicos en el ERP se complete en un máximo de 15 segundos y verifique que todos los documentos requeridos estén presentes
Para no recibir expedientes incompletos que generen reprocesos

**RNF-10** (asociado a RF-05)
Como auditor médico de SanaRed
Quiero que la integración entre HCE, laboratorio, imágenes y repositorio de consentimientos tenga una disponibilidad del 99.9%
Para que la consolidación del expediente no se vea interrumpida por caídas de alguno de los sistemas de origen

**RNF-11** (asociado a RF-06)
Como auditor médico de SanaRed
Quiero que la notificación de expediente listo para revisión me llegue en un máximo de 1 minuto desde que el expediente esté disponible
Para que el flujo de auditoría no genere cuellos de botella que retrasen el envío del expediente a la aseguradora

**RNF-12** (asociado a RF-06)
Como auditor médico de SanaRed
Quiero que cada acción de aprobación u observación que realice sobre un expediente quede registrada con mi usuario, fecha y hora
Para garantizar trazabilidad completa del proceso de auditoría y cumplir con controles de acceso por rol
