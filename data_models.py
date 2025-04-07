#llm dict state

from pydantic import BaseModel
from typing import TypedDict, Annotated

    #   - Position: {job_title}
    #   - Expected Start Date: {expected_start_date}
    #   - Department: {department}
    #   - Recruitment Type: {recruitment_type}
    #   - Job duties: {job_duties}
    #   - Required qualifications: {job_qualification}
class JobDataModel(BaseModel):
    job_title: str
    job_type: str
    department: str
    expiry_date: str
    job_duties: str
    job_qualification: str
    expected_start_date: str
    job_location: str
    job_description: Annotated[str, "COMPILED JOB DESCRIPTION"]

    #       - Position: {job_title}1
    #   - Expected Start Date: {expected_start_date}7
    #   - Department: {department}3
    #   - Recruitment Type: {recruitment_type}2
    #   - Job duties: {job_duties}5
    #   - Required qualifications: {job_qualification}6
    #   - Job Expiration Date: {expiry_date}4

    
class JobDescriptionGraphState(TypedDict):
    job_title: str
    job_type: str
    department: str
    expiry_date: str
    job_duties: str
    job_qualification: str
    expected_start_date: str
    job_description: JobDataModel
    job_location: str

