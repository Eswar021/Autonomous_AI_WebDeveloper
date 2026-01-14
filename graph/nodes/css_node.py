# graph/nodes/css_node.py
import json
from schemas.state import GraphState
from configs.paths import CSS_INSTR_PATH, CSS_LOG_DIR, CSS_OUT
from configs.run_utils import write_node_logs, write_text


def _extract_code_block(s: str) -> str:
    if "```" not in (s or ""):
        return s or ""
    parts = s.split("```")
    blocks = [p for p in parts if p.strip()]
    return blocks[-1].strip() if blocks else (s or "")


def css_node(state: GraphState) -> GraphState:
    instr = CSS_INSTR_PATH.read_text(encoding="utf-8") if CSS_INSTR_PATH.exists() else ""

    from llm.llm_client import make_llm
    llm = make_llm()

    html_code = state.html or ""

    prompt = (
        f"{instr}\n\n"
        "Return only CSS.\n\n"
        f"USER_IDEA:\n{state.user_idea}\n\n"
        f"SITE_BRIEF_JSON:\n{json.dumps(state.site_brief, indent=2, ensure_ascii=False)}\n\n"
        f"ASSETS_MANIFEST_JSON:\n{json.dumps(state.assets_manifest, indent=2, ensure_ascii=False)}\n\n"
        f"CURRENT_INDEX_HTML:\n{html_code}\n"
    )

    raw = llm.invoke(prompt).content or ""
    css = _extract_code_block(raw)

    state.css = css
    write_text(CSS_OUT, css)

    prompt_text = f"[SYSTEM]\n{instr}\n\n[USER]\n{state.user_idea}"
    write_node_logs(CSS_LOG_DIR, prompt_text, raw)

    return state
