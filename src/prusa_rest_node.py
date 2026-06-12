from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

from prusa_driver import run_parametric_loop
from camera_driver import get_single_measurement

app = FastAPI(title="Prusa MK4S MADSci Node")
NODE_NAME = os.getenv("NODE_NAME", "prusa_alpha")

current_state = "IDLE"

class ActionRequest(BaseModel):
    action: str
    args: dict

@app.get("/state")
def get_state():
    return {"state": current_state}

@app.get("/about")
def get_about():
    return {
        "name": NODE_NAME,
        "model": "Prusa MK4S & Optical Sensor Node",
        "actions": ["slice_and_print", "measure_fluid"]
    }

@app.post("/action")
def perform_action(req: ActionRequest):
    global current_state
    
    if current_state != "IDLE":
        raise HTTPException(status_code=400, detail="Node is currently busy.")

    if req.action == "slice_and_print":
        current_state = "RUNNING"
        try:
            ridge_length = float(req.args.get("length", 50.0))
            print(f"[{NODE_NAME}] Printing length {ridge_length}mm")
            run_parametric_loop(ridge_length)
            current_state = "IDLE"
            return {"status": "success", "action": req.action, "result": "Print initiated"}
        except Exception as e:
            current_state = "ERROR"
            raise HTTPException(status_code=500, detail=str(e))

    elif req.action == "measure_fluid":
        current_state = "RUNNING"
        try:
            target = int(req.args.get("target_bucket", 3))
            print(f"[{NODE_NAME}] Measuring bucket {target}")
            height = get_single_measurement(target_bucket=target, total_buckets=5, pixels_per_mm=3.2)
            current_state = "IDLE"
            return {"status": "success", "action": req.action, "result": {"height_mm": height}}
        except Exception as e:
            current_state = "ERROR"
            raise HTTPException(status_code=500, detail=str(e))
            
    else:
        raise HTTPException(status_code=404, detail=f"Action '{req.action}' not supported.")