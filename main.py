from mcp.server.fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("HR-MCP")

public_holidays = [
    "2025-04-13", "2025-08-19", "2025-09-15",
    "2025-09-25", "2025-10-03", "2025-10-13", "2025-10-14"
]

TOTAL_LEAVE_PER_YEAR = 30

employee_data = {
    "employees": [
        {
            "id": "EMP001",
            "name": "Ashim Baral",
            "work_from_home_days": 15,
            "leaves_taken": 10,
            "attendance": {
                "April": {
                    "2025-04-01": ["07:00", "16:00"],
                    "2025-04-02": ["07:10", "16:00"],
                    "2025-04-03": ["07:00", "15:30"],
                    "2025-04-05": ["07:05", "16:00"]
                }
            }
        },
        {
            "id": "EMP002",
            "name": "Ram Thapa",
            "work_from_home_days": 5,
            "leaves_taken": 20,
            "attendance": {
                "April": {
                    "2025-04-01": ["07:00", "16:00"],
                    "2025-04-02": ["07:30", "15:00"],
                    "2025-04-03": [],
                    "2025-04-04": ["07:00", "16:00"]
                }
            }
        }
    ]
}

def get_employee(emp_id: str):
    return next((emp for emp in employee_data["employees"] if emp["id"] == emp_id), None)

@mcp.tool()
def leave_summary(emp_id: str) -> dict:
    emp = get_employee(emp_id)
    if not emp:
        return {"error": "Employee not found"}
    remaining = TOTAL_LEAVE_PER_YEAR - emp["leaves_taken"]
    return {
        "name": emp["name"],
        "leaves_taken": emp["leaves_taken"],
        "available_leaves": remaining,
        "work_from_home_days": emp["work_from_home_days"],
        "public_holidays": len(public_holidays)
    }

@mcp.tool()
def attendance_summary(emp_id: str, month: str = "April") -> dict:
    WORK_START = "07:00"
    WORK_END = "16:00"
    WORK_HOURS_REQUIRED = 9

    emp = get_employee(emp_id)
    if not emp or month not in emp.get("attendance", {}):
        return {"error": "Attendance not found"}
    
    full, late, early, incomplete = 0, 0, 0, 0

    for date, times in emp["attendance"][month].items():
        if len(times) != 2:
            incomplete += 1
            continue
        checkin = datetime.strptime(times[0], "%H:%M")
        checkout = datetime.strptime(times[1], "%H:%M")
        work_hours = (checkout - checkin).seconds / 3600

        if work_hours >= WORK_HOURS_REQUIRED:
            if times[0] > WORK_START:
                late += 1
            elif times[1] < WORK_END:
                early += 1
            else:
                full += 1
        else:
            incomplete += 1

    return {
        "name": emp["name"],
        "month": month,
        "full_days": full,
        "late_days": late,
        "early_leave_days": early,
        "incomplete_days": incomplete
    }

@mcp.tool()
def apply_leave(emp_id: str, leave_date: str) -> str:
    emp = get_employee(emp_id)
    if not emp:
        return "Employee not found"
    
    if leave_date in emp["attendance"].get("April", {}):
        return "Leave for this date is already applied."
    
    available = TOTAL_LEAVE_PER_YEAR - emp["leaves_taken"]
    if available <= 0:
        return "No leave days available."
    
    if "April" not in emp["attendance"]:
        emp["attendance"]["April"] = {}
        
    emp["attendance"]["April"][leave_date] = []  # Empty list indicates leave for that day
    emp["leaves_taken"] += 1  # Increment leaves taken
    
    return f"Leave applied for {leave_date}. Total leaves now: {emp['leaves_taken']}. Remaining: {TOTAL_LEAVE_PER_YEAR - emp['leaves_taken']}"

@mcp.tool()
def apply_work_from_home(emp_id: str, days: int) -> str:
    emp = get_employee(emp_id)
    if not emp:
        return "Employee not found"
    emp["work_from_home_days"] += days
    return f"Work from home approved. Total WFH days now: {emp['work_from_home_days']}"

@mcp.tool()
def upcoming_holidays() -> list:
    today = datetime.today().date()
    upcoming = [date for date in public_holidays if datetime.strptime(date, "%Y-%m-%d").date() >= today]
    return sorted(upcoming)

@mcp.tool()
def recent_holidays() -> list:
    today = datetime.today().date()
    recent = [date for date in public_holidays if datetime.strptime(date, "%Y-%m-%d").date() < today]
    return sorted(recent, reverse=True)

@mcp.tool()
def find_employee(query: str) -> dict:
    """Find employee by ID or name (case insensitive)"""
    results = []
    for emp in employee_data["employees"]:
        if query.lower() in emp["id"].lower() or query.lower() in emp["name"].lower():
            results.append({
                "id": emp["id"],
                "name": emp["name"],
                "leaves_taken": emp["leaves_taken"],
                "work_from_home_days": emp["work_from_home_days"]
            })
    if not results:
        return {"message": "No matching employee found"}
    return {"matches": results}

@mcp.tool()
def get_full_summary(emp_id: str) -> dict:
    """Return both leave and attendance summary for employee"""
    return {
        "leave": leave_summary(emp_id),
        "attendance": attendance_summary(emp_id)
    }

@mcp.tool()
def get_employee_details(emp_id: str) -> dict:
    """Return all details of an employee"""
    return get_employee(emp_id)
