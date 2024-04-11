"""The server that takes incoming WEI flow requests from the experiment application"""
import json
import time

from argparse import ArgumentParser
from contextlib import asynccontextmanager
import ast
import uvicorn

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse

import garby_driver

workcell = None
global garby, state
local_ip = 'garby.alcf.anl.gov' # 130.202.25.104
local_port = 8000 # 50596

@asynccontextmanager
async def lifespan(app: FastAPI):
    global garby, state
    try:
            state = "IDLE"
    except Exception as err:
            print(err)
            state = "ERROR"
    yield
    pass

app = FastAPI(lifespan=lifespan, )

#@app.get("/state")
#def get_state():
#    global barty, state
#    if state != "BUSY":
#        barty.get_status()
#        if barty.status_msg == 3:
#                    msg.data = 'State: ERROR'
#                    state = "ERROR"
#        elif barty.status_msg == 0:
#                    state = "IDLE"
#    return JSONResponse(content={"State": state})

@app.get("/description")
async def description():
    global garby, state
    return JSONResponse(content={"State": state})

@app.get("/resources")
async def resources():
    global garby, state
    return JSONResponse(content={"State": state})

@app.post("/action")
def do_action(
    action_handle: str,
):

    global garby, state
    state = "BUSY"
    

    if action_handle == "trash_plate":  
        try:           
            garby_driver.trash_plate()
            response_content = {
                    "action_msg": "StepStatus.Succeeded",
                    "action_response": "True",
                    "action_log": ""
                }
            state = "IDLE"
            return JSONResponse(content=response_content)
        except Exception as e:
            response_content = {
            "status": "failed",
            "error": str(e),
        }
            state = "IDLE"
            return JSONResponse(content=response_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("garby_REST:app", host=local_ip, port=local_port, reload=True, ws_max_size=100000000000000000000000000000000000000)



