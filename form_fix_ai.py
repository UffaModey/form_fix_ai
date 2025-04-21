import json
import boto3
import pandas as pd
import openai
from openai import OpenAI
import io
import os

# Set up environment variables
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REGION_NAME = os.getenv("AWS_REGION", "eu-west-2")
AWS_KEY_ID = os.getenv("AWS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

openai.api_key = OPENAI_API_KEY
client = OpenAI()
s3 = boto3.client("s3",
                  aws_access_key_id=AWS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  region_name="eu-west-2")


# Function to clean availability values using OpenAI
def clean_availability_column(values):
    print("Cleaning and Analysing Availability Data")
    prompt = (
        "You are a data cleaning assistant. Given a list of user availability responses, "
        "standardize each one into one of the following categories: 'Yes', 'No', 'Maybe', or 'Unknown'.\n\n"
        f"Original values: {values}\n\n"
        "Return a JSON list of cleaned responses."
    )

    response = client.responses.create(
        model="gpt-4",
        input=[{"role": "user", "content": prompt}],
        temperature=0
    )

    try:
        cleaned = json.loads(response.output_text)
    except Exception as e:
        print("Error parsing OpenAI response:", e)
        raise

    return cleaned


# Lambda handler
def clean_and_analyse_data(event, context):
    try:
        # Extract the keyname from event payload
        s3_key = event.get("s3_key")

        if not s3_key:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing s3_key"})}

        # Download file from S3
        print(f"Accessing S3 bucket: {S3_BUCKET} ...")
        try:
            obj = s3.get_object(Bucket=S3_BUCKET, Key=s3_key)
            print("Downloaded file from S3")
        except Exception as e:
            return {"statusCode": 500, "error": str(e)}
        df = pd.read_csv(obj['Body'])

        # Clean the Availability column
        if 'Availability' not in df.columns:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing 'Availability' column in CSV"})}

        dirty_values = df['Availability'].fillna("").tolist()
        cleaned_values = clean_availability_column(dirty_values)
        print("Availability Data cleaned with AI")
        df['Availability'] = cleaned_values

        # Save cleaned file to new location in S3
        cleaned_key = s3_key.replace(".csv", "_cleaned.csv")
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        s3.put_object(Bucket=S3_BUCKET, Key=cleaned_key, Body=csv_buffer.getvalue())

        s3_url = f"https://{S3_BUCKET}.s3.{REGION_NAME}.amazonaws.com/{cleaned_key}"
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "File cleaned successfully", "cleaned_s3_url": s3_url})
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
