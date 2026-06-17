from llm_generator import llm_generation

def generate_questions(position, role, experience_level, question_type, current_stage):
    """
    Generates a list of interview questions based on predefined topics.
    Returns:
        list: A list of interview questions.
    """
    
    agent_prompt = f"""
    You are an hiring manager for a {position} position.
    You are interviewing a candidate for the role of {role}.
    The candidate has {experience_level} experience in the field.
    """

    question_prompt = f"""
    Ask a {question_type} type question related to the given details above.
    The interview is currently at the {current_stage} stage.
    """
    
    full_prompt = agent_prompt + question_prompt
    response = llm_generation(full_prompt, temperature=0.7, max_output_tokens=200)
    
    return response

def follow_up_question(previous_question, previous_answer):
    """
    Generates a follow-up question based on the previous question and answer.
    Returns:
        str: A follow-up interview question.
    """
    
    follow_up_prompt = f"""
    Based on the previous question: "{previous_question}" and the candidate's answer: "{previous_answer}",
    generate a relevant follow-up question to further assess the candidate's knowledge and skills.
    """

    response = llm_generation(follow_up_prompt, temperature=0.7, max_output_tokens=150)
    return response

def answer_evaluation(question, answer):
    """
    Evaluates the candidate's answer to a given question.
    Returns:
        int: A feedback for the quality and relevance of the answers out of 10.
    """
    
    evaluation_prompt = f"""
    Evaluate the candidate's answer: 
    {answer}
    To the question: 
    {question}

    Give a rating for this out of 10, based on the technical accuracy, depth and relevance of the response.
    Return in JSON. Example: {{"score": 7}}
    """

    response = llm_generation(evaluation_prompt, temperature=0.5, max_output_tokens=50)
    try:
        score = int(response['score'].strip())
        return score
    except (ValueError, KeyError):
        print(f"Unexpected response for evaluation: {response}")
        return 0

def scoring_system(technical_scores, communication_scores):
    """
    Combines LLM scores and analyser scores to produce a final score.
    Returns:
        float: The final combined score.
    """

    technical_score = sum(technical_scores) / len(technical_scores) if technical_scores else 0
    communication_score = sum(communication_scores) / len(communication_scores) if communication_scores else 0

    final_score = (
        technical_score * 0.6
        +
        communication_score * 0.4
    ) * 10

    return round(final_score, 2)

def final_feedback(questions, answers, score):
    """
    Evaluates the candidate's answer to a given question.
    Returns:
        str: A feedback describing the quality of the answers and improvement suggestions, from the total score for the interview.
    """
    
    evaluation_prompt = f"""
    Evaluate the candidate's answer: 
    {answers}
    To the question: 
    {questions}
    Scored {score} out of 100 based on sentence structure, relevance, clarity, pause, and confidence.

    Give a feedback for the candidate whose answer is provided above. Give top 3 advice for the candidate to improve.
    """

    response = llm_generation(evaluation_prompt, temperature=0.5, max_output_tokens=300)
    return response