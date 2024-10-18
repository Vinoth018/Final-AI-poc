# from flask import Flask, render_template, request, redirect, url_for, flash
# import whisper
# from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
# from deep_translator import GoogleTranslator
# from gtts import gTTS 
# import os
# import time

# app = Flask(__name__)
# app.secret_key = "your_secret_key"

# model = whisper.load_model("tiny")

# # Define supported languages
# language_choices = {
#     'en': 'English', 
#     'es': 'Spanish',
#     'fr': 'French',
#     'de': 'German',
#     'hi': 'Hindi',
#     'ml': 'Malayalam',
#     'kn': 'Kannada',
#     'ta': 'Tamil',
#     'te': 'Telugu',
#     'mr': 'Marathi',
#     'bn': 'Bengali',
#     'ur': 'Urdu'
# }

# def extract_audio(video_path, audio_path):
#     """Extract audio from video."""
#     video_clip = VideoFileClip(video_path)
#     video_clip.audio.write_audiofile(audio_path)

# def transcribe_and_detect_language_with_timestamps(audio_path):
#     """Transcribe audio and detect language."""
#     result = model.transcribe(audio_path, word_timestamps=True)
#     detected_language = result['language']
#     segments = result['segments']
#     return detected_language, segments

# def translate_text(text, target_lang):
#     """Translate text to the target language."""
#     translator = GoogleTranslator(source='auto', target=target_lang)
#     return translator.translate(text)

# def save_translated_audio(translated_segments, target_lang):
#     """Generate audio from translated text and save it."""
#     full_translated_text = ' '.join([segment['text'] for segment in translated_segments])
#     tts = gTTS(text=full_translated_text, lang=target_lang)
#     audio_file_path = os.path.join("static", "translated_audio.mp3")
#     tts.save(audio_file_path)
#     return audio_file_path

# def merge_audio_with_video(video_path, translated_audio_path, output_video_path):
#     """Combine translated audio with the original video."""
#     video_clip = VideoFileClip(video_path)
#     translated_audio = AudioFileClip(translated_audio_path)
#     video_with_translated_audio = video_clip.set_audio(translated_audio)
#     video_with_translated_audio.write_videofile(output_video_path, codec='libx264', audio_codec='aac')

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         video_file = request.files.get("video")
#         target_lang = request.form.get("language")
        
#         if video_file and target_lang:
#             video_path = os.path.join("static", video_file.filename)
#             video_file.save(video_path)

#             audio_path = "audio.wav"  # Temporary audio file

#             try:
#                 # Extract audio from video
#                 extract_audio(video_path, audio_path)
                
#                 # Transcribe and detect the original language
#                 detected_language, segments = transcribe_and_detect_language_with_timestamps(audio_path)

#                 # Translate text and generate translated segments
#                 translated_segments = []
#                 for segment in segments:
#                     translated_text = translate_text(segment['text'], target_lang)
#                     translated_segments.append({
#                         'start': segment['start'],
#                         'end': segment['end'],
#                         'text': translated_text
#                     })

#                 # Generate translated audio
#                 translated_audio_path = save_translated_audio(translated_segments, target_lang)

#                 # Merge translated audio with the original video
#                 output_video_path = os.path.join("static", "output_video.mp4")
#                 merge_audio_with_video(video_path, translated_audio_path, output_video_path)

#                 # Clean up temporary audio files
#                 os.remove(audio_path)

#                 return render_template(
#                     "output.html", 
#                     video_path="output_video.mp4", 
#                     captions=translated_segments, 
#                     translated_audio_path=translated_audio_path
#                 )

#             except Exception as e:
#                 flash(f"Error processing video: {e}")
#                 return redirect(url_for("index"))
#         else:
#             flash("Please upload a video and select a language.")
#             return redirect(url_for("index"))

#     return render_template("index.html", languages=language_choices)

# if __name__ == "__main__":
#     app.run(debug=True)



from flask import Flask, render_template, request, redirect, url_for, flash
import whisper
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
from deep_translator import GoogleTranslator
from gtts import gTTS 
import os
import time

app = Flask(__name__)
app.secret_key = "your_secret_key"

model = whisper.load_model("tiny")

# Define supported languages
language_choices = {
    'en': 'English', 
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'hi': 'Hindi',
    'ml': 'Malayalam',
    'kn': 'Kannada',
    'ta': 'Tamil',
    'te': 'Telugu',
    'mr': 'Marathi',
    'bn': 'Bengali',
    'ur': 'Urdu'
}

def extract_audio(video_path, audio_path):
    video_clip = VideoFileClip(video_path)
    video_clip.audio.write_audiofile(audio_path)

def transcribe_and_detect_language_with_timestamps(audio_path):
    result = model.transcribe(audio_path, word_timestamps=True)
    detected_language = result['language']
    segments = result['segments']
    return detected_language, segments

def translate_text(text, target_lang):
    translator = GoogleTranslator(source='auto', target=target_lang)
    return translator.translate(text)

def save_translated_audio(translated_segments, target_lang):
    full_translated_text = ' '.join([segment['text'] for segment in translated_segments])
    tts = gTTS(text=full_translated_text, lang=target_lang)
    audio_file_path = os.path.join("static", "translated_audio.mp3")
    tts.save(audio_file_path)
    return audio_file_path

def merge_audio_with_video(video_path, translated_audio_path, output_video_path):
    video_clip = VideoFileClip(video_path)
    translated_audio = AudioFileClip(translated_audio_path)
    video_with_translated_audio = video_clip.set_audio(translated_audio)
    video_with_translated_audio.write_videofile(output_video_path, codec='libx264', audio_codec='aac')

@app.route("/")
def mainpage():
    """Render the main page."""
    return render_template("mainpage.html")

@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_file = request.files.get("video")
        target_lang = request.form.get("language")
        
        if video_file and target_lang:
            video_path = os.path.join("static", video_file.filename)
            video_file.save(video_path)

            audio_path = "audio.wav"  # Temporary audio file

            try:
                extract_audio(video_path, audio_path)
                detected_language, segments = transcribe_and_detect_language_with_timestamps(audio_path)

                translated_segments = []
                for segment in segments:
                    translated_text = translate_text(segment['text'], target_lang)
                    translated_segments.append({
                        'start': segment['start'],
                        'end': segment['end'],
                        'text': translated_text
                    })

                translated_audio_path = save_translated_audio(translated_segments, target_lang)
                output_video_path = os.path.join("static", "output_video.mp4")
                merge_audio_with_video(video_path, translated_audio_path, output_video_path)

                os.remove(audio_path)

                return render_template(
                    "translate.html", 
                    video_path="output_video.mp4", 
                    captions=translated_segments, 
                    translated_audio_path=translated_audio_path
                )

            except Exception as e:
                flash(f"Error processing video: {e}")
                return redirect(url_for("index"))
        else:
            flash("Please upload a video and select a language.")
            return redirect(url_for("index"))

    return render_template("index.html", languages=language_choices)

if __name__ == "__main__":
    app.run(debug=True)
