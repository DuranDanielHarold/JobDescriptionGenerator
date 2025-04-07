from langgraph.graph import START, StateGraph, END
from langgraph.graph import StateGraph
from data_models import JobDescriptionGraphState
from utils import CacheManager # Assuming cache_manager is defined in utils.py
from typing import List, Dict
from agents import create_jd_agent  # Replace 'some_module' with the actual module where create_rar_agent is defined

cache_manager = CacheManager()
# NODE TO CREATE JOB DESCRIPTION
def create_job_description(state: JobDescriptionGraphState) -> JobDescriptionGraphState:
    try:
            if not cache_manager.has("jdw_agent_chain"):
                cache_manager.set("jdw_agent_chain", create_jd_agent())

            jdw_agent_chain = cache_manager.get("jdw_agent_chain")
            #GET ALL JOB REQUIREMENTS FOR GENERATION OF JOB DESCRIPTION
            job_title = state.get("job_title", "")
            job_location = state.get("job_location", "")
            job_type = state.get("job_type", "")
            department = state.get("department", "")
            expiry_date = state.get("expiry_date", "")
            start_date = state.get("expected_start_date", "")
            job_qualifications = state.get("job_qualification", "")
            job_location = state.get("job_location", "")
            job_duties = state.get("job_duties", "")

            messages = jdw_agent_chain.invoke({
                "job_title": job_title,
                "expected_start_date": start_date,
                "department": department,
                "recruitment_type": job_type,
                "job_duties": job_duties,
                "job_qualification": job_qualifications,
                "expiry_date": expiry_date,
                "job_location": job_location
            })

            return {"job_description": messages.job_description,
                    "job_title": messages.job_title,
                    "job_type": messages.job_type,
                    "department": messages.department,
                    "expiry_date": messages.expiry_date,
                    "expected_start_date": messages.expected_start_date,
                    "job_qualification": messages.job_qualification,
                    "job_duties": messages.job_duties,
                    "job_location": messages.job_location}
    
    except Exception as e:
        raise RuntimeError(f"ERROR IN 'create_job_description' NODE: {str(e)}")
def graphbuilder():
    #PLOT THE GRAPH
    graph_builder = StateGraph(JobDescriptionGraphState)
    ## ADD NODES TO THE GRAPH
    graph_builder.add_node("CreateJobDescription",create_job_description )

    ## ADD EDGES TO THE GRAPH
    graph_builder.add_edge(START, "CreateJobDescription")
    graph_builder.add_edge("CreateJobDescription", END)

    return graph_builder.compile()
