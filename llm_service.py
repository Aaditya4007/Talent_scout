import google.generativeai as genai
import json

def generate_technical_questions(tech_stack, language="en"):
    try:
        model = genai.GenerativeModel('gemini-pro')

        prompt_template = """Generate 2 technical interview questions for {technology}.
Each question must be concept-focused and:
1. Test core {technology} fundamentals at a medium to hard difficulty level
2. Require in-depth understanding of underlying concepts
3. Focus on practical implementation and best practices

Return response in this exact JSON format:
[
  {{
    "question": "Detailed technical question here that tests deep understanding",
    "expected_concepts": ["concept1", "concept2", "concept3"],
    "difficulty": "medium/hard"
  }},
  {{
    "question": "Another technical question focusing on implementation details",
    "expected_concepts": ["concept1", "concept2", "concept3"],
    "difficulty": "medium/hard"
  }}
]"""

        all_questions = []
        print(f"Starting to generate questions for tech stack: {tech_stack}")

        for tech in tech_stack:
            prompt = prompt_template.format(technology=tech)
            response = model.generate_content(prompt)

            if not response.text:
                print(f"Empty response for {tech}")
                continue

            try:
                questions = json.loads(response.text)
                if isinstance(questions, list):
                    print(f"Successfully generated {len(questions)} questions for {tech}")
                    all_questions.extend(questions)
                else:
                    print(f"Invalid response format for {tech}")
            except json.JSONDecodeError as e:
                print(f"JSON parsing error for {tech}: {str(e)}")
                continue

        if not all_questions:
            print("No questions generated, using fallback")
            return [{
                "question": f"Explain in detail the core concepts and practical applications of {tech_stack[0]}. Include specific examples and best practices.",
                "expected_concepts": ["Core principles", "Practical implementation", "Best practices"],
                "difficulty": "medium"
            }]

        return all_questions

    except Exception as e:
        print(f"Error in generate_technical_questions: {str(e)}")
        return [{
            "question": f"Please explain your experience with {tech_stack[0]}, focusing on technical challenges you've solved",
            "expected_concepts": ["Technical experience", "Problem solving", "Implementation details"],
            "difficulty": "medium"
        }]

def evaluate_answer(question, answer, expected_concepts, language="en"):
    try:
        model = genai.GenerativeModel('gemini-pro')

        evaluation_prompt = f"""Evaluate this technical interview answer:

Question: {question}
Expected concepts to cover: {', '.join(expected_concepts)}
Candidate's Answer: {answer}

Evaluate based on:
1. Concept Coverage (40%): How well were the expected concepts covered?
2. Technical Accuracy (40%): Is the explanation technically correct and detailed?
3. Communication (20%): Is the answer clear and well-structured?

Provide a detailed evaluation in this exact JSON format:
{{
    "score": <number between 0-100>,
    "feedback": "<constructive feedback with specific improvement suggestions>",
    "covered_concepts": ["list", "of", "concepts", "actually", "covered"],
    "missing_concepts": ["concepts", "that", "were", "not", "addressed"]
}}"""

        response = model.generate_content(evaluation_prompt)
        if not response.text:
            raise ValueError("Empty response from API")

        evaluation = json.loads(response.text)
        if not isinstance(evaluation, dict) or 'score' not in evaluation or 'feedback' not in evaluation:
            raise ValueError("Invalid evaluation format")

        return evaluation

    except Exception as e:
        print(f"Error in evaluate_answer: {str(e)}")
        return {
            "score": 50,
            "feedback": "We encountered a technical issue while evaluating your answer. However, we've recorded your response for review. Please continue with the remaining questions.",
            "covered_concepts": [],
            "missing_concepts": []
        }