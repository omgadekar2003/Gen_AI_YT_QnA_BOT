# from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

# def get_transcript(video_id):
#     try:
#         transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
#         transcript = " ".join(chunk["text"] for chunk in transcript_list)
#         print("[Transcript loaded successfully]")
#         return transcript
#     except TranscriptsDisabled:
#         print("[Transcripts are disabled for this video.]")
#         return ""
#     except Exception as e:
#         print(f"[Error loading transcript: {e}]")
#         return ""

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import time

def get_transcript(video_id, max_retries=3, delay=2):
    for attempt in range(1, max_retries + 1):
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
            transcript = " ".join(chunk["text"] for chunk in transcript_list)
            print("[Transcript loaded successfully]")
            return transcript
        except TranscriptsDisabled:
            print(f"[Transcripts are disabled for video ID: {video_id}]")
            return ""
        except NoTranscriptFound:
            print(f"[No English transcript found for video ID: {video_id}]")
            return ""
        except Exception as e:
            print(f"[Attempt {attempt}/{max_retries}] Error loading transcript for video ID {video_id}: {e}")
            if attempt == max_retries:
                print(f"[Failed to load transcript after {max_retries} attempts]")
                return ""
            time.sleep(delay)  # Wait before retrying
    return ""







