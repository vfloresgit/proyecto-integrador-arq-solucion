```gherkin
Feature RF-01: Envío automático del expediente de cobro a la aseguradora mediante API
  Como facturador de SanaRed
  Quiero que el ERP de facturación envíe el expediente de cobro a la aseguradora mediante API al cierre del episodio sin intervención manual
  Para eliminar el envío por correo o portal web y reducir el ciclo de facturación con cada financiador

  # Escenario positivo

  Scenario: Envío exitoso del expediente al cierre del episodio
    Given que un episodio clínico ha sido cerrado y auditado en el ERP de facturación
    And el expediente contiene factura, prestaciones, autorizaciones, informes y consentimientos completos
    And la aseguradora asociada al paciente tiene una API disponible
    When el ERP de facturación intenta enviar el expediente a la API de la aseguradora
    Then el sistema debe enviar el expediente automáticamente sin intervención del facturador
    And debe registrar el envío en el log con estado "Enviado" y timestamp
    And debe actualizar el estado del expediente a "Enviado a aseguradora" en el ERP

  # Escenario negativo

  Scenario: Fallo en el envío por API de la aseguradora no disponible
    Given que un expediente está listo para ser enviado a la aseguradora
    And la API de la aseguradora no está disponible o devuelve un error
    When el ERP de facturación intenta enviar el expediente
    Then el sistema no debe marcar el expediente como enviado
    And debe encolar el expediente en el sistema de mensajería para reintento automático
    And debe registrar el intento en el log con estado "Enviado con error" y detalle del fallo
    And debe notificar al facturador sobre el fallo con el detalle del error
```

```gherkin
Feature RF-02: Recepción automática de respuesta de liquidación mediante webhook
  Como facturador de SanaRed
  Quiero que el ERP de facturación reciba automáticamente la respuesta de liquidación mediante webhook cuando la aseguradora lo soporte
  Para que la notificación del resultado llegue de forma inmediata al ERP sin que SanaRed tenga que consultar activamente

  # Escenario positivo

  Scenario: Recepción exitosa de respuesta de liquidación por webhook
    Given que un expediente fue enviado a la aseguradora y está pendiente de respuesta
    And la aseguradora soporta notificación por webhook
    When la aseguradora procesa el expediente y llama al endpoint del ERP con el resultado
    Then el ERP debe registrar automáticamente la respuesta con estado, timestamp y código de liquidación
    And debe actualizar el estado del expediente según la respuesta recibida

  # Escenario negativo

  Scenario: Webhook recibido con token de autenticación inválido
    Given que el ERP expone un endpoint para recibir webhooks de aseguradoras
    When una llamada entrante llega al endpoint con un token de autenticación inválido o no autorizado
    Then el ERP debe rechazar la notificación con código de error 401
    And debe registrar el intento fallido en el log de auditoría con IP de origen y timestamp
```

```gherkin
Feature RF-02b: Consulta periódica a API de aseguradora para obtener estado de liquidación
  Como facturador de SanaRed
  Quiero que el ERP de facturación consulte periódicamente la API de la aseguradora para obtener el estado de liquidación cuando esta no soporte webhook
  Para garantizar que la respuesta se registre automáticamente sin intervención manual independientemente de la madurez tecnológica de la aseguradora

  # Escenario positivo

  Scenario: Consulta periódica exitosa con respuesta de liquidación disponible
    Given que un expediente fue enviado a una aseguradora que no soporta webhook
    And el ERP tiene configurado un intervalo de consulta para esa aseguradora
    When el ERP ejecuta la consulta periódica a la API de la aseguradora
    Then el sistema debe obtener el estado de liquidación y registrarlo en el expediente
    And debe actualizar el estado del expediente automáticamente sin intervención del facturador

  # Escenario negativo

  Scenario: Consulta periódica fallida por API de aseguradora no disponible
    Given que el ERP intenta consultar periódicamente el estado de liquidación de un expediente
    And la API de la aseguradora no responde en los 3 reintentos configurados
    When se agotan los reintentos
    Then el ERP debe registrar el intento en el log con estado "Sin respuesta" y timestamp
    And debe notificar al facturador para seguimiento manual del caso
```

