from google.protobuf.pyext._message import (
    RepeatedScalarContainer,
    RepeatedCompositeContainer,
    )


def message_to_json(message):
    """
    Convert Message data to json
    ---
        message: Grpc Message Object
    """
    data = {}
    for field_name in dir(message):
        if not field_name.endswith('_FIELD_NUMBER'):
            continue
        field_alias = field_name.split('_FIELD_NUMBER')[0]
        field_alias = field_alias.lower()
        value = getattr(message, field_alias)
        if type(value) in [float, bool, int, str]:
            data[field_alias] = value
        elif type(value) in [RepeatedScalarContainer,
                             RepeatedCompositeContainer]:
            value_list = []
            for val in value:
                if type(val) in [float, bool, int, str]:
                    value_list.append(val)
                else:
                    value_list.append(message_to_json(val))
            data[field_alias] = value_list
        else:
            data[field_alias] = message_to_json(value)
    return data
