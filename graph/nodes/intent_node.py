from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from schemas.state import GraphState
from configs.paths import INTENT_INSTR_PATH, INTENT_LOG_DIR
from configs.run_utils import write_node_logs, extract_json_block
from llm.llm_client import make_llm
import json

def intent_node(state: GraphState) -> GraphState:
    
    instr = INTENT_INSTR_PATH.read_text(encoding="utf-8") if INTENT_INSTR_PATH.exists() else ""
    
    llm = make_llm()
    
    prompt = (
        f"{instr}\n\n"
        "Return ONLY JSON.\n\n"
        F"USER_IDEA:\n{state.user_idea}\n"
    )
    
    raw = llm.invoke(prompt).content or ""
    
    obj = {}
    obj = json.loads(extract_json_block(raw))
    
    build_site = obj.get("build_site", None)
    reason = obj.get("reason", "")
    
    state.build_site = build_site
    state.intent_reason = reason
    
    prompt_text = f"[SYSTEM]\n {instr}\n\n[USER]\n{state.user_idea}"
    write_node_logs(INTENT_LOG_DIR, prompt_text, raw)
    
    return state