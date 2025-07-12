import random
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from judgeval import JudgmentClient
from judgeval.data import Example
from judgeval.scorers import AnswerRelevancyScorer


chat_model = ChatOllama(model="llama3")  


client = JudgmentClient()

# Sample behavioral interview questions
questions = [
    "Tell me about a time you worked on a team project.",
    "Describe a challenge you overcame.",
    "Give an example of when you showed leadership."
]


def ask_question():
    question = random.choice(questions)
    print(f"\n📝 Interview Question:\n➡️ {question}")
    return question

# Generate detailed feedback using Ollama's LLaMA 3
def generate_feedback_with_ollama(question, user_response):
    system_message = SystemMessage(content="""
    You are a career coaching expert. Your task is to give clear, detailed feedback on behavioral interview answers.
    Evaluate whether the answer follows the STAR (Situation, Task, Action, Result) method, uses strong action words, and is well-structured.
    Provide actionable advice on how to improve.
    """)

    user_message = HumanMessage(content=f"""
    Interview Question: {question}
    Candidate's Response: {user_response}

    Please provide detailed feedback.
    """)

    response = chat_model.invoke([system_message, user_message])
    return response.content

# Evaluate the feedback with judgeval 
def evaluate_feedback(question, feedback):
    example = Example(
        input=question,
        actual_output=feedback,
        retrieval_context=[
            "Good feedback on behavioral answers should mention structure, clarity, use of STAR method, and action words."
        ]
    )

    scorer = AnswerRelevancyScorer(threshold=0.5)

    result = client.run_evaluation(
        examples=[example],
        scorers=[scorer],
        model="gpt-4o",  # Note: The actual feedback is generated using the local llama3 model via Ollama.
                        #This model name is used purely for judgeval's metadata requirements, as judgeval does not currently accept custom/local model names.
        project_name="interview-coach-agent"
    )

    print("\n🎯 Judgeval Evaluation Result:")
    print(result)


def run_agent():
    question = ask_question()
    user_response = input("\nYour Response:\n> ")

    feedback = generate_feedback_with_ollama(question, user_response)
    print("\n🗒️ AI-Generated Feedback:")
    print(feedback)

    evaluate_feedback(question, feedback)

if __name__ == "__main__":
    run_agent()
