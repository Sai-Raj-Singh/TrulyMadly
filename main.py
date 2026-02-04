
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.planner import create_plan
from agents.executor import execute_plan
from agents.verifier import verify_and_recommend
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Outdoor Activity Planner")

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def home():
    return {"message": "AI Outdoor Activity Planner is running. Use POST /query to get recommendations."}

@app.post("/query")
def get_recommendation(request: QueryRequest):
    """
    Main pipeline: Planner -> Executor -> Verifier
    """
    user_query = request.query
    if not user_query:
        raise HTTPException(status_code=400, detail="Query is empty")

    plan = create_plan(user_query)
    if "error" in plan:
         raise HTTPException(status_code=500, detail=f"Planning failed: {plan['error']}")

    execution_data = execute_plan(plan)
    if "error" in execution_data:
         return {"status": "error", "message": execution_data["error"], "details": execution_data.get("details")}

    report = verify_and_recommend(execution_data)
    
    return {
        "query": user_query,
        "plan": plan,
        "recommendation": report
    }
