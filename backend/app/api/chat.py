from fastapi import APIRouter
from fastapi import Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.chat import ChatRequest
from app.schemas.chat import ChatResponse
from app.schemas.chat import EnquirySubmit

from app.services.workflow.chat_service import ChatWorkflowService
import base64
from voice_service import synthesize_speech_to_mp3

router = APIRouter(
    tags=["Chat"]
)


@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    response = ChatWorkflowService().process(
        db=db,
        session_id=request.session_id,
        message=request.message
    )

    audio_b64 = None
    alignment_data = None
    answer_text = response.get("answer", "")
    if answer_text:
        try:
            audio_b64, alignment_data = synthesize_speech_to_mp3(answer_text)
        except Exception as e:
            print(f"TTS Error: {e}")

    return ChatResponse(
        answer=answer_text,
        session_id=request.session_id,
        intent=response.get("intent", "knowledge"),
        step=response.get("step"),
        options=response.get("options"),
        ticket_number=response.get("ticket_number"),
        onboarding=response.get("onboarding"),
        audio=audio_b64,
        alignment=alignment_data,
        service_table=response.get("service_table"),
        footer=response.get("footer")
    )


@router.post("/enquiry/", response_model=ChatResponse)
def submit_enquiry(
    request: EnquirySubmit,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    response = ChatWorkflowService().submit_enquiry(
        db=db,
        session_id=request.session_id,
        data=request.model_dump(exclude={"session_id"}),
        background_tasks=background_tasks
    )

    audio_b64 = None
    alignment_data = None
    answer_text = response.get("answer", "")
    if answer_text:
        try:
            audio_b64, alignment_data = synthesize_speech_to_mp3(answer_text)
        except Exception as e:
            print(f"TTS Error: {e}")

    return ChatResponse(
        answer=answer_text,
        session_id=request.session_id,
        intent=response.get("intent", "lead"),
        step=response.get("step"),
        options=response.get("options"),
        ticket_number=response.get("ticket_number"),
        audio=audio_b64,
        alignment=alignment_data,
        service_table=response.get("service_table"),
        footer=response.get("footer")
    )
