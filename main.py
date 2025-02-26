from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import slide
app = FastAPI(openapi_url="/openapi.json", docs_url="/docs", redoc_url="/redoc")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the powerpoint API"}

# Thêm middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(slide.router, prefix="/api/slide")
if __name__ == '__main__':
    app.run(debug=True)