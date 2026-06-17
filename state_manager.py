
class InterviewState:
    def __init__(self, experience, position, time_duration=30):
        self.question_no = 0
        self.questions = []
        self.answers = []
        self.status = 'not_started'
        self.experience_level = experience
        self.position = position
        self.technical_score = []
        self.communication_score = []
        self.question_switches = 0
        self.time_duration = time_duration

    states = ['not_started', 'intro', 'basic technical', 'advanced technical', 'behavioural', 'final' 'completed']

    def update_status(self):
        """
        Update the status of the interview process.
        """
        if self.is_completed():
            return None
        
        current = self.states.index(self.status)
        if current < len(self.states) - 1:
            self.status = self.states[current + 1]

        return self.status

    def update_state_manager(self, question=None, answer=None, technical_score=None, communication_score=None, q_switch=False):
        """
        Update the StateManager with new question, answer, score, or status.
        """        

        if q_switch:
            self.question_switches += 1

        if question is not None and answer is not None:
            self.questions.append(question)
            self.answers.append(answer)
            self.question_no += 1
            
        if technical_score is not None:
            self.technical_score.append(technical_score)
        if communication_score is not None:
            self.communication_score.append(communication_score)
        
        return self.current_state()

    def current_state(self):
        """
        Retrieve the current state of the interview.
        """
        return {
            "question_no": self.question_no,
            "questions": self.questions,
            "answers": self.answers,
            "status": self.status,
            "experience_level": self.experience_level,
            "position": self.position,
            "technical_score": self.technical_score,
            "communication_score": self.communication_score,
            "question_switches": self.question_switches,
            "time_duration": self.time_duration
        }

    def is_completed(self):
        """
        Check if the interview process is completed.
        """

        if self.time_duration == 0 or self.question_switches >= 10:
            self.status = 'completed'

        return self.status == 'completed'