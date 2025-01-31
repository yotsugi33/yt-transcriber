import whisper
import os
import sys
import yt_dlp


def download_audio(url, output_path="audio_temp.mp4"):
    """Download audio using yt-dlp."""
    try:
        import yt_dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_path
    except Exception as e:
        print(f"Error downloading audio: {str(e)}")
        return None

def transcribe_audio(audio_path, model_size="base"):
    """Transcribe audio using Whisper."""
    try:
        model = whisper.load_model(model_size)
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        print(f"Error transcribing audio: {str(e)}")
        return None
    finally:
        # Clean up the temporary audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)

def save_transcript(transcript, filename="transcript.txt"):
    """Save transcript to a file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(transcript)
        print(f"Transcript saved to {filename}")
    except Exception as e:
        print(f"Error saving transcript: {str(e)}")

def main():
    url = input("Please paste the YouTube video URL: ")
    model_size = input("Choose model size (tiny/base/small/medium/large) [default: base]: ") or "base"

    print("Downloading audio...")
    audio_path = download_audio(url)
    if not audio_path:
        sys.exit(1)

    print(f"Transcribing with {model_size} model (this may take a while)...")
    transcript = transcribe_audio(audio_path, model_size)
    if not transcript:
        sys.exit(1)

    save_choice = input("Save transcript to file? (yes/no): ").lower()
    if save_choice.startswith('y'):
        filename = input("Enter filename [default: transcript.txt]: ") or "transcript.txt"
        save_transcript(transcript, filename)
    else:
        print("\nTranscript:")
        print(transcript)

if __name__ == "__main__":
    main()
