from youtube_transcript_api import YouTubeTranscriptApi
import argparse
import sys

def get_video_id(url):
    """Extract video ID from YouTube URL."""
    if "youtu.be" in url:
        return url.split("/")[-1]
    elif "youtube.com" in url:
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
    return url  # Assume it's already a video ID if not a URL

def get_transcript(video_id):
    """Retrieve transcript for a given video ID."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript_list
    except Exception as e:
        print(f"Error retrieving transcript: {str(e)}")
        return None

def format_transcript(transcript_list):
    """Format transcript data into readable text."""
    if not transcript_list:
        return ""
    
    formatted_transcript = []
    for entry in transcript_list:
        text = entry['text']
        timestamp = entry['start']
        minutes = int(timestamp // 60)
        seconds = int(timestamp % 60)
        formatted_transcript.append(f"[{minutes:02d}:{seconds:02d}] {text}")
    
    return "\n".join(formatted_transcript)

def save_transcript(transcript, output_file=None):
    """Save transcript to file or print to console."""
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(transcript)
            print(f"Transcript saved to {output_file}")
        except Exception as e:
            print(f"Error saving transcript: {str(e)}")
    else:
        print(transcript)

def main():
    parser = argparse.ArgumentParser(description="Download YouTube video transcripts")
    parser.add_argument("url", help="YouTube video URL or ID")
    parser.add_argument("-o", "--output", help="Output file path (optional)")
    args = parser.parse_args()

    video_id = get_video_id(args.url)
    transcript_list = get_transcript(video_id)
    
    if transcript_list:
        formatted_transcript = format_transcript(transcript_list)
        save_transcript(formatted_transcript, args.output)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
