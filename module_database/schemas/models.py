# module_database/schemas/models.py
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(200))
    role = Column(String(50), default="developer")  # admin, manager, developer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships will be added later
    # projects = relationship("Project", back_populates="owner")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    repository_url = Column(String(500))
    language = Column(String(50))  # python, javascript, java
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    settings = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    total_files = Column(Integer, default=0)
    files_analyzed = Column(Integer, default=0)
    critical_issues = Column(Integer, default=0)
    high_issues = Column(Integer, default=0)
    medium_issues = Column(Integer, default=0)
    low_issues = Column(Integer, default=0)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Issue(Base):
    __tablename__ = "issues"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("analyses.id"))
    file_path = Column(String(500), nullable=False)
    line_start = Column(Integer)
    line_end = Column(Integer)
    column_start = Column(Integer)
    column_end = Column(Integer)
    issue_type = Column(String(100))  # bug, vulnerability, code_smell, performance
    severity = Column(String(20))  # critical, high, medium, low
    rule_id = Column(String(100))
    message = Column(Text)
    description = Column(Text)
    suggestion = Column(Text)
    code_snippet = Column(Text)
    confidence = Column(Float, default=1.0)  # ML confidence score
    is_false_positive = Column(Boolean, default=False)
    is_fixed = Column(Boolean, default=False)
    fixed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())