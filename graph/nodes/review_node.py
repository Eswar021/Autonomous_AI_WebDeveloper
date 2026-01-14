# graph/nodes/review_node.py
import json
from schemas.state import GraphState
from configs.paths import REVIEW_INSTR_PATH, REVIEW_LOG_DIR
from configs.run_utils import write_node_logs, extract_json_block


def review_node(state: GraphState) -> GraphState:
    instr = REVIEW_INSTR_PATH.read_text(encoding="utf-8") if REVIEW_INSTR_PATH.exists() else ""

    from llm.llm_client import make_llm
    llm = make_llm()

    html_code = state.html or ""
    css_code = state.css or ""
    js_code = state.js or ""

    prompt = (
        f"{instr}\n\n"
        "Return JSON only.\n\n"
        f"USER_IDEA:\n{state.user_idea}\n\n"
        f"SITE_BRIEF_JSON:\n{json.dumps(state.site_brief, indent=2, ensure_ascii=False)}\n\n"
        f"ASSETS_MANIFEST_JSON:\n{json.dumps(state.assets_manifest, indent=2, ensure_ascii=False)}\n\n"
        f"INDEX_HTML:\n{html_code}\n\n"
        f"STYLES_CSS:\n{css_code}\n\n"
        f"APP_JS:\n{js_code}\n"
    )

    raw = llm.invoke(prompt).content or ""

    review = {}
    try:
        review = json.loads(extract_json_block(raw))
    except Exception:
        review = {}

    state.review = review

    prompt_text = f"[SYSTEM]\n{instr}\n\n[USER]\n{state.user_idea}"
    write_node_logs(REVIEW_LOG_DIR, prompt_text, raw)

    return state
