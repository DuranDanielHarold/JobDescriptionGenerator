#llm dict state

from pydantic import BaseModel
from typing_extensions import TypeDict

    #   - Position: {job_title}
    #   - Expected Start Date: {expected_start_date}
    #   - Department: {department}
    #   - Recruitment Type: {recruitment_type}
    #   - Job duties: {job_duties}
    #   - Required qualifications: {job_qualification}
class JobDataModel(BaseModel):
    job_title: str
    job_location: str
    job_type: str
    department: str
    expiry_date: str
    job_description: str
class JobDescriptionGraphState(TypeDict):
    job_title: str
    job_location: str
    job_type: str
    department: str
    expiry_date: str
    job_description: str

