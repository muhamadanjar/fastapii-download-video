import yt_dlp
from app.worker import celery_app


@celery_app.task(bind=True)
def download_video(self, video_url: str):
    """Tugas Celery untuk mengunduh video dengan progres"""

    def progress_hook(d):
        if d['status'] == 'downloading':
            self.update_state(
                state='PROGRESS',
                meta={
                    'progress': d.get('_percent_str', '0%').strip(),
                    'speed': d.get('_speed_str', '0B/s').strip(),
                    'eta': d.get('_eta_str', 'N/A').strip(),
                }
            )

    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'progress_hooks': [progress_hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return {"status": "completed", "file": "downloads/filename.mp4"}
    except Exception as e:
        return {"status": "error", "error": str(e)}