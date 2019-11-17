import json
import utils

class Base():
    """Base class of model.

    Suitable for JSON base data.
    """

    def __init__(self, **kwargs):
        pass

    def as_json_string(self):
        """Return JSON string from this object.

        :rtype: str
        :return:
        """
        return json.dumps(self.as_json_dict(), sort_keys=True)

    def as_json_dict(self):
        """Return dictionary from this object.

        :return: dict
        """
        data = {}
        for key, value in self.__dict__.items():
            camel_key = utils.to_camel_case(key)
            if isinstance(value, (list, tuple, set)):
                data[camel_key] = list()
                for item in value:
                    if hasattr(item, 'as_json_dict'):
                        data[camel_key].append(item.as_json_dict())
                    else:
                        data[camel_key].append(item)

            elif hasattr(value, 'as_json_dict'):
                data[camel_key] = value.as_json_dict()
            elif value is not None:
                data[camel_key] = value

        return data

    @classmethod
    def new_from_json_dict(cls, data):
        """Create a new instance from a dict.

        :param data: JSON dict
        :rtype:
        :return:
        """
        new_data = {utils.to_snake_case(key): value
                    for key, value in data.items()}
        return cls(**new_data)

    @staticmethod
    def get_or_new_from_json_dict(data, cls):
        """Get `cls` object w/ deserialization from json if needed.

        If data is instance of cls, return data.
        Else if data is instance of dict, create instance from dict.
        Else, return None.

        :param data:
        :param cls:
        :rtype: object
        :return:
        """
        if isinstance(data, cls):
            return data
        elif isinstance(data, dict):
            return cls.new_from_json_dict(data)

        return None

    @staticmethod
    def get_or_new_from_json_dict_with_types(
            data, cls_map, type_key='type'
    ):

        if isinstance(data, tuple(cls_map.values())):
            return data
        elif isinstance(data, dict):
            type_val = data[type_key]
            if type_val in cls_map:
                return cls_map[type_val].new_from_json_dict(data)

        return None
