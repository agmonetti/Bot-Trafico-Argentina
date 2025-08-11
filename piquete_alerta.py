import time
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, date
import re

# Cargar variables de entorno desde .env
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Variables de entorno cargadas desde .env")
except ImportError:
    print("⚠️ python-dotenv no instalado. Usando variables de entorno del sistema.")

# ========================
# CONFIGURACIÓN
# ========================
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
URL_PIQUETES = 'https://www.alertastransito.com/p/pronostico-de-piquetes.html'
INTERVALO_EJECUCION = 5400  # 1:30 hora en segundos

# Verificar que las variables estén configuradas
if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ ERROR: TELEGRAM_TOKEN y TELEGRAM_CHAT_ID deben estar configurados")
    print(f"TELEGRAM_TOKEN configurado: {'✅' if TELEGRAM_TOKEN else '❌'}")
    print(f"TELEGRAM_CHAT_ID configurado: {'✅' if TELEGRAM_CHAT_ID else '❌'}")
else:
    print("✅ Variables de Telegram configuradas correctamente")

def obtener_fecha_actual():
    """
    Obtiene la fecha actual en diferentes formatos.
    """
    ahora = datetime.now()
    fecha_obj = ahora.date()
    
    # Meses en español
    meses_es = {
        1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
        5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
        9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
    }
    
    mes_nombre = meses_es[fecha_obj.month]
    
    return {
        'objeto': fecha_obj,
        'formato_es': f"{fecha_obj.day} de {mes_nombre}",
        'dia': fecha_obj.day,
        'mes': fecha_obj.month,
        'año': fecha_obj.year,
        'timestamp': ahora,
        'mes_nombre': mes_nombre
    }

