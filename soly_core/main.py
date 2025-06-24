from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from soly_core.agent.request_dto import QueryRequest, QueryResponse
from soly_core.agent.agent_setup import run_with_summary
import json
from soly_core.agent.streaming_agent_setup import stream_with_summary
import asyncio
import boto3

app = FastAPI(
    title="Soly AI Agent API",
    description="오솔라 고객지원을 위한 AI Agent API",
    version="1.0.0",
    root_path="/default"
)

@app.post("/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    result, summary = run_with_summary(request.question, request.user.model_dump(), request.history)
    return QueryResponse(answer=result, summary=summary)

@app.post("/query-stream")
async def query_agent_stream(request: QueryRequest):
    async def event_stream():
        async for chunk in stream_with_summary(
            question=request.question,
            user_info=request.user.model_dump(),
            history=request.history
        ):
            yield f"data: {chunk}\n\n"
            await asyncio.sleep(0) 
    return StreamingResponse(event_stream(), media_type="text/event-stream")


async def run_streaming_test():
    print("📩 Soly CLI Agent 테스트 모드")
    question = input("질문을 입력하세요: ")

    user_json = input("UserInfo JSON을 입력하세요 (엔터 시 기본값 사용): ").strip()
    
    if user_json:
        user_data = json.loads(user_json)
    else:
        user_data = {}  

    from soly_core.agent.request_dto import QueryRequest
    request = QueryRequest(
        question=question,
        user=user_data,
        history=["지난달 매출은 1,200,000원이었어요.", "계약 대상은 한국전력공사입니다."]
    )

    print("\n🧠 Claude Streaming 응답:\n")

    async for chunk in stream_with_summary(
        request.question,
        request.user,
        request.history
    ):
        print(chunk, end="", flush=True) 

    print() 

def handler(event, context):
    connection_id = event["requestContext"]["connectionId"]
    domain_name = event["requestContext"]["domainName"]
    stage = event["requestContext"]["stage"]

    body = json.loads(event["body"])
    question = body.get("question")
    user_info = body.get("user", {})
    history = body.get("history", [])

    async def _main():
        apigw = boto3.client("apigatewaymanagementapi", endpoint_url=f"https://{domain_name}/{stage}")
        async for chunk in stream_with_summary(question, user_info, history):
            try:
                apigw.post_to_connection(
                    ConnectionId=connection_id,
                    Data=chunk.encode("utf-8")
                )
            except apigw.exceptions.GoneException:
                print(f"[Gone] Connection {connection_id}")
                break

        try:
            apigw.post_to_connection(
                ConnectionId=connection_id,
                Data="[DONE]".encode("utf-8")
            )
        except apigw.exceptions.GoneException:
            pass
    asyncio.run(_main())

    return {
        "statusCode": 200,
        "body": "Stream started"
    }
