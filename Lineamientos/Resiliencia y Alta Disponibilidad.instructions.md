Feature: LA-RES-01: Modo de contingencia por autonomía de sede en admisión
  Como admisionista de la Clínica SanaRed
  Quiero operar con datos de elegibilidad locales si la API externa de la aseguradora se cae
  Para evitar retrasos en el ingreso del paciente y eliminar el uso de formularios de papel

  Scenario: Activación de caché rápida ante fallo de disponibilidad en el portal externo
    Given que un paciente se presenta en ventanilla para una cita ambulatoria durante una campaña masiva
    And la API en tiempo real de la aseguradora asociada no se encuentra disponible (Timeout de 5 segundos)
    When el sistema de admisión central detecta la indisponibilidad del servicio externo
    Then el sistema debe conmutar automáticamente al repositorio de caché local (Azure Cosmos DB / Amazon DynamoDB)
    And debe recuperar los datos de póliza y deducibles si fueron guardados en las últimas 24 horas
    And debe permitir el registro del episodio clínico en el sistema local mostrando una alerta de contingencia

    Feature: LA-RES-02: Gestión de flujo excedente e inmunidad a fallos masivos (DLQ)
  Como Arquitecto de Soluciones Multinube
  Quiero aislar de forma automatizada los mensajes de facturación corruptos o incompatibles
  Para evitar que los errores estructurales detengan el pipeline de facturación en horas de alta demanda

  Scenario: Aislamiento de un mensaje con errores de codificación graves en la cola de fallas
    Given que el bus de integración multinube está procesando una carga masiva de expedientes de facturación
    When un mensaje estructurado contiene un formato de prestación inválido y falla tras 3 reintentos automáticos
    Then el sistema debe extraer el mensaje del flujo de procesamiento principal
    And debe moverlo de manera automática a la cola de mensajes no entregados (Dead Letter Queue - DLQ)
    And debe continuar procesando las siguientes facturas de la cola sin generar cuellos de botella ni caídas del integrador