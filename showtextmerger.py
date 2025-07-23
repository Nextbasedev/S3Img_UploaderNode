class ShowTextMerger:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "urls1": ("STRING", {"forceInput": True}),
                "urls2": ("STRING", {"forceInput": True}),
                "name": ("STRING", {"default": "DefaultFolder2"})
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "merge_urls"
    CATEGORY = "text"
    def merge_urls(self, urls1, urls2,name):
        try:
            # Combine the URLs into a single list
            merged_urls = [urls1, urls2]
            
            # Flatten the list if needed
            flattened_urls = [url for sublist in merged_urls for url in (sublist if isinstance(sublist, list) else [sublist])]
            
            # Return the flattened list as a string
            # result = {'final_output': flattened_urls}
            result = {
            "ui": {f"{name}": flattened_urls},
            "result": (flattened_urls,)
            # "result": (object_keys,)
            }

            return result
            # return (str(flattened_urls),)
            
        except Exception as e:
            return (f"Error: {str(e)}",)

NODE_CLASS_MAPPINGS = {
    "ShowTextMerger": ShowTextMerger
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShowTextMerger": "Show Text Merger"
}