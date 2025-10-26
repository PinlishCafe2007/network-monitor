from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import requests
import time
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.exists('status.db'):
    os.remove('status.db')
conn = sqlite3.connect('status.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE checks (name TEXT, status INTEGER, response_time REAL)')
conn.commit()

resources = [
    {"name": "Google", "url": "https://google.com"},
    {"name": "GitHub", "url": "https://github.com"},
    {"name": "RuTube", "url": "https://rutube.ru"}
]

@app.get("/status")
def get_status():
    results = []
    for resource in resources:
        try:
            start = time.time()
            response = requests.get(resource["url"], timeout=5)
            response_time = round((time.time() - start) * 1000, 2)
            status = True
        except:
            response_time = None
            status = False
        
        cursor.execute("INSERT INTO checks VALUES (?, ?, ?)", 
                      (resource["name"], 1 if status else 0, response_time))
        conn.commit()
        
        results.append({
            "name": resource["name"],
            "url": resource["url"],
            "status": status,
            "response_time": response_time,
            "error": None if status else "Connection failed"
        })
    
    return results

@app.get("/stats")
def get_stats():
    cursor.execute("SELECT name, COUNT(*), AVG(status)*100, AVG(response_time) FROM checks GROUP BY name")
    stats = []
    for name, total, uptime, avg_time in cursor.fetchall():
        stats.append({
            "name": name,
            "uptime": round(uptime, 1),
            "avg_time": round(avg_time, 1) if avg_time else 0,
            "total_checks": total
        })
    return stats

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)