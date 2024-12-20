from fastapi import FastAPI, BackgroundTasks, HTTPException


import yt_dlp

app = FastAPI()

def download_video(video_url: str, output_path: str = 'downloads/'):
    """Fungsi untuk mengunduh video dari YouTube, Instagram, atau LinkedIn"""
    ydl_opts = {
        'outtmpl': f'{output_path}%(title)s.%(ext)s',  # Menyimpan file di folder downloads/
        'format': 'bestvideo+bestaudio/best',  # Mengunduh video dan audio dengan kualitas terbaik
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"✅ Video dari {video_url} berhasil diunduh ke folder '{output_path}'")
    except Exception as e:
        print(f"❌ Gagal mengunduh video dari {video_url}: {e}")

@app.post("/download/")
async def download_video_endpoint(video_url: str, background_tasks: BackgroundTasks):
    """
    Endpoint API untuk mengunduh video dari URL.
    Mendukung YouTube, Instagram, dan LinkedIn menggunakan yt-dlp.
    """
    # Validasi URL hanya menerima URL dari YouTube, Instagram, dan LinkedIn
    supported_platforms = ['youtube.com', 'youtu.be', 'instagram.com', 'linkedin.com']
    if not any(platform in video_url for platform in supported_platforms):
        raise HTTPException(status_code=400, detail="URL tidak didukung. Hanya mendukung YouTube, Instagram, dan LinkedIn.")
    
    # Tambahkan unduhan ke background task
    background_tasks.add_task(download_video, video_url)
    
    return {"message": f"Pengunduhan video dari {video_url} dimulai. Periksa folder 'downloads/'."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8070)
