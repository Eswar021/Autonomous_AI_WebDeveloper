from schemas.state import GraphState

def default_answer_node(state: GraphState) -> GraphState:
    
    state.final_response = (
        "Please enter a valid website prompt (what to build) and optionally attach assets.\n\n"
        "Example:\n"
        "- Build a dark-theme portfolio site with hero, projects, skills, timeline, contact.\n"
        "- Use my uploaded images as profile + project demos."
    )
    return state

