from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
from pydantic import BaseModel

from app.database import get_db
from app.models.lead import Lead
from app.models.ticket import Ticket
from app.models.escalation import Escalation
from app.models.callback import Callback
from app.models.team_member import TeamMember
from app.models.chat_history import ChatHistory
from app.models.client import Client
from app.models.call_log import CallLog
from app.models.chat_transcript import ChatTranscript

router = APIRouter(prefix="/api/crm", tags=["CRM"])

@router.get("/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    # Stats
    new_leads = db.query(Lead).filter(Lead.status == "NEW").count()
    open_tickets = db.query(Ticket).filter(Ticket.status == "OPEN").count()
    pending_callbacks = db.query(Callback).filter(Callback.status == "Requested").count()
    escalations = db.query(Escalation).filter(Escalation.status == "Pending").count()

    # Recent Tickets
    recent_tickets = (
        db.query(Ticket)
        .order_by(Ticket.created_at.desc())
        .limit(5)
        .all()
    )

    escalations_list = [
        {
            "id": e.id,
            "lead_id": e.lead_id,
            "reason": e.reason,
            "raised_on": e.raised_on.isoformat() if e.raised_on else None
        } for e in db.query(Escalation).filter(Escalation.status == "Pending").order_by(Escalation.raised_on.desc()).all()
    ]

    return {
        "stats": {
            "new_leads": new_leads,
            "open_tickets": open_tickets,
            "pending_callbacks": pending_callbacks,
            "escalations": escalations
        },
        "escalations_list": escalations_list,
        "recent_tickets": [
            {
                "id": t.ticket_number,
                "query": t.issue[:50] + "..." if t.issue and len(t.issue) > 50 else t.issue,
                "status": t.status
            } for t in recent_tickets
        ]
    }

@router.get("/clients")
def get_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).order_by(Client.id.desc()).all()
    return [
        {
            "id": c.id,
            "reference_id": f"REF-{c.id}",
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "company_name": c.company_name,
            "client_type": c.client_type,
            "status": c.status,
            "created_at": c.created_at,
            "last_contacted_at": c.last_contacted_at or c.updated_at or c.created_at
        } for c in clients
    ]

@router.get("/leads")
def get_leads(db: Session = Depends(get_db)):
    leads = db.query(Lead).order_by(Lead.id.desc()).all()
    return [
        {
            "lead_id": lead.id,
            "reference_id": f"REF-{lead.id}",
            "service_interest": lead.service,
            "product": lead.product_name,
            "interest_details": lead.purpose,
            "lead_status": lead.status,
            "session_id": lead.session_id
        } for lead in leads
    ]

