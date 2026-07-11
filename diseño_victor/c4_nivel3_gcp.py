"""
C4 Model - Nivel 3: Componentes (Alternativa GCP)
Sistema: Sistema Integrado de Facturación Multinube (Core de Automatización Administrativa)
SanaRed - Fase 5 Facturación - Google Cloud Platform

Convenciones C4 Nivel 3:
  - Personas/Actores: fuera del sistema
  - Sistemas externos: fuera del sistema
  - Componentes internos: dentro del boundary del sistema
  - Relaciones etiquetadas con tecnología y protocolo

Instalar dependencias:
  pip install diagrams

Ejecutar:
  python c4_nivel3_gcp.py
"""

from diagrams import Cluster, Diagram, Edge
from diagrams.gcp.api import APIGateway
from diagrams.gcp.compute import Run, Functions
from diagrams.gcp.database import Firestore
from diagrams.gcp.devtools import Scheduler
from diagrams.gcp.operations import Logging, Monitoring
from diagrams.gcp.security import Iam, Kms
from diagrams.gcp.storage import GCS
from diagrams.gcp.analytics import PubSub
from diagrams.onprem.database import Oracle
from diagrams.onprem.client import Users
from diagrams.onprem.queue import Kafka
from diagrams.generic.blank import Blank

with Diagram(
    "C4 Nivel 3 - Componentes GCP\nSistema Integrado de Facturación Multinube - SanaRed",
    filename="proyecto-integrador-arq-solucion/diseño_victor/c4_nivel3_gcp_output",
    show=False,
    direction="TB"
):

    # ── [Person] Actores externos ──
    facturador = Users("Facturador\n[Person]\nUsuario Administrativo")
    auditor    = Users("Auditor Médico\n[Person]\nUsuario Clínico")

    # ── [Software System] Sistemas externos ──
    with Cluster("[Software Systems] Sistemas Externos"):
        hce        = Oracle("HCE Oracle\n[System: On-Premises]\nHistoria Clínica\nPrestaciones + CIE-10")
        erp        = Oracle("ERP Facturación\n[System: Nube Privada]\nContabilidad Interna")
        lis        = Blank("LIS\n[System: Azure]\nResultados Laboratorio")
        pacs       = Blank("PACS\n[System: Local]\nImágenes Diagnósticas")
        consent    = Blank("SaaS Firma\n[System: Externo]\nConsentimientos")
        aseguradora = Blank("APIs Aseguradoras\n[System: Externo]\nEndpoints RF-01/RF-02")

    # ── [System Boundary] Sistema Integrado de Facturación Multinube ──
    with Cluster("[System Boundary] Sistema Integrado de Facturación Multinube - GCP"):

        # ── [Component] Seguridad y Acceso ──
        with Cluster("[Component] Seguridad y Acceso"):
            idp = Iam("Identity Platform\n[Component: GCP]\nSSO + OAuth 2.0\nRNF-25")
            kms = Blank("Cloud KMS\n[Component: GCP]\nCifrado AES-256\nRNF-23")
            iam = Iam("Cloud IAM\n[Component: GCP]\nControl por Rol\nRNF-06/12")

        # ── [Component] Capa de Integración ──
        with Cluster("[Component] Capa de Integración - RF-01/02/07"):
            apigw = APIGateway("API Gateway\n[Component: GCP]\nWebhooks + OAuth\nHTTPS/TLS 1.3\nRNF-04")
            cf    = Functions("Cloud Functions\n[Component: GCP]\nValidador CIE-10\nIdempotencia\nLA-INT-02 / RF-04")

        # ── [Component] Mensajería Asíncrona ──
        with Cluster("[Component] Mensajería Asíncrona - LA-INT-01"):
            pubsub = PubSub("Cloud Pub/Sub\n[Component: GCP]\nBus de Eventos\nRNF-17")
            dlq    = Kafka("Dead Letter Queue\n[Component: GCP]\nMensajes Fallidos\ntras 3 reintentos\nLA-RES-02")

        # ── [Component] Orquestación ──
        with Cluster("[Component] Orquestación - RF-05/06"):
            cr        = Run("Cloud Run\n[Component: GCP]\nOrquestador Central\nAuto-scaling x2\nRNF-19/21")
            scheduler = Scheduler("Cloud Scheduler\n[Component: GCP]\nPolling Periódico\nRF-02b")

        # ── [Component] Almacenamiento ──
        with Cluster("[Component] Almacenamiento - RNF-16"):
            gcs       = GCS("Cloud Storage\n[Component: GCP]\nBucket Expedientes\nCifrado KMS\nRNF-16/23")
            firestore = Firestore("Firestore\n[Component: GCP]\nEstados + Idempotencia\nLA-INT-02")

        # ── [Component] Notificaciones ──
        with Cluster("[Component] Notificaciones - RNF-05/11"):
            tasks = Blank("Cloud Tasks\n[Component: GCP]\nColas Notificación\n≤ 1 minuto")

        # ── [Component] Observabilidad ──
        with Cluster("[Component] Observabilidad - LA-OBS-01"):
            logging    = Logging("Cloud Logging\n[Component: GCP]\nLogs Inmutables\nCorrelation-ID\nRNF-18/24")
            monitoring = Monitoring("Cloud Monitoring\n[Component: GCP]\nSLA 99.9%\nRNF-10/14")

    # ════════════════════════════════════════
    # Flujo 1: HCE → Pub/Sub → CF → ERP (RF-04)
    # ════════════════════════════════════════
    hce >> Edge(label="Evento prestaciones\n+ CIE-10 [async]") >> pubsub
    pubsub >> Edge(label="Valida CIE-10\nIdempotencia") >> cf
    cf >> Edge(label="Prestaciones válidas\n[HTTP interno]") >> erp
    cf >> Edge(label="Inválido: 3 reintentos\n[DLQ]", color="red") >> dlq
    cf >> Edge(label="Alerta CIE-10\n[async]", color="orange") >> tasks
    tasks >> Edge(label="Bloqueado:\nCodificación incompleta") >> facturador

    # ════════════════════════════════════════
    # Flujo 2: Consolidación Expediente (RF-05)
    # ════════════════════════════════════════
    hce     >> Edge(label="Diagnósticos\ny órdenes [HL7]") >> cr
    lis     >> Edge(label="Resultados lab\n[API REST]") >> cr
    pacs    >> Edge(label="Imágenes\n[DICOM]") >> cr
    consent >> Edge(label="Consentimientos\n[API REST]") >> cr
    cr      >> Edge(label="Expediente consolidado\n[objeto cifrado]") >> gcs
    kms     >> Edge(label="Cifrado AES-256\nen reposo", style="dashed") >> gcs

    # ════════════════════════════════════════
    # Flujo 3: Auditoría Médica (RF-06)
    # ════════════════════════════════════════
    cr    >> Edge(label="Listo para auditoría\n[event]") >> tasks
    tasks >> Edge(label="Notificación\n≤ 1 min [push]") >> auditor
    auditor >> Edge(label="Signed URL TTL 15min\n[LA-SEG-01]", style="dashed") >> gcs
    auditor >> Edge(label="Aprobación /\nObservación [HTTPS]") >> cr
    cr    >> Edge(label="Estado actualizado\n[API REST]") >> erp
    cr    >> Edge(label="Observado:\nPendiente corrección", color="orange") >> tasks
    tasks >> Edge(label="Alerta corrección\n[push]") >> facturador

    # ════════════════════════════════════════
    # Flujo 4: Envío a Aseguradora (RF-01)
    # ════════════════════════════════════════
    erp      >> Edge(label="Expediente aprobado\n[event]") >> pubsub
    pubsub   >> Edge(label="Descarga expediente\n[GCS signed URL]") >> gcs
    pubsub   >> Edge(label="Envío HTTPS\nOAuth 2.0") >> apigw
    apigw    >> Edge(label="POST expediente\nTLS 1.3") >> aseguradora
    firestore >> Edge(label="Verifica idempotencia\n[no duplicar]", style="dashed") >> cf

    # ════════════════════════════════════════
    # Flujo 5: Respuesta Webhook (RF-02)
    # ════════════════════════════════════════
    aseguradora >> Edge(label="Webhook respuesta\n[HTTPS + Token]") >> apigw
    apigw       >> Edge(label="Valida token OAuth") >> cr
    cr          >> Edge(label="Registra estado\n[API REST]") >> erp
    cr          >> Edge(label="Notifica resultado\n[push]") >> tasks

    # ════════════════════════════════════════
    # Flujo 6: Polling RF-02b
    # ════════════════════════════════════════
    scheduler >> Edge(label="Consulta periódica\n[cron]") >> apigw
    apigw     >> Edge(label="GET estado liquidación\n[HTTPS]") >> aseguradora

    # ════════════════════════════════════════
    # Flujo 7: Gestión Observados (RF-03)
    # ════════════════════════════════════════
    cr    >> Edge(label="Observado/Rechazado\n[event]", color="red") >> tasks
    tasks >> Edge(label="Alerta con detalle\n≤ 1 min [push]") >> facturador

    # ════════════════════════════════════════
    # Seguridad
    # ════════════════════════════════════════
    facturador >> Edge(label="SSO [HTTPS]", style="dashed") >> idp
    auditor    >> Edge(label="SSO [HTTPS]", style="dashed") >> idp
    idp >> iam

    # ════════════════════════════════════════
    # Observabilidad
    # ════════════════════════════════════════
    cf     >> Edge(label="Logs + Correlation-ID", style="dashed") >> logging
    cr     >> Edge(label="Logs + Correlation-ID", style="dashed") >> logging
    apigw  >> Edge(label="Logs", style="dashed") >> logging
    logging >> monitoring
