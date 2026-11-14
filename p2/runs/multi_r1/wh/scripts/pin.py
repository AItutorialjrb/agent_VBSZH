"""Analysis commit pin (A7): the orchestrator writes the hash into p2/combination/vh_ws/ANALYSIS_COMMIT; generators read it so that regeneration keeps the pin."""
import os
_p = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/combination/vh_ws/ANALYSIS_COMMIT"
COMMIT = open(_p).read().strip() if os.path.exists(_p) and open(_p).read().strip() else "ORCH_COMMIT_PLACEHOLDER"
