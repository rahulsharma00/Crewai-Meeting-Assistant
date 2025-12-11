from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from crewai import Crew
from .tasks import MeetingPrepTasks
from .agents import MeetingPrepAgents
from .tools import ExaSearchToolset
from .main import run_meeting_prep

app = FastAPI()

class MeetingRequest(BaseModel):
    participants: str
    context: str
    objective: str

@app.post("/run-meeting-prep")
async def run_meeting(req: MeetingRequest):
    try:
        result = run_meeting_prep(
            req.participants,
            req.context,
            req.objective
        )
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
