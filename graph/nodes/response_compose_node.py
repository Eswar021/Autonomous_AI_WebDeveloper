from schemas.state import GraphState
from configs.paths import SITE_DIR

def response_compose_node(state: GraphState) -> GraphState:
    if state.build_site:
        state.final_response = (
            "✅ Website generated successfully.\n\n"
            f"Run ID: {state.run_id}\n"
            f"Output folder: {SITE_DIR}\n\n"
            "Files created:\n"
            "- index.html\n"
            "- styles.css\n"
            "- app.js\n"
            "- assets/ (your uploaded files)\n"
            "- helpers/ (manifests, inputs)\n"
            "- logs/ (node prompts + raw outputs)\n"
        )
    # else: default_answer_node already set final_response
    return state
