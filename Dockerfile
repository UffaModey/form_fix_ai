# Use the AWS Lambda Python 3.11 base image
FROM public.ecr.aws/lambda/python:3.11

# Set working directory
WORKDIR /var/task

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --target . -r requirements.txt

# Copy your Lambda function
COPY form_fix_ai.py .

# Copy the .env file to the container
COPY ../.env .

# Set the Lambda function handler
CMD ["form_fix_ai.clean_and_analyse_data"]
