"""Compatibility wrapper: rebuilds the reference pack data (Example Group) with the engine.

Client data lives in pack/clients/<slug>/client.yaml; the engine is pack/engine/build.py.
To build another client's whole pack, use pack/reskin.py.
"""
import runpy, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.argv = [str(HERE / "engine" / "build.py"), str(HERE / "clients" / "example-group" / "client.yaml"), str(HERE / "data")]
runpy.run_path(sys.argv[0], run_name="__main__")
