# Guia rapida para la practica de Jenkins

Esta configuracion esta pensada para el backend Python de este repositorio. El objetivo es que puedas levantar Jenkins, conectarlo a GitHub y ejecutar una pipeline sencilla de integracion continua.

## 1. Archivos preparados

- `backend/Jenkinsfile`: pipeline para Jenkins.
- `backend/jenkins/docker-compose.yml`: servidor Jenkins con Docker.
- `backend/jenkins/.env.jenkins.example`: ejemplo de variables para credenciales.
- `backend/jenkins/take-screenshot.ps1`: script para capturas de pantalla desde PowerShell.

## 2. Comandos para instalar y arrancar Jenkins

Ejecuta estos comandos desde la raiz del repo:

```powershell
cd C:\Users\dylan\Desktop\proyecto\proyecto\backend\jenkins
docker compose up -d
docker ps
```

Abre Jenkins en:

```text
http://localhost:8085
```

Para obtener la clave inicial del administrador:

```powershell
docker exec backend-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

## 3. Capturas recomendadas para el apartado 1

Haz capturas de:

1. Contenedor Jenkins levantado con `docker ps`.
2. Pantalla de desbloqueo de Jenkins.
3. Instalacion de plugins sugeridos.
4. Panel `Manage Jenkins`.
5. Pantalla de credenciales creadas.

## 4. Plugins recomendados

Instala al menos estos:

- `Pipeline`
- `Git`
- `GitHub`
- `Credentials Binding`
- `Plain Credentials`
- `Matrix Authorization Strategy` si quieres enseñar seguridad/permisos

## 5. Credenciales en Jenkins

En `Manage Jenkins > Credentials`, crea dos credenciales de tipo `Secret text`:

- ID: `backend-database-url`
- ID: `backend-jwt-secret`

Si quieres documentarlo mejor, explica que Jenkins inyecta estos secretos en la pipeline sin guardarlos en el repositorio.

## 6. Creacion del job

Para el apartado 2, crea un job de tipo `Pipeline`:

1. `New Item`
2. Nombre sugerido: `backend-ci`
3. Tipo: `Pipeline`
4. Marca `GitHub project` y pega la URL del repo
5. En `Pipeline`, selecciona `Pipeline script from SCM`
6. `SCM`: `Git`
7. URL del repositorio: la vuestra
8. Branch: `*/main` o la rama que useis
9. `Script Path`: `backend/Jenkinsfile`

## 7. Lanzamiento del job

Para el apartado 3:

1. Guarda el job.
2. Pulsa `Build Now`.
3. Entra en `Build History`.
4. Abre `Console Output`.
5. Comprueba que aparecen las fases `Checkout`, `Prepare Python`, `Static Validation` y `Health Smoke Test`.

## 8. Comandos para capturas de pantalla

Desde PowerShell, en otra terminal:

```powershell
cd C:\Users\dylan\Desktop\proyecto\proyecto\backend\jenkins
powershell -ExecutionPolicy Bypass -File .\take-screenshot.ps1
```

Para guardar varias capturas con nombres reconocibles:

```powershell
powershell -ExecutionPolicy Bypass -File .\take-screenshot.ps1 -Prefix 01-jenkins-login
powershell -ExecutionPolicy Bypass -File .\take-screenshot.ps1 -Prefix 02-plugins
powershell -ExecutionPolicy Bypass -File .\take-screenshot.ps1 -Prefix 03-credenciales
powershell -ExecutionPolicy Bypass -File .\take-screenshot.ps1 -Prefix 04-job-pipeline
powershell -ExecutionPolicy Bypass -File .\take-screenshot.ps1 -Prefix 05-build-now
powershell -ExecutionPolicy Bypass -File .\take-screenshot.ps1 -Prefix 06-console-output
```

Todas se guardaran en:

```text
backend\jenkins\capturas
```

## 9. Comandos utiles para la memoria

Ver logs del contenedor:

```powershell
docker logs backend-jenkins
```

Ver logs en tiempo real:

```powershell
docker logs -f backend-jenkins
```

Parar Jenkins:

```powershell
cd C:\Users\dylan\Desktop\proyecto\proyecto\backend\jenkins
docker compose down
```

## 10. Texto breve que puedes explicar en la entrega

La integracion continua se ha implementado con Jenkins mediante una pipeline declarativa almacenada en el repositorio. Cada ejecucion clona el codigo del backend, crea un entorno virtual de Python, instala dependencias y realiza comprobaciones basicas de integridad, compilacion e invocacion del endpoint `/health`. Las credenciales sensibles, como la conexion a la base de datos y la clave JWT, se gestionan desde Jenkins para evitar exponer secretos en el repositorio.
