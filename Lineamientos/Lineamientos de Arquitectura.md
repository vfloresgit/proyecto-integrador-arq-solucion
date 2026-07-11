#Lineamientos de Arquitectura (Especificaciones Técnicas y Criterios de Diseño)
ARQ-01: La solución debe separarse por capas o dominios con responsabilidades claras.
•	Especificación Técnica: El sistema debe estructurarse utilizando un enfoque de Arquitectura Hexagonal o DDD (Domain-Driven Design). Los dominios de "Admisión", "Auditoría Médica" y "Facturación" deben tener fronteras lógicas e infraestructuras de datos aisladas. 
•	Condición de Satisfacción: La capa de presentación (interfaces web/móviles) no puede realizar consultas directas a la base de datos de la Historia Clínica (HCE Oracle on-premises). Toda petición debe pasar obligatoriamente por la capa de aplicación expuesta en el API Gateway. 
ARQ-02: Debe evitarse el acoplamiento fuerte entre componentes.
•	Especificación Técnica: La comunicación entre la infraestructura local on-premises y los servicios distribuidos en AWS/Azure debe implementarse bajo un patrón asíncrono utilizando colas y tópicos duraderos (AWS SQS o Azure Service Bus). 
•	Condición de Satisfacción: Si el ERP de facturación o los portales de las aseguradoras sufren una caída o degradación, la HCE on-premises y el sistema de admisión local de las sedes deben continuar operando y registrando transacciones sin generar bloqueos de hilos ni caídas en cascada. 
ARQ-03: Cada servicio o módulo debe tener una responsabilidad bien definida.
•	Especificación Técnica: Se debe aplicar estrictamente el Principio de Responsabilidad Única (SRP). Los microservicios o funciones serverless deben encargarse de una sola unidad de negocio (ej. un componente exclusivo para validar la elegibilidad de pólizas, otro para enrutar las alertas a la DLQ y otro para consolidar reportes). 
•	Condición de Satisfacción: El componente encargado de procesar y enviar el expediente de cobro (API Despatcher) no debe contener lógica interna para limpiar identidades duplicadas de pacientes; esa tarea le corresponde únicamente al microservicio de EMPI. 
ARQ-04: La arquitectura debe favorecer bajo acoplamiento y alta cohesión.
•	Especificación Técnica: Los componentes internos de un microservicio deben estar íntimamente relacionados con su función principal (alta cohesión) y depender lo mínimo posible de servicios externos para completar su ciclo de vida básico (bajo acoplamiento). 
•	Condición de Satisfacción: El microservicio de facturación debe empaquetar de forma cohesiva la lógica de tarifas, prestaciones y liquidaciones. Si se requiere modificar la lógica de una tarifa corporativa, el impacto debe quedar confinado a este módulo sin alterar el flujo de triaje o agenda médica. 
ARQ-05: Deben preferirse contratos explícitos entre componentes sobre dependencias implícitas.
•	Especificación Técnica: Toda interacción e intercambio de datos entre sistemas (HCE on-premises, LIS en Azure, PACS en GCP y el ERP) debe gobernarse mediante contratos de API formalizados bajo el estándar OpenAPI (REST) o esquemas JSON/HL7 estrictos. 
•	Condición de Satisfacción: Ningún componente en la nube puede realizar consultas directas via links de base de datos (DBLinks) o compartir esquemas de tablas con la base de datos central de la clínica. El intercambio de información contable o clínica se hará únicamente consumiendo los payloads definidos en el contrato de la API. 
ARQ-06: Las reglas de negocio no deben quedar embebidas en canales o interfaces.
•	Especificación Técnica: Las aplicaciones web de admisión, los portales del paciente y las apps móviles de terceros actúan únicamente como capas de captura y renderizado de datos. Las reglas críticas (cálculo de copagos, cruce lógico de diagnósticos CIE-10 y topes de pólizas) deben ejecutarse exclusivamente en el backend de la nube. 
•	Condición de Satisfacción: Si la clínica cambia los porcentajes de deducibles o los criterios para observar un expediente, la actualización se realiza únicamente en el motor de reglas centralizado (AWS Lambda / Azure Functions), sin necesidad de compilar o actualizar las aplicaciones móviles o interfaces del usuario. 
ARQ-07: Los componentes deben poder evolucionar con mínimo impacto lateral.
•	Especificación Técnica: El diseño debe basarse en abstracciones e interfaces. El uso de patrones como Adapter Pattern debe aislar los servicios internos de SanaRed frente a las variaciones tecnológicas de las entidades externas (aseguradoras). 
•	Condición de Satisfacción: Si una aseguradora actualiza su API o cambia su mecanismo de comunicación a Webhooks (RF-02), la modificación técnica solo afectará al adaptador específico de esa aseguradora en la nube, garantizando que el ERP core y el flujo de trabajo de los facturadores permanezcan intactos. 
ARQ-08: Deben definirse criterios claros para decidir entre monolito, microservicios o serverless.
•	Especificación Técnica: Se establecen directrices basadas en patrones de tráfico y criticidad operativa:
o	Serverless (AWS Lambda): Elegido para tareas intermitentes orientadas a eventos con picos de demanda variables, como la ingesta de webhooks de liquidación (RF-02) o consultas masivas de pólizas en campañas corporativas. 
o	Microservicios (AKS): Elegido para procesos Core de larga duración que exigen consistencia transaccional síncrona inmediata y alta transaccionalidad. 
o	Monolito Híbrido: Mantenido estrictamente para los sistemas legados on-premises (HCE Oracle) cuya migración inmediata represente un riesgo clínico inaceptable. 
•	Condición de Satisfacción: La adopción de infraestructura Serverless en la capa perimetral debe justificar una reducción en los costos fijos de TI (pago por uso exacto) y garantizar un escalamiento horizontal automático sin intervención manual del equipo de soporte ante duplicaciones de tráfico.

