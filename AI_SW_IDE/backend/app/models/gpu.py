# app/models/gpu.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
import datetime

class GPUUsage(Base):
    __tablename__ = "gpu_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  
    worker_node = Column(String, nullable=False) 
    gpu_id = Column(Integer, nullable=False)
    mig_id = Column(Integer, nullable=False)
    flavor_id = Column(Integer, nullable=False)
    server_id = Column(Integer, nullable=False)
    
    
class Flavor(Base):
    __tablename__ = "gpu_flavor"
    
    id = Column(Integer, primary_key=True, index=True)
    gpu_name = Column(String, nullable=False)
    available = Column(Integer, nullable=False)
    worker_node = Column(String, nullable=False)
    gpu_id = Column(Integer, nullable=False)
    mig_id = Column(Integer, nullable=False)
