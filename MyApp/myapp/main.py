from fastapi import FastAPI
from .routers import login, user, map, point, template, feedback
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(docs_url="/")

# origins = [
#     "https://my-app.netlify.app",   # Domain Frontend
#     "http://localhost:8100",        # Ionic local
# ]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,  # or ["*"] for test
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)
app.include_router(map.router)
app.include_router(user.router)
app.include_router(point.router)
app.include_router(template.router)
app.include_router(feedback.router)
