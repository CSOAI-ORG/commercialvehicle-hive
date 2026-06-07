#!/usr/bin/env python3
"""EvoAgentX bootstrap for commercialvehicle.ai hive.

EvoAgentX (arXiv:2507.03616) autoconstructs agent workflows from
a single prompt. Three SOTA optimizers built in:
  - TextGrad  (Nature 2025) — gradient-based prompt optimization
  - MIPRO     (arXiv:2406.11695) — Bayesian prompt optimization
  - AFlow     (arXiv:2410.10762) — MCTS-based workflow evolution

HITL gate: domain owner (Nick) must approve before deployment.
"""
from __future__ import annotations
import json
import os
from pathlib import Path

import evoagentx  # pip install evoagentx==v0.1.0

HIVE_NAME = "commercialvehicle"
PALETTE   = "fleet grey + route blue"
TOOLS     = ["logistics-ai-mcp"]

def spawn():
    """Build the multi-agent workflow for this hive."""
    hive = evoagentx.spawn(
        domain=HIVE_NAME,
        tools=TOOLS,
        autonomy_level="supervised",   # HITL gate
        design_palette=PALETTE,
        initial_agents=["Route Optimiser", "Telematics Analyst", "Compliance Checker (DTC)"],
        evolution_loop="textgrad",
    )
    # HITL checkpoint: write a proposal for Nick to review
    proposal = Path("hive_proposal.json")
    proposal.write_text(json.dumps({
        "hive": HIVE_NAME,
        "agents": hive.agents,
        "workflow": hive.workflow,
        "tools": TOOLS,
        "estimated_token_cost_per_request": hive.estimate_cost(),
    }, indent=2))
    print("Wrote " + str(proposal) + ". Nick must approve before deployment.")
    return hive

if __name__ == "__main__":
    spawn()
