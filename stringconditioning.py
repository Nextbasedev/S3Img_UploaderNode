class StringCondition:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(self):
        string_condition_list = ["include", "exclude",]
        return {"required": {
                "text": ("STRING", {"multiline": False}),
                "condition": (string_condition_list,),
                "sub_string": ("STRING", {"multiline": False}),
            },}

    RETURN_TYPES = ("BOOLEAN", "STRING",)
    RETURN_NAMES = ("output", "string",)
    FUNCTION = 'string_condition'
    CATEGORY = 'String'

    def string_condition(self, text, condition, sub_string):
        ret = False
        if condition == "include":
            ret = sub_string in text
        if condition == "exclude":
            ret = sub_string not in text
        return (ret, str(ret))

NODE_CLASS_MAPPINGS = {
    "StringCondition": StringCondition
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "StringCondition": "StringCondition"
}

