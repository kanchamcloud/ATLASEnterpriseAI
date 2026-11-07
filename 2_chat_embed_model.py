import json
import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

def get_bedrock_client(region_name):
    """
    Initializes the Amazon Bedrock Runtime Client.
    Make sure your local environment has active AWS credentials configured.
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
    messages = [
        {
            "role": "user",
            "content": [{"text": prompt_text}]
        }
    ]
    
    inference_config = {
        "maxTokens": 500,
        "temperature": 0.7,
        "topP": 0.9
    }

    try:
        print(f"Sending prompt to text model: {model_id}...")
        response = client.converse(
            modelId=model_id,
            messages=messages,
            inferenceConfig=inference_config
        )
        
        output_text = response['output']['message']['content'][0]['text']
        return output_text

    except ClientError as e:
        print(f"AWS Client Error: {e.response['Error']['Message']}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def generate_embeddings(client, model_id, text_to_embed):
    """
    Generates semantic vector embeddings for a given text snippet.
    Uses invoke_model since the Converse API does not support embedding models.
    """
    # Structuring the payload specifically for Amazon Titan Text Embeddings (V1/V2)
    native_request = {
        "inputText": text_to_embed,
        "dimensions": 1024,  # Titan V2 supports 256, 512, or 1024
        "normalize": True
    }

    try:
        print(f"Generating embeddings using model: {model_id}...")
        response = client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(native_request)
        )
        print("Response generated ----------------------------------------->")
        # Parse the streaming body response
        response_body = json.loads(response.get("body").read())
        
        # Extract the vector array
        embedding = response_body.get("embedding")
        return embedding

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
    region_name = os.getenv("AWS_REGION", "us-east-1")
    bedrock_runtime = get_bedrock_client(region_name)
    
    # 1. Test the Chat/Text Generation Model
    CHAT_MODEL = os.getenv("BEDROCK_CHAT_MODEL", "amazon.titan-text-express-v1")
    prompt = "When is El Niño ending in South India?"
    
    chat_result = generate_text(bedrock_runtime, CHAT_MODEL, prompt)
    if chat_result:
        print("\n--- Chat Model Response ---")
        print(chat_result)
        print("-" * 30)

    # 2. Test the Embedding Model
    EMBEDDING_MODEL = os.getenv("BEDROCK_EMBED_MODEL", "amazon.titan-embed-text-v2:0")
    sample_text = "Great great GREAT greAT"
    
    vector_result = generate_embeddings(bedrock_runtime, EMBEDDING_MODEL, sample_text)
    if vector_result:
        print("\n--- Embedding Model Response ---")
        print(f"Successfully generated vector embedding!")
        print(f"Vector Dimensions: {len(vector_result)}")
        print(f"Sample values (First 5 dimensions): {vector_result[:5]}")
        print("-" * 30)