def obtener_pronostico_piquetes():
    """
    Obtiene el pronóstico de piquetes del día actual usando Selenium.
    """
    driver = None
    piquetes_hoy = []
    
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1200,800')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(URL_PIQUETES)
        
        # Esperar a que cargue la página
        time.sleep(8)
        
        # Obtener fecha actual DINÁMICA
        fecha_actual = obtener_fecha_actual()
        hoy = fecha_actual['objeto']
        
        # Formatear fecha como aparece en la página
        dias_semana = {
            0: 'LUNES', 1: 'MARTES', 2: 'MIÉRCOLES', 3: 'JUEVES',
            4: 'VIERNES', 5: 'SÁBADO', 6: 'DOMINGO'
        }
        
        meses_es_mayus = {
            1: 'ENERO', 2: 'FEBRERO', 3: 'MARZO', 4: 'ABRIL',
            5: 'MAYO', 6: 'JUNIO', 7: 'JULIO', 8: 'AGOSTO',
            9: 'SEPTIEMBRE', 10: 'OCTUBRE', 11: 'NOVIEMBRE', 12: 'DICIEMBRE'
        }
        
        dia_semana = dias_semana[hoy.weekday()]
        mes_nombre = meses_es_mayus[hoy.month]
        dia_numero = hoy.day
        
        fecha_buscada = f"{dia_semana} {dia_numero} DE {mes_nombre}"
        
        print(f"🗓️ Fecha actual del sistema: {fecha_actual['formato_es']}")
        print(f"🔍 Buscando: {fecha_buscada}")
        
        # Guardar HTML para depuración
        html_content = driver.page_source
        with open("piquetes_debug.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("📄 HTML guardado en piquetes_debug.html para análisis")
        
        # Obtener el texto completo de la página
        page_text = driver.execute_script("return document.body.innerText;")
        print("📖 Contenido de la página (primeros 3000 caracteres):")
        print(page_text[:3000])
        print("\n--- FIN DEL CONTENIDO ---")
        
        # Dividir en líneas para análisis línea por línea
        lines = page_text.split('\n')
        
        # Buscar la fecha específica del día y la sección MANIFESTACIONES
        fecha_encontrada = False
        en_seccion_manifestaciones = False
        info_piquetes = []
        
        for i, line in enumerate(lines):
            line_clean = line.strip()
            
            # Buscar la fecha del día actual
            if fecha_buscada in line_clean:
                fecha_encontrada = True
                print(f"✅ Encontrada fecha: {line_clean}")
                
                # Buscar cualquier sección de tránsito después de la fecha
                j = i + 1
                secciones_validas = ['MANIFESTACIONES', 'CORTE POR OBRA', 'SINIESTROS VIALES', 'EVENTOS DEPORTIVOS', 'OBRAS', 'OPERATIVO DE BOMBEROS']
                en_seccion_manifestaciones = False
                
                while j < len(lines):
                    siguiente_linea = lines[j].strip()
                    
                    # Si encontramos cualquier sección válida, comenzar a extraer información
                    if siguiente_linea in secciones_validas:
                        en_seccion_manifestaciones = True
                        print(f"✅ Encontrada sección: {siguiente_linea}")
                        j += 1
                        continue
                    
                    # Si estamos en una sección válida, extraer información
                    if en_seccion_manifestaciones:
                        # Parar si encontramos otra fecha
                        if (any(dia in siguiente_linea for dia in dias_semana.values()) and 
                            any(mes in siguiente_linea for mes in meses_es_mayus.values()) and
                            siguiente_linea != line_clean):
                            print(f"🛑 Fin de sección, encontrada nueva fecha: {siguiente_linea}")
                            break
                        
                        # Parar si encontramos otra sección mayor (como "OBRAS Actualizadas")
                        if siguiente_linea.startswith('⚠️') or siguiente_linea.startswith('🚧') or siguiente_linea.startswith('📆'):
                            print(f"🛑 Fin de sección, encontrada nueva sección: {siguiente_linea}")
                            break
                        
                        # Agregar líneas con información útil de tránsito
                        if (siguiente_linea and 
                            len(siguiente_linea) > 5 and
                            siguiente_linea not in ['', '-', '•'] and
                            not siguiente_linea.startswith('📄') and
                            not siguiente_linea.startswith('🔍')):
                            
                            # Detectar información relevante de tránsito
                            palabras_clave = ['av.', 'calle', 'corte', 'obra', 'siniestro', 'manifestación', 
                                            'piquete', 'tránsito', 'policía', 'bomberos', 'incendio', 
                                            'reducción', 'involucra', 'altura', 'sentido']
                            
                            if any(palabra in siguiente_linea.lower() for palabra in palabras_clave) or siguiente_linea.isupper():
                                info_piquetes.append(siguiente_linea)
                                print(f"📝 Agregando información de tránsito: {siguiente_linea}")
                    
                    j += 1
                break
        
        if not fecha_encontrada:
            print(f"❌ No se encontró la fecha {fecha_buscada}")
            return []
        
        if not en_seccion_manifestaciones:
            print(f"❌ No se encontraron secciones de tránsito válidas para {fecha_buscada}")
            return []
        
        # Procesar la información encontrada agrupando por ubicación y eliminando duplicados
        if info_piquetes:
            print(f"📋 Información de tránsito encontrada: {len(info_piquetes)} líneas")
            
            # Set para detectar ubicaciones ya procesadas
            ubicaciones_procesadas = set()
            descripciones_vistas = set()
            
            # Mejorar el agrupamiento de información
            i = 0
            while i < len(info_piquetes):
                linea_actual = info_piquetes[i].strip()
                
                # Detectar si es una ubicación real (contiene indicadores de ubicación)
                indicadores_ubicacion = ['Av.', 'calle', 'MTB', 'Acceso']
                
                # También detectar intersecciones (nombre y nombre) pero no descripciones
                es_interseccion = (' y ' in linea_actual and len(linea_actual.split()) <= 5 and
                                 not any(word in linea_actual.lower() for word in ['bomberos', 'agentes', 'lugar', 'policía', 'particular', 'colectivo']))
                
                es_ubicacion = ((any(indicator in linea_actual for indicator in indicadores_ubicacion) or es_interseccion) and
                               not linea_actual.lower().startswith(('reduccion', 'corte total', 'obra ', 'involucra', 'policia')))
                
                if es_ubicacion:
                    ubicacion = linea_actual
                    
                    # Verificar si ya procesamos esta ubicación
                    if ubicacion in ubicaciones_procesadas:
                        print(f"🔄 Ubicación duplicada ignorada: {ubicacion}")
                        i += 1
                        continue
                    
                    ubicaciones_procesadas.add(ubicacion)
                    descripcion_partes = []
                    
                    # Buscar las siguientes líneas que describen el evento
                    j = i + 1
                    while j < len(info_piquetes):
                        siguiente = info_piquetes[j].strip()
                        
                        # Parar si encontramos otra ubicación válida
                        es_siguiente_interseccion = (' y ' in siguiente and len(siguiente.split()) <= 5 and
                                                   not any(word in siguiente.lower() for word in ['bomberos', 'agentes', 'lugar', 'policía', 'particular', 'colectivo']))
                        if ((any(indicator in siguiente for indicator in indicadores_ubicacion) or es_siguiente_interseccion) and
                            not siguiente.lower().startswith(('reduccion', 'corte total', 'obra ', 'involucra', 'policia'))):
                            break
                            
                        # Agregar información descriptiva no duplicada
                        if (siguiente and len(siguiente) > 3 and
                            not siguiente.startswith('🛑') and 
                            not siguiente.startswith('📝') and
                            siguiente not in descripcion_partes):  # Evitar duplicados en la misma descripción
                            descripcion_partes.append(siguiente)
                        
                        j += 1
                    
                    # Crear descripción completa
                    if descripcion_partes:
                        descripcion_completa = f"{ubicacion} - {' - '.join(descripcion_partes)}"
                    else:
                        descripcion_completa = ubicacion
                    
                    # Verificar si la descripción completa es única
                    descripcion_normalizada = descripcion_completa.lower().strip()
                    if descripcion_normalizada not in descripciones_vistas:
                        descripciones_vistas.add(descripcion_normalizada)
                        
                        piquetes_hoy.append({
                            'horario': "Horario no especificado",
                            'tiene_piquete': True,
                            'ubicacion': ubicacion,
                            'descripcion': descripcion_completa[:300]  # Aumentar límite
                        })
                        print(f"🎯 Evento agrupado: {ubicacion}")
                        print(f"    Descripción: {descripcion_completa[:150]}...")
                    else:
                        print(f"🔄 Descripción duplicada ignorada: {ubicacion}")
                    
                    i = j  # Saltar las líneas ya procesadas
                else:
                    # Información general sin ubicación específica
                    if any(keyword in linea_actual.lower() for keyword in 
                           ['corte', 'obra', 'siniestro', 'operativo', 'bomberos', 'incendio']):
                        
                        # Verificar duplicados en información general
                        linea_normalizada = linea_actual.lower().strip()
                        if linea_normalizada not in descripciones_vistas:
                            descripciones_vistas.add(linea_normalizada)
                            
                            piquetes_hoy.append({
                                'horario': "Horario no especificado",
                                'tiene_piquete': True,
                                'descripcion': linea_actual[:200]
                            })
                            print(f"🎯 Información general: {linea_actual[:80]}...")
                        else:
                            print(f"🔄 Información general duplicada ignorada: {linea_actual[:50]}...")
                    
                    i += 1
        
        driver.quit()
        
        if piquetes_hoy:
            print(f"✅ Se encontraron {len(piquetes_hoy)} eventos de tránsito para {fecha_buscada}")
            for p in piquetes_hoy:
                print(f"   - {p['descripcion'][:100]}...")
        else:
            print(f"ℹ️ No se encontraron eventos de tránsito específicos para {fecha_buscada}")
            
        return piquetes_hoy
        
    except Exception as e:
        print(f"❌ Error al obtener pronóstico de piquetes: {e}")
        if driver:
            driver.quit()
        return []

def should_send_message(new_message):
    """
    Verifica si el mensaje es diferente al último enviado para evitar spam.
    """
    try:
        with open('last_message.txt', 'r', encoding='utf-8') as f:
            last_message = f.read().strip()
        
        # Comparar mensajes (ignorar diferencias menores de formato)
        return new_message.strip() != last_message
    except FileNotFoundError:
        # Primera ejecución - siempre enviar
        print("📝 Primer mensaje - no hay historial previo")
        return True

def save_last_message(message):
    """
    Guarda el mensaje para comparación futura.
    """
    try:
        with open('last_message.txt', 'w', encoding='utf-8') as f:
            f.write(message.strip())
        print("💾 Mensaje guardado para próxima comparación")
    except Exception as e:
        print(f"⚠️ Error guardando mensaje: {e}")

def enviar_alerta_piquetes(piquetes_info):
    """
    Envía alerta por Telegram sobre piquetes del día.
    """
    if not piquetes_info:
        print("ℹ️ No hay información de piquetes para enviar")
        return
    
    fecha_actual = obtener_fecha_actual()
    
    # Crear mensaje dinámico basado en la información scrapeada
    mensaje = f"🚦 ALERTA DE TRÁNSITO - {fecha_actual['formato_es'].upper()}\n\n"
    
    # Filtrar solo la información relevante del día
    piquetes_confirmados = [p for p in piquetes_info if p['tiene_piquete']]
    
    if piquetes_confirmados:
        mensaje += "⚠️ EVENTOS DE TRÁNSITO REPORTADOS:\n\n"
        for piquete in piquetes_confirmados:
            # Limpiar completamente el texto
            horario = str(piquete['horario']).strip()
            descripcion = str(piquete['descripcion']).strip()
            
            # Remover caracteres problemáticos
            descripcion_limpia = (descripcion
                                .replace('📆', '')
                                .replace('MANIFESTACIONES', '')
                                .replace('*', '')
                                .replace('_', '')
                                .replace('[', '')
                                .replace(']', '')
                                .replace('(', '')
                                .replace(')', '')
                                .strip())
            
            # Tomar solo los primeros 150 caracteres de descripción útil
            if len(descripcion_limpia) > 150:
                descripcion_limpia = descripcion_limpia[:150] + "..."
            
            mensaje += f"🕐 {horario}\n"
            mensaje += f"📍 {descripcion_limpia}\n\n"
    else:
        mensaje += "✅ Sin eventos de tránsito reportados para hoy\n"
    
    # Limitar longitud total del mensaje
    if len(mensaje) > 4000:
        mensaje = mensaje[:4000] + "...\n\nMensaje truncado"
    
    # Verificar si el mensaje es diferente al anterior
    if should_send_message(mensaje):
        print("🆕 Mensaje nuevo detectado - procediendo con envío")
        
        # Mostrar el mensaje en terminal
        print("=" * 60)
        print("📱 MENSAJE QUE SE ENVIARÍA POR TELEGRAM:")
        print("=" * 60)
        print(mensaje)
        print("=" * 60)
        print(f"📊 Longitud del mensaje: {len(mensaje)} caracteres")
        
        # Código original de Telegram (comentado temporalmente)
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        
        # Enviar mensaje sin formato especial para evitar errores
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": mensaje
        }
        
        try:
            response = requests.post(url, data=data, timeout=30)
            
            if response.status_code == 200:
                print("📤 Alerta de tránsito enviada por Telegram")
                print(f"Mensaje enviado: {mensaje[:200]}...")
                # Guardar mensaje después de enviarlo exitosamente
                save_last_message(mensaje)
            else:
                print(f"❌ Error al enviar mensaje: {response.status_code}")
                print(f"Respuesta: {response.text}")
                    
        except Exception as e:
            print(f"❌ Error enviando alerta: {e}")
        
    else:
        print("🔄 Mensaje idéntico al anterior - omitiendo envío para evitar spam")
        print("📝 Tip: Solo se enviarán mensajes cuando la información de tránsito cambie")

