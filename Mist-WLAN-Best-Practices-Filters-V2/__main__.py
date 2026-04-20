#!/usr/bin/env python3
"""
Entry point so the package can be run with:
    python -m Mist-WLAN-Best-Practices-Filters-V2
"""
import runpy
import os

runpy.run_path(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "mist_wlan_best_practices-V2.py"),
    run_name="__main__"
)
