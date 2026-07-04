# Requerimientos No Funcionales
## Iniciativa: Automatización Administrativa y Facturación

---

## Punto 1: Integrar portales de aseguradoras mediante API

**RNF-01** (asociado a RF-01)
Como área de facturación de SanaRed
Quiero que el ERP de facturación envíe el expediente a la API de la aseguradora en un máximo de 5 segundos por transacción
Para garantizar que el cierre de episodios no se vea interrumpido por demoras en la transmisión

**RNF-02** (asociado a RF-01)
Como área de facturación de SanaRed
Quiero que la transmisión del expediente a la aseguradora se realice mediante HTTPS con autenticación OAuth 2.0
Para garantizar que los datos clínicos y financieros del paciente se transmitan de forma segura y cumpliendo estándares de seguridad

**RNF-16** (asociado a RF-01)
Como área de facturación de SanaRed
Quiero que el expediente digital generado se almacene automáticamente en un bucket de almacenamiento en la nube antes de ser enviado
Para garantizar su durabilidad y permitir que el ERP lo descargue y lo envíe a la aseguradora mediante API sin depender de almacenamiento local

**RNF-17** (asociado a RF-01)
Como área de facturación de SanaRed
Quiero que el envío del expediente a la aseguradora pase por un encolador de mensajes que gestione reintentos automáticos ante fallos
Para garantizar que ningún expediente se pierda por caídas temporales de la API de la aseguradora y que el reintento sea automático sin intervención manual

**RNF-18** (asociado a RF-01)
Como área de facturación de SanaRed
Quiero que el ERP registre logs de cada intento de envío del expediente con los estados: enviado, no enviado y enviado con error
Para tener trazabilidad completa de cada transacción y facilitar la identificación y resolución de fallos en el proceso de envío

**RNF-19** (asociado a RF-01)
Como área de facturación de SanaRed
Quiero que el ERP de facturación tenga capacidad de escalar automáticamente generando nuevas instancias ante picos de demanda
Para garantizar que el proceso de envío de expedientes no se degrade ni se interrumpa durante campañas preventivas o cierres masivos de episodios

**RNF-03** (asociado a RF-02)
Como área de facturación de SanaRed
Quiero que el ERP procese y registre la notificación de liquidación recibida por webhook en un máximo de 5 segundos con timestamp y código de respuesta
Para tener trazabilidad completa de cada notificación recibida de la aseguradora y detectar demoras en el ciclo de cobro

**RNF-04** (asociado a RF-02)
Como área de facturación de SanaRed
Quiero que el ERP exponga un endpoint seguro mediante HTTPS para recibir los webhooks de las aseguradoras con autenticación por token
Para garantizar que solo las aseguradoras autorizadas puedan notificar resultados de liquidación al ERP

**RNF-04b** (asociado a RF-02b)
Como área de facturación de SanaRed
Quiero que el ERP consulte periódicamente la API de la aseguradora en intervalos configurables y reintente automáticamente hasta 3 veces ante fallo de conexión
Para garantizar resiliencia ante caídas temporales de los portales externos sin requerir intervención manual

**RNF-04c** (asociado a RF-02b)
Como área de facturación de SanaRed
Quiero que el ERP registre cada consulta periódica a la API de la aseguradora con su resultado: respuesta obtenida, sin respuesta o error de conexión
Para tener trazabilidad del historial de consultas y detectar aseguradoras con baja disponibilidad en sus APIs

**RNF-05** (asociado a RF-03)
Como área de facturación de SanaRed
Quiero que las notificaciones de expedientes observados o rechazados lleguen al equipo en un máximo de 1 minuto desde la respuesta de la aseguradora
Para que la corrección y reenvío sea inmediata y no impacte el ciclo de cobro

**RNF-06** (asociado a RF-03)
Como área de facturación de SanaRed
Quiero que solo usuarios con rol de facturación tengan acceso a la gestión de expedientes observados o rechazados
Para proteger la integridad del proceso de cobro y cumplir con controles de acceso por rol

---

## Punto 2: Integrar ERP con HCE y Auditoría Médica

**RNF-07** (asociado a RF-04)
Como área de facturación de SanaRed
Quiero que la transferencia de prestaciones desde la HCE al ERP se complete en un máximo de 10 segundos por episodio cerrado
Para que las prestaciones estén disponibles en el ERP sin demoras que retrasen el inicio del ciclo de facturación

**RNF-08** (asociado a RF-04)
Como área de facturación de SanaRed
Quiero que el ERP valide que el 100% de las prestaciones transferidas cuenten con código CIE-10 antes de registrarlas
Para garantizar la integridad de la codificación y reducir los expedientes observados por las aseguradoras

**RNF-09** (asociado a RF-05)
Como área de facturación de SanaRed
Quiero que la consolidación de documentos clínicos en el ERP se complete en un máximo de 15 segundos y verifique que todos los documentos requeridos estén presentes
Para que el auditor médico no reciba expedientes incompletos que generen reprocesos

**RNF-10** (asociado a RF-05)
Como área de facturación de SanaRed
Quiero que la integración entre HCE, laboratorio, imágenes y repositorio de consentimientos tenga una disponibilidad del 99.9%
Para que la consolidación del expediente no se vea interrumpida por caídas de alguno de los sistemas de origen

**RNF-11** (asociado a RF-06)
Como área de facturación de SanaRed
Quiero que la notificación al auditor médico se envíe en un máximo de 1 minuto desde que el expediente esté listo para revisión
Para que el flujo de auditoría no genere cuellos de botella que retrasen el envío del expediente a la aseguradora

**RNF-12** (asociado a RF-06)
Como área de facturación de SanaRed
Quiero que solo usuarios con rol de auditor médico puedan aprobar u observar expedientes en el ERP y que cada acción quede registrada con usuario, fecha y hora
Para garantizar trazabilidad completa del proceso de auditoría y cumplir con controles de acceso por rol
