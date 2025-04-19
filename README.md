# 🧠 Emotion Audio Analyzer

**Emotion Audio Analyzer** is a lightweight Python tool that records a short audio clip, transcribes the speech using OpenAI Whisper, and analyzes the emotional tone and possible unusual vocal patterns with `GPT-4o`.

This tool is ideal for:
- Monitoring emotional changes
- Detecting stress, sadness, anger, or euphoria
- Identifying irregular patterns in tone, rhythm, or speech cadence

> 🎯 Built for developers, researchers, and mental health tech experiments.

---

## 📸 What it does

1. 🎙️ Records a voice clip (default 10 seconds)  
2. 🔊 Generates a **spectrogram** (visual sound analysis)  
3. 📝 Transcribes voice to text via `Whisper`  
4. 🧠 Performs emotional analysis using `GPT-4o`  
5. 🖥️ Prints results to console  

---

## 🚀 How to Run

### 1. Clone this repo

```bash
git clone https://github.com/agui1era/emotionAudioAnalyzer.git
cd emotionAudioAnalyzer
```

### 2. Create and activate virtual environment

```bash
python3 -m venv env
source env/bin/activate   # On macOS/Linux
env\Scripts\activate.bat  # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your `.env` file

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
AUDIO_DURATION=10
AUDIO_FILENAME=recording.wav
SPECTROGRAM_IMAGE=spectrogram.png
SAMPLE_RATE=44100
```

### 5. Run the analyzer

```bash
python emotionAudioAnalyzer.py
```

---

## 📦 Requirements

- Python 3.8+
- `openai`
- `sounddevice`
- `scipy`
- `matplotlib`
- `Pillow`
- `python-dotenv`

Install with:

```bash
pip install openai sounddevice scipy matplotlib Pillow python-dotenv
```

---

## 📊 Example Output

```
🎙️ Recording...
✅ Recording saved.
📊 Spectrogram saved.

📝 Transcript:
"I don't know what else to say. I'm just tired of everything."

🧠 Emotion Analysis:
The speaker expresses emotional fatigue, possibly depression or stress.
The tone suggests a lack of motivation and emotional exhaustion.
Could be a signal of burnout or personal overload.
```

---

## 🔒 Notes

- All processing is local except transcription and emotion detection via OpenAI API.
- You can extend this to send alerts (e.g., Telegram) or trigger events.

---

## 🧠 Future Ideas

- Real-time emotion detection
- Detecting vocal anomalies (anger, panic, etc.)
- Integration with wearable health monitors
- Smart home integration for mental wellness