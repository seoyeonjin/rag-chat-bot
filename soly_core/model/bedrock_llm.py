import boto3
from langchain_aws.embeddings import BedrockEmbeddings
from langchain_aws import ChatBedrock
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")

embedding_model = BedrockEmbeddings(
    client=bedrock_client,
    model_id="amazon.titan-embed-text-v2:0"
)

llm = ChatBedrock(
    client=bedrock_client,
    # model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    model_kwargs={
        "temperature": 0.0,
        "system": None,
        "anthropic_version": "bedrock-2023-05-31"
    }
)

stream_llm = ChatBedrock(
    client=bedrock_client,
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()], 
    model_kwargs={
        "temperature": 0.0,
        "max_tokens": 4096,
        "anthropic_version": "bedrock-2023-05-31"
    }
)