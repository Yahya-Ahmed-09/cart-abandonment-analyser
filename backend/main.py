"""Cart abandonment dashboard API (read-only, SQLite).

Run from the backend folder:  uvicorn main:app --reload --port 8000
Docs:                         http://127.0.0.1:8000/docs
"""
import os
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

DB_PATH = Path(os.getenv("DB_PATH", "../artifacts/dashboard.db")).resolve()
if not DB_PATH.exists():
    raise RuntimeError(f"Database not found: {DB_PATH}")

ALLOWED_BANDS = {"High", "Medium", "Low"}

app = FastAPI(title="Cart Abandonment Dashboard API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def query(sql: str, params=()):
    """Run a read-only query and return a list of dicts (one connection per call)."""
    with closing(sqlite3.connect(f"{DB_PATH.as_uri()}?mode=ro", uri=True)) as con:
        con.row_factory = sqlite3.Row
        return [dict(r) for r in con.execute(sql, params).fetchall()]


CATALOG = {r["code"]: r for r in query("SELECT * FROM reasons_catalog")}


def reason_info(code: Optional[str]):
    if not code or code not in CATALOG:
        return None
    c = CATALOG[code]
    return {
        "code": code,
        "title": c["title"],
        "explanation": c["explanation"],
        "suggested_action": c["suggested_action"],
    }


def common_filters(
    date_from: Optional[str] = Query(None, description="YYYY-MM-DD"),
    date_to: Optional[str] = Query(None, description="YYYY-MM-DD"),
    brand: Optional[str] = None,
    category_id: Optional[int] = None,
):
    """Shared filters: returns (list of SQL clauses, list of parameters)."""
    clauses, params = [], []
    if date_from:
        clauses.append("event_date >= ?")
        params.append(date_from)
    if date_to:
        clauses.append("event_date <= ?")
        params.append(date_to)
    if brand:
        clauses.append("brand = ?")
        params.append(brand)
    if category_id is not None:
        clauses.append("category_id = ?")
        params.append(category_id)
    return clauses, params


def where(clauses):
    return (" WHERE " + " AND ".join(clauses)) if clauses else ""


def parse_bands(bands: str):
    values = [b.strip().capitalize() for b in bands.split(",") if b.strip()]
    if not values or any(b not in ALLOWED_BANDS for b in values):
        raise HTTPException(status_code=400, detail="bands must be a comma list of High, Medium, Low")
    return values


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/filters")
def filters():
    rng = query("SELECT MIN(event_date) AS min_date, MAX(event_date) AS max_date FROM scored_carts")[0]
    brands = query("""SELECT brand, COUNT(*) AS carts FROM scored_carts
                      WHERE brand <> 'unknown' GROUP BY brand ORDER BY carts DESC LIMIT 200""")
    return {"date_range": rng, "brands": brands}


@app.get("/api/kpis")
def kpis(f=Depends(common_filters)):
    clauses, params = f
    row = query(f"""
        SELECT COUNT(*) AS total_carts,
               AVG(actual_is_abandoned) AS abandonment_rate,
               SUM(price) AS total_cart_value,
               SUM(CASE WHEN actual_is_abandoned = 1 THEN price ELSE 0 END) AS abandoned_value,
               SUM(CASE WHEN risk_band = 'High' THEN 1 ELSE 0 END) AS high_risk_carts,
               SUM(CASE WHEN risk_band = 'Medium' THEN 1 ELSE 0 END) AS medium_risk_carts,
               SUM(CASE WHEN risk_band = 'High' THEN price ELSE 0 END) AS high_risk_value
        FROM scored_carts{where(clauses)}""", params)[0]
    return {k: (v if v is not None else 0) for k, v in row.items()}


@app.get("/api/reasons")
def reasons(f=Depends(common_filters), bands: str = "High,Medium"):
    clauses, params = f
    band_list = parse_bands(bands)
    clauses = clauses + ["main_reason_code <> ''",
                         f"risk_band IN ({','.join('?' * len(band_list))})"]
    rows = query(f"""
        SELECT main_reason_code AS code, COUNT(*) AS carts, SUM(price) AS cart_value
        FROM scored_carts{where(clauses)}
        GROUP BY main_reason_code ORDER BY carts DESC""", params + band_list)
    total = sum(r["carts"] for r in rows) or 1
    return [{**reason_info(r["code"]), "carts": r["carts"],
             "cart_value": r["cart_value"], "share_pct": round(r["carts"] * 100 / total, 1)}
            for r in rows]


def breakdown(dim: str, clauses, params, min_carts: int, limit: int):
    """Per-brand or per-category table with its most common reason among High-risk carts."""
    high_clauses = clauses + ["risk_band = 'High'", "main_reason_code <> ''"]
    sql = f"""
        WITH stats AS (
            SELECT {dim} AS name, COUNT(*) AS carts,
                   AVG(actual_is_abandoned) AS abandonment_rate,
                   SUM(CASE WHEN risk_band = 'High' THEN 1 ELSE 0 END) AS high_risk_carts,
                   SUM(CASE WHEN risk_band = 'High' THEN price ELSE 0 END) AS revenue_at_risk
            FROM scored_carts{where(clauses)}
            GROUP BY {dim} HAVING COUNT(*) >= ?
        ), top_reason AS (
            SELECT {dim} AS name, main_reason_code AS code,
                   ROW_NUMBER() OVER (PARTITION BY {dim} ORDER BY COUNT(*) DESC) AS rn
            FROM scored_carts{where(high_clauses)}
            GROUP BY {dim}, main_reason_code
        )
        SELECT s.name, s.carts, s.abandonment_rate, s.high_risk_carts,
               s.revenue_at_risk, r.code AS top_reason_code
        FROM stats s LEFT JOIN top_reason r ON r.name = s.name AND r.rn = 1
        ORDER BY s.revenue_at_risk DESC LIMIT ?"""
    rows = query(sql, params + [min_carts] + params + [limit])
    for r in rows:
        r["top_reason"] = reason_info(r.pop("top_reason_code"))
    return rows


@app.get("/api/brands")
def brands(f=Depends(common_filters), min_carts: int = 50,
           limit: int = Query(50, le=500), include_unknown: bool = False):
    clauses, params = f
    if not include_unknown:
        clauses = clauses + ["brand <> 'unknown'"]
    return breakdown("brand", clauses, params, min_carts, limit)


@app.get("/api/categories")
def categories(f=Depends(common_filters), min_carts: int = 50, limit: int = Query(50, le=500)):
    clauses, params = f
    return breakdown("category_id", clauses, params, min_carts, limit)


@app.get("/api/carts/at-risk")
def at_risk_carts(f=Depends(common_filters), bands: str = "High",
                  sort: str = Query("risk", pattern="^(risk|value)$"),
                  limit: int = Query(25, le=200), offset: int = 0):
    clauses, params = f
    band_list = parse_bands(bands)
    clauses = clauses + [f"risk_band IN ({','.join('?' * len(band_list))})"]
    params = params + band_list
    order = {"risk": "risk_score DESC", "value": "price DESC"}[sort]
    total = query(f"SELECT COUNT(*) AS n FROM scored_carts{where(clauses)}", params)[0]["n"]
    rows = query(f"""
        SELECT row_id, user_id, product_id, category_id, brand, price, event_time,
               risk_band, risk_score, reason_1, reason_2, reason_3
        FROM scored_carts{where(clauses)} ORDER BY {order} LIMIT ? OFFSET ?""",
        params + [limit, offset])
    for r in rows:
        r["reasons"] = [reason_info(r.pop(k)) for k in ("reason_1", "reason_2", "reason_3")
                        if r[k]]
    return {"total": total, "items": rows}


@app.get("/api/trends")
def trends(f=Depends(common_filters)):
    clauses, params = f
    return query(f"""
        SELECT event_date AS date, COUNT(*) AS carts,
               AVG(actual_is_abandoned) AS abandonment_rate,
               SUM(CASE WHEN risk_band = 'High' THEN 1 ELSE 0 END) AS high_risk_carts,
               SUM(CASE WHEN risk_band = 'High' THEN price ELSE 0 END) AS revenue_at_risk
        FROM scored_carts{where(clauses)}
        GROUP BY event_date ORDER BY event_date""", params)