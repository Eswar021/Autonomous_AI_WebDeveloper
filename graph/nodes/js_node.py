# graph/nodes/js_node.py
import json
from schemas.state import GraphState
from configs.paths import JS_INSTR_PATH, JS_LOG_DIR, JS_OUT
from configs.run_utils import write_node_logs, write_text


def _extract_code_block(s: str) -> str:
    if "```" not in (s or ""):
        return s or ""
    parts = s.split("```")
    blocks = [p for p in parts if p.strip()]
    return blocks[-1].strip() if blocks else (s or "")


def js_node(state: GraphState) -> GraphState:
    instr = JS_INSTR_PATH.read_text(encoding="utf-8") if JS_INSTR_PATH.exists() else ""

    from llm.llm_client import make_llm
    llm = make_llm()

    html_code = state.html or ""
    css_code = state.css or ""

    prompt = (
        f"{instr}\n\n"
        "Return only JS.\n\n"
        f"USER_IDEA:\n{state.user_idea}\n\n"
        f"SITE_BRIEF_JSON:\n{json.dumps(state.site_brief, indent=2, ensure_ascii=False)}\n\n"
        f"ASSETS_MANIFEST_JSON:\n{json.dumps(state.assets_manifest, indent=2, ensure_ascii=False)}\n\n"
        f"CURRENT_INDEX_HTML:\n{html_code}\n\n"
        f"CURRENT_STYLES_CSS:\n{css_code}\n"
    )

    raw = llm.invoke(prompt).content or ""
    js = _extract_code_block(raw)

    state.js = js
    write_text(JS_OUT, js)

    prompt_text = f"[SYSTEM]\n{instr}\n\n[USER]\n{state.user_idea}"
    write_node_logs(JS_LOG_DIR, prompt_text, raw)

    return state
