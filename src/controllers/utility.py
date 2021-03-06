import os
import shutil


def remove_tempdir_contents() -> None:
    """
    Remove all temporary files from temp folder
    """
    for root, dirs, files in os.walk('temp'):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
