import uuid

def get_random_id():
    code = str(uuid.uuid5())[:8].replace('-','').lower()

    return code
