# Sistema de Cotizaciones - Capital & Farmer

## Instalación

1. Clona el repositorio:  
   `git clone `

2. Accede a la carpeta del proyecto:  
   `cd apellido-capital-farmer-exam`

3. Crea y activa un entorno virtual (opcional pero recomendado):  
   - Windows PowerShell:  
     `python -m venv venv`  
     `.\venv\Scripts\Activate.ps1``


## Uso

- Abre tu navegador y visita: `http://localhost:5000`  
- Completa el formulario con tus datos y descripción del caso legal.  
- Al enviar, recibirás una cotización automática con análisis de complejidad, ajuste de precio recomendado, servicios adicionales y propuesta profesional generada con inteligencia artificial.  
- Los datos se almacenan en la base de datos SQLite `cotizaciones.db`.

## APIs utilizadas

- **OpenAI API** (modelo GPT-4o-mini) para el análisis de complejidad y generación automática de propuestas profesionales.


## Funcionalidades bonus implementadas

- Integración con OpenAI para enriquecer cotizaciones con inteligencia artificial.  
- Manejo de errores en la llamada a la API.  
- Generación de un número de cotización único.  
- Almacenamiento de cotizaciones en SQLite.  


## Respuestas 
1.Arquitectura Modular:
Modularizaría el sistema usando una arquitectura basada en microservicios o módulos desacoplados, cada uno con su propia lógica y base de datos si es posible. Se comunicarían vía APIs REST o eventos, permitiendo que cada módulo evolucione y se mantenga de forma independiente sin afectar a los demás.

2.Escalabilidad:
Para escalar de 10 a 100 usuarios, migraría la base SQLite a un motor cliente-servidor como PostgreSQL o SQL Server para manejar mayor concurrencia y transacciones. También implementaría índices en columnas claves y optimizaría consultas para mejorar el rendimiento.

3.Integraciones:
Automatizaría el guardado de documentos mediante APIs de Google Drive o Dropbox, integrando OAuth para autenticación segura y usando webhooks o triggers que al guardar o actualizar un documento en el sistema dispare el upload automático a la nube.

4.Deployment:
Desplegaría la aplicación en servicios cloud económicos como Heroku o Railway, que soportan despliegue continuo, auto escalado básico y HTTPS, facilitando acceso desde cualquier dispositivo con bajo costo y sin complicaciones de infraestructura.

5.Seguridad:
Implementaría HTTPS para cifrar la comunicación, validaría y sanitizaría toda entrada del usuario, almacenaría contraseñas con hash seguro, limitaría accesos mediante roles básicos y mantendría actualizadas las dependencias para reducir vulnerabilidades.