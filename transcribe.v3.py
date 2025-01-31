import whisper
import yt_dlp
import os
import sys
import torch
import warnings

# Filter out specific warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

def download_audio(url, output_path="audio_temp.mp4"):
    """Download audio using yt-dlp."""
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_path
    except Exception as e:
        print(f"Error downloading audio: {str(e)}")
        return None

def load_model_safely(model_size="base", device=None):
    """Load Whisper model with safe settings."""
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Use safer loading options
    torch.set_grad_enabled(False)
    if device == "cpu":
        torch.set_num_threads(4)
    
    return whisper.load_model(
        model_size,
        device=device,
        download_root=os.path.expanduser("~/.cache/whisper"),
        weights_only=True  # This addresses the FutureWarning
    )

def transcribe_audio(audio_path, model_size="base"):
    """Transcribe audio using Whisper."""
    try:
        # Load model with safe settings
        model = load_model_safely(model_size)
        
        # Set appropriate options based on device
        options = {}
        if not torch.cuda.is_available():
            options["fp16"] = False  # Prevent FP16 warning on CPU
        
        # Transcribe with options
        result = model.transcribe(audio_path, **options)
        return result["text"]
    except Exception as e:
        print(f"Error transcribing audio: {str(e)}")
        return None
    finally:
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
    print("YouTube Video Transcriber")
    print("-----------------------")
    url = input("Please paste the YouTube video URL: ")
    
    model_choices = {
        '1': 'tiny',
        '2': 'base',
        '3': 'small',
        '4': 'medium',
        '5': 'large'
    }
    
    print("\nChoose model size:")
    print("1. tiny   (fastest, least accurate)")
    print("2. base   (default, balanced)")
    print("3. small  (slower, more accurate)")
    print("4. medium (even more accurate)")
    print("5. large  (most accurate, slowest)")
    
    choice = input("\nEnter choice [2]: ").strip() or '2'
    model_size = model_choices.get(choice, 'base')
    
    print(f"\nDownloading audio from YouTube...")
    audio_path = download_audio(url)
    if not audio_path:
        sys.exit(1)
    
    print(f"Transcribing with {model_size} model (this may take a while)...")
    transcript = transcribe_audio(audio_path, model_size)
    if not transcript:
        sys.exit(1)
    
    save_choice = input("\nSave transcript to file? (yes/no): ").lower()
    if save_choice.startswith('y'):
        filename = input("Enter filename [transcript.txt]: ").strip() or "transcript.txt"
        save_transcript(transcript, filename)
    else:
        print("\nTranscript:")
        print("-----------")
        print(transcript)

if __name__ == "__main__":
    main()
