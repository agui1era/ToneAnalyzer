import os
import openai
import sounddevice as sd
from scipy.io.wavfile import write, read
import matplotlib.pyplot as plt
import subprocess
from dotenv import load_dotenv

# ==== Config ====
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
DURATION = 5
FILENAME = "recording.wav"
SPECTROGRAM_IMAGE = "spectrogram.png"
SAMPLE_RATE = 44100

# ==== Grabar audio ====
def grabar():
    print("🎙️ Grabando...")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()
    write(FILENAME, SAMPLE_RATE, audio)
    print("✅ Grabado como recording.wav")

# ==== Generar espectrograma ====
def espectrograma():
    rate, data = read(FILENAME)
    if data.ndim > 1:
        data = data[:, 0]
    plt.figure(figsize=(10, 4))
    plt.specgram(data, Fs=rate, NFFT=1024, noverlap=512)
    plt.xlabel('Tiempo')
    plt.ylabel('Frecuencia')
    plt.title('Espectrograma')
    plt.colorbar(label='Intensidad (dB)')
    plt.tight_layout()
    plt.savefig(SPECTROGRAM_IMAGE)
    plt.close()
    print("📊 Espectrograma generado")

# ==== Transcripción ====
def transcribir():
    try:
        with open(FILENAME, "rb") as f:
            resultado = openai.audio.transcriptions.create(
                model="whisper-1", file=f, response_format="text"
            )
        texto = resultado.strip()
        print("📝 Transcripción:", texto)
        return texto
    except Exception as e:
        print("❌ Error transcripción:", e)
        return ""

# ==== Análisis emocional ====
def analizar_emocion(texto):
    try:
        respuesta = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un analista emocional. Dado un texto transcrito, entrega en español una evaluación de tono emocional o mental en máximo 3 líneas."},
                {"role": "user", "content": texto}
            ],
            max_tokens=300
        )
        analisis = respuesta.choices[0].message.content.strip()
        print("🧠 Análisis emocional:", analisis)
        return analisis
    except Exception as e:
        print("❌ Error análisis:", e)
        return "[Error al analizar emociones]"

# ==== Mostrar notificación en macOS ====
def mostrar_popup(mensaje):
    mensaje = mensaje.replace('"', "'")  # evitar errores de comillas
    subprocess.run(["osascript", "-e", f'display notification "{mensaje}" with title "🧠 Resultado emocional"'])

# ==== Pipeline ====
def main():
    grabar()
    espectrograma()
    texto = transcribir()
    if texto:
        analisis = analizar_emocion(texto)
        mostrar_popup(analisis)

if __name__ == "__main__":
    main()