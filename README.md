# 🚦 Bot de Alertas de Tránsito Buenos Aires

Bot de Telegram que monitorea automáticamente el sitio web de AlertasTransito.com y envía notificaciones inteligentes sobre cortes de tránsito, obras, siniestros viales y operativos de emergencia en Buenos Aires y GBA.

## ✨ Características

- 🔍 **Scraping automático** del sitio AlertasTransito.com cada 1.5 horas
- 🚫 **Anti-spam inteligente**: Solo envía mensajes cuando la información cambia
- 📱 **Notificaciones por Telegram** con formato limpio y organizado
- 🎯 **Detección de múltiples tipos de eventos**:
  - Cortes por obra
  - Siniestros viales
  - Operativos de bomberos
  - Manifestaciones y piquetes
- 🧠 **Agrupamiento inteligente** por ubicación geográfica
- 🔄 **Eliminación automática de duplicados**
- 🐧 **Compatible con Docker** para fácil despliegue

## 📋 Requisitos

- Python 3.8+
- Google Chrome o Chromium
- ChromeDriver
- Conexión a internet
- Token de bot de Telegram

## 🚀 Instalación

### Opción 1: Instalación Local

1. **Clona el repositorio**:
```bash
git clone https://github.com/tu-usuario/BotPiquetes.git
cd BotPiquetes
```

2. **Crea un entorno virtual**:
```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate   # En Windows
```

3. **Instala las dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configura las variables de entorno**:
```bash
export TELEGRAM_TOKEN="tu_token_aqui"
export TELEGRAM_CHAT_ID="tu_chat_id_aqui"
```

5. **Ejecuta el bot**:
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

## 🐛 Solución de Problemas

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

## 🔄 Sistema Anti-Spam

El bot incluye un sistema inteligente que:

- ✅ Guarda el último mensaje enviado
- ✅ Compara mensajes nuevos con el anterior
- ✅ Solo envía si hay cambios reales
- ✅ Evita notificaciones duplicadas

Los mensajes se almacenan en `last_message.txt` (excluido del repositorio).

## 📊 Arquitectura

```
piquete_alerta.py
├── obtener_fecha_actual()      # Manejo de fechas en español
├── obtener_pronostico_piquetes() # Web scraping con Selenium
├── should_send_message()       # Sistema anti-spam
├── save_last_message()         # Persistencia de mensajes
├── enviar_alerta_piquetes()    # Envío por Telegram
└── main()                      # Loop principal
```

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras un bug o tienes una mejora:

1. Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Próximas Mejoras

- [ ] Interfaz web para configuración
- [ ] Soporte para múltiples ciudades
- [ ] Integración con más fuentes de información
- [ ] Notificaciones push web
- [ ] API REST para consultas
- [ ] Dashboard de estadísticas

## ⚠️ Limitaciones

- Depende de la estructura HTML del sitio AlertasTransito.com
- Requiere Chrome/Chromium instalado
- Límite de 4096 caracteres por mensaje de Telegram
- Intervalo mínimo recomendado: 30 minutos (para no sobrecargar el sitio)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- [AlertasTransito.com](https://www.alertastransito.com) por proporcionar información pública
- Comunidad de Python y Selenium
- Telegram Bot API

## 📞 Contacto

- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu-email@ejemplo.com

---

**⭐ Si este proyecto te ayuda, considera darle una estrella en GitHub!**

## 🔧 Para Desarrolladores

### Estructura del Proyecto
```
BotPiquetes/
├── piquete_alerta.py       # Script principal
├── requirements.txt        # Dependencias
├── Dockerfile             # Contenedor Docker
├── README.md              # Documentación
├── .gitignore            # Archivos excluidos
└── last_message.txt      # Cache de mensajes (auto-generado)
```

### Debug Mode

Para desarrollo, puedes comentar el envío de Telegram y solo ver los mensajes:

```python
# En enviar_alerta_piquetes(), las líneas de Telegram están comentadas
# Solo se muestra el mensaje en terminal para debugging
```

### Tests

```bash
# Ejecutar una vez para testing
python -c "from piquete_alerta import verificar_piquetes; verificar_piquetes()"
```