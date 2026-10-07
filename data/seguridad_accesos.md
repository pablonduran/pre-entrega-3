Normativa de Seguridad y Gestion de Accesos

1. Autenticacion y Autorizacion de Servicios
- Todas las APIs externas e internas estan protegidas mediante OAuth 2.0 y tokens JWT (JSON Web Tokens).
- Vigencia de credenciales:
  - Los Access Tokens tienen una validez maxima de 15 minutos.
  - Los Refresh Tokens tienen una validez de 7 dias y se invalidan ante cambio de contrasena o cierre de sesion.

2. Acceso Administrativo a Infraestructura
- El acceso directo por SSH a servidores o clusters de base de datos esta prohibido desde la internet publica.
- El personal tecnico debe conectarse a traves de la VPN interna WireGuard.
- Es obligatorio el uso de autenticacion multifactor (MFA) respaldado por llaves de hardware FIDO2 o aplicaciones TOTP autorizadas.

3. Gestion de Secretos y Llaves API
- Queda terminantemente prohibido almacenar contrasenas, tokens o claves de API en el codigo fuente.
- Los secretos se administran centralizadamente en HashiCorp Vault.
- Las llaves de servicio y credenciales de bases de datos se rotan automaticamente cada 90 dias.
