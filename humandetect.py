import torch
import clip
from PIL import Image
import numpy as np

class HumanDetectionNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "detect_human"
    CATEGORY = "image/analysis"

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device, download_root="/clip")

        # Improved set of text descriptions for better detection
        # self.text_descriptions = [
        #     "a photo of a full person with face and body visible",
        #     "a photo showing only a single hand or arm",
        #     "a close-up of just a hand",
        #     "only fingers visible",
        #     "a close-up of a hand holding something",
        # ]
        self.text_descriptions = [
        "a photo of a person",
        "a photo of a full person with face and body visible",
        "a photo of a person's upper body",
        "a photo showing only a hand",
        "a close-up of just a hand",
        "a photo without any people",
            ]
        self.text_tokens = clip.tokenize(self.text_descriptions).to(self.device)

    def detect_human(self, image):
        try:
            # Convert image tensor to numpy
            img_np = (image * 255).byte().cpu().numpy()[0]

            if img_np.size == 0 or 0 in img_np.shape:
                return ("False during image validation",)

            # Convert numpy to PIL image
            pil_image = Image.fromarray(img_np)

            # Preprocess and run through model
            image_input = self.preprocess(pil_image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                image_features = self.model.encode_image(image_input)
                text_features = self.model.encode_text(self.text_tokens)

                similarities = (100.0 * image_features @ text_features.T)
                probs = similarities.softmax(dim=-1)

                # Optionally: print similarity scores
                print("\n--- Similarity Scores ---")
                for desc, score in zip(self.text_descriptions, probs[0]):
                    print(f"{desc:<55} : {score.item():.4f}")
                print("--------------------------")

                top_index = probs[0].argmax().item()
                top_desc = self.text_descriptions[top_index]

                # is_person = (top_index == 0)
                is_person = top_index in [0, 1, 2]  # any human-like prompt
                print(f"Predicted: {top_desc} | Human detected: {is_person}")
                if is_person:
                    return (True,)
                else:
                    return (False,)

        except Exception as e:
            print("Error during detection:", e)
            return (False,)

# Registering node with ComfyUI
NODE_CLASS_MAPPINGS = {
    "HumanDetectionNode": HumanDetectionNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "HumanDetectionNode": "Human Detection Node"
}
