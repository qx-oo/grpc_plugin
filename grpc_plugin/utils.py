
def message_to_json(message):
    data = {}
    for field_name in dir(message):
        if not field_name.endswith('_FIELD_NUMBER'):
            continue
        field_alias = field_name.split('_FIELD_NUMBER')[0]
        field_alias = field_alias.lower()
        value = getattr(message, field_alias)
        if type(value) in [float, bool, int, str]:
            data[field_alias] = value
        else:
            data[field_alias] = message_to_json(value)
    return data
