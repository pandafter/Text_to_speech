import os
import time
import threading
from flask import Flask, request, jsonify, send_from_directory
from gtts import gTTS
import playsound

app = Flask(__name__)

def convertir_texto_a_voz(texto, archivo_audio):
    carpeta_audios = 'audios_temporales'
    ruta_archivo = os.path.join(carpeta_audios, archivo_audio)

    tts = gTTS(text=texto, lang='es')
    tts.save(ruta_archivo)

def reproducir_audio(archivo_audio):
    playsound.playsound(archivo_audio)

def eliminar_archivo(archivo):
    time.sleep(10)  # Esperar 10 segundos antes de eliminar el archivo
    os.remove(archivo)

@app.route('/api/convertir-texto-a-voz', methods=['POST'])
def api_convertir_texto_a_voz():
    data = request.get_json()
    texto = data['texto']
    archivo_audio = data['archivo_audio']

    convertir_texto_a_voz(texto, archivo_audio)

    # Iniciar el proceso de eliminación del archivo en segundo plano
    app.logger.info(f'Eliminando archivo {archivo_audio} en segundo plano')
    app.logger.info('Esperando 10 segundos antes de eliminar')
    app.logger.info('Puedes modificar el tiempo de espera según tus necesidades')
    app.logger.info('Para evitar que el disco se llene de archivos temporales, asegúrate de que se eliminen correctamente')

    ruta_archivo = os.path.join('audios_temporales', archivo_audio)
    eliminar_archivo_thread = threading.Thread(target=eliminar_archivo, args=(ruta_archivo,))
    eliminar_archivo_thread.start()

    return jsonify({'status': 'success', 'mensaje': 'Audio generado correctamente.'})

@app.route('/api/reproducir-audio', methods=['POST'])
def api_reproducir_audio():
    data = request.get_json()
    archivo_audio = data['archivo_audio']

    ruta_archivo = os.path.join('audios_temporales', archivo_audio)
    reproducir_audio(ruta_archivo)

    return jsonify({'status': 'success', 'mensaje': 'Audio reproducido correctamente.'})

@app.route('/audios_temporales/<path:nombre_archivo>')
def servir_audio_temporal(nombre_archivo):
    carpeta_audios = 'audios_temporales'
    return send_from_directory(carpeta_audios, nombre_archivo)

if __name__ == '__main__':
    if not os.path.exists('audios_temporales'):
        os.makedirs('audios_temporales')

    app.run()
