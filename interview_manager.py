from database import save_interview, get_candidate_by_id
from llm_service import generate_technical_questions, evaluate_answer

class InterviewManager:
    def __init__(self, candidate_id, tech_stack, language="en"):
        self.candidate_id = candidate_id
        self.tech_stack = tech_stack
        self.language = language
        self.questions = []
        self.answers = {}
        self.current_question = 0
        self.score = 0

        # Get candidate information
        candidate_info = get_candidate_by_id(candidate_id)
        if candidate_info:
            self.candidate_name = candidate_info['full_name']
            self.desired_position = candidate_info['desired_position']

    def start_interview(self):
        """Generate concept-focused technical questions for each technology"""
        if not self.questions:  # Only generate questions if we haven't already
            print(f"Generating questions for tech stack: {self.tech_stack}")
            self.questions = generate_technical_questions(self.tech_stack, self.language)
            print(f"Generated {len(self.questions)} questions")

        return self.get_current_question()

    def get_current_question(self):
        """Get the current question if available"""
        if self.current_question < len(self.questions):
            return self.questions[self.current_question]
        return None

    def submit_answer(self, answer):
        """Submit and evaluate an answer"""
        current_q = self.get_current_question()
        if not current_q:
            return None

        print(f"Evaluating answer for question {self.current_question + 1}")
        evaluation = evaluate_answer(
            current_q['question'],
            answer,
            current_q.get('expected_concepts', []),
            self.language
        )

        self.answers[self.current_question] = {
            'question': current_q['question'],
            'expected_concepts': current_q.get('expected_concepts', []),
            'answer': answer,
            'score': evaluation['score'],
            'feedback': evaluation['feedback'],
            'covered_concepts': evaluation.get('covered_concepts', []),
            'missing_concepts': evaluation.get('missing_concepts', [])
        }

        # Calculate running average score
        self.score = sum(a['score'] for a in self.answers.values()) / len(self.answers)
        self.current_question += 1

        return evaluation

    def is_complete(self):
        """Check if the interview is complete"""
        return self.current_question >= len(self.questions)

    def save_results(self):
        """Save interview results and determine status"""
        status = "PASSED" if self.score >= 70 else "FAILED"

        interview_data = {
            'candidate_id': self.candidate_id,
            'questions': self.questions,
            'answers': self.answers,
            'score': self.score,
            'status': status
        }

        save_interview(interview_data)
        return status
