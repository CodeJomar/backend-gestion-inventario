from fastapi.middleware.cors import CORSMiddleware

def configurar_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",  # React local
            "http://127.0.0.1:3000",  # FastAPI local
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)