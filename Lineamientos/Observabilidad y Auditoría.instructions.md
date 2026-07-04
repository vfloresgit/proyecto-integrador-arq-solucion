Feature: LA-OBS-01: Trazabilidad distribuida única en el ecosistema multinube
  Como ingeniero del equipo de Soporte y SRE de SanaRed
  Quiero que cada transacción administrativa genere un ID de correlación único y global
  Para rastrear el ciclo de vida completo de un expediente clínico a través de los sistemas desconexos

  Scenario: Seguimiento de logs distribuidos durante una auditoría o fallo técnico
    Given que se registra una nueva orden de atención o cobro en el sistema
    When la arquitectura genera y asocia un identificador único global (Correlation-ID) a la transacción
    Then todas las trazas de logs emitidas por la HCE on-premises, el portal AWS, las APIs de Azure y el ERP deben estampar dicho ID
    And el equipo de TI debe poder buscar el ID en el panel central de observabilidad y ver la secuencia temporal completa del caso