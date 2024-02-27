from pytube import YouTube
import os
import subprocess

# directory where the downloaded files will be saved
DOWNLOADS_DIR = "/Users/cjhosea/Downloads"

def download_video(url):
    try:
        # create a youtube object for the given url
        yt = YouTube(url)
        
        # attempt to find 1440p stream and if there isn't download lower quality
        stream = yt.streams.filter(res="1440p", progressive=True).first()
        if not stream:
            print("1440p stream not available, trying other streams.")
            stream = yt.streams.filter(progressive=True).first()
        
        # if a suitable stream is found, download the video
        if stream:
            filename = f"{yt.title}.{stream.subtype}"
            stream.download(output_path=DOWNLOADS_DIR, filename=filename)
            print(f"video downloaded successfully as {filename}")
            return filename
        else:
            print("no suitable streams available for download.")
    except Exception as e:
        print("error:", e)

def convert_to_mp3(video_filename):
    try:
        # paths for the input and output files
        mp4_filename = os.path.join(DOWNLOADS_DIR, video_filename)
        mp3_filename = os.path.splitext(video_filename)[0] + ".mp3"
        mp3_path = os.path.join(DOWNLOADS_DIR, mp3_filename)
        
        # convert audio to mp3 using ffmpeg
        cmd = f"ffmpeg -i \"{mp4_filename}\" -vn -ar 44100 -ac 2 -b:a 192k \"{mp3_path}\""
        subprocess.run(cmd, shell=True, check=True)
        
        # remove the original mp4 file if user asks for mp3
        os.remove(mp4_filename)
        
        print(f"audio converted to mp3: {mp3_path}")
    except Exception as e:
        print("error:", e)

def main():
    # prompt user to enter youtube video url and desired format
    url = input("enter youtube video url: ")
    file_format = input("enter 'mp3' or 'mp4' to choose format: ").lower()
    
    # validate input format
    if file_format not in ['mp3', 'mp4']:
        print("invalid format, please choose 'mp3' or 'mp4'.")
        return

    # perform download or conversion based on the selected format
    if file_format == 'mp4':
        video_filename = download_video(url)
        if video_filename:
            print(f"video downloaded to {os.path.join(DOWNLOADS_DIR, video_filename)}")
    else:
        video_filename = download_video(url)
        if video_filename:
            convert_to_mp3(video_filename)

if __name__ == "__main__":
    main()
