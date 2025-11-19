from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class News(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    slug: str = Field(..., min_length=3, max_length=200)
    category: str = Field(..., pattern=r"^(Campaigns|Events|Press Releases)$")
    summary: str = Field(..., min_length=10, max_length=600)
    content: str
    date: datetime
    image_url: Optional[str] = None

class Event(BaseModel):
    title: str
    date: datetime
    location: str
    description: str
    rsvp_url: Optional[str] = None
    image_url: Optional[str] = None

class SuccessStory(BaseModel):
    title: str
    summary: str
    content: str
    date: datetime

class ContactSubmission(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    message: str
    type: str = Field(..., pattern=r"^(general|advice|affiliate|volunteer)$")

class SupportAtWorkCase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    postcode: Optional[str] = None
    union_member: Optional[bool] = None
    employer: Optional[str] = None
    issue: str

class RSVP(BaseModel):
    event_id: str
    name: str
    email: EmailStr

class Pagination(BaseModel):
    page: int = 1
    page_size: int = 10

class NewsFilter(BaseModel):
    category: Optional[str] = None
    search: Optional[str] = None
