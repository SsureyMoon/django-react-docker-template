from rest_framework.exceptions import ValidationError


def serializer_factory(serializer_class, conversion_map, data, many=False, extra=None):
    if extra is None:
        extra = dict()

    if many:
        results = []
        for each_data in data:
            results.append(serializer_factory(serializer_class, conversion_map, each_data, False, extra))  # recursive call
        return results

    else:
        result = dict()
        _errors = []
        for key in data:
            if key in conversion_map and data.get(key):

                field = conversion_map[key][0]
                value = data[key]
                if conversion_map[key][1]:
                    value = conversion_map[key][1](value)
                    if type(value) is ValidationError:
                        _errors.append((field, value))
                result[field] = value
        serializer = serializer_class(data=dict(result, **extra))
        for error in _errors:
            serializer.fields[error[0]].error_messages.update({'custom': error[1]})
        return serializer
