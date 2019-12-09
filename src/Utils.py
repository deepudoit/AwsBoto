import os
import io
from zipfile import ZipFile


class Utils:
    @staticmethod
    def make_zip_filebytes(path):
        buff = io.BytesIO()
        with ZipFile(buff, 'w') as z:
            for full_path, archive_name in Utils.make_zip(path):
                z.write(full_path, archive_name)
        return buff.getvalue()

    @staticmethod
    def make_zip(path):
        for root, dirs, files in os.walk(path):
            for f in files:
                full_path = os.path.join(root, f)
                archive_name = full_path[len(path) + len(os.sep):]
                yield full_path, archive_name
