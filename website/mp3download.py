from pytube import YouTube

output_path = "C:/Users/axell/OneDrive/Desktop/Projects/spotimy/website/static/audio"

def download_youtube_audio(url):
    try:
        # Create a YouTube object
        youtube = YouTube(url)

        # Get the audio stream with the highest quality (assuming MP3 format)
        audio_stream = youtube.streams.filter(only_audio=True).first()

        # Download the audio stream to the specified output path
        audio_stream.download(output_path)
        
        return audio_stream.title

    except Exception as e:
        print("An error occurred:", str(e))
