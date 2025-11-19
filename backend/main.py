from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from database import create_document, get_documents, get_db, DATABASE_URL, DATABASE_NAME
from schemas import News, Event, SuccessStory, ContactSubmission, SupportAtWorkCase, RSVP

app = FastAPI(title="ETUC API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "ETUC API is running"}


@app.get("/test")
def test_connection():
    db = get_db()
    collections = db.list_collection_names()
    return {
        "backend": "FastAPI",
        "database": "MongoDB",
        "database_url": DATABASE_URL,
        "database_name": DATABASE_NAME,
        "connection_status": "ok",
        "collections": collections,
    }


# News endpoints
@app.post("/news", response_model=dict)
def create_news(item: News):
    news_id = create_document("news", item.model_dump())
    return {"id": news_id}


@app.get("/news", response_model=List[dict])
def list_news(category: Optional[str] = None, search: Optional[str] = None, limit: int = 20):
    filter_dict = {}
    if category:
        filter_dict["category"] = category
    if search:
        # naive search in title/summary
        filter_dict["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"summary": {"$regex": search, "$options": "i"}},
        ]
    docs = get_documents("news", filter_dict, limit)
    # sort by date desc if present
    docs.sort(key=lambda d: d.get("date", datetime.min), reverse=True)
    return docs


@app.get("/news/{slug}", response_model=dict)
def get_news_by_slug(slug: str):
    docs = get_documents("news", {"slug": slug}, limit=1)
    if not docs:
        raise HTTPException(status_code=404, detail="News not found")
    return docs[0]


# Events endpoints
@app.post("/events", response_model=dict)
def create_event(item: Event):
    event_id = create_document("event", item.model_dump())
    return {"id": event_id}


@app.get("/events", response_model=List[dict])
def list_events(limit: int = 50):
    docs = get_documents("event", {}, limit)
    docs.sort(key=lambda d: d.get("date", datetime.min))
    return docs


# Success stories
@app.post("/stories", response_model=dict)
def create_story(item: SuccessStory):
    story_id = create_document("successstory", item.model_dump())
    return {"id": story_id}


@app.get("/stories", response_model=List[dict])
def list_stories(limit: int = 20):
    docs = get_documents("successstory", {}, limit)
    docs.sort(key=lambda d: d.get("date", datetime.min), reverse=True)
    return docs


# Contact & forms
@app.post("/contact", response_model=dict)
def submit_contact(item: ContactSubmission):
    contact_id = create_document("contactsubmission", item.model_dump())
    return {"id": contact_id, "status": "received"}


@app.post("/support-at-work", response_model=dict)
def submit_support_case(item: SupportAtWorkCase):
    case_id = create_document("supportatworkcase", item.model_dump())
    return {"id": case_id, "status": "received"}


@app.post("/rsvp", response_model=dict)
def rsvp(item: RSVP):
    rsvp_id = create_document("rsvp", item.model_dump())
    return {"id": rsvp_id, "status": "received"}
