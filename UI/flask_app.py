# UI/flask_app.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from flask import Flask, abort, jsonify, render_template, request, send_file
from werkzeug.datastructures import FileStorage

from agent import WebDevAgent
from configs.paths import HISTORY_DIR
from UI.ui_utils import (
    list_history_runs,
    read_run_payload,
    resolve_inside,
    history_site_dir,
    zip_site_dir,
    save_uploaded_assets,
)

_UI_DIR = Path(__file__).parent
_UPLOADS_DIR = _UI_DIR / "uploads"

# single agent instance (keeps it simple)
_AGENT = WebDevAgent()


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=str(_UI_DIR / "templates"),
        static_folder=str(_UI_DIR / "static"),
    )

    # allow bigger uploads if needed
    app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024  # 200MB

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/api/history")
    def api_history():
        return jsonify({"ok": True, "runs": list_history_runs(limit=100)})

    @app.get("/api/run/<run_id>")
    def api_get_run(run_id: str):
        try:
            payload = read_run_payload(run_id)
            return jsonify(
                {
                    "ok": True,
                    "run_id": payload.run_id,
                    "html": payload.html,
                    "css": payload.css,
                    "js": payload.js,
                    "site_manifest": payload.site_manifest,
                    "assets_manifest": payload.assets_manifest,
                    "preview_url": payload.preview_url,
                    "download_url": payload.download_url,
                }
            )
        except FileNotFoundError:
            return jsonify({"ok": False, "error": "Run not found"}), 404

    @app.post("/api/run")
    def api_run():
        """
        multipart/form-data:
          - prompt: string
          - assets: multiple files
          - asset_desc: multiple strings (same order as assets)
        """
        prompt = (request.form.get("prompt") or "").strip()
        if not prompt:
            return jsonify({"ok": False, "error": "Prompt is required"}), 400

        files = request.files.getlist("assets")  # type: ignore
        descs = request.form.getlist("asset_desc")  # type: ignore

        asset_paths = []
        asset_desc_map: Dict[str, str] = {}

        if files:
            asset_paths, asset_desc_map = save_uploaded_assets(_UPLOADS_DIR, files, descs)

        # minimal change: pass descriptions through prompt (agent logic unchanged)
        if asset_desc_map:
            prompt = (
                prompt
                + "\n\nASSET_DESCRIPTIONS_JSON:\n"
                + json.dumps(asset_desc_map, indent=2, ensure_ascii=False)
            )

        # run the main pipeline (unchanged)
        final_state = _AGENT.run(user_prompt=prompt, asset_paths=asset_paths)

        # your main project archives into db/history/<run_id>/run automatically
        run_id = getattr(final_state, "run_id", None) or "unknown_run"

        try:
            payload = read_run_payload(run_id)
            return jsonify(
                {
                    "ok": True,
                    "run_id": payload.run_id,
                    "html": payload.html,
                    "css": payload.css,
                    "js": payload.js,
                    "site_manifest": payload.site_manifest,
                    "assets_manifest": payload.assets_manifest,
                    "preview_url": payload.preview_url,
                    "download_url": payload.download_url,
                    "final_response": getattr(final_state, "final_response", ""),
                }
            )
        except Exception:
            # fallback: return run_id even if UI can't load it
            return jsonify(
                {
                    "ok": True,
                    "run_id": run_id,
                    "html": getattr(final_state, "html", "") or "",
                    "css": getattr(final_state, "css", "") or "",
                    "js": getattr(final_state, "js", "") or "",
                    "final_response": getattr(final_state, "final_response", ""),
                }
            )

    @app.get("/preview/<run_id>/<path:filename>")
    def preview_file(run_id: str, filename: str):
        base = history_site_dir(run_id)
        if not base.exists():
            abort(404)

        fp = (base / filename).resolve()
        if not resolve_inside(base, fp):
            abort(403)
        if not fp.exists() or not fp.is_file():
            abort(404)

        return send_file(fp)

    @app.get("/download/<run_id>.zip")
    def download_zip(run_id: str):
        try:
            buf = zip_site_dir(run_id)
        except FileNotFoundError:
            abort(404)

        return send_file(
            buf,
            mimetype="application/zip",
            as_attachment=True,
            download_name=f"{run_id}.zip",
        )

    return app