```gherkin
Feature RF-03: Gestión automática de expedientes observados o rechazados
  Como facturador de SanaRed
  Quiero que el ERP de facturación gestione automáticamente los expedientes observados o rechazados por la aseguradora notificando al equipo con el detalle de la observación
  Para que la corrección y reenvío del expediente sea inmediata y reducir el impacto en el ciclo de cobro por discrepancias de codificación

  # Escenario positivo

  Scenario: Notificación inmediata al equipo por expediente observado
    Given que la aseguradora ha respondido con una observación sobre un expediente enviado
    And el ERP recibe el detalle de la observación con el motivo específico
    When el ERP procesa la respuesta de la aseguradora
    Then debe actualizar el estado del expediente a "Observado" con el detalle del motivo
    And debe notificar al equipo de facturación en un máximo de 1 minuto con el detalle de la observación

  # Escenario negativo

  Scenario: Expediente rechazado sin detalle de motivo por parte de la aseguradora
    Given que la aseguradora responde con un rechazo sobre un expediente enviado
    And la respuesta no incluye detalle del motivo de rechazo
    When el ERP procesa la respuesta
    Then debe marcar el expediente con estado "Rechazado - Motivo no especificado"
    And debe notificar al facturador indicando que debe contactar a la aseguradora para obtener el detalle
```

```gherkin
Feature RF-04: Transferencia automática de prestaciones de HCE al ERP con codificación correcta
  Como facturador de SanaRed
  Quiero que las prestaciones registradas en la Historia Clínica Electrónica se transfieran automáticamente al ERP con su codificación correcta
  Para eliminar la carga manual de prestaciones y reducir las inconsistencias de codificación que generan expedientes observados por las aseguradoras

  # Escenario positivo

  Scenario: Transferencia exitosa de prestaciones con codificación CIE-10 válida
    Given que un médico ha cerrado y firmado un episodio clínico en la HCE
    And todas las prestaciones del episodio tienen código CIE-10 asignado
    When el servicio de integración transfiere las prestaciones al ERP
    Then el ERP debe registrar las prestaciones con su codificación correcta de forma automática
    And el episodio debe quedar disponible para el ciclo de facturación sin intervención manual

  # Escenario negativo

  Scenario: Transferencia bloqueada por prestación sin codificación correcta
    Given que un episodio clínico ha sido cerrado en la HCE
    And al menos una prestación no tiene código CIE-10 asignado o tiene un código inválido
    When el servicio de integración intenta transferir las prestaciones al ERP
    Then el ERP no debe registrar las prestaciones del episodio
    And debe marcar el episodio con estado "Bloqueado - Codificación incompleta"
    And debe notificar al facturador con el detalle de las prestaciones con error de codificación
```

```gherkin
Feature RF-05: Consolidación automática de documentos clínicos para auditoría
  Como auditor médico de SanaRed
  Quiero que el ERP de facturación consolide automáticamente los documentos clínicos requeridos para auditoría: diagnósticos, órdenes, informes y consentimientos
  Para revisar y aprobar expedientes desde una sola interfaz sin acceder manualmente a múltiples sistemas

  # Escenario positivo

  Scenario: Consolidación exitosa de todos los documentos clínicos en el ERP
    Given que un episodio clínico ha sido cerrado y las prestaciones transferidas al ERP
    And los documentos clínicos están disponibles en HCE, laboratorio, imágenes y repositorio de consentimientos
    When el ERP ejecuta la consolidación del expediente
    Then debe reunir automáticamente diagnósticos, órdenes, informes y consentimientos en una sola vista
    And debe marcar el expediente como "Listo para auditoría" y notificar al auditor médico

  # Escenario negativo

  Scenario: Consolidación bloqueada por documento clínico no disponible
    Given que el ERP intenta consolidar los documentos de un episodio
    And al menos uno de los documentos requeridos no está disponible en su sistema de origen
    When el ERP ejecuta el proceso de consolidación
    Then no debe marcar el expediente como listo para auditoría
    And debe notificar al auditor médico indicando qué documento está faltante y en qué sistema de origen
```

