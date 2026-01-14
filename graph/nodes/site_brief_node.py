from schemas.state import GraphState
from configs.paths import SITE_BRIEF_INSTR_PATH, SITE_BRIEF_LOG_DIR
from configs.run_utils import write_node_logs, extract_json_block
from llm.llm_client import make_llm
import json

def site_brief_node(state: GraphState) -> GraphState:
    
    instr = SITE_BRIEF_INSTR_PATH.read_text(encoding="utf-8") if SITE_BRIEF_INSTR_PATH.exists() else ""
    
    llm = make_llm()
    
    prompt = (
        f"{instr}\n\n"
        "Return JSON only.\n\n"
        f"USER_IDEA:\n{state.user_idea}\n\n"
        f"ASSETS_MANIFEST_JSON:\n{json.dumps(state.assets_manifest, indent=2, ensure_ascii=False)}\n"
    )
    
    raw  = llm.invoke(prompt).content or "" 
    
    brief = {}
    brief = json.loads(extract_json_block(raw))

    state.site_brief = brief
    
    prompt_text = (
        f"[SYSTEM]\n{instr}\n\n"
        f"[USER]\nUSER_IDEA:\n{state.user_idea}\n\n"
        f"ASSETS_MANIFEST_JSON:\n{json.dumps(state.assets_manifest, indent=2, ensure_ascii=False)}"
    )
    
    write_node_logs(SITE_BRIEF_LOG_DIR, prompt_text, raw)

    return state