# 🧠 FormFix AI — Clean & Analyze Messy Form Data with Python, OpenAI & AWS

FormFix AI is a serverless data cleaning and sentiment analysis tool that uses Python, OpenAI, and AWS to transform inconsistent form responses into structured, readable formats.

---

## 🚀 Features
- ✅ Standardizes inconsistent fields (e.g. "maybeee", "IDK", "nah fam") into `Yes`, `No`, `Maybe`, or `Unknown`
- 🧠 Uses OpenAI for intelligent classification and analysis
- ☁️ Serverless deployment with AWS Lambda and Docker
- 📂 Fetches and stores data via AWS S3
- 🔁 One-command execution from terminal

---

## ⚙️ How It Works
1. Upload your CSV to an S3 bucket
2. Trigger the Lambda function from your terminal using a bash script
3. The function:
    - Retrieves the file from S3
    - Extracts the necessary column using `pandas`
    - Sends it to OpenAI for context-aware analysis
    - Writes the cleaned output back to S3 as a new CSV

---

## 🧰 Tech Stack
- Python 3.11
- OpenAI API (gpt-3.5-turbo)
- AWS Lambda (Dockerized)
- AWS S3
- Libraries: `boto3`, `pandas`, `openai`, `python-dotenv`

---

## 📁 Project Structure
```
formfix-ai/
├── .gitignore
│── dirty_data_sample.csv        # Lambda function handler
│── form_fix_ai.py          # Utility functions for S3 and OpenAI
├── Dockerfile            # AWS Lambda base image
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (local only)
├── local_lambda_deploy.sh                # Bash script to build & deploy
├── README.md             # Project documentation
```

---

## 🔧 Setup Instructions
### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/formfix-ai.git
cd formfix-ai
```

### 2. Set Up Environment Variables
Create a `.env` file and add:
```
OPENAI_API_KEY=your_openai_api_key
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
S3_BUCKET_NAME=your_bucket_name
S3_INPUT_FILE=input.csv
S3_OUTPUT_FILE=cleaned.csv
TARGET_COLUMN_NAME=your_column_to_clean
```

### 3. Build and Deploy Lambda
```bash
bash local_lambda_deploy.sh
```

---

## 📈 Example Use Case
You’ve collected survey responses with inconsistent answers in a column like `"Availability"` — responses like:
```
"yes", "yeah", "nah", "no", "idk", "maybeee"
```
FormFix AI will convert those into clean values:
```
"Yes", "No", "Maybe", "Unknown"
```

---

## 🙌 Contribute or Remix
Feel free to fork this repo, modify the prompts, and adapt the pipeline for your own use cases. Want to add a GUI or streamlit frontend? Go for it.

If you share your remix or build publicly, tag with `#AIWithFafa` so we can connect and amplify! 🚀

---

## 🔗 License
GNU GPL License

---

## 🔍 Author
**Fafa Modey** — Python Engineer, AI Builder, and Digital Rights Advocate

Follow my journey on Instagram: [@fafacodes](https://instagram.com/fafacodes)

Project page: [Link in bio]

