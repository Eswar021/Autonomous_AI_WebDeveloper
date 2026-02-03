# UI/ui_utils.py
from __future__ import annotations

import io
import json
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from werkzeug.utils import secure_filename

from configs.paths import HISTORY_DIR, SITE_DIR, HELPERS_DIR
from configs.run_utils import read_text


@dataclass
class RunPayload:
    run_id: str
    html: str
    css: str
    js: str
    site_manifest: Dict[str, Any]
    assets_manifest: Dict[str, Any]
    preview_url: str
    download_url: str


def _safe_read_text(p: Path) -> str:
    try:
        return read_text(p) if p.exists() else ""
    except Exception:
        return ""


def history_run_root(run_id: str) -> Path:
    # main project: db/history/<run_id>/run
    return (HISTORY_DIR / run_id / "run").resolve()


def history_site_dir(run_id: str) -> Path:
    # outputs/run/site copied to db/history/<run_id>/run/site
    return (history_run_root(run_id) / "site").resolve()


def list_history_runs(limit: int = 50) -> List[Dict[str, Any]]:
    if not HISTORY_DIR.exists():
        return []

    runs = []
    for p in HISTORY_DIR.iterdir():
        if p.is_dir() and p.name.startswith("run_"):
            try:
                mtime = p.stat().st_mtime
            except Exception:
                mtime = 0
            runs.append({"run_id": p.name, "mtime": mtime})

    runs.sort(key=lambda x: x["mtime"], reverse=True)
    runs = runs[:limit]

    # add a human time string
    for r in runs:
        try:
            r["mtime_iso"] = datetime.fromtimestamp(r["mtime"]).isoformat()
        except Exception:
            r["mtime_iso"] = ""
    return runs


def read_run_payload(run_id: str) -> RunPayload:
    base = history_site_dir(run_id)
    if not base.exists():
        raise FileNotFoundError(run_id)

    html = _safe_read_text(base / "index.html")
    css = _safe_read_text(base / "styles.css")
    js = _safe_read_text(base / "app.js")

    # helpers live under site/helpers in your main project
    helpers = base / "helpers"
    site_manifest = {}
    assets_manifest = {}

    sm = helpers / "site_manifest.json"
    am = helpers / "assets_manifest.json"
    if sm.exists():
        try:
            site_manifest = json.loads(sm.read_text(encoding="utf-8"))
        except Exception:
            site_manifest = {}
    if am.exists():
        try:
            assets_manifest = json.loads(am.read_text(encoding="utf-8"))
        except Exception:
            assets_manifest = {}

    return RunPayload(
        run_id=run_id,
        html=html,
        css=css,
        js=js,
        site_manifest=site_manifest,
        assets_manifest=assets_manifest,
        preview_url=f"/preview/{run_id}/index.html",
        download_url=f"/download/{run_id}.zip",
    )


def resolve_inside(base: Path, maybe_child: Path) -> bool:
    # basic traversal guard
    try:
        base_res = base.resolve()
        child_res = maybe_child.resolve()
        return str(child_res).startswith(str(base_res))
    except Exception:
        return False


def zip_site_dir(run_id: str) -> io.BytesIO:
    base = history_site_dir(run_id)
    if not base.exists():
        raise FileNotFoundError(run_id)

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for fp in base.rglob("*"):
            if fp.is_file():
                rel = fp.relative_to(base)
                zf.write(fp, arcname=str(rel))

    buf.seek(0)
    return buf


def save_uploaded_assets(
    uploads_root: Path,
    files,
    descriptions: List[str],
) -> Tuple[List[str], Dict[str, str]]:
    """
    Saves uploaded files into a timestamped folder under UI/uploads/.
    Returns:
      - asset_paths: absolute paths to saved files (for agent.run)
      - asset_desc_map: {original_filename: description}
    """
    uploads_root.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = uploads_root / ts
    run_dir.mkdir(parents=True, exist_ok=True)

    saved_paths: List[str] = []
    desc_map: Dict[str, str] = {}

    for idx, f in enumerate(files):
        if not f or not getattr(f, "filename", ""):
            continue
        original = f.filename
        safe = secure_filename(original) or f"asset_{idx}"
        dest = run_dir / safe
        f.save(dest)

        saved_paths.append(str(dest.resolve()))
        desc = (descriptions[idx] if idx < len(descriptions) else "").strip()
        if desc:
            desc_map[original] = desc

    return saved_paths, desc_map
