import json, shutil
from pathlib import Path
from typing import Any, Dict, List

from configs.paths import (
    RUN_DIR, LOGS_DIR, ASSETS_DIR, SITE_DIR, HELPERS_DIR,
    USER_IDEA_PATH, ASSETS_INPUT_PATH, ASSETS_MANIFEST_PATH, SITE_MANIFEST_PATH, run_history_dir
    )

def ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p

def write_text(path: Path, text: str):
    ensure_dir(path.parent)
    path.write_text(text, encoding="utf-8")
    
def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")
    
def write_json(path: Path, obj: Any):
    ensure_dir(path.parent)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")

def read_json(path: Path) -> Any:
    return json.loads(read_text(path))

def extract_json_block(s: str) -> str:
    start = s.find("{")
    end = s.rfind("}")
    if start == -1 or end == -1 or end < start:
        return "{}"
    return s[start : end + 1]

def reset_run_dir():
    """
    Always start fresh: delete outputs/run and recreate.
    """
    if RUN_DIR.exists():
        shutil.rmtree(RUN_DIR, ignore_errors=True)

    ensure_dir(LOGS_DIR)
    ensure_dir(SITE_DIR)
    ensure_dir(ASSETS_DIR)
    ensure_dir(HELPERS_DIR)

def init_run_inputs(user_idea: str, asset_paths: List[str]):
    """
    Store the raw inputs used in this run.
    """
    write_text(USER_IDEA_PATH, user_idea)
    write_json(ASSETS_INPUT_PATH, {"asset_paths": asset_paths})

def prepare_assets(asset_paths: List[str]) -> Dict[str, Any]:
    """
    Copy user assets into outputs/run/site/assets and build manifest.
    """
    ensure_dir(ASSETS_DIR)

    items = []
    for idx, raw in enumerate(asset_paths or []):
        p = Path(raw).expanduser()
        item: Dict[str, Any] = {
            "id": f"asset_{idx+1}",
            "original_path": str(p),
            "exists": p.is_file(),
            "filename": p.name,
            "extension": p.suffix.lower(),
            "site_rel_path": None,
        }
        if p.is_file():
            dest = ASSETS_DIR / p.name
            dest.write_bytes(p.read_bytes())
            item["site_rel_path"] = f"assets/{p.name}"
        items.append(item)

    manifest = {
        "assets": items,
        "note": "Assets copied into outputs/run/site/assets. Use site_rel_path in HTML src/href.",
    }
    write_json(ASSETS_MANIFEST_PATH, manifest)
    return manifest

def build_site_manifest(run_id: str, user_idea: str, assets_manifest: Dict[str, Any], review: Dict[str, Any]) -> Dict[str, Any]:
    manifest = {
        "run_id": run_id,
        "user_idea_chars": len(user_idea or ""),
        "asset_count": len((assets_manifest or {}).get("assets", [])),
        "outputs": {
            "site_dir": str(SITE_DIR),
            "logs_dir": str(LOGS_DIR),
            "helpers_dir": str(HELPERS_DIR),
        },
        "review": review or {},
    }
    write_json(SITE_MANIFEST_PATH, manifest)
    return manifest

def archive_run_to_history(run_id: str):
    """
    Copy outputs/run => db/history/<run_id>
    """
    hist = run_history_dir(run_id)
    ensure_dir(hist)

    # Copy entire run folder
    dest = hist / "run"
    if dest.exists():
        shutil.rmtree(dest, ignore_errors=True)

    shutil.copytree(RUN_DIR, dest, dirs_exist_ok=True)

def write_node_logs(log_dir: Path, prompt_text: str, raw_output: str):
    ensure_dir(log_dir)
    write_text(log_dir / "prompt.txt", prompt_text)
    write_text(log_dir / "output_raw.txt", raw_output)

if __name__ == "__main__":
    pass