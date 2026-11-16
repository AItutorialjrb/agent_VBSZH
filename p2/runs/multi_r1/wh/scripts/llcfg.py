"""Reads config/lostlep_qcd.json (the single input of the QCD lost-lepton estimate)."""
import json, os
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "lostlep_qcd.json"); CFG = json.load(open(_p)) if os.path.exists(_p) else {"sample": "F_QCD_llajj_loose", "use_vbs_x_C": False}
LLQ = CFG["sample"]; USE_VBS = bool(CFG.get("use_vbs_x_C", False))
