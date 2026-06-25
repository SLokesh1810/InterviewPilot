import os
from dotenv import load_env
from audio_extractor.main import get_transcript, analyze_audio

load_env()
BASE_PATH = os.getenv("BASE_PATH")

def get_word_count(category):
    return category['count']

def get_confidence_report(section, confidence_drift):
    return {
        "word_count": confidence_drift[section]["word_count"],
        "wpm": confidence_drift[section]["wpm"],
        "fillers": confidence_drift[section]["fillers"]["total_fillers"]["count"]
    }

def retrieve_transcript(audio_name):
    transcript_details = get_transcript(
        base_path=BASE_PATH,
        audio_filename=audio_name
    )
    return transcript_details


async def analyse_transcript(
    audio_name,
    audio_duration_sec,
    pause_data,
    transcript
):
    report = analyze_audio(
        transcript=transcript,
        audio_duration_sec=audio_duration_sec,
        pause_data=pause_data,
        base_path=BASE_PATH,
        audio_filename=audio_name,
        model_size="small",
        top_k=3,
        long_sentence_threshold=25,
        top_phrases=3,
        return_json=True,
        save_json=False
    )

    scores = report["score"]
    sentence_analysis = report["sentence_analysis"]
    word_categories = report["word_categories"]
    filler_analysis = report["filler_analysis"]
    confidence_drift = report["confidence_drift"]

    response_report = {
        "score": {
            "fluency": scores["fluency"],
            "confidence": scores["confidence"],
            "clarity": scores["clarity"],
            "communication": scores["overall"]
        },
        "sentence_analysis": {
            "total_sentences": sentence_analysis["total_sentences"],
            "longest_sentence_length": sentence_analysis["longest_sentence_length"],
            "longest_sentence_length_raw": sentence_analysis["raw_speech_issues"]["max_sentence_length"]
        },
        "word_categories": {
            "total_words": report["audio_info"]["total_words"],
            "self_reference": get_word_count(word_categories["Self references"]),
            "connectors": get_word_count(word_categories["Connectors (basic)"]) + get_word_count(word_categories["Connectors (advanced)"]),
            "action_verbs": get_word_count(word_categories["Action verbs"]),
            "emotion_words": get_word_count(word_categories["Emotion verbs"]),
            "planning_words": get_word_count(word_categories["Planning words"]),
            "weak_language": get_word_count(word_categories["Weak language (confidence killers)"]),
            "discourse_markers": get_word_count(word_categories["Discourse markers"]),
            "professional_language": get_word_count(word_categories["Professional language"])
        },
        "pause_analysis": report["pause_analysis"],
        "filler_analysis": {
            "filler_words": filler_analysis["filler_words"]["count"],
            "filler_phrases": filler_analysis["filler_phrases"]["count"],
            "total_fillers": filler_analysis["total_fillers"]["count"]
        },
        "confidence_drift": {
            "start": get_confidence_report("start", confidence_drift),
            "middle": get_confidence_report("middle", confidence_drift),
            "end": get_confidence_report("end", confidence_drift)
        }
    }

    return response_report