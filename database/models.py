"""
SQLAlchemy models for Compliance-AI.

Defines the PostgreSQL schema for security telemetry,
compliance evidence, and governance data.
"""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# ==========================================================
# USERS
# ==========================================================

class User(Base):
    __tablename__ = "users"

    employee_id = Column(String(20), primary_key=True)

    name = Column(String(100), nullable=False)

    department = Column(String(100), nullable=False)

    job_title = Column(String(100), nullable=False)

    privilege = Column(String(50), nullable=False)

    source_file = Column(String(255))

    ingested_at = Column(DateTime)

    data_classification = Column(String(50))

    access_reviews = relationship(
        "AccessReview",
        back_populates="user",
    )

    policy_exceptions = relationship(
        "PolicyException",
        back_populates="owner",
    )

    alerts = relationship(
        "Alert",
        back_populates="user",
    )


# ==========================================================
# HOSTS
# ==========================================================

class Host(Base):
    __tablename__ = "hosts"

    hostname = Column(String(100), primary_key=True)

    ip_address = Column(String(50))

    operating_system = Column(String(100))

    criticality = Column(String(50))

    owner_employee_id = Column(
        String(20),
        ForeignKey("users.employee_id"),
    )

    source_file = Column(String(255))

    ingested_at = Column(DateTime)

    data_classification = Column(String(50))

    alerts = relationship(
        "Alert",
        back_populates="host",
    )


# ==========================================================
# ALERTS
# ==========================================================

class Alert(Base):
    __tablename__ = "alerts"

    alert_id = Column(String(30), primary_key=True)

    timestamp = Column(DateTime)

    employee_id = Column(
        String(20),
        ForeignKey("users.employee_id"),
    )

    hostname = Column(
        String(100),
        ForeignKey("hosts.hostname"),
    )

    severity = Column(String(20))

    alert_type = Column(String(100))

    mitre_attack = Column(String(100))

    source_ip = Column(String(50))

    destination_ip = Column(String(50))

    description = Column(String)

    # Metadata added during ingestion
    source_file = Column(String(255))

    ingested_at = Column(DateTime)

    data_classification = Column(String(50))

    user = relationship(
        "User",
        back_populates="alerts",
    )

    host = relationship(
        "Host",
        back_populates="alerts",
    )


# ==========================================================
# ACCESS REVIEWS
# ==========================================================

class AccessReview(Base):
    __tablename__ = "access_reviews"

    review_id = Column(String(30), primary_key=True)

    employee_id = Column(
        String(20),
        ForeignKey("users.employee_id"),
    )

    employee_name = Column(String(100))

    department = Column(String(100))

    system = Column(String(100))

    access_level = Column(String(50))

    reviewer = Column(String(100))

    approved = Column(Boolean)

    review_date = Column(DateTime)

    source_file = Column(String(255))

    ingested_at = Column(DateTime)

    data_classification = Column(String(50))

    user = relationship(
        "User",
        back_populates="access_reviews",
    )


# ==========================================================
# POLICY EXCEPTIONS
# ==========================================================

class PolicyException(Base):
    __tablename__ = "policy_exceptions"

    exception_id = Column(String(30), primary_key=True)

    policy = Column(String(200))

    owner_employee_id = Column(
        String(20),
        ForeignKey("users.employee_id"),
    )

    owner_name = Column(String(100))

    department = Column(String(100))

    risk_level = Column(String(20))

    justification = Column(String)

    approved = Column(Boolean)

    created_date = Column(DateTime)

    expiration_date = Column(DateTime)

    source_file = Column(String(255))

    ingested_at = Column(DateTime)

    data_classification = Column(String(50))

    owner = relationship(
        "User",
        back_populates="policy_exceptions",
    )


# ==========================================================
# CONTROL TESTS
# ==========================================================

class ControlTest(Base):
    __tablename__ = "control_tests"

    test_id = Column(String(30), primary_key=True)

    control_id = Column(String(50))

    control_description = Column(String)

    framework = Column(String(100))

    result = Column(String(20))

    evidence_id = Column(String(50))

    tester = Column(String(100))

    test_date = Column(DateTime)

    finding = Column(String)

    source_file = Column(String(255))

    ingested_at = Column(DateTime)

    data_classification = Column(String(50))

class AuditLog(Base):
    __tablename__ = "audit_logs"

    audit_id = Column(
        String(50),
        primary_key=True
    )

    user = Column(
        String(100)
    )

    action = Column(
        String(100)
    )

    table_accessed = Column(
        String(100)
    )

    record_count = Column(
        Integer
    )

    timestamp = Column(
        DateTime
    )

    purpose = Column(
        String
    )

class Control(Base):
    __tablename__ = "controls"

    control_id = Column(
        String(50),
        primary_key=True
    )

    name = Column(
        String(200)
    )

    description = Column(
        String
    )

    policy_id = Column(
        String(50)
    )

    evidence_sources = Column(
        String
    )