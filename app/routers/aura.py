import json
import asyncio
import random

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas import AuraChatRequest
from app.mock_data import _AURA_SCENARIOS, _aura_default_response

router = APIRouter()


@router.post("/api/aura/chat")
async def aura_chat(payload: AuraChatRequest):
    msg_lower = payload.message.lower()
    response = None
    for keywords, handler in _AURA_SCENARIOS:
        if any(kw in msg_lower for kw in keywords):
            response = handler()
            break
    if response is None:
        response = _aura_default_response(payload.message)

    async def stream_sse():
        meta = {
            "message_id": response["message_id"],
            "timestamp": response["timestamp"],
        }
        yield f"event: meta\ndata: {json.dumps(meta)}\n\n"
        await asyncio.sleep(random.uniform(0.3, 0.6))

        for block in response["content"]:
            yield f"event: block\ndata: {json.dumps(block)}\n\n"
            await asyncio.sleep(random.uniform(0.4, 0.9))

        if response.get("suggested_followups"):
            yield f"event: followups\ndata: {json.dumps(response['suggested_followups'])}\n\n"

        yield "event: done\ndata: {}\n\n"

    return StreamingResponse(
        stream_sse(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
