from typing import List, Optional

from configs.paths import now_ist_str

from configs.run_utils import (
    reset_run_dir,
    init_run_inputs,
    prepare_assets,
    build_site_manifest,
    archive_run_to_history,
)

from graph.graph import build_graph
from schemas.state import GraphState

class WebDevAgent:
    def __init__(self):
        self.app = build_graph()
        
        
    def run(self, user_prompt: str, asset_paths: Optional[List[str]] = None) -> GraphState:
        
        asset_paths = asset_paths or []
        
        # 1) run_id from the beginning
        run_id = now_ist_str()

        # 2) clean outputs/run
        reset_run_dir()

        # 3) persist inputs
        init_run_inputs(user_prompt, asset_paths)

        # 4) assets pipeline
        assets_manifest = prepare_assets(asset_paths)

        # 5) initial state
        state = GraphState(
            run_id=run_id,
            user_idea=user_prompt,
            asset_paths=asset_paths,
            assets_manifest=assets_manifest,
        )
        
        # 6) invoke graph
        out = self.app.invoke(state.model_dump())
        final_state = GraphState(**out) if isinstance(out, dict) else out

        # 7) manifest in helpers
        build_site_manifest(run_id, user_prompt, assets_manifest, final_state.review)

        # 8) archive run
        archive_run_to_history(run_id)

        return final_state
        