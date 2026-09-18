import io
import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sklearn.linear_model import LinearRegression

app = FastAPI(title="FLYTOALL", version="1.0.0")

state = {
    "columns": [],
    "rows": [],
    "targets": [],
    "predictions": {},
    "updated_at": None,
}
clients = set()

def now():
    return datetime.now(timezone.utc).isoformat()

def json_safe(value):
    if pd.isna(value):
        return None
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    return value

def dataframe_payload(df):
    records = []
    for row in df.to_dict(orient="records"):
        records.append({k: json_safe(v) for k, v in row.items()})
    return records

def calculate_predictions():
    result = {}
    if not state["rows"]:
        return result

    df = pd.DataFrame(state["rows"])
    for target in state["targets"]:
        if target not in df.columns:
            continue

        y = pd.to_numeric(df[target], errors="coerce")
        valid = y.dropna()
        if len(valid) < 3:
            result[target] = {"status": "dados insuficientes"}
            continue

        x = np.arange(len(valid)).reshape(-1, 1)
        model = LinearRegression().fit(x, valid.to_numpy())
        horizon = min(12, max(3, len(valid) // 3))
        future_x = np.arange(len(valid), len(valid) + horizon).reshape(-1, 1)
        pred = model.predict(future_x)

        result[target] = {
            "status": "ok",
            "last": round(float(valid.iloc[-1]), 4),
            "slope": round(float(model.coef_[0]), 6),
            "r2": round(float(model.score(x, valid.to_numpy())), 4),
            "forecast": [round(float(v), 4) for v in pred],
        }
    return result

async def broadcast():
    payload = {
        "type": "state",
        "columns": state["columns"],
        "rows": state["rows"][-200:],
        "targets": state["targets"],
        "predictions": state["predictions"],
        "updated_at": state["updated_at"],
    }
    dead = []
    for ws in clients:
        try:
            await ws.send_text(json.dumps(payload))
        except Exception:
            dead.append(ws)
    for ws in dead:
        clients.discard(ws)

@app.get("/")
async def home():
    return FileResponse("static/index.html")

@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    raw = await file.read()
    name = file.filename.lower()

    if name.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(raw))
    elif name.endswith((".xlsx", ".xls")):
        df = pd.read_excel(io.BytesIO(raw))
    else:
        return {"error": "Envie CSV, XLSX ou XLS."}

    df = df.replace({np.nan: None})
    state["columns"] = [str(c) for c in df.columns]
    state["rows"] = dataframe_payload(df)
    state["targets"] = []
    state["predictions"] = {}
    state["updated_at"] = now()
    await broadcast()
    return {"ok": True, "columns": state["columns"], "rows": state["rows"]}

@app.post("/api/targets")
async def targets(payload: dict):
    selected = [c for c in payload.get("targets", []) if c in state["columns"]]
    state["targets"] = selected
    state["predictions"] = calculate_predictions()
    state["updated_at"] = now()
    await broadcast()
    return {"ok": True, "targets": selected, "predictions": state["predictions"]}

@app.post("/api/cell")
async def update_cell(payload: dict):
    row = int(payload["row"])
    column = str(payload["column"])
    value = payload.get("value")

    if row < 0 or row >= len(state["rows"]) or column not in state["columns"]:
        return {"ok": False, "error": "Célula inválida."}

    state["rows"][row][column] = value
    state["predictions"] = calculate_predictions()
    state["updated_at"] = now()
    await broadcast()
    return {"ok": True}

@app.post("/api/add-row")
async def add_row():
    state["rows"].append({c: "" for c in state["columns"]})
    state["predictions"] = calculate_predictions()
    state["updated_at"] = now()
    await broadcast()
    return {"ok": True}

@app.post("/api/add-column")
async def add_column(payload: dict):
    column = str(payload.get("column", "")).strip()
    if not column or column in state["columns"]:
        return {"ok": False, "error": "Nome de coluna inválido ou duplicado."}
    state["columns"].append(column)
    for row in state["rows"]:
        row[column] = ""
    state["updated_at"] = now()
    await broadcast()
    return {"ok": True}

@app.get("/api/export")
async def export_csv():
    df = pd.DataFrame(state["rows"], columns=state["columns"])
    path = "/tmp/flytoall_export.csv"
    df.to_csv(path, index=False)
    return FileResponse(path, filename="flytoall_export.csv", media_type="text/csv")

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    await ws.send_text(json.dumps({
        "type": "state",
        "columns": state["columns"],
        "rows": state["rows"][-200:],
        "targets": state["targets"],
        "predictions": state["predictions"],
        "updated_at": state["updated_at"],
    }))
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        clients.discard(ws)
    except Exception:
        clients.discard(ws)

app.mount("/static", StaticFiles(directory="static"), name="static")
