import os
from cv2 import cv2
import mimetypes
from typing import List


def get_images_in_a_directory(filepath: str) -> List[str]:
    """pass in a filepath to get a sorted list of images in a dir

    Args:
        filepath (str): path to images

    Returns:
        List[str]: sorted list of image files
    """
    all_files = os.listdir(filepath)
    files = []
    for f in all_files:
        if os.path.isfile(os.path.join(filepath, f)):
            datatype = mimetypes.guess_type(f)
            if datatype[0] is not None:
                if datatype[0][:5] == "image":
                    files.append(os.path.join(filepath, f))
    return sorted(files)

def make_movie(filepath: str, moviename="video", fps=25.0) -> str:
    """Make a movie from a bunch of images in a folder!

    Args:
        filepath (String): Pass in the file path where the images are.
                            JPEGs work for sure, any image should do.
        fps (float, optional): Frames per seconds. Higher values make
                            for faster videos. Defaults to 25.0.
        moviename (string, optional): pass in the new file path name for
                            newly generated movie, which will be placed
                            in the same path as the images. If specifying
                            the moviename, include the .mp4 extension.

    Returns:
        str: name of new movie file
    """
    image_files = get_images_in_a_directory(filepath)
    images = []
    for img in image_files:
        images.append(cv2.imread(img))
    height, width, layers = images[1].shape #noqa

    if moviename == "video":
        # Default value, just append to the image path
        outputvid = os.path.join(filepath, f"{moviename}.mp4")
    else:
        # TODO: check to ensure we have a valid, writeable path
        outputvid = moviename

    # Set an encoding so we don't have an enormous output file
    # to skip compression, set fourcc to 0
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    video = cv2.VideoWriter(
        outputvid, fourcc, fps, (width, height)
    )

    for img in images:
        video.write(img)
    cv2.destroyAllWindows()
    video.release()
    return outputvid
