# Healthcare Translation App

An AI-powered application that transcribes audio recordings, translates the transcriptions into a target language, and generates synthesized speech for the translated text. This tool is especially useful in multilingual healthcare settings where clear communication is critical.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Cleanup and Security](#cleanup-and-security)
- [Approach and AI Integration](#approach-and-ai-integration)
- [License](#license)

---

## Features

- **Audio Transcription:**  
  Utilizes Google's Speech Recognition API to convert spoken audio into text.
  
- **Natural Audio Segmentation:**  
  Uses silence detection to split audio into manageable chunks for improved transcription accuracy.
  
- **Translation:**  
  Translates the transcribed text from a source language to a target language using the Google Translate API via `googletrans`.
  
- **Text-to-Speech (TTS):**  
  Converts the translated text into natural-sounding speech using Google Text-to-Speech (gTTS).
  
- **User-Friendly Interface:**  
  Built with Gradio, the interface allows users to upload audio files, choose languages, and view both original and translated outputs side-by-side, along with audio playback.

---

## Project Structure

```
├── README.md
├── app.py               # Main application code
├── audio_chunks/        # Temporary directory for silence-based audio chunks
├── audio_fixed_chunks/  # Temporary directory for fixed-interval audio chunks
└── requirements.txt     # List of dependencies
```

- **app.py:**  
  Contains the code for audio processing, transcription, translation, text-to-speech conversion, and the Gradio interface.

- **Temporary Directories:**  
  `audio_chunks` and `audio_fixed_chunks` are used for storing temporary audio segments during processing. These directories are cleaned up after each process run.

---

## Requirements

- Python 3.7+
- [Gradio](https://gradio.app)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [pydub](https://github.com/jiaaro/pydub)
- [googletrans](https://pypi.org/project/googletrans/)
- [gTTS](https://pypi.org/project/gTTS/)

> **Note:**  
> Ensure `ffmpeg` is installed on your system, as it is required by `pydub` for audio file handling.

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/healthcare-translation-app.git
   cd healthcare-translation-app
   ```

2. **Create a Virtual Environment (Optional but Recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the Required Packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install `ffmpeg`:**

   - **macOS:**  
     ```bash
     brew install ffmpeg
     ```
   - **Ubuntu/Debian:**  
     ```bash
     sudo apt-get install ffmpeg
     ```
   - **Windows:**  
     Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to your PATH.

---

## Usage

1. **Run the Application:**

   Execute the main script:

   ```bash
   python app.py
   ```

2. **Interact with the Interface:**

   - **Audio Upload:**  
     Use the audio file upload widget to either record via your microphone or upload an existing audio file.
     
   - **Language Selection:**  
     Choose the transcription language (source) and the translation language (target) from the provided dropdowns.
     
   - **Processing:**  
     Once an audio file is uploaded and the languages are selected, the app automatically:
     - Splits the audio into smaller chunks.
     - Transcribes the speech.
     - Translates the text.
     - Converts the translated text into speech.
     
   - **View & Listen:**  
     The interface displays the original transcription and the translated text side-by-side. You can also listen to the translated audio using the playback widget.

---

## Cleanup and Security

- **Temporary Files:**  
  After processing, the application cleans up temporary directories (`audio_chunks` and `audio_fixed_chunks`) to prevent disk space misuse and data retention.  
  You can find the cleanup routine in the `cleanup_temp_dirs()` function within the code.

- **Security Considerations:**  
  - The app uses HTTPS for external API calls to ensure secure communication.
  - Temporary files are removed immediately after processing.
  - Always validate uploaded files to prevent potential security risks.

---

## Approach and AI Integration

This project integrates several AI components:
- **Speech Recognition:** Converts audio into text using advanced machine learning models.
- **Machine Translation:** Uses generative AI models for context-aware translations.
- **Text-to-Speech (TTS):** Synthesizes natural-sounding speech from the translated text.
- **Gradio Interface:** Provides an accessible and interactive web interface for seamless user interaction.

Each of these components works together to provide an efficient solution for multilingual communication in healthcare environments.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to contribute or raise issues if you find any bugs or have suggestions for improvements!