```gherkin
Feature RF-06: Notificación automática al auditor médico y registro digital de aprobación
  Como auditor médico de SanaRed
  Quiero que el ERP de facturación me notifique automáticamente cuando un expediente esté listo para revisión y registre digitalmente mi aprobación u observación
  Para que el flujo de auditoría sea completamente trazable y eliminar la gestión manual que retrasa el cierre y envío del expediente a la aseguradora

  # Escenario positivo

  Scenario: Notificación y aprobación exitosa del expediente por auditor médico
    Given que el ERP ha consolidado todos los documentos clínicos de un expediente
    And el expediente tiene estado "Listo para auditoría"
    When el auditor médico recibe la notificación y revisa el expediente en el ERP
    Then debe poder registrar su aprobación digitalmente desde la misma interfaz
    And el ERP debe actualizar el estado del expediente a "Aprobado para envío" con usuario, fecha y hora

  # Escenario negativo

  Scenario: Expediente observado por el auditor médico por inconsistencia clínica
    Given que el auditor médico revisa un expediente consolidado en el ERP
    And detecta una inconsistencia entre el diagnóstico registrado y el procedimiento facturado
    When el auditor médico registra una observación en el expediente
    Then el ERP debe actualizar el estado a "Observado - Pendiente corrección" con el detalle de la inconsistencia
    And debe notificar al facturador para que gestione la corrección con el médico tratante
```

```gherkin
Feature RF-07: Consulta automática de póliza del paciente mediante API
  Como admisionista de SanaRed
  Quiero que el sistema consulte de manera directa y automática la póliza del paciente
  Para eliminar las validaciones manuales en portales externos y agilizar el ingreso del paciente

  # Escenario positivo

  Scenario: Consulta exitosa de póliza con cobertura activa
    Given que un paciente llega a admisión y el admisionista ingresa su documento de identidad
    And el paciente tiene una póliza activa con una aseguradora integrada por API
    When el sistema consulta automáticamente la API de la aseguradora
    Then debe retornar los datos de cobertura activa sin que el admisionista acceda a ningún portal externo
    And debe mostrar en pantalla el mensaje "Cobertura verificada" con el detalle de la póliza

  # Escenario negativo

  Scenario: Consulta fallida por paciente sin póliza activa
    Given que un paciente llega a admisión y el admisionista ingresa su documento de identidad
    And el paciente no tiene póliza activa o su póliza está vencida según la API de la aseguradora
    When el sistema consulta automáticamente la API de la aseguradora
    Then debe mostrar el mensaje "Sin cobertura activa" en la interfaz del admisionista
    And debe permitir continuar la admisión como paciente particular
```

```gherkin
Feature RF-08: Registro automático de copago, deducible e ID de autorización en el episodio
  Como admisionista de SanaRed
  Quiero que el sistema registre automáticamente el porcentaje de copago, el deducible y el ID de autorización en el episodio clínico al recibir respuesta de la aseguradora
  Para que no se requiera que el admisionista ingrese a un portal externo ni realice capturas de pantalla

  # Escenario positivo

  Scenario: Registro automático exitoso de datos de cobertura en el episodio
    Given que la API de la aseguradora ha retornado la cobertura activa del paciente
    And la respuesta incluye porcentaje de copago, deducible e ID de autorización
    When el sistema procesa la respuesta de la aseguradora
    Then debe registrar automáticamente el copago, deducible e ID de autorización en el episodio clínico
    And el admisionista no debe ingresar ningún dato manualmente ni tomar capturas de pantalla

  # Escenario negativo

  Scenario: Registro bloqueado por respuesta de aseguradora con datos incompletos
    Given que la API de la aseguradora ha retornado una respuesta de cobertura
    And la respuesta no incluye alguno de los campos requeridos: copago, deducible o ID de autorización
    When el sistema intenta registrar los datos en el episodio clínico
    Then no debe registrar datos parciales en el episodio
    And debe mostrar al admisionista un mensaje indicando los campos faltantes en la respuesta
    And debe registrar el incidente en el log para seguimiento con la aseguradora
```
