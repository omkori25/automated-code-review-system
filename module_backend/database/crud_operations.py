# module_backend/database/crud_operations.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from . import models
import logging

logger = logging.getLogger(__name__)

class UserCRUD:
    @staticmethod
    def create_user(db: Session, user_data: Dict[str, Any]):
        """Create new user"""
        db_user = models.User(
            id=uuid.uuid4(),
            **user_data
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_user(db: Session, user_id: str):
        """Get user by ID"""
        return db.query(models.User).filter(models.User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        """Get user by email"""
        return db.query(models.User).filter(models.User.email == email).first()

class ProjectCRUD:
    @staticmethod
    def create_project(db: Session, project_data: Dict[str, Any]):
        """Create new project"""
        db_project = models.Project(
            id=uuid.uuid4(),
            **project_data
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    
    @staticmethod
    def get_user_projects(db: Session, user_id: str):
        """Get all projects for a user"""
        return db.query(models.Project).filter(
            models.Project.owner_id == user_id
        ).all()

class AnalysisCRUD:
    @staticmethod
    def create_analysis(db: Session, analysis_data: Dict[str, Any]):
        """Create new analysis"""
        db_analysis = models.Analysis(
            id=uuid.uuid4(),
            **analysis_data
        )
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        return db_analysis
    
    @staticmethod
    def update_analysis_status(db: Session, analysis_id: str, status: str):
        """Update analysis status"""
        analysis = db.query(models.Analysis).filter(
            models.Analysis.id == analysis_id
        ).first()
        if analysis:
            analysis.status = status
            if status == "completed":
                analysis.completed_at = datetime.now()
            db.commit()
        return analysis

class IssueCRUD:
    @staticmethod
    def create_issue(db: Session, issue_data: Dict[str, Any]):
        """Create new issue"""
        db_issue = models.Issue(
            id=uuid.uuid4(),
            **issue_data
        )
        db.add(db_issue)
        db.commit()
        db.refresh(db_issue)
        return db_issue
    
    @staticmethod
    def get_analysis_issues(db: Session, analysis_id: str):
        """Get all issues for an analysis"""
        return db.query(models.Issue).filter(
            models.Issue.analysis_id == analysis_id
        ).all()
    
    @staticmethod
    def mark_false_positive(db: Session, issue_id: str):
        """Mark issue as false positive"""
        issue = db.query(models.Issue).filter(
            models.Issue.id == issue_id
        ).first()
        if issue:
            issue.is_false_positive = True
            db.commit()
        return issue