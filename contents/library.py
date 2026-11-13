from IPython.display import HTML, IFrame
from pathlib import Path
import warnings, os

def style_notebook():
    if os.getenv('JUPYTER_UI') is not None:
        if os.environ['JUPYTER_UI'] != '/lab':
            style = Path(__file__).with_name("style.css").read_text(encoding="utf-8")
            return HTML(style)

def show_video_file(url,width,height):
    return HTML(f'<video width="{width}" height="{height}" controls><source src="{url}" type="video/mp4"></video>')

def show_youtube(url, width, height):
    return IFrame(url,width,height)

def play_mp3(file):
    return HTML('<audio src="'+file+'" controls><p>If you are reading this, it is because your browser does not support the audio element</p></audio>')

def play_mp4(file, width, height):
    return HTML("<video width='"+str(width)+"' height='"+str(height)+"' controls><source src='"+file+"' type='video/mp4'>Your browser does not support HTML5 video.</video>")

warnings.filterwarnings('ignore')
