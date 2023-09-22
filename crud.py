from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List

app = FastAPI()

DATABASE_URL = "sqlite:///crud.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    url = Column(String)
    logo = Column(String)
    created = Column(String)
    updated = Column(String)
    address = Column(String)
    email = Column(String)
    domains = Column(String)
    office_phone = Column(String)
    fax_phone = Column(String)
    twitter = Column(String)
    facebook = Column(String)
    linkedin = Column(String)
    instagram = Column(String)
    pinterest = Column(String)
    tiktok = Column(String)
    ein = Column(String)
    is_default = Column(Boolean)
    is_active = Column(Boolean)

Base.metadata.create_all(bind=engine)

class User(BaseModel):
    name: str
    description: str = None
    url: str
    logo: str
    created: str
    updated: str
    address: str
    email: str
    domains: str
    office_phone: str
    fax_phone: str
    twitter: str
    facebook: str
    linkedin: str
    instagram: str
    pinterest: str
    tiktok: str
    ein: str
    is_default: bool
    is_active: bool

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
def get_all_items(db: Session = Depends(get_db)):
    items = db.query(UserModel).all()
    return items

@app.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(UserModel).filter(UserModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items/", response_model=User)
def create_item(item: User, db: Session = Depends(get_db)):
    db_item = UserModel(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.put("/items/{item_id}", response_model=User)
def update_item(item_id: int, item: User, db: Session = Depends(get_db)):
    db_item = db.query(UserModel).filter(UserModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, value in item.dict().items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(UserModel).filter(UserModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return 'Item Deleted Successfully'