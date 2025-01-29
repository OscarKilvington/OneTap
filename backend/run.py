import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=51692,
        reload=True,
        ws_ping_interval=None,
        ws_ping_timeout=None
    )