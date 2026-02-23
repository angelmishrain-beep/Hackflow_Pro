from fastapi import FastAPI
from fastapi import File, UploadFile
from pydantic import BaseModel
import mysql.connector
import os
import google.generativeai as genai

genai.configure(api_key=("AIzaSyAZRTWl3jXsTzS-p4fF8D0CMX_Gnr8d4ME"))

app = FastAPI()

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",       
        password="root",  
        database="hackathon_db"
    )

class TeamInfo(BaseModel):
    team_name: str
    leader_name: str
    leader_email: str
    members: list

class HackathonInfo(BaseModel):
    theme: str
    problem_statement: str = None
    duration: int
    time_unit: str

class HelpRequest(BaseModel):
    query: str

class TrackRequest(BaseModel):
    project_url: str

@app.get("/")
def root():
    return {"message": "Backend is running"}


@app.post("/save_team")
def save_team(info: TeamInfo):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO teams (team_name, leader_name, leader_email) VALUES (%s,%s,%s)",
        (info.team_name, info.leader_name, info.leader_email)
    )
    team_id = cursor.lastrowid

    for m in info.members:
        cursor.execute(
            "INSERT INTO members (team_id, email, skill_level) VALUES (%s,%s,%s)",
            (team_id, m["email"], m["level"])
        )

    db.commit()
    cursor.close()
    db.close()
    return {"message": "Team saved successfully "}

@app.post("/save_hackathon")
def save_hackathon(info: HackathonInfo):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO hackathon (theme, problem_statement, duration, time_unit) VALUES (%s,%s,%s,%s)",
        (info.theme, info.problem_statement, info.duration, info.time_unit)
    )

    db.commit()
    cursor.close()
    db.close()
    return {"message": "Hackathon info saved"}

@app.post("/assign_tasks")
def assign_tasks():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM hackathon ORDER BY id DESC LIMIT 1")
    hackathon = cursor.fetchone()

    cursor.execute("SELECT * FROM teams ORDER BY id DESC LIMIT 1")
    team = cursor.fetchone()

    cursor.execute("SELECT * FROM members WHERE team_id=%s", (team["id"],))
    members = cursor.fetchall()

    cursor.close()
    db.close()

    prompt = f"""
    You are an AI assistant for a hackathon. 
    Hackathon Theme: {hackathon['theme']}
    Problem Statement: {hackathon['problem_statement']}
    Duration: {hackathon['duration']} {hackathon['time_unit']}
    
    Team: {team['team_name']} led by {team['leader_name']}
    Members and their skills:
    {members}

     Assign tasks to each member based on their skill level.
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return {"tasks": response.text}


@app.post("/help")
def get_help(req: HelpRequest):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(req.query)
    return {"answer": response.text}


@app.post("/track")
def track_progress(req: TrackRequest):
    prompt = f"Track the progress of this project: {req.project_url}. Give a % completion estimate."
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    progress = 90
    return {"progress": progress, "details": response.text}

class Project(BaseModel):
    project_url: str
@app.post("/track")
def track_progress(req: TrackRequest):
    # Mock tracking with Gemini (can integrate GitHub APIs here)
    prompt = f"Track the progress of this project: {req.project_url}. Give a % completion estimate."
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    # Simple mock: extract % if exists, else default
    progress = 70
    return {"progress": progress, "details":response.text}

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_mysql_username",
        password="your_mysql_password",
        database="your_database_name",
    )


@app.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO code_files (file_name, file_content) VALUES (%s, %s)"
    cursor.execute(sql, (file.filename, content))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": f"File '{file.filename}' uploaded successfully"}
pull_requests_db = {
    "pr1": {"title": "Feature A", "status": "open", "conflicts": False},
    "pr2": {"title": "Bugfix B", "status": "open", "conflicts": True},
}

@app.get("/github/prs")
def list_pull_requests():
    # Return all PRs with conflict info
    return pull_requests_db

@app.get("/github/prs/{pr_id}/suggest_merge")
def suggest_merge(pr_id: str):
    pr = pull_requests_db.get(pr_id)
    if not pr:
        return {"error": "PR not found"}
    if pr["conflicts"]:
        return {"suggestion": f"PR '{pr['title']}' has conflicts. Please resolve before merging."}
    else:
        return {"suggestion": f"PR '{pr['title']}' is clear. Safe to merge."}
 