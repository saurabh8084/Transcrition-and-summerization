from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
import wave
from google.cloud import storage
import os


def mp3_to_wav(audio_file_name):
    if audio_file_name.split('.')[1] == 'mp3':
        sound = AudioSegment.from_mp3(audio_file_name)
        audio_file_name = audio_file_name.split('.')[0] + '.wav'
        sound.export(audio_file_name, format="wav")


def frame_rate_channel(audio_file_name):
    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        return frame_rate, channels


def stereo_to_mono(audio_file_name):
    sound = AudioSegment.from_wav(audio_file_name)
    sound = sound.set_channels(1)
    sound.export(audio_file_name, format="wav")


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)


def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()


def google_transcribe(audio_file_name,language_opt):
    file_name = filepath + audio_file_name
    mp3_to_wav(file_name)

    # The name of the audio file to transcribe

    frame_rate, channels = frame_rate_channel(file_name)

    if channels > 1:
        stereo_to_mono(file_name)

    bucket_name = 'transcribe_project_bucket'
    source_file_name = filepath + audio_file_name
    destination_blob_name = audio_file_name

    upload_blob(bucket_name, source_file_name, destination_blob_name)

    gcs_uri = 'gs://transcribe_project_bucket/' + audio_file_name
    transcript = ''

    client = speech.SpeechClient()
    audio = types.RecognitionAudio(uri=gcs_uri)
    config = speech.types.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=frame_rate,
        language_code=language_opt,
        enable_speaker_diarization=True,
        enable_automatic_punctuation=True
    )

    # Detects speech in the audio file
    # operation = client.long_running_recognize(config, audio)
    operation = client.long_running_recognize(
        request={"config": config, "audio": audio}
    )
    response = operation.result(timeout=10000)
    result = response.results[-1]
    words_info = result.alternatives[0].words

    tag = 0
    speaker = ""

    for word_info in words_info:
        if word_info.speaker_tag == tag:
            speaker = speaker + " " + word_info.word
        else:
            transcript += "speaker {}: {}".format(tag, speaker) + '\n'
            tag = word_info.speaker_tag
            speaker = "" + word_info.word

    transcript += "speaker {}: {}".format(tag, speaker)

    delete_blob(bucket_name, destination_blob_name)
    return transcript


def write_transcripts(transcript_filename, transcript):
    f = open(output_filepath + transcript_filename, "w+")
    f.write(transcript)
    f.close()


filepath = "./Audio-File/"
output_filepath = "./Transcripts/"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/hp/PycharmProjects/FinalYearProject/APIs/G_final-project-344512-3507c7d2a7e7.json"


def start_TranscriptPart(language_opt):
    filename = os.listdir(filepath)
    audio_filename = filename[0]
    transcript = google_transcribe(audio_filename,language_opt)
    transcript_filename = audio_filename.split('.')[0] + '.txt'
    write_transcripts(transcript_filename, transcript)
    print('Transcript Generated')
