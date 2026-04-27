from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False, unique=True, index=True)

    studies = relationship(
        "Study",
        back_populates="patient",
        cascade="all, delete-orphan",
    )


class Study(Base):
    __tablename__ = "studies"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    doctor_name = Column(String(120), nullable=False)
    specialization = Column(String(120), nullable=False)
    status = Column(String(50), nullable=False)
    report_text = Column(Text, nullable=False)
    study_file_name = Column(String(200), nullable=False)

    patient = relationship("Patient", back_populates="studies")
