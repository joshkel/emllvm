import os.path
from urllib.request import urlopen

def download(url, file_name=None, block_size=8192):
    """Downloads a file over HTTP.

    Based on http://stackoverflow.com/a/22776/25507."""
    if not file_name:
        file_name = url.split('/')[-1]
    u = urlopen(url)
    with open(file_name, 'wb') as f:
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.get_all("Content-Length")[0])
        print("Downloading %s (%s bytes)" % (os.path.basename(file_name), file_size))

        file_size_dl = 0
        while True:
            buffer = u.read(block_size)
            if not buffer:
                return

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%6.2f%%]" % (file_size_dl, file_size_dl * 100 / file_size)
            print(status, end='\r')

