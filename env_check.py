import subprocess

def check_ffmpeg():
    """If ffmpeg is installed, return the version"""
    try:
        res = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # ffmpeg is installed
        if res.returncode == 0:
            version_line = res.stdout.splitlines()[0]
            version = version_line.split()[2]
            return version
    except FileNotFoundError:
        print('ERROR: ffmpeg is not installed')
        return None
    return None