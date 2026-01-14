from schemas.state import GraphState
from configs.paths import HTML_INSTR_PATH, HTML_LOG_DIR, HTML_OUT
from configs.run_utils import write_node_logs, write_text
from llm.llm_client import make_llm
import json

def _extract_code_block(s: str) -> str:
    if "```" not in (s or ""):
        return s or ""
    parts = s.split("```")
    blocks = [p for p in parts if p.strip()]
    return blocks[-1].strip() if blocks else (s or "")

def html_node(state: GraphState) -> GraphState:
    instr = HTML_INSTR_PATH.read_text(encoding="utf-8") if HTML_INSTR_PATH.exists() else ""
    llm = make_llm()

    prompt = (
        f"{instr}\n\n"
        "Return ONLY the HTML code.\n\n"
        f"USER_IDEA:\n{state.user_idea}\n\n"
        f"SITE_BRIEF_JSON:\n{json.dumps(state.site_brief, indent=2, ensure_ascii=False)}\n\n"
        f"ASSETS_MANIFEST_JSON:\n{json.dumps(state.assets_manifest, indent=2, ensure_ascii=False)}\n"
    )

    raw = llm.invoke(prompt).content or ""
    html = _extract_code_block(raw)

    state.html = html
    write_text(HTML_OUT, html)

    prompt_text = f"[SYSTEM]\n{instr}\n\n[USER]\n{state.user_idea}"
    write_node_logs(HTML_LOG_DIR, prompt_text, raw)

    return state
