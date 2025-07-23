class ListInputNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_list": ("LIST", {"default": []}),
            }
        }
    
    RETURN_TYPES = ("LIST",)
    FUNCTION = "process_list"
    CATEGORY = "custom/list_operations"

    def process_list(self, input_list):
        print(f"input_list: {input_list}")
        return (input_list,)