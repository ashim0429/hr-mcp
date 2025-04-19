# 🧠 HR-MCP Server with Claude Desktop + UV

This project is an **HR Modular Control Program (MCP)** server built in Python. It provides tools to:

- Track employee leave, attendance, and WFH days
- Apply for leave or work from home
- View upcoming or recent public holidays
- Search employees by name or ID

---

### 🔧 Prerequisites

Make sure the following are installed on your system:

- [Python](https://www.python.org/downloads/) (≥ 3.10)
- [`pip`](https://pip.pypa.io/en/stable/installation/)
- [`uv`](https://github.com/astral-sh/uv) – faster Python environment manager
- [Claude Desktop](https://claude.ai) (installed and running)

---

### 🚀 Setup Instructions

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd <project-directory>
```

2. **Install MCP dependencies and server**

```bash
uv run mcp install main.py
```

> ✅ This command will register the MCP server into Claude Desktop’s config so Claude can detect and use your tools.

3. **Start Claude Desktop**

- Open Claude Desktop app
- You should see your MCP server listed with tools like `leave_summary`, `attendance_summary`, `apply_leave`, etc.

---

### 🛠️ Included Tools

| Tool                                 | Description                                          |
| ------------------------------------ | ---------------------------------------------------- |
| `leave_summary(emp_id)`              | Shows total and available leave info                 |
| `attendance_summary(emp_id, month)`  | Displays full, late, early, or incomplete attendance |
| `apply_leave(emp_id, leave_date)`    | Apply leave for a specific date                      |
| `apply_work_from_home(emp_id, days)` | Apply for WFH                                        |
| `upcoming_holidays()`                | View next public holidays                            |
| `recent_holidays()`                  | View previous holidays                               |
| `find_employee(query)`               | Search employee by name or ID                        |
| `get_full_summary(emp_id)`           | Combined view of leave + attendance                  |

---

### 🧪 Example Usage in Claude

```plaintext
Tool: apply_leave
Input: emp_id=EMP001, leave_date=2025-04-05
```

```plaintext
Tool: get_full_summary
Input: EMP001
```

---

### 💬 Feedback / Improvements

Want to add more features like half-day leave, CSV reports, or email alerts? Open an issue or submit a PR!
