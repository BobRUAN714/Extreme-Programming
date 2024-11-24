from sqlalchemy.orm import Session
import pandas as pd
from . import models, schemas

def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Contact).offset(skip).limit(limit).all()

def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(name=contact.name, is_favorite=contact.is_favorite)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def toggle_favorite(db: Session, contact_id: int):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if contact:
        contact.is_favorite = not contact.is_favorite
        db.commit()
    return contact

def add_contact_info(db: Session, contact_id: int, info: schemas.ContactInfoCreate):
    db_info = models.ContactInfo(**info.dict(), contact_id=contact_id)
    db.add(db_info)
    db.commit()
    db.refresh(db_info)
    return db_info

def import_contacts_from_df(db: Session, df: pd.DataFrame):
    for _, row in df.iterrows():
        contact = create_contact(db, schemas.ContactCreate(
            name=row['Name'],
            is_favorite=row['Favorite']
        ))
        for column in df.columns:
            if column not in ['Name', 'Favorite'] and pd.notna(row[column]):
                values = str(row[column]).split(';')
                for value in values:
                    if value.strip():
                        add_contact_info(db, contact.id, schemas.ContactInfoCreate(
                            info_type=column,
                            value=value.strip()
                        ))
    return {"message": "Import successful"}

def export_contacts_to_excel(db: Session):
    contacts = get_contacts(db)
    data = []
    info_types = set()
    
    for contact in contacts:
        for info in contact.info:
            info_types.add(info.info_type)
    
    for contact in contacts:
        row = {'Name': contact.name, 'Favorite': contact.is_favorite}
        info_dict = {}
        for info in contact.info:
            if info.info_type not in info_dict:
                info_dict[info.info_type] = []
            info_dict[info.info_type].append(info.value)
        
        for info_type in info_types:
            row[info_type] = ';'.join(info_dict.get(info_type, []))
        data.append(row)
    
    df = pd.DataFrame(data)
    return df