from fastapi import FastAPI, HTTPException
from graph.workflow import run_workflow
from services.compare_service import compare_tickers
from storage.report_store import list_reports, read_report
from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="AI Financial Market Research API"
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/analyze/{ticker}")
def analyze_ticker(ticker: str):

    try:
        return run_workflow(ticker.upper())

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.get("/api/compare")
def compare(ticker_a: str, ticker_b: str):

    try:
        return compare_tickers(
            ticker_a.upper(),
            ticker_b.upper()
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Comparison failed: {str(e)}"
        )
    

@app.get("/api/reports")
def get_reports():
    return {
        "reports": list_reports()
    }


@app.get("/api/reports/{filename}")
def get_report(filename: str):
    try:
        return read_report(filename)

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )