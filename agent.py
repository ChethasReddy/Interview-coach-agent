import random
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from judgeval import JudgmentClient
from judgeval.data import Example
from judgeval.scorers import AnswerRelevancyScorer
from judgeval.common.tracer import Tracer
from judgeval.integrations.langgraph import JudgevalCallbackHandler



chat_model = ChatOllama(model="llama3")  


client = JudgmentClient()

tracer = Tracer(project_name="interview-coach-agent", enable_monitoring=True)
handler = JudgevalCallbackHandler(tracer)



def generate_questions(num_questions=3):
    system_message = SystemMessage(content="""
    You are an expert interview coach. Please generate a list of diverse behavioral interview questions that help evaluate a candidate’s experience, problem-solving, teamwork, and leadership skills. Only return a numbered list.
    """)

    user_message = HumanMessage(content=f"""
    Generate {num_questions} behavioral interview questions.
    """)

    response = chat_model.invoke([system_message, user_message])
    
    lines = response.content.strip().split("\n")
    questions = [line.split(".", 1)[1].strip() for line in lines if "." in line]
    return questions

def ask_question(questions):
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
    # Manual checks (acting as basic rule-based evals)
    if "STAR" not in feedback.upper():
        print("⚠️ Feedback does not mention STAR method.")
    if len(feedback.split()) < 50:
        print("⚠️ Feedback is too short.")

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


def run_agent(callbacks=None):

    questions = generate_questions(num_questions=5)
    question = ask_question(questions)
    user_response = input("\nYour Response:\n> ")

    feedback = generate_feedback_with_ollama(question, user_response)
    print("\n🗒️ AI-Generated Feedback:")
    print(feedback)

    evaluate_feedback(question, feedback)

if __name__ == "__main__":

    run_agent(callbacks=[handler])

    example = Example(
        input={"handler": handler, "query": "Describe a challenge you overcame."},
        expected_tools=[]  
    )

    client.assert_test(
        scorers=[AnswerRelevancyScorer()],
        examples=[example],
        tracer=handler,
        function=run_agent,
        eval_run_name="interview_coach_demo",
        project_name="interview-coach-agent"
    )

