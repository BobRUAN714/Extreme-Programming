from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import io

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db=db, contact=contact)

@app.get("/contacts/", response_model=List[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = crud.get_contacts(db, skip=skip, limit=limit)
    return contacts

@app.put("/contacts/{contact_id}/favorite")
def toggle_favorite(contact_id: int, db: Session = Depends(get_db)):
    return crud.toggle_favorite(db=db, contact_id=contact_id)

@app.post("/contacts/{contact_id}/info")
def add_contact_info(
    contact_id: int, 
    info: schemas.ContactInfoCreate, 
    db: Session = Depends(get_db)
):
    return crud.add_contact_info(db=db, contact_id=contact_id, info=info)

@app.post("/contacts/import")
async def import_contacts(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="Only Excel files are allowed")
    
    contents = await file.read()
    df = pd.read_excel(io.BytesIO(contents))
    return crud.import_contacts_from_df(db=db, df=df)

@app.get("/contacts/export")
def export_contacts(db: Session = Depends(get_db)):
    df = crud.export_contacts_to_excel(db=db)
    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output.getvalue()