Feature: LA-SEG-01: Acceso documental efímero por referencia temporal
  Como Oficial de Seguridad de la Información
  Quiero que el ERP de facturación renderice los soportes clínicos usando URLs firmadas con expiración
  Para evitar la persistencia local de PDFs sensibles y mitigar los riesgos de exposición de datos clínicos

  Scenario: Generación de acceso temporal para la revisión del auditor médico
    Given que un auditor médico inicia sesión en el ERP y selecciona un expediente para su auditoría[cite: 1]
    And el expediente requiere recuperar documentos sensibles del LIS (Azure) y del PACS (GCP)
    When el ERP solicita la visualización de los adjuntos de diagnósticos e imágenes
    Then el sistema debe generar URLs firmadas de manera temporal (AWS Presigned / Azure SAS Tokens)
    And debe otorgar un tiempo de vida (TTL) estricto de 15 minutos al enlace
    And debe invalidar automáticamente el acceso al archivo una vez superado el tiempo de expiración