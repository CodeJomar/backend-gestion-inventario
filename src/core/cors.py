from fastapi.middleware.cors import CORSMiddleware

def configurar_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",  # React local
            "http://127.0.0.1:5173",  # FastAPI local
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)