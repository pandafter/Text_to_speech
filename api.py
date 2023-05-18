from flask import Flask, request, jsonify
from gtts import gTTS
import playsound

app = Flask(__name__)

def convertir_texto_a_voz(texto, archivo_audio):
    tts = gTTS(text=texto, lang='es')
    tts.save(archivo_audio)

def reproducir_audio(archivo_audio):
    playsound.playsound(archivo_audio)

@app.route('/api/convertir-texto-a-voz', methods=['POST'])
def api_convertir_texto_a_voz():
    data = request.get_json()
    texto = data['texto']
    archivo_audio = data['archivo_audio']

    convertir_texto_a_voz(texto, archivo_audio)

    return jsonify({'status': 'success', 'mensaje': 'Audio generado correctamente.'})

@app.route('/api/reproducir-audio', methods=['POST'])
def api_reproducir_audio():
    data = request.get_json()
    archivo_audio = data['archivo_audio']

    reproducir_audio(archivo_audio)

    return jsonify({'status': 'success', 'mensaje': 'Audio reproducido correctamente.'})

if __name__ == '__main__':
    app.run()