@router.post("/leads/{id}/convert")
def convert_lead(id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    lead.status = "Converted"
    
    # Check if client exists
    client = None
    if lead.email:
        client = db.query(Client).filter(Client.email == lead.email).first()
    if not client and lead.phone:
        client = db.query(Client).filter(Client.phone == lead.phone).first()
        
    if not client:
        client = Client(
            name=lead.name or "Unknown",
            email=lead.email,
            phone=lead.phone,
            client_type="Existing Client",
            status="Active"
        )
        db.add(client)
    
    db.commit()
    return {"message": "Lead converted successfully"}

@router.get("/tickets")
def get_tickets(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).order_by(Ticket.id.desc()).all()
    result = []
    for ticket in tickets:
        client_ref = "N/A"
        if ticket.lead_id:
            lead = db.query(Lead).filter(Lead.id == ticket.lead_id).first()
            if lead:
                client = None
                if lead.email:
                    client = db.query(Client).filter(Client.email == lead.email).first()
                if not client and lead.phone:
                    client = db.query(Client).filter(Client.phone == lead.phone).first()
                if client:
                    client_ref = f"REF-{client.id}"
                else:
                    client_ref = f"REF-{lead.id}"
                    
        result.append({
            "ticket_id": ticket.ticket_number,
            "category": ticket.category or "Support",
            "description": ticket.issue,
            "priority": ticket.priority or "Normal",
            "status": ticket.status,
            "last_updated": ticket.last_updated or ticket.created_at,
            "client_reference_id": client_ref
        })
    return result

class TicketUpdate(BaseModel):
    status: str

@router.put("/tickets/{ticket_number}")
def update_ticket(ticket_number: str, update_data: TicketUpdate, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.ticket_number == ticket_number).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    ticket.status = update_data.status
    db.commit()
    return {"message": "Ticket updated successfully"}

@router.get("/callbacks")
def get_callbacks(db: Session = Depends(get_db)):
    callbacks = db.query(Callback).order_by(Callback.id.desc()).all()
    return [
        {
            "callback_id": cb.id,
            "customer_name": cb.name,
            "phone": cb.phone,
            "email": cb.email,
            "topic": cb.topic,
            "requested_time": cb.requested_time.isoformat() if cb.requested_time else None,
            "status": cb.status,
            "related_lead": cb.lead_id,
            "related_ticket": cb.ticket_id,
            "session_id": cb.session_id or (cb.lead.session_id if hasattr(cb, 'lead') and cb.lead else None)
        } for cb in callbacks
    ]

@router.get("/call-logs")
def get_call_logs(db: Session = Depends(get_db)):
    logs = db.query(CallLog).all()
    return [
        {
            "call_id": log.call_id,
            "callback_id": log.callback_id,
            "member_id": log.member_id,
            "received_at": log.received_at.isoformat() if log.received_at else None,
            "picked": log.picked,
            "picked_at": log.picked_at.isoformat() if log.picked_at else None,
            "escalated_to": log.escalated_to,
            "outcome": log.outcome,
            "duration_seconds": log.duration_seconds,
            "recording_url": log.recording_url,
            "call_summary": log.call_summary
        } for log in logs
    ]

@router.get("/team")
def get_team(db: Session = Depends(get_db)):
    team = db.query(TeamMember).all()
    result = []
    for member in team:
        logs = db.query(CallLog).filter(CallLog.member_id == member.id).all()
        calls_received = len(logs)
        picked_logs = [log for log in logs if log.picked]
        calls_picked = len(picked_logs)
        pickup_rate = f"{int((calls_picked / calls_received) * 100)}%" if calls_received > 0 else "0%"
        
        # Calculate escalated count (missed calls that were escalated)
        escalated_count = len([log for log in logs if log.outcome == "Missed Call" and log.escalated_to is not None])
        
        # Calculate avg time to pick
        total_seconds = 0
        valid_picks = 0
        for p_log in picked_logs:
            if p_log.picked_at and p_log.received_at:
                diff = (p_log.picked_at - p_log.received_at).total_seconds()
                if diff > 0:
                    total_seconds += diff
                    valid_picks += 1
        avg_pick_seconds = int(total_seconds / valid_picks) if valid_picks > 0 else 0
        avg_time_to_pick = f"{avg_pick_seconds}s"
        
        result.append({
            "id": member.id,
            "name": member.name,
            "role": member.role,
            "service_desk": member.service_desk,
            "escalation_level": member.escalation_level,
            "is_active": member.is_active if hasattr(member, 'is_active') else True,
            "calls_received": calls_received,
            "calls_picked": calls_picked,
            "pickup_rate": pickup_rate,
            "escalated_count": escalated_count,
            "avg_time_to_pick": avg_time_to_pick
        })
    return result

@router.get("/chat-transcripts")
def get_chat_transcripts(db: Session = Depends(get_db)):
    transcripts = db.query(ChatTranscript).all()
    return [
        {
            "transcript_id": t.transcript_id,
            "session_id": t.session_id,
            "related_id": t.related_id,
            "channel": t.channel,
            "started_at": t.started_at.isoformat() if t.started_at else None,
            "ended_at": t.ended_at.isoformat() if t.ended_at else None,
            "transcript": t.transcript,
            "summary": t.summary
        } for t in transcripts
    ]

class TeamMemberUpdate(BaseModel):
    role: str
    service_desk: str
    escalation_level: str
    is_active: bool

@router.put("/team/{id}")
def update_team_member(id: int, update_data: TeamMemberUpdate, db: Session = Depends(get_db)):
    member = db.query(TeamMember).filter(TeamMember.id == id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Team member not found")
    
    member.role = update_data.role
    member.service_desk = update_data.service_desk
    member.escalation_level = update_data.escalation_level
    member.is_active = update_data.is_active
    db.commit()
    return {"message": "Team member updated"}

@router.get("/client/{id}/360")
def get_client_360(id: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
        
    # Find leads connected to this client
    leads = db.query(Lead).filter(Lead.email == client.email).all()
    if not leads and client.phone:
        leads = db.query(Lead).filter(Lead.phone == client.phone).all()
        
    lead_ids = [l.id for l in leads]
    session_ids = [l.session_id for l in leads if l.session_id]
    
    tickets = db.query(Ticket).filter(Ticket.lead_id.in_(lead_ids)).all() if lead_ids else []
    callbacks = db.query(Callback).filter(Callback.lead_id.in_(lead_ids)).all() if lead_ids else []
    
    chat_history = []
    if session_ids:
        chat_history = db.query(ChatHistory).filter(ChatHistory.session_id.in_([l.session_id for l in leads if l.session_id])).all()
    
    # Get call logs related to the client's leads/tickets/callbacks
    lead_ids = [l.id for l in leads]
    ticket_ids = [t.id for t in tickets]
    callback_ids = [c.id for c in callbacks]
    call_logs = db.query(CallLog).filter(
        CallLog.callback_id.in_(callback_ids)
    ).all() if callback_ids else []

    return {
        "client": {
            "id": client.id,
            "reference_id": f"REF-{client.id}",
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
            "client_type": client.client_type,
            "status": client.status,
            "created_at": client.created_at,
            "last_contacted_at": client.last_contacted_at
        },
        "leads": [{"lead_id": l.id, "service_interest": l.service, "status": l.status, "created_at": l.created_at} for l in leads],
        "tickets": [{"ticket_id": t.ticket_number, "category": t.category, "status": t.status, "created_at": t.created_at} for t in tickets],
        "callbacks": [{"callback_id": c.id, "topic": c.topic, "status": c.status, "created_at": c.created_at} for c in callbacks],
        "chat_history": [{"question": c.question, "answer": c.answer, "timestamp": c.created_at} for c in chat_history],
        "call_logs": [{
            "id": c.call_id, 
            "status": "Picked" if c.picked else "Missed", 
            "outcome": c.outcome, 
            "time": c.received_at.isoformat() if c.received_at else None, 
            "duration": c.duration_seconds,
            "summary": c.call_summary,
            "recording_url": c.recording_url
        } for c in call_logs]
    }
