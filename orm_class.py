from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, DateTime, ForeignKey, UUID, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer,Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import datetime
import uuid
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import BIT


Base = declarative_base()

class SlackConversations(Base):
    __tablename__ = 'slack_conversations'

    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id = Column(String(255))
    thread_ts = Column(String(255))
    payload = Column(JSONB)

class TeamsConversations(Base):
    __tablename__ = 'teams_conversations'

    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_email = Column(String(255))
    payload = Column(JSONB)

class Organization(Base):
    __tablename__ = 'organization'
 
    organization_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_name = Column(String(120), nullable=False)
    organization_logo = Column(String, nullable=False)
    organization_identifier = Column(String(120), nullable=False)
    status = Column(Boolean, default=True)
    has_datasource = Column(Boolean, default=False)
    roi_info = Column(Boolean, default=False)
    is_draft = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_by = Column(String(120))
    modified_by = Column(String(120))

class Intent(Base):
    __tablename__ = 'intent'
    intent_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey('workflow.workflow_id'), nullable=False)
    intent_name = Column(String(100), nullable=False)
    intent_description = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_by = Column(String(120))
    modified_by = Column(String(120))
 
class PreviewWorkflowUrl(Base):
    __tablename__ = 'preview_workflow_url'
    preview_workflow_url_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey('workflow.workflow_id'), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organization.organization_id'), nullable=False)
    channel_id = Column(UUID(as_uuid=True), ForeignKey('channel.channel_id'), nullable=False)
    deployed_url = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_by = Column(String(120))
    modified_by = Column(String(120))
 
class Workflow(Base):
    __tablename__ = 'workflow'
    workflow_id = Column(UUID(as_uuid=True), primary_key=True,server_default=func.uuid_generate_v4())
    organization_id = Column(UUID(as_uuid=True))
    workflow_name = Column(String(120), nullable=False)
    workflow_tags = Column(String(255), nullable=False)
    workflow_description = Column(String)
    ai_cost = Column(Numeric)
    static_cost = Column(Numeric)
    reference_id = Column(UUID, ForeignKey('reference.reference_id'))
    is_predefined = Column(Integer)
    field_values = Column(String)
    workflow_notes = Column(String)
    generated_version = Column(String)
    is_draft = Column(Integer)
    is_active =  Column(BIT(1), server_default=text("B'1'"))
    created_at = Column(TIMESTAMP, server_default=func.now())
    modified_at = Column(TIMESTAMP, onupdate=func.now())
    created_by = Column(String(120))
    modified_by = Column(String(120))

class Organizations(Base):
    __tablename__ = 'organization'

    organization_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_name = Column(String(120), nullable=False)
    organization_logo = Column(String, nullable=False)
    organization_identifier = Column(String(120), nullable=False)
    status = Column(Boolean, default=True)
    has_datasource = Column(Boolean, default=False)
    roi_info = Column(Boolean, default=False)
    is_draft = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    modified_at = Column(DateTime)
    created_by = Column(String(120))
    modified_by = Column(String(120))
    industry_vertical = Column(String(120))
    environment = Column(String(120))

class SlackConversationsUrl(Base):
    __tablename__ = 'slack_conversations_url'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_email = Column(String(255))
    workflow_url = Column(String(2048))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
 