import os
import time
import openai
import sounddevice as sd
from scipy.io.wavfile import write
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from scipy.io import wavfile

# Cargar .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuración desde .env
DURATION = int(os.getenv("AUDIO_DURATION", "10"))
FILENAME = os.getenv("AUDIO_FILENAME", "recording.wav")
SPECTROGRAM_IMAGE = os.getenv("SPECTROGRAM_IMAGE", "spectrogram.png")
SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", "44100"))

def record_audio():
    print("🎙️ Recording...")
    recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()
    write(FILENAME, SAMPLE_RATE, recording)
    print("✅ Recording saved.")

def generate_spectrogram():
    rate, data = wavfile.read(FILENAME)
    if data.ndim > 1:
        data = data[:, 0]
    plt.figure(figsize=(10, 4))
    plt.specgram(data, Fs=rate, NFFT=1024, noverlap=512)
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.title('Spectrogram')
    plt.colorbar(label='Intensity (dB)')
    plt.tight_layout()
    plt.savefig(SPECTROGRAM_IMAGE)
    plt.close()
    print("📊 Spectrogram saved.")

def transcribe_audio():
    try:
        with open(FILENAME, "rb") as f:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="text"
            )
        return transcript.strip()
    except Exception as e:
        return f"[❌ Transcription error: {e}]"

def analyze_emotion(text):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an emotional analysis assistant. Given a transcript, analyze the emotional tone, "
                        "possible mental state, or any unusual vocal patterns. Summarize findings in 3 lines max."
                    )
                },
                {"role": "user", "content": text}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[❌ GPT analysis error: {e}]"

def main():
    record_audio()
    generate_spectrogram()
    transcript = transcribe_audio()
    print(f"\n📝 Transcript:\n{transcript}\n")
    analysis = analyze_emotion(transcript)
    print(f"🧠 Emotion Analysis:\n{analysis}\n")

if __name__ == "__main__":
    main()
