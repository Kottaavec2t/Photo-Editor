def remove_file_extension(fname: str, fextension: str = None) -> str:
    '''
    Remove the extension of the given filename.

    :param fname: The name of the file.
    :type fname: str
    :param fextension: The extension of the file.
    :type fextension: str
    :return: The filename without the extension.
    :rtype: str
    '''
    if not fextension:
        for i, char in enumerate(fname):
            if char == '.':
                return fname[:-i]
    return fname[:-len(fextension)]
