# make a dataset class creator that takes a folder as input and creates a dataset from it
import os
import glob
import subprocess
import ast
import soundfile as sf
from pytube import YouTube

def download_youtube_audio(url, output_path):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(output_path=output_path, filename="andrej" + '.mp3')

# # Example usage
# youtube_url = "https://www.youtube.com/watch?v=kCc8FmEb1nY"
# output_folder = "./andrej"  # Replace with your desired path

# download_youtube_audio(youtube_url, output_folder)

# ## use subprocess to convert mp3 to wav
# subprocess.call(['ffmpeg', '-i', './andrej/andrej.mp3', './andrej/andrej.wav'])
# ## remove the mp3 file
# os.remove('./andrej/andrej.mp3')

# subprocess.call(['whisper', 'andrej.wav'])

class DataSetCreator:
    def __init__(self, folder, transcribe=False, create_audio_files=True, create_csv_files=True):
        self.folder = folder
        self.transcribe = transcribe
        self_transcriptions = self.transcribe_files()
        self.create_audio_files = create_audio_files
        self.create_csv_files = create_csv_files
        self.data = self.create_data_from_files()

    def transcribe_files(self):
        if self.transcribe == True:
            # transcribe files
            return True
        else:
            return False

    def create_data_from_files(self):
        # read .vtt files in folder
        return [self.data_processing(file) for file in glob.glob(f"{self.folder}/*.vtt")]    

    def data_processing(self, file_path):
        with open(file_path) as transcript:
            next(transcript)
            next(transcript)
            text = transcript.read()
            lines = text.split('\n\n')
            file_name = file_path.split(".vtt")[0]
            data, samplerate = sf.read(file_name + ".wav")
            counter = 0
            for line in lines: 
                if line != '':
                    line1, line2 = line.strip().split('\n')
                    start_time, end_time = line1.split(" --> ")
                    transcribed = line2.strip()

                    start_time_in_seconds = self.parse_time(start_time)
                    end_time_in_seconds = self.parse_time(end_time)
                    duration_in_seconds = end_time_in_seconds - start_time_in_seconds

                    # split the last part of the file name
                    sample_file_name = file_name + "_" + str(counter) + ".wav"
                    name =  sample_file_name.split("/")[len(sample_file_name.split("/"))-1]

                    # name without .wav
                    # remove the last for chars in name without .wav
                    name_without_wav = name[:-4]
  
                    if (self.create_audio_files):
                        sample_file = data[(int(start_time_in_seconds*samplerate)):(int(end_time_in_seconds*samplerate))]
                        sf.write("./data/wavs/" + name, sample_file, samplerate)

                    if (self.create_csv_files):
                        with open("data/metadata.csv", 'a') as f:
                            f.write(f"{name_without_wav}|{transcribed}|{transcribed}\n")
                    counter = counter + 1

            return True

    def parse_time(self, time_string):
        # check for hours
        split_time = time_string.split(":")
        # we have an hour
        if (len(split_time) == 3):
            hours = int(time_string.split(":")[0])
            minutes = int(time_string.split(":")[1])
            seconds = float(time_string.split(":")[2])
            total_time = (hours*60*60) + (minutes*60) + seconds
            return total_time
        else:
            minutes = int(time_string.split(":")[0])
            seconds = float(time_string.split(":")[1])
            total_time = minutes*60 + seconds
            return total_time

# take the input in the vtt format
# the output folder should be a folder with the audio file and a .vtt file with transcriptions created in whisper
dataset = DataSetCreator("/home/bmoell/tts-dataset/andrej", False, True, True)