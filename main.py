
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

    # Step 1: Plan
    plan_result = create_plan(user_query)
    if "error" in plan_result:
         raise HTTPException(status_code=500, detail=f"Planning failed: {plan_result['error']}")
    
    plan = plan_result["plan"]
    planner_usage = plan_result.get("usage", {})

    # Step 2: Execute
    execution_data = execute_plan(plan)
    if "error" in execution_data:
         return {"status": "error", "message": execution_data["error"], "details": execution_data.get("details")}

    # Step 3: Verify / Report
    verifier_result = verify_and_recommend(execution_data)
    if isinstance(verifier_result, str): # Handle legacy error string return if any
        report = verifier_result
        verifier_usage = {}
    else:
        report = verifier_result["report"]
        verifier_usage = verifier_result.get("usage", {})

    # Aggregate Usage
    total_usage = {
        "prompt_tokens": planner_usage.get("prompt_token_count", 0) + verifier_usage.get("prompt_token_count", 0),
        "candidates_tokens": planner_usage.get("candidates_token_count", 0) + verifier_usage.get("candidates_token_count", 0),
        "total_tokens": planner_usage.get("total_token_count", 0) + verifier_usage.get("total_token_count", 0)
    }
    
    return {
        "query": user_query,
        "plan": plan,
        "recommendation": report,
        "usage_stats": total_usage
    }
