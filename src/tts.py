from gtts import gTTS

def text_to_speech(text, output_path="summary_audio.mp3"):
    tts = gTTS(text=text, lang="en")
    tts.save(output_path)
    return output_path