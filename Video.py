import yt_dlp

def download_media_from_url(url):
    try:
        # 设置下载选项，确保下载并合并音视频流
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # 下载最佳视频和最佳音频，并合并
            'outtmpl': '%(title)s.%(ext)s',         # 设置输出文件名
            'noplaylist': True,                     # 只下载单个视频，避免下载整个专辑
            'quiet': False,                         # 显示下载进度
            'ffmpeg_location': r'G:\Program Files\ffmpeg-master-latest-win64-gpl-shared\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe',  # 手动指定 ffmpeg 路径
            'merge_output_format': 'mp4',  # 确保输出格式为 mp4，这样可以确保音视频合并
        }

        # 使用 yt-dlp 下载视频
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])  # 下载链接
            print("下载完成！")

    except Exception as e:
        print(f"下载失败，错误: {e}")

if __name__ == '__main__':
    # 获取用户输入的链接
    url = input("请输入 Instagram 分享链接: ")
    
    # 调用下载函数
    download_media_from_url(url)