def verificar_piquetes():
    """
    Función principal que verifica piquetes y envía alertas.
    """
    try:
        print(f"⏱️ Iniciando verificación - {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Obtener pronóstico de piquetes
        piquetes_info = obtener_pronostico_piquetes()
        print(f"Estados obtenidos: {piquetes_info}")
        
        if piquetes_info:
            print(f"Información encontrada: {len(piquetes_info)} registros para hoy")
            enviar_alerta_piquetes(piquetes_info)
        else:
            print("✅ No se encontraron piquetes para hoy")
            
    except Exception as e:
        print(f"❌ Error en verificación: {e}")

def main():
    """
    Función principal del bot.
    """
    print("🚀 Iniciando Bot de Alertas de Piquetes")
    print(f"⏰ Configurado para ejecutarse cada {INTERVALO_EJECUCION // 60} minutos")
    print(f"🌐 Monitoreando: {URL_PIQUETES}")
    
    while True:
        verificar_piquetes()
        
        # Mostrar cuándo será la próxima ejecución
        proxima_ejecucion = time.strftime('%Y-%m-%d %H:%M:%S', 
                                          time.localtime(time.time() + INTERVALO_EJECUCION))
        print(f"💤 Esperando hasta la próxima ejecución ({proxima_ejecucion})...")
        
        # Esperar el intervalo configurado
        time.sleep(INTERVALO_EJECUCION)

if __name__ == "__main__":
    main()
