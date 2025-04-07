from langgraph.graph import START, StateGraph, END
from langgraph.graph import State, Transition
from langgraph.graph import StateGraphBuilder
from data_models import JobDescriptionGraphState
from utils import cache_manager  # Assuming cache_manager is defined in utils.py
from typing import List, Dict
from agents import create_jd_agent  # Replace 'some_module' with the actual module where create_rar_agent is defined

# NODE TO CREATE JOB DESCRIPTION
def create_job_description(state: JobDescriptionGraphState) -> JobDescriptionGraphState:
    try:
         if not cache_manager.has("jdw_agent_chain"):
            cache_manager.set("jdw_agent_chain", create_jd_agent())
            jdw_agent_chain = cache_manager.get("jdw_agent_chain")
            #GET ALL JOB REQUIREMENTS FOR GENERATION OF JOB DESCRIPTION
            job_title = state.job_title.get("job_title", "")
            job_location = state.job_location.get("job_location", "")
            job_type = state.job_type.get("job_type", "")
            department = state.department.get("department", "")
            expiry_date = state.expiry_date.get("expiry_date", "")
            job_description = state.job_description.get("job_description", "")
            messages = jdw_agent_chain.invoke({
                "job_title": job_title,
                "job_location": job_location,
                "job_type": job_type,
                "department": department,
                "expiry_date": expiry_date,
                "job_description": job_description
            })

            return {"job_description": messages.content}
    except Exception as e:
        raise RuntimeError(f"ERROR IN 'create_job_description' NODE: {str(e)}")
    
#PLOT THE GRAPH
graph_builder = StateGraph(JobDescriptionGraphState)
## ADD NODES TO THE GRAPH
graph_builder.add_node("Create Job Description",create_job_description )

## ADD EDGES TO THE GRAPH
graph_builder.add_edge(START, "Create Job Description")
graph_builder.add_edge("Create Job Description", END)

graph = graph_builder.compile()
