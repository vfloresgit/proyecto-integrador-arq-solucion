Feature: LA-INT-01: Desacoplamiento asíncrono entre sistemas locales y nube
  Como Arquitecto multinube de SanaRed
  Quiero que la HCE local envíe las prestaciones al ERP mediante un bus de eventos distribuidos
  Para asegurar que una caída en el enlace o en el ERP no bloquee la continuidad del registro clínico

  Scenario: Sincronización de prestaciones cuando el ERP de facturación no está disponible
    Given que el médico tratante cierra un episodio clínico en la HCE on-premises
    And el canal de comunicación o el ERP en la nube privada experimenta una caída temporal
    When la HCE despacha el evento con las prestaciones y códigos CIE-10 del paciente
    Then el sistema de mensajería (AWS SQS / Azure Service Bus) debe recibir y persistir el payload de forma segura[cite: 1, 2]
    And debe mantener el mensaje en la cola con estado "Pendiente de procesamiento"
    And la interfaz de la HCE local no debe congelarse ni mostrar errores al usuario clínico

  Feature: LA-INT-02: Idempotencia en el procesamiento de cobros a aseguradoras
  Como motor de integración de SanaRed
  Quiero procesar las solicitudes de envío de expedientes de forma idempotente
  Para prevenir cobros duplicados ante las aseguradoras causados por reintentos automáticos de la red

  Scenario: Intento de reenvío automático de un expediente de facturación ya despachado
    Given que un expediente de facturación con el ID único "FAC-2026-9876" fue enviado con éxito a la aseguradora
    When el bus de eventos multinube intenta procesar un duplicado del mismo mensaje por una política de reintento
    Then el sistema de orquestación debe verificar el ID único contra el registro del estado actual en la base de datos
    And debe descartar el procesamiento del payload duplicado sin enviarlo nuevamente a la API externa de la aseguradora
    And debe registrar el evento en el log con la etiqueta "Mensaje duplicado omitido - Idempotencia aplicada"