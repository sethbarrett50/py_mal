import io

import mss

from PIL import Image


class ScreenHandler:
    def get_frame(self, quality: int = 60) -> bytes:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)

            img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=quality)
            return buffer.getvalue()
