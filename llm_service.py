import google.generativeai as genai
import json

def generate_technical_questions(tech_stack, language="en"):
    try:
        model = genai.GenerativeModel('gemini-pro')

        prompt_template = """Generate exactly 3-5 specific technical interview questions for {technology}.
Each question MUST:
1. Focus on a distinct core concept of {technology}
2. Present a specific technical scenario or problem
3. Be at medium to hard difficulty level
4. Require detailed implementation knowledge

Example format for Python:
[
  {{
    "question": "Explain how Python's context managers work internally. Implement a custom context manager for managing database connections that includes connection pooling and automatic retry on failure.",
    "expected_concepts": ["Context manager protocol", "Enter/Exit methods", "Resource management", "Exception handling"],
    "difficulty": "hard",
    "topic_area": "Core Language Features"
  }},
  {{
    "question": "Design a thread-safe producer-consumer queue implementation in Python. Address race conditions, deadlock prevention, and proper resource cleanup.",
    "expected_concepts": ["Threading", "Synchronization primitives", "Race conditions", "Resource management"],
    "difficulty": "hard",
    "topic_area": "Concurrency"
  }},
  {{
    "question": "Implement a custom decorator that caches function results while considering memory constraints. Include cache invalidation strategy and handling of mutable arguments.",
    "expected_concepts": ["Decorators", "Memoization", "Cache strategies", "Memory management"],
    "difficulty": "medium",
    "topic_area": "Advanced Python"
  }}
]

Return 3-5 questions in the exact JSON format shown above."""

        all_questions = []
        print(f"Generating specific questions for tech stack: {tech_stack}")

        for tech in tech_stack:
            prompt = prompt_template.format(technology=tech)
            response = model.generate_content(prompt)

            if not response.text:
                print(f"Empty response for {tech}")
                continue

            try:
                questions = json.loads(response.text)
                if isinstance(questions, list) and 3 <= len(questions) <= 5:
                    print(f"Successfully generated {len(questions)} questions for {tech}")
                    all_questions.extend(questions)
                else:
                    print(f"Invalid response format or question count for {tech}")
            except json.JSONDecodeError as e:
                print(f"JSON parsing error for {tech}: {str(e)}")
                continue

        if not all_questions:
            print("No questions generated, using fallback")
            return [
                {
                    "question": f"Implement a production-ready error handling system in {tech_stack[0]}. Include logging, custom exceptions, and recovery strategies. Provide specific code examples.",
                    "expected_concepts": ["Error handling patterns", "Custom exceptions", "Logging best practices", "Recovery strategies"],
                    "difficulty": "medium",
                    "topic_area": "Error Handling"
                },
                {
                    "question": f"Design and implement a scalable caching system in {tech_stack[0]}. Consider cache invalidation, memory management, and concurrent access.",
                    "expected_concepts": ["Caching strategies", "Concurrency handling", "Memory management", "Performance optimization"],
                    "difficulty": "hard",
                    "topic_area": "System Design"
                },
                {
                    "question": f"Create a robust testing framework for a {tech_stack[0]} application. Include unit tests, integration tests, and performance tests. Discuss mocking strategies.",
                    "expected_concepts": ["Testing methodologies", "Mocking", "Test coverage", "Performance testing"],
                    "difficulty": "medium",
                    "topic_area": "Testing"
                }
            ]

        return all_questions

    except Exception as e:
        print(f"Error in generate_technical_questions: {str(e)}")
        return [
            {
                "question": f"Design and implement a robust error handling and logging system in {tech_stack[0]}. Include specific examples of handling different types of errors and implementing custom exceptions.",
                "expected_concepts": ["Error handling", "Logging", "Custom exceptions", "Best practices"],
                "difficulty": "medium",
                "topic_area": "Error Handling"
            },
            {
                "question": f"Implement a scalable caching mechanism in {tech_stack[0]}. Discuss cache invalidation strategies and handling race conditions.",
                "expected_concepts": ["Caching", "Concurrency", "Performance", "System design"],
                "difficulty": "hard",
                "topic_area": "System Design"
            },
            {
                "question": f"Create a comprehensive testing strategy for a {tech_stack[0]} application. Include different types of tests and mocking approaches.",
                "expected_concepts": ["Testing", "Mocking", "Test coverage", "Quality assurance"],
                "difficulty": "medium",
                "topic_area": "Testing"
            }
        ]

def evaluate_answer(question, answer, expected_concepts, language="en"):
    try:
        model = genai.GenerativeModel('gemini-pro')

        evaluation_prompt = f"""Evaluate this technical interview answer comprehensively:

Question: {question}
Expected concepts to cover: {', '.join(expected_concepts)}
Candidate's Answer: {answer}

Evaluate based on:
1. Concept Coverage (40%): How well were the expected concepts covered? Identify specific concepts discussed and missed.
2. Technical Accuracy (40%): Is the explanation technically correct and detailed? Evaluate depth of understanding.
3. Communication (20%): Is the answer clear, well-structured, and professionally presented?

Provide a detailed evaluation in this exact JSON format:
{{
    "score": <number between 0-100>,
    "feedback": "<detailed constructive feedback with specific improvement suggestions>",
    "covered_concepts": ["list", "of", "concepts", "well", "explained"],
    "missing_concepts": ["concepts", "that", "need", "more", "detail"],
    "strengths": ["key", "strong", "points"],
    "areas_for_improvement": ["specific", "improvement", "areas"]
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
            "feedback": "We encountered a technical issue while evaluating your answer. Please continue with the remaining questions.",
            "covered_concepts": [],
            "missing_concepts": [],
            "strengths": [],
            "areas_for_improvement": []
        }
