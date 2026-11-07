import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os

load_dotenv()

def get_bedrock_client(region_name):
    """
    Initializes the Amazon Bedrock Runtime Client.
    Make sure your local environment has active AWS credentials configured:
    e.g., via ~/.aws/credentials file or environment variables.
    """
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=region_name,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

def generate_text(client, model_id, prompt_text):
    """
    Sends a message to the specified model using the Converse API.
    """
    # Structuring the conversation history
    messages = [
        {
            "role": "user",
            "content": [{"text": prompt_text}]
        }
    ]
    
    # Optional inference configuration parameters
    inference_config = {
        "maxTokens": 500,
        "temperature": 0.7,
        "topP": 0.9
    }

    try:
        print(f"Sending prompt to model: {model_id}...")
        response = client.converse(
            modelId=model_id,
            messages=messages,
            inferenceConfig=inference_config
        )
        
        # Extract and return the generated text response
        output_text = response['output']['message']['content'][0]['text']
        return output_text

    except ClientError as e:
        print(f"AWS Client Error: {e.response['Error']['Message']}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # Initialize the client (ensure model access is granted in this AWS region)
    region_name = os.getenv("AWS_REGION")
    bedrock_runtime = get_bedrock_client(region_name)
    
    # Common model IDs available on Bedrock:
    # - Anthropic Claude 3.5 Sonnet: "anthropic.claude-3-5-sonnet-20240620-v1:0"
    # - Amazon Titan Text Express:  "amazon.titan-text-express-v1"
    # - Meta Llama 3.1 8B Instruct: "meta.llama3-1-8b-instruct-v1:0"
    TARGET_MODEL = os.getenv("BEDROCK_CHAT_MODEL")
    
    prompt = "When is El Nini ending in South India?"
    
    result = generate_text(bedrock_runtime, TARGET_MODEL, prompt)
    
    if result:
        print("\n--- Model Response ---")
        print(result)
