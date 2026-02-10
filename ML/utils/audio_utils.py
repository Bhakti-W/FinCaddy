import librosa
import soundfile as sf

def preprocess_audio(path, target_sr=16000):
    audio, sr = librosa.load(path, sr=target_sr, mono=True)
    audio = librosa.util.normalize(audio)
    return audio, target_sr










    