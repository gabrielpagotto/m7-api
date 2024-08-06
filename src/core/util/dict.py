import re


def camel_to_snake(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def convert_dict_keys_to_snake_case(data):
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            new_key = camel_to_snake(key)
            new_dict[new_key] = convert_dict_keys_to_snake_case(value) if isinstance(value, (dict, list)) else value
        return new_dict
    elif isinstance(data, list):
        return [convert_dict_keys_to_snake_case(item) for item in data]
    else:
        return data
