import inspect
import json


def get_object_info_json(obj):
    """
    获取对象的所有信息并以优化的JSON字符串格式返回

    Args:
        obj (object): 要获取信息的对象

    Returns:
        str: 优化打印的JSON字符串，包含对象所属类的信息、实例属性、方法等信息。如果发生错误，返回包含错误信息的JSON字符串。
    """
    try:
        obj_class = obj.__class__
        class_info = {
            "class_name": obj_class.__name__,
            "module": obj_class.__module__,
            "bases": [],
            "attributes": {},
            "methods": {}
        }

        # 获取基类信息
        try:
            class_info["bases"] = [base.__name__ for base in obj_class.__bases__]
        except Exception as e:
            class_info["bases_error"] = f"Error getting base classes: {str(e)}"

        # 获取实例属性信息
        for attr_name in dir(obj):
            try:
                attr = getattr(obj, attr_name)
                if not callable(attr) and not attr_name.startswith("__"):
                    class_info["attributes"][attr_name] = str(type(attr))
            except Exception as e:
                class_info["attributes_error"] = class_info.get("attributes_error", {})
                class_info["attributes_error"][attr_name] = f"Error getting attribute: {str(e)}"

        # 获取实例方法信息
        for method_name in dir(obj):
            try:
                method = getattr(obj, method_name)
                if callable(method) and not method_name.startswith("__"):
                    method_info = {
                        "signature": str(inspect.signature(method)),
                        "docstring": inspect.getdoc(method)
                    }
                    class_info["methods"][method_name] = method_info
            except Exception as e:
                class_info["methods_error"] = class_info.get("methods_error", {})
                class_info["methods_error"][method_name] = f"Error getting method: {str(e)}"

        # 递归获取基类的信息（如果有）
        for base in obj_class.__bases__:
            try:
                base_info = get_class_info_json(base)
                base_info_json = json.loads(base_info)
                class_info["bases_info"] = class_info.get("bases_info", []) + [base_info_json]
            except Exception as e:
                class_info["bases_info_error"] = class_info.get("bases_info_error", {})
                class_info["bases_info_error"][base.__name__] = f"Error getting base class info: {str(e)}"

        return json.dumps(class_info, indent=4)
    except Exception as e:
        error_info = {
            "error": "An error occurred while getting object info.",
            "message": str(e)
        }
        return json.dumps(error_info, indent=4)


class MyBaseClass:
    base_attr = "Base Attribute"

    def base_method(self):
        """Base method docstring"""
        print("This is a base method.")


class MyClass(MyBaseClass):
    class_attr = "Class Attribute"

    def __init__(self):
        self.instance_attr = "Instance Attribute"

    def my_method(self, x: int) -> int:
        """
        My method docstring

        Args:
            x (int): An integer parameter.

        Returns:
            int: The result.
        """
        return x + 1



if __name__ == "__main__":
    # 调用函数获取类信息的JSON字符串并打印
    class_info_json = get_object_info_json(MyClass)
    print(class_info_json)