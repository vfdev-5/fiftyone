class BaseType:
    def __init__(self):
        pass

    def to_json(self):
        return {
            "name": self.__class__.__name__,
        }


class Object(BaseType):
    def __init__(self, **kwargs):
        self.properties = {}
        self._needsResolution = False

    def add_property(self, name, property):
        self.properties[name] = property
        return property

    def get_property(self, name):
        return self.properties.get(name, None)

    def define_property(self, name, type, **kwargs):
        label = kwargs.get("label", None)
        description = kwargs.get("description", None)
        view = kwargs.get("view", None)
        if view is None:
            view = View()
        else:
            view = view.clone()
        if label is not None:
            view.label = label
        if description is not None:
            view.description = description
        args = {**kwargs, "view": view}
        property = Property(type, **args)
        self.add_property(name, property)
        return property

    def str(self, name, **kwargs):
        return self.define_property(name, String(), **kwargs)

    def bool(self, name, **kwargs):
        return self.define_property(name, Boolean(), **kwargs)

    def int(self, name, **kwargs):
        return self.define_property(name, Number(int=True), **kwargs)

    def float(self, name, **kwargs):
        return self.define_property(name, Number(float=True), **kwargs)

    def enum(self, name, choices, **kwargs):
        return self.define_property(name, Enum(choices), **kwargs)

    def list(self, name, element_type, **kwargs):
        return self.define_property(name, List(element_type), **kwargs)

    def to_json(self):
        # convert properties to json
        properties = {}
        for name, property in self.properties.items():
            properties[name] = property.to_json()
        return {
            "name": self.__class__.__name__,
            "properties": properties,
            "needsResolution": self._needsResolution,
        }

    def dynamic(self):
        self._needsResolution = True


class Property(BaseType):
    def __init__(self, type, **kwargs):
        self.type = type
        invalid_descendants = self.has_invalid_descendants()
        self.invalid = kwargs.get("invalid", invalid_descendants)
        self.default = kwargs.get("default", None)
        self.required = kwargs.get("required", False)
        self.choices = kwargs.get("choices", None)
        self.error_message = kwargs.get("error_message", "Invalid")
        self.view = kwargs.get("view", None)

    def has_invalid_descendants(self):
        if isinstance(self.type, Object):
            for property in self.type.properties.values():
                if property.invalid or property.has_invalid_descendants():
                    return True
        return False

    def to_json(self):
        return {
            "type": self.type.to_json(),
            "default": self.default,
            "required": self.required,
            "choices": self.choices,
            "view": self.view.to_json() if self.view else None,
        }


class String(BaseType):
    def __init__(self):
        pass


class Boolean(BaseType):
    def __init__(self):
        pass


class Number(BaseType):
    def __init__(self, min=None, max=None, int=False, float=False):
        self.min = min
        self.max = max
        self.int = int

    def to_json(self):
        return {
            "name": self.__class__.__name__,
            "min": self.min,
            "max": self.max,
            "int": self.int,
        }


class List(BaseType):
    def __init__(self, element_type, min_items=None, max_items=None):
        self.element_type = element_type
        self.min_items = min_items
        self.max_items = max_items

    def to_json(self):
        return {
            "name": self.__class__.__name__,
            "element_type": self.element_type.to_json(),
            "min_items": self.min_items,
            "max_items": self.max_items,
        }


class SampleID(String):
    def __init__(self):
        pass


class Enum(BaseType):
    def __init__(self, values):
        self.values = values

    def to_json(self):
        return {"name": self.__class__.__name__, "values": self.values}


class Plot(BaseType):
    def __init__(self, **kwargs):
        self.title = kwargs.get("title", None)
        self.description = kwargs.get("description", None)
        self.caption = kwargs.get("caption", None)
        self.space = kwargs.get("space", None)

    def to_json(self):
        return {"name": self.__class__.__name__, "values": self.values}


#
# Trigger
#


class Trigger(BaseType):
    def __init__(self, operator, params=None):
        self.operator = operator
        self.params = params

    def to_json(self):
        return {
            "name": self.__class__.__name__,
            "operator": self.operator,
            "params": self.params,
        }


#
# Views
#


class View:
    def __init__(self, **kwargs):
        self.label = kwargs.get("label", None)
        self.description = kwargs.get("description", None)
        self.caption = kwargs.get("caption", None)
        self.space = kwargs.get("space", None)
        self._kwargs = kwargs

    def clone(self):
        return self.__class__(**self._kwargs)

    def to_json(self):
        return {
            "name": self.__class__.__name__,
            "label": self.label,
            "description": self.description,
            "caption": self.caption,
            "space": self.space,
        }


class Choice(View):
    def __init__(self, value, **kwargs):
        super().__init__(**kwargs)
        self.value = value

    def clone(self):
        clone = Choice(self.value, **self._kwargs)
        return clone

    def to_json(self):
        return {**super().to_json(), "value": self.value}


class Choices(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.choices = kwargs.get("choices", [])

    def values(self):
        return [choice.value for choice in self.choices]

    def add_choice(self, value, **kwargs):
        choice = Choice(value, **kwargs)
        self.choices.append(choice)
        return choice

    def clone(self):
        clone = super().clone()
        clone.choices = [choice.clone() for choice in self.choices]
        return clone

    def to_json(self):
        return {
            **super().to_json(),
            "name": self.__class__.__name__,
            "choices": [choice.to_json() for choice in self.choices]
            # "choices": self.choices,
        }


class RadioGroup(Choices):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Dropdown(Choices):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Notice(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Header(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Warning(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Button(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)