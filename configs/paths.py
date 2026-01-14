from pathlib import Path
from datetime import datetime, timedelta, timezone

PROJECT_ROOT = Path(__file__).parent.parent
print("PROJECT_ROOT:", PROJECT_ROOT)

CONFIGS_DIR = PROJECT_ROOT / "configs"
DB_DIR = PROJECT_ROOT / "db"
HISTORY_DIR = DB_DIR / "history"

GRAPH_DIR = PROJECT_ROOT / "graph"
PROMPTS_DIR = GRAPH_DIR / "prompts"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
RUN_DIR = OUTPUTS_DIR / "run"

LOGS_DIR = RUN_DIR / "logs"
SITE_DIR = RUN_DIR / "site"
ASSETS_DIR = SITE_DIR / "assets"
HELPERS_DIR = SITE_DIR / "helpers"

# Core input "State" for each run
USER_IDEA_PATH =  HELPERS_DIR / "user_idea.txt"
ASSETS_INPUT_PATH = HELPERS_DIR / "assets_input.json"
ASSETS_MANIFEST_PATH = HELPERS_DIR / "assets_manifest.json"
SITE_MANIFEST_PATH = HELPERS_DIR / "site_manifest.json"

# Main site artifacts (single-page application)
HTML_OUT = SITE_DIR / "index.html"
CSS_OUT = SITE_DIR / "styles.css"
JS_OUT = SITE_DIR / "app.js"

# Prompt instruction files
INTENT_INSTR_PATH = PROMPTS_DIR / "intent_node_instructions.txt"
SITE_BRIEF_INSTR_PATH = PROMPTS_DIR / "site_brief_node_instructions.txt"
HTML_INSTR_PATH = PROMPTS_DIR / "html_node_instructions.txt"
CSS_INSTR_PATH = PROMPTS_DIR / "css_node_instructions.txt"
JS_INSTR_PATH = PROMPTS_DIR / "js_node_instructions.txt"
REVIEW_INSTR_PATH = PROMPTS_DIR / "review_node_instructions.txt"

# Logs – per node 
INTENT_LOG_DIR = LOGS_DIR / "intent_node"
SITE_BRIEF_LOG_DIR = LOGS_DIR / "site_brief_node"
HTML_LOG_DIR = LOGS_DIR / "html_node"
CSS_LOG_DIR = LOGS_DIR / "css_node"
JS_LOG_DIR = LOGS_DIR / "js_node"
REVIEW_LOG_DIR = LOGS_DIR / "review_node"


def now_ist_str() -> str:
    tz = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(tz).strftime("run_%Y%m%d_%H%M%S_IST")


def run_history_dir(run_id: str) -> Path:
    return HISTORY_DIR / run_id

if __name__ == "__main__":
    pass