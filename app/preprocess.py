def prepare_input_record(record):
    """
    Takes a raw dictionary of weather parameters from the form,
    converts them to floats, and returns a dictionary of processed features.
    """
    processed = {
        'cloud': float(record.get('cloud', 0.0)),
        'annual': float(record.get('annual', 0.0)),
        'janfeb': float(record.get('janfeb', 0.0)),
        'marmay': float(record.get('marMay', 0.0)),
        'junesep': float(record.get('juneSept', 0.0))
    }
    return processed
