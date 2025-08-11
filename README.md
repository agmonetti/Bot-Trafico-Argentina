# 🚦 Bot de Alertas de Tránsito Buenos Aires

Bot de Telegram que monitorea automáticamente el sitio web de AlertasTransito.com y envía notificaciones inteligentes sobre cortes de tránsito, obras, siniestros viales y operativos de emergencia en Buenos Aires y GBA.

## Características

- **Scraping automático** del sitio AlertasTransito.com cada 1.5 horas
- **Anti-spam inteligente**: Solo envía mensajes cuando la información cambia
- **Notificaciones por Telegram** con formato limpio y organizado
- **Detección de múltiples tipos de eventos**:
  - Cortes por obra
  - Siniestros viales
  - Operativos de bomberos
  - Manifestaciones y piquetes
- **Agrupamiento inteligente** por ubicación geográfica
- **Eliminación automática de duplicados**
- **Compatible con Docker** para fácil despliegue

## 📋 Requisitos

- Python 3.8+
- Google Chrome o Chromium
- ChromeDriver
- Conexión a internet
- Token de bot de Telegram

## Instalación

### Opción 1: Instalación Local

1. **Clona el repositorio**:
```bash
git clone https://github.com/tu-usuario/Bot-Trafico-Argentina.git
cd Bot-Trafico-Argentina
```

2. **Configura las variables de entorno**:
```bash
# Copia el template
cp .env.template .env

# Edita .env con tus tokens reales
# TELEGRAM_TOKEN=tu_token_real
# TELEGRAM_CHAT_ID=tu_chat_id_real
```

3. **Instala dependencias**:
```bash
pip install -r requirements.txt
```

4. **Ejecuta el bot**:
```bash
python piquete_alerta.py
```

### Opción 2: Docker

1. **Construye la imagen**:
```bash
docker build -t bot-piquetes .
```

2. **Ejecuta el contenedor**:
```bash
docker run -e TELEGRAM_TOKEN="tu_token" -e TELEGRAM_CHAT_ID="tu_chat_id" bot-piquetes
```

## ⚙️ Configuración

### Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `TELEGRAM_TOKEN` | Token del bot de Telegram | `123456789:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `TELEGRAM_CHAT_ID` | ID del chat donde enviar mensajes | `123456789` |

### Obtener Token de Telegram

1. Habla con [@BotFather](https://t.me/BotFather) en Telegram
2. Crea un nuevo bot con `/newbot`
3. Copia el token que te proporciona
4. Para obtener el Chat ID, envía un mensaje a tu bot y visita:
   ```
   https://api.telegram.org/bot<TU_TOKEN>/getUpdates
   ```

## 🔧 Personalización

### Modificar Intervalo de Ejecución

Edita la variable `INTERVALO_EJECUCION` en `piquete_alerta.py`:

```python
INTERVALO_EJECUCION = 5400  # 1.5 horas en segundos
# INTERVALO_EJECUCION = 3600  # 1 hora
# INTERVALO_EJECUCION = 1800  # 30 minutos
```

### Agregar Nuevas Secciones

Modifica la lista `secciones_validas` para detectar nuevos tipos de eventos:

```python
secciones_validas = [
    'MANIFESTACIONES', 
    'CORTE POR OBRA', 
    'SINIESTROS VIALES', 
    'EVENTOS DEPORTIVOS', 
    'OBRAS',
    'OPERATIVO DE BOMBEROS',
    'TU_NUEVA_SECCION'  # Agrega aquí
]
```

## 📱 Ejemplo de Mensaje

```
🚦 ALERTA DE TRÁNSITO - 8 DE AGOSTO

⚠️ EVENTOS DE TRÁNSITO REPORTADOS:

🕐 Horario no especificado
📍 Av. Olazabal y Superi - Corte total - Obra EMUI

🕐 Horario no especificado
📍 Av. Gral. Paz altura Av. Emilio Castro - Corte total sentido Riachuelo

🕐 Horario no especificado
📍 Av. Gaona y Joaquín V. Gonzalez - Reducción de calzada
```

## Solución de Problemas

### El bot no encuentra información

- Verifica que la fecha del sistema sea correcta
- El sitio web puede haber cambiado su estructura
- Revisa los logs para ver qué secciones se detectaron

### Error de ChromeDriver

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install chromium-browser chromium-chromedriver

# Arch Linux
sudo pacman -S chromium chromedriver
```

### Error de permisos con pip

Usa un entorno virtual en lugar de instalación global:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Sistema Anti-Spam

El bot incluye un sistema inteligente que:

- ✅ Guarda el último mensaje enviado
- ✅ Compara mensajes nuevos con el anterior
- ✅ Solo envía si hay cambios reales
- ✅ Evita notificaciones duplicadas

Los mensajes se almacenan en `last_message.txt` (excluido del repositorio).


## ⚠️ Limitaciones

- Depende de la estructura HTML del sitio AlertasTransito.com
- Requiere Chrome/Chromium instalado
- Límite de 4096 caracteres por mensaje de Telegram
- Intervalo mínimo recomendado: 30 minutos (para no sobrecargar el sitio)

## Agradecimientos

- [AlertasTransito.com](https://www.alertastransito.com) por proporcionar información pública
- Comunidad de Python y Selenium
- Telegram Bot API

## Creditos

- Desarrollado por Agustin Monetti.
- GitHub: [@agmonetti](https://github.com/agmonetti)
- Email: agmonetti@uade.edu.ar

---
