from fastapi import FastAPI, HTTPException, Request
from celery.result import AsyncResult
from app.tasks import download_video


app = FastAPI()


@app.post("/download/")
async def download_video_endpoint(request: Request):
    body = await request.json()
    print(body)
    video_url = body.get('video_url')
    print("video url", video_url)
    supported_platforms = ['youtube.com', 'instagram.com', 'linkedin.com']
    if not any(platform in video_url for platform in supported_platforms):
        raise HTTPException(status_code=400, detail="URL tidak didukung.")
    try: 
        task = download_video.apply_async(args=[video_url],)
        return {"task_id": task.id, "message": "Pengunduhan dimulai."}
    except Exception as e:
        print(e)    


@app.get("/progress/{task_id}")
async def get_progress(task_id: str):
    """Endpoint untuk memeriksa progres pengunduhan"""
    task_result = AsyncResult(task_id)
    if task_result.state == 'PENDING':
        return {"status": "pending", "progress": "0%"}
    elif task_result.state == 'PROGRESS':
        return {"status": "in_progress", **task_result.info}
    elif task_result.state == 'SUCCESS':
        return {"status": "completed", "result": task_result.result}
    elif task_result.state == 'FAILURE':
        return {"status": "failed", "error": str(task_result.result)}
    else:
        return {"status": task_result.state}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8070)
