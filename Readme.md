# Mini Interview Coach Agent

An AI-powered Interview Coach that asks behavioral interview questions, analyzes your answers using a Large Language Model (LLM) powered by **Ollama (LLaMA 3)** running locally, and optionally evaluates feedback quality using **Judgment Labs' judgeval SDK**.

---

## 🚀 Features

- Asks randomly selected behavioral interview questions.
- Uses an **LLM (LLaMA 3 via Ollama)** to generate detailed feedback based on the STAR method.
- (Optional) Uses **judgeval** to evaluate the quality of the feedback.

---

## 📝 Prerequisites

### 1. Install Python and Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Required Python Packages

```bash
pip install -r requirements.txt
```

Content of `requirements.txt`:

```txt
langchain
langchain-community
judgeval
python-dotenv
```

### 3. Install Ollama Locally (Mac/Linux)

```bash
brew install ollama
```

- For Windows or other platforms: Visit https://ollama.com/download

### 4. Run the Ollama Server

```bash
ollama serve
```

👉 This must be running in the background for the agent to work.

### 5. Download and Run LLaMA 3 Model (Optional Manual Step)

```bash
ollama run llama3
```

_This will ensure the model is downloaded to your machine._

### 6. Set Up judgeval Environment Variables (Optional)

If you wish to enable judgeval evaluation:

1. Create a `.env` file in the project root:

```
JUDGMENT_API_KEY=your_judgment_api_key_here
JUDGMENT_ORG_ID=your_organization_id_here
```

2. judgeval is optional and only required for evaluation.

---

## 🏃 Running the Agent

### 1. Activate Virtual Environment (if not already active)

```bash
source venv/bin/activate
```

### 2. Ensure Ollama Server is Running

```bash
ollama serve
```

### 3. Run the Agent

```bash
python agent.py
```

### 4. What Happens:

- The agent asks a behavioral interview question.
- You type your answer.
- The **LLaMA 3 model** generates actionable feedback based on STAR.
- (Optional) The feedback is evaluated using **judgeval**.

---

## 🛠 Troubleshooting

| Issue                                      | Solution                                                                                                        |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| `ollama server not responding`             | Run `ollama serve` in a separate terminal.                                                                      |
| judgeval `Project limit exceeded`          | This is a quota limit on Judgment Labs—evaluation can be commented out in code without breaking the main agent. |
| `ModuleNotFoundError: langchain_community` | Run `pip install langchain-community`.                                                                          |

---

## 📄 Notes

- The **LLM feedback** works entirely offline with **Ollama**.
- **Judgeval** integration is optional but demonstrates real-world evaluation pipelines.
- Costs: Using **Ollama** is free. Using **OpenAI API** (if chosen) may incur costs.

---

## ✅ Example Interaction

```
📝 Interview Question:
➡️ Describe a challenge you overcame.

Your Response:
> I had to lead a team during a tight deadline project...

🗒️ AI-Generated Feedback:
[Detailed STAR-based feedback provided by the agent.]

🎯 Judgeval Evaluation Result:
[Optional evaluation result or skipped if quota exceeded.]
```

---

## 📬 Submission Note

If you encounter **judgeval quota limits**:

> "The Judgeval evaluation step is integrated but disabled due to project quota limits. The core agent functionality and AI feedback work as expected."

---

## 🤝 Acknowledgments

- [Ollama](https://ollama.com)
- [LangChain](https://python.langchain.com)
- [Judgment Labs](https://github.com/JudgmentLabs)

---

✅ You're now ready to coach yourself on interviews with AI! 🎯
