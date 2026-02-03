def remove_file_extension(fname: str, fextension: str = None) -> str:
    '''
    Remove the extension of the given filename
    
    :param fname: the name of the file
    :type fname: str
    :param fextension: the extension of the file
    :type fextension: str
    :return: the filename without the extension
    :rtype: str
    '''
    if not fextension:
        index = 0
        for char in fname:
            index += 1
            if char == '.':
                return fname[:-index]
    return fname[:-len(fextension)]