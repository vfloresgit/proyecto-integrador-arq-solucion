"""
Diagrama de Arquitectura - Fase 5: Facturación
SanaRed - Google Cloud Platform
Generado con diagrams (https://diagrams.mingrammer.com)

Instalar dependencias:
  pip install diagrams
  pip install diagrams[gcp]

Ejecutar:
  python diagrama_arquitectura.py
"""

from diagrams import Cluster, Diagram, Edge
from diagrams.gcp.api import APIGateway
from diagrams.gcp.compute import Run, Functions
from diagrams.gcp.database import Firestore
from diagrams.gcp.devtools import Scheduler
from diagrams.gcp.iot import IotCore
from diagrams.gcp.network import LoadBalancing
from diagrams.gcp.operations import Logging, Monitoring
from diagrams.gcp.security import Iam
from diagrams.generic.blank import Blank
from diagrams.gcp.storage import GCS
from diagrams.onprem.database import Oracle
from diagrams.onprem.client import Users
from diagrams.generic.blank import Blank
from diagrams.custom import Custom

with Diagram(
    "Fase 5 - Facturación SanaRed / Google Cloud",
    filename="proyecto-integrador-arq-solucion/diseño_victor/diagrama_arquitectura_output",
    show=False,
    direction="TB"
):

    # ── Actores ──
    with Cluster("Actores"):
        facturador = Users("Facturador")
        auditor = Users("Auditor Médico")

    # ── On-Premises ──
    with Cluster("On-Premises SanaRed"):
        hce = Oracle("HCE Oracle\nHistoria Clínica\nPrestaciones + CIE-10")
        erp = Oracle("ERP Facturación\nNube Privada\nProveedor Local")

    # ── Sistemas Externos ──
    with Cluster("Sistemas Externos"):
        lis = Blank("LIS - Azure\nResultados Lab")
        pacs = Blank("PACS - Local\nImágenes")
        consent = Blank("SaaS Firma\nElectrónica")
        aseguradora = Blank("Aseguradoras\nAPI / Webhook")

    # ── Google Cloud ──
    with Cluster("Google Cloud Platform"):

        with Cluster("Seguridad y Acceso"):
            idp = Iam("Identity Platform\nSSO + OAuth 2.0")
            kms = Blank("Cloud KMS\nAES-256")
            iam = Iam("Cloud IAM\nRoles")

        with Cluster("Capa de Integración"):
            apigw = APIGateway("API Gateway\nWebhooks + OAuth")
            cf = Functions("Cloud Functions\nValidador CIE-10\nIdempotencia")

        with Cluster("Mensajería Asíncrona"):
            pubsub = Blank("Cloud Pub/Sub\nBus de Eventos")
            dlq = Blank("Dead Letter Queue\nMensajes Fallidos")

        with Cluster("Orquestación"):
            cr = Run("Cloud Run\nOrquestador\nAuto-scaling x2")
            scheduler = Scheduler("Cloud Scheduler\nPolling Periódico\nRF-02b")

        with Cluster("Almacenamiento"):
            gcs = GCS("Cloud Storage\nBucket Expedientes\nCifrado KMS")
            firestore = Firestore("Firestore\nEstados\nIdempotencia")

        with Cluster("Notificaciones"):
            tasks = Blank("Cloud Tasks\nNotificaciones\n≤ 1 minuto")

        with Cluster("Observabilidad"):
            logging = Logging("Cloud Logging\nLogs Inmutables\nCorrelation-ID")
            monitoring = Monitoring("Cloud Monitoring\nSLA 99.9%")

    # ── Flujo 1: HCE → ERP (RF-04) ──
    hce >> Edge(label="Evento prestaciones\n+ CIE-10") >> pubsub
    pubsub >> Edge(label="Valida CIE-10\nIdempotencia") >> cf
    cf >> Edge(label="Prestaciones válidas") >> erp
    cf >> Edge(label="Inválido tras\n3 reintentos", color="red") >> dlq
    cf >> Edge(label="Alerta codificación", color="orange") >> tasks
    tasks >> Edge(label="Bloqueado: CIE-10\nincompleto") >> facturador

    # ── Flujo 2: Consolidación Expediente (RF-05) ──
    hce >> Edge(label="Diagnósticos\ny órdenes") >> cr
    lis >> Edge(label="Resultados lab") >> cr
    pacs >> Edge(label="Imágenes") >> cr
    consent >> Edge(label="Consentimientos") >> cr
    cr >> Edge(label="Expediente\nconsolidado") >> gcs
    kms >> Edge(label="Cifrado\nen reposo") >> gcs

    # ── Flujo 3: Auditoría Médica (RF-06) ──
    cr >> Edge(label="Listo para\nauditoría") >> tasks
    tasks >> Edge(label="Notif ≤ 1min") >> auditor
    auditor >> Edge(label="Signed URL\nTTL 15min", style="dashed") >> gcs
    auditor >> Edge(label="Aprobación /\nObservación") >> cr
    cr >> Edge(label="Estado actualizado") >> erp
    cr >> Edge(label="Observado:\nNotifica corrección", color="orange") >> tasks
    tasks >> Edge(label="Alerta corrección") >> facturador

    # ── Flujo 4: Envío a Aseguradora (RF-01) ──
    erp >> Edge(label="Expediente\naprobado") >> pubsub
    pubsub >> Edge(label="Descarga\nexpediente") >> gcs
    pubsub >> Edge(label="Envío HTTPS\nOAuth 2.0") >> apigw
    apigw >> Edge(label="POST TLS 1.3") >> aseguradora
    firestore >> Edge(label="Verifica\nidempotencia", style="dashed") >> cf

    # ── Flujo 5: Webhook Aseguradora (RF-02) ──
    aseguradora >> Edge(label="Webhook\nrespuesta") >> apigw
    apigw >> Edge(label="Valida token") >> cr
    cr >> Edge(label="Registra estado:\nAprobado/Rechazado") >> erp
    cr >> Edge(label="Notifica resultado") >> tasks

    # ── Flujo 6: Polling (RF-02b) ──
    scheduler >> Edge(label="Consulta\nperiódica") >> apigw
    apigw >> Edge(label="GET estado") >> aseguradora

    # ── Flujo 7: Gestión Observados (RF-03) ──
    cr >> Edge(label="Observado/Rechazado\n≤ 1min", color="red") >> tasks
    tasks >> Edge(label="Alerta con\ndetalle motivo") >> facturador

    # ── Seguridad ──
    facturador >> Edge(label="SSO", style="dashed") >> idp
    auditor >> Edge(label="SSO", style="dashed") >> idp
    idp >> iam

    # ── Observabilidad ──
    cf >> Edge(label="Logs +\nCorrelation-ID", style="dashed") >> logging
    cr >> Edge(label="Logs +\nCorrelation-ID", style="dashed") >> logging
    apigw >> Edge(label="Logs", style="dashed") >> logging
    logging >> monitoring
