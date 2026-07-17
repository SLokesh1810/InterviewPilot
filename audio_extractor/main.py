import os
import librosa
import gc

from . import convertor
from .config import (
    DEFAULT_MODEL_SIZE,
    DEFAULT_TOP_K,
    DEFAULT_LONG_SENTENCE_THRESHOLD,
    DEFAULT_TOP_PHRASES
)

from audio_analyser.pause_analysis import analyze_pauses
from audio_analyser.pipeline import analyze_transcript
from audio_analyser.transcription import (
    transcribe_audio
)

def get_transcript(
    base_path,
    audio_filename,
    model_size=DEFAULT_MODEL_SIZE
):
    """
    Load audio and return transcript-related data.
    """

    audio_path = os.path.join(base_path, audio_filename)

    # Ensure audio exists
    print("Audio not found, converting from video...")
    audio_path = convertor.convert(audio_path)

    # Load audio
    audio_array, sr = librosa.load(audio_path, sr=16000)
    audio_duration_sec = librosa.get_duration(y=audio_array, sr=sr)

    pause_data = analyze_pauses(audio_path)


    transcript = transcribe_audio(audio_array, model_size)

    del audio_array
    gc.collect()

    return {
        "audio_path": audio_path,
        "transcript": transcript,
        "audio_duration_sec": audio_duration_sec,
        "pause_data": pause_data
    }

def analyze_audio(
        transcript,
        audio_duration_sec,
        pause_data,
        top_k=DEFAULT_TOP_K,
        long_sentence_threshold=DEFAULT_LONG_SENTENCE_THRESHOLD,
        top_phrases=DEFAULT_TOP_PHRASES
    ):

    analysis_results = analyze_transcript(
        transcript,
        audio_duration_sec,
        top_k,
        long_sentence_threshold,
        top_phrases,
        pause_data
    )

    return analysis_results

def main(
    base_path,
    audio_filename,
    model_size=DEFAULT_MODEL_SIZE,
    top_k=DEFAULT_TOP_K,
    long_sentence_threshold=DEFAULT_LONG_SENTENCE_THRESHOLD,
    top_phrases=DEFAULT_TOP_PHRASES
):

    transcript_data = get_transcript(
        base_path,
        audio_filename,
        model_size
    )

    analysis_results = analyze_audio(
        transcript=transcript_data["transcript"],
        audio_duration_sec=transcript_data["audio_duration_sec"],
        pause_data=transcript_data["pause_data"],
        base_path=base_path,
        audio_filename=audio_filename,
        top_k=top_k,
        long_sentence_threshold=long_sentence_threshold,
        top_phrases=top_phrases
    )

    return analysis_results, transcript_data["transcript"]