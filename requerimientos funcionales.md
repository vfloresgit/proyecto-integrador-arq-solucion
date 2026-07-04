# Iniciativa: Automatización Administrativa y Facturación

---

## Punto 1: Integrar portales de aseguradoras mediante API

**RF-01**
Como facturador de SanaRed
Quiero que el ERP de facturación envíe el expediente de cobro a la aseguradora mediante API al cierre del episodio sin intervención manual
Para eliminar el envío por correo o portal web y reducir el ciclo de facturación con cada financiador

**RF-02**
Como facturador de SanaRed
Quiero que el ERP de facturación reciba automáticamente la respuesta de liquidación mediante webhook cuando la aseguradora lo soporte
Para que la notificación del resultado llegue de forma inmediata al ERP sin que SanaRed tenga que consultar activamente

**RF-02b**
Como facturador de SanaRed
Quiero que el ERP de facturación consulte periódicamente la API de la aseguradora para obtener el estado de liquidación cuando esta no soporte webhook
Para garantizar que la respuesta se registre automáticamente sin intervención manual independientemente de la madurez tecnológica de la aseguradora

**RF-03**
Como facturador de SanaRed
Quiero que el ERP de facturación gestione automáticamente los expedientes observados o rechazados por la aseguradora notificando al equipo de facturación con el detalle de la observación
Para que la corrección y reenvío del expediente sea inmediata y reducir el impacto en el ciclo de cobro por discrepancias de codificación

**RF-07**
Como admisionista de SanaRed
Quiero que el sistema consulte de manera directa y automática la póliza del paciente
Para eliminar las validaciones manuales en portales externos y agilizar el ingreso del paciente

**RF-08**
Como admisionista de SanaRed
Quiero que el sistema registre automáticamente el porcentaje de copago, el deducible y el ID de autorización en el episodio clínico al recibir respuesta de la aseguradora
Para que no se requiera que el admisionista ingrese a un portal externo ni realice capturas de pantalla

---

## Punto 2: Integrar ERP con HCE y Auditoría Médica

**RF-04**
Como facturador de SanaRed
Quiero que las prestaciones registradas en la Historia Clínica Electrónica se transfieran automáticamente al ERP con su codificación correcta
Para eliminar la carga manual de prestaciones y reducir las inconsistencias de codificación que generan expedientes observados por las aseguradoras

**RF-05**
Como auditor médico de SanaRed
Quiero que el ERP de facturación consolide automáticamente los documentos clínicos requeridos para auditoría: diagnósticos, órdenes, informes y consentimientos
Para revisar y aprobar expedientes desde una sola interfaz sin acceder manualmente a múltiples sistemas

**RF-06**
Como auditor médico de SanaRed
Quiero que el ERP de facturación me notifique automáticamente cuando un expediente esté listo para revisión y registre digitalmente mi aprobación u observación
Para que el flujo de auditoría sea completamente trazable y eliminar la gestión manual que retrasa el cierre y envío del expediente a la aseguradora

---
