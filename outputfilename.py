import os


def get_output_filename(threshold, filename):
    """
    Creates the appropriate folder and return appropriate file-path for given occurrence threshold and filename
    :param threshold: occurrence threshold
    :param filename: filename
    :return: file-path (also, create folders as needed)
    """

    file_path = 'output/' + str(threshold) + '/' + filename
    directory = os.path.dirname(file_path)

    try:
        os.stat(directory)
    except OSError:
        os.mkdir(directory)

    return file_path
