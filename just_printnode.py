class PrintNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "message": ("STRING", {"default": "Hello World"})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "print_message"
    CATEGORY = "utils"

    def print_message(self, message):
        print(message)
        return (message,)

# This is important for ComfyUI to recognize and register the node
NODE_CLASS_MAPPINGS = {
    "PrintNode": PrintNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PrintNode": "Print Message"
}
