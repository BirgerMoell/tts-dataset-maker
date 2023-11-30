# tts-dataset-maker
<img src="tts_data.png">

### Install
```
pip install -r requirements.txt
````

```
python create_dataset.py
```

## About
TTS dataset is a dataset that automatically creates data in the format needed for working with tts systems such as VITS.

By running the script ona folder with a wav file and a .vtt file created by whisper you will automatically create a data folder with metadata.csv and wavs split up that you can use for training your own TTS system.

Uncomment the code to download a youtube video and store it in a folder to be used as training data.

