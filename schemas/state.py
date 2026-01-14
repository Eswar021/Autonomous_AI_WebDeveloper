from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class GraphState(BaseModel):
    run_id: str = Field(..., description="Unique run id created at invocation start.")

    # Inputs
    user_idea: str = Field("", description="Raw user prompt/brief.")
    asset_paths: List[str] = Field(default_factory=list, description="User-provided asset file paths.")

    # Intent gating
    build_site: bool = Field(True, description="If false, skip build pipeline and return default response.")
    intent_reason: str = Field("", description="Why build_site was true/false.")

    # Intermediate artifacts
    assets_manifest: Dict[str, Any] = Field(default_factory=dict)
    site_brief: Dict[str, Any] = Field(default_factory=dict)

    # Generated code
    html: Optional[str] = None
    css: Optional[str] = None
    js: Optional[str] = None

    # Review JSON (optional)
    review: Dict[str, Any] = Field(default_factory=dict)

    # Final response to UI
    final_response: str = Field("", description="What app.py returns to the user.")

