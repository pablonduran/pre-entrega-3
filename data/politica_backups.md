Politica de Copias de Seguridad (Backups)

1. Frecuencia y Tipos de Backup
- Bases de datos principales (PostgreSQL y MySQL):
  - Backup incremental diario programado a las 02:00 UTC.
  - Backup completo semanal programado los domingos a las 03:00 UTC.
- Volumenes de archivos y almacenamiento de usuarios:
  - Snapshots diarios de volumenes EBS a las 04:00 UTC.

2. Almacenamiento y Cifrado
- Todos los respaldos se envian a buckets dedicados en AWS S3 con cifrado en reposo habilitado mediante AES-256.
- Politica de ciclo de vida:
  - Primeros 30 dias en S3 Standard para recuperacion inmediata.
  - De 31 a 365 dias en S3 Glacier Flexible Retrieval para cumplimiento legal y auditoria.
  - Eliminacion definitiva automatica tras 365 dias.

3. Metricas de Recuperacion y Pruebas
- RPO (Punto Objetivo de Recuperacion): Maximo 1 hora de perdida de datos tolerable.
- RTO (Tiempo Objetivo de Recuperacion): Maximo 4 horas para restablecer el servicio critico.
- Simulacro de restauracion: Se realiza de forma obligatoria el primer martes de cada mes en un entorno aislado de staging.
