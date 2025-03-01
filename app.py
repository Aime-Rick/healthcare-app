import os
import gradio as gr
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from googletrans import Translator
from gtts import gTTS
import shutil
# Initialize the recognizer and translator
r = sr.Recognizer()
translator = Translator()

def cleanup_temp_dirs():
    for folder in ["audio_chunks", "audio_fixed_chunks"]:
        if os.path.isdir(folder):
            shutil.rmtree(folder)
            print(f"Removed temporary folder: {folder}")

# Function to recognize speech in an audio file (for one audio chunk)
def transcribe_audio(path, source_lang):
    with sr.AudioFile(path) as source:
        audio_listened = r.record(source)
        try:
            text = r.recognize_google(audio_listened, language=source_lang)
        except sr.UnknownValueError:
            text = "Could not understand the audio in this chunk."
    return text

# Function to split audio based on silence for natural segmentation
def get_large_audio_transcription_on_silence(path, source_lang):
    sound = AudioSegment.from_file(path)
    chunks = split_on_silence(
        sound,
        min_silence_len=500,
        silence_thresh=sound.dBFS - 14,
        keep_silence=500
    )
    folder_name = "audio_chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        text = transcribe_audio(chunk_filename, source_lang)
        whole_text += f"{text.capitalize()}. "
    return whole_text

# Function to split audio into fixed interval chunks (used for very large files)
def get_large_audio_transcription_fixed_interval(path, source_lang, minutes=5):
    sound = AudioSegment.from_file(path)
    chunk_length_ms = minutes * 60 * 1000
    chunks = [sound[i:i + chunk_length_ms] for i in range(0, len(sound), chunk_length_ms)]
    folder_name = "audio_fixed_chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        text = transcribe_audio(chunk_filename, source_lang)
        whole_text += f"{text.capitalize()}. "
    return whole_text

async def process_audio(audio_file, source_language, target_language):
    if audio_file is not None:
        path = audio_file
        file_size = os.path.getsize(path)
        try:
            # Choose transcription method based on file size
            if file_size < 50 * 1024 * 1024:
                transcribed_text = get_large_audio_transcription_on_silence(path, source_language)
            else:
                transcribed_text = get_large_audio_transcription_fixed_interval(path, source_language, minutes=5)

            # Translation using googletrans
            try:
                translated_obj = await translator.translate(transcribed_text, src=source_language, dest=target_language)
                translated_text = translated_obj.text
            except Exception as e:
                translated_text = f"Translation error: {str(e)}"

            # Generate audio playback from the translated text using gTTS
            try:
                tts = gTTS(translated_text, lang=target_language)
                playback_path = "translated.mp3"
                tts.save(playback_path)
            except Exception as e:
                playback_path = None
                translated_text += f"\n(TTS generation error: {str(e)})"

            return transcribed_text, translated_text, playback_path
        finally:
            # Clean up temporary files and directories
            cleanup_temp_dirs()
    return "No audio file provided", "", None



# Create Gradio interface with dual transcript display and language selection
def create_interface():
    with gr.Blocks() as demo:
        gr.Markdown("## Healthcare Translation App")
        gr.Markdown(
            "Record an audio to obtain a live transcription (original) and a translation. "
            "Select the source and target languages as needed."
        )
        with gr.Tab("Audio File Recording"):
            audio_input = gr.Audio(type="filepath", label="Record Audio File", sources=["microphone"])
            source_language = gr.Dropdown(
                choices=["en", "es", "fr", "de", "it"],
                value="en",
                label="Transcription Language"
            )
            target_language = gr.Dropdown(
                choices=["en", "es", "fr", "de", "it"],
                value="fr",
                label="Translation Language"
            )
            # Create a row for side-by-side text outputs
            with gr.Row():
                original_output = gr.Textbox(label="Original Transcription", lines=6, interactive=False)
                translated_output = gr.Textbox(label="Translated Text", lines=6, interactive=False)
            audio_playback = gr.Audio(label="Translated Audio Playback")
            # Link the input change to the processing function
            audio_input.change(
                fn=process_audio,
                inputs=[audio_input, source_language, target_language],
                outputs=[original_output, translated_output, audio_playback]
            )
    return demo

# Launch the app
demo = create_interface()
demo.launch()
