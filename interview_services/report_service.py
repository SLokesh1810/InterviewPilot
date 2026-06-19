
def score_calculator(
    communication_score,
    technical_score
):
    return (communication_score * 40) + (technical_score * 60)
    
def update_confidence(
    current_confidence,
    new_confidence
):
    
    return {
        "word_count": current_confidence["word_count"] + new_confidence["word_count"],
        "wpm": current_confidence["wpm"] + new_confidence["wpm"],
        "fillers": current_confidence["fillers"] + new_confidence["fillers"]
    }

def update_report(
    current_report,
    analyser_report,
    technical_evaluation
):
    ovr_score = score_calculator(
        analyser_report["score"]["communication"],
        technical_evaluation["score"]
    )

    if current_report is None:
        current_report = analyser_report

        current_report["questions_processed"] = 1

        current_report["score"]["overall"] = ovr_score
        current_report["missing_concepts"] = technical_evaluation["missing_concepts"]

    current_report["questions_processed"] += 1

    # Scores update
    new_scores = analyser_report["score"]

    current_report["score"]["fluency"] += new_scores["fluency"]
    current_report["score"]["confidence"] += new_scores["confidence"]
    current_report["score"]["clarity"] += new_scores["clarity"]
    current_report["score"]["communication"] += new_scores["communication"]
    current_report["score"]["relevance_score"] += technical_evaluation["score"]
    current_report["score"]["overall"] += ovr_score

    # Sentence report update
    sentence_analysis = analyser_report["sentence_analysis"]
    
    current_report["sentence_analysis"]["total_sentences"] += sentence_analysis["total_sentences"]
    current_report["sentence_analysis"]["longest_sentence_length"] = max(
        current_report["sentence_analysis"]["longest_sentence_length"],
        sentence_analysis["longest_sentence_length"]
    )
    current_report["sentence_analysis"]["longest_sentence_length_raw"] = max(
        current_report["sentence_analysis"]["longest_sentence_length_raw"],
        sentence_analysis["longest_sentence_length_raw"]
    )
    
    # Word categories update
    word_category = analyser_report["word_categories"]

    current_report["word_categories"]["total_words"] += word_category["total_words"]
    current_report["word_categories"]["self_reference"] += word_category["self_reference"]
    current_report["word_categories"]["connectors"] += word_category["connectors"]
    current_report["word_categories"]["action_verbs"] += word_category["action_verbs"]
    current_report["word_categories"]["emotion_words"] += word_category["emotion_words"]
    current_report["word_categories"]["planning_words"] += word_category["planning_words"]
    current_report["word_categories"]["weak_language"] += word_category["weak_language"]
    current_report["word_categories"]["discourse_markers"] += word_category["discourse_markers"]
    current_report["word_categories"]["professional_language"] += word_category["professional_language"]

    # Pause analysis update
    pause_analysis = analyser_report["pause_analysis"]

    current_report["pause_analysis"]["total_pauses"] += pause_analysis["total_pauses"]
    current_report["pause_analysis"]["long_pauses"] += pause_analysis["long_pauses"]
    current_report["pause_analysis"]["avg_pauses"] += pause_analysis["avg_pauses"]

    # Filler analysis update
    filler_analysis = analyser_report["filler_analysis"]

    current_report["filler_analysis"]["filler_words"] += filler_analysis["filler_words"]
    current_report["filler_analysis"]["filler_phases"] += filler_analysis["filler_phases"]
    current_report["filler_analysis"]["total_filler"] += filler_analysis["total_fillers"]

    # Confidence analysis update
    confidence_analysis = analyser_report["confidence_analysis"]

    current_report["confidence_drift"]["start"] = update_confidence(
        current_report["confidence_drift"]["start"],
        confidence_analysis["start"]
    )
    current_report["confidence_drift"]["middle"] = update_confidence(
        current_report["confidence_drift"]["middle"],
        confidence_analysis["middle"]
    )
    current_report["confidence_drift"]["end"] = update_confidence(
        current_report["confidence_drift"]["end"],
        confidence_analysis["end"]
    )

    # Updating missing or lacking concepts

    current_report["missing_concepts"] += technical_evaluation["missing_concepts"]

    return current_report

def get_average_score(
    total_score,
    count
):
    return round(
        total_score / count, 2
    )

def final_score_update(
    report,
    question_count
):
    question_count = report["questions_processed"]

    if question_count == 0:
        return report

    # Finalizing scores
    scores = report["score"]

    report["score"]["fluency"] = final_score_update(scores["fluency"], question_count)
    report["score"]["confidence"] = final_score_update(scores["confidence"], question_count)
    report["score"]["clarity"] = final_score_update(scores["clarity"], question_count)
    report["score"]["communication"] = final_score_update(scores["communication"],question_count)
    report["score"]["technical"] = final_score_update(scores["technical"], question_count)
    report["score"]["overall"] = round(scores["overall"], question_count)

    # Creating percentages for word category
    word_category = report["word_categories"]

    report["word_categories"]["self_reference_percent"] = get_average_score(
        word_category["self_reference"],
        question_count
    )
    report["word_categories"]["connectors"] = get_average_score(
        word_category["connectors"],
        question_count
    )
    report["word_categories"]["action_verbs"] = get_average_score(
        word_category["action_verbs"],
        question_count
    )
    report["word_categories"]["emotion_words"] = get_average_score(
        word_category["emotion_words"],
        question_count
    )
    report["word_categories"]["planning_words"] = get_average_score(
        word_category["planning_words"],
        question_count
    )
    report["word_categories"]["weak_language"] = get_average_score(
        word_category["weak_language"],
        question_count
    )
    report["word_categories"]["discourse_markers"] = get_average_score(
        word_category["discourse_markers"],
        question_count
    )
    report["word_categories"]["professional_language"] = get_average_score(
        word_category["professional_language"],
        question_count
    )

    # Finalizing pause analysis

    report["pause_analysis"]["avg_pauses"] = get_average_score(
        report["pause_analysis"]["avg_pause"],
        question_count
    )

    # Finalizing filler analysis

    report["filler_analysis"]["avg_filler"] = get_average_score(
        report["filler_analysis"]["avg_filler"],
        question_count
    )

    # Finalizing wpm in confidence_analysis

    report["confidence_drift"]["start"] = get_average_score(
        report["confidence_drift"]["start"],
        question_count
    )
    report["confidence_drift"]["middle"] = get_average_score(
        report["confidence_drift"]["middle"],
        question_count
    )
    report["confidence_drift"]["end"] = get_average_score(
        report["confidence_drift"]["end"],
        question_count
    )

    # Removing duplicate missing_concepts

    report["missing_concepts"] = set(report["missing_concepts"])

    return report