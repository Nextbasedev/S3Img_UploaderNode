import ast

class Listmerger:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "urls1": ("STRING", {"forceInput": True}),
                "urls2": ("STRING", {"forceInput": True})
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "merge_urls"
    CATEGORY = "text"

    def merge_urls(self, urls1, urls2):
        try:
            # Parse input strings as lists
            list1 = ast.literal_eval(urls1)
            list2 = ast.literal_eval(urls2)
            
            # Ensure both are lists
            if not isinstance(list1, list):
                list1 = [list1]
            if not isinstance(list2, list):
                list2 = [list2]
            
            # Merge lists
            merged_urls = list1 + list2
            
            # Remove duplicates while preserving order
            merged_urls = list(dict.fromkeys(merged_urls))
            
            # Return the merged list as a string
            return (str(merged_urls),)
        
        except Exception as e:
            return (f"Error: {str(e)}",)

NODE_CLASS_MAPPINGS = {
    "Listmerger": Listmerger
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShowTextMerger": "Show Text Merger"
}