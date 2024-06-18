def sounds(key):
    key = key
    address= 'sounds/notes/key-' + key
    fileType= '.mp3'
    sounds_mapping={
        1: address + "/1" + fileType,
        2: address + "/2" + fileType,
        3: address + "/3" + fileType,
        4: address + "/4" + fileType,
        5: address + "/5" + fileType,
        6: address + "/6" + fileType,
        7: address + "/7" + fileType,
        8: address + "/8" + fileType,
    }
    return sounds_mapping