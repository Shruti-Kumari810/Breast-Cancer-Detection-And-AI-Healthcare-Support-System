"""Initial schema.

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-06-21
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer(), primary_key=True),
        sa.Column("full_name", sa.String(120), nullable=False),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role", sa.String(40), nullable=False, server_default="doctor"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "patients",
        sa.Column("patient_id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("phone", sa.String(40), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("address", sa.String(500), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "doctors",
        sa.Column("doctor_id", sa.Integer(), primary_key=True),
        sa.Column("doctor_name", sa.String(120), nullable=False),
        sa.Column("specialization", sa.String(120), nullable=False),
        sa.Column("hospital_name", sa.String(180), nullable=False),
        sa.Column("city", sa.String(120), nullable=False),
        sa.Column("experience", sa.Integer(), nullable=False),
        sa.Column("contact", sa.String(80), nullable=False),
    )
    op.create_table(
        "health_resources",
        sa.Column("resource_id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(160), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("resource_type", sa.String(80), nullable=False),
        sa.Column("url", sa.String(500), nullable=False),
    )
    op.create_table(
        "predictions",
        sa.Column("prediction_id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), sa.ForeignKey("patients.patient_id", ondelete="CASCADE")),
        sa.Column("algorithm_used", sa.String(80), nullable=False),
        sa.Column("prediction_result", sa.String(40), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("prediction_date", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "appointments",
        sa.Column("appointment_id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), sa.ForeignKey("patients.patient_id", ondelete="CASCADE")),
        sa.Column("doctor_id", sa.Integer(), sa.ForeignKey("doctors.doctor_id")),
        sa.Column("appointment_date", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(40), nullable=False, server_default="booked"),
    )


def downgrade() -> None:
    op.drop_table("appointments")
    op.drop_table("predictions")
    op.drop_table("health_resources")
    op.drop_table("doctors")
    op.drop_table("patients")
    op.drop_table("users")

