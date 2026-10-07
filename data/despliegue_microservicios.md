Guia de Despliegue de Microservicios

1. Integracion y Entrega Continua (CI/CD)
- El codigo se integra mediante Pull Requests en GitHub con revision obligatoria de dos ingenieros.
- GitHub Actions ejecuta pruebas unitarias, analisis de vulnerabilidades con SonarQube y construccion de imagenes Docker.
- Las imagenes etiquetadas con el hash de commit se publican en GitHub Container Registry (GHCR).

2. Orquestacion y Plataforma
- El orquestador principal es Kubernetes administrado en AWS EKS.
- La sincronizacion declarativa del estado de la infraestructura se realiza mediante ArgoCD siguiendo practicas de GitOps.

3. Estrategia de Despliegue y Rollback
- Se utiliza una estrategia Blue/Green combinada con Canary release.
- Al publicar una nueva version, un 10% del trafico se redirige a los pods Canary durante un lapso de 15 minutos para medir la tasa de errores y latencia con Prometheus.
- Si la tasa de respuestas HTTP 5xx supera el 1% o la latencia media se incrementa mas del 25%, ArgoCD activa un rollback automatico cancelando el despliegue en menos de 60 segundos.
