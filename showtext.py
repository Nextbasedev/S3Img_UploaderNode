class ShowTextss:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            }
        }
    
    INPUT_IS_LIST = True
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "show_value"
    CATEGORY = "showtext"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True,)

    def show_value(self, text):
        print(f"show text: {text}")
        return {"ui": {"text": text}, "result": (text,)}

