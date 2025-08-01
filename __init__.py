from .s3_uploader_node import S3ImgUploaderNode
from .randomint import UniqueRandomIntGenerator
from .showtextmerger import ShowTextMerger
from .URLListAppender import Listmerger
from .mask_region_node import MaskRegionNode
from .imageinfo import ImageInfo

from .stringconditioning import StringCondition
from .humandetect import HumanDetectionNode
from .maskbatchcombiner import MaskBatchCombiner
from .listcheker import ListInputNode
from .conditionchecker import StringConditionalNode
from .boolconditionTF import BoolConditionTF
from .s3_uploader_node_nameip import S3ImgUploaderNodeImageNamePrefix
from .imagebackmask import ImageBackMask
from .test_node import test_node
from .just_printnode import PrintNode
from .maskpasser import MaskPasser
from .boxmask_node import BoxMaskNode
from .ImageRemovePadding import ImageRemovePadding
from .image_watermark import CUSTOM_OverlayTransparentImage
from .load_img_fromurl import UtilLoadImageFromUrlss
from .showtext import ShowTextss
from .upload_video_to_s3.py import upload_video_to_s3
NODE_CLASS_MAPPINGS = {
    "upload_video_to_s3": upload_video_to_s3
    "S3ImgUploaderNode": S3ImgUploaderNode,
    "UniqueRandomIntGenerator": UniqueRandomIntGenerator,
    "ShowTextMerger": ShowTextMerger,
    "Listmerger": Listmerger,
    "MaskRegionNode": MaskRegionNode,
    "ImageInfo": ImageInfo,
    "StringCondition": StringCondition,
    "HumanDetectionNode": HumanDetectionNode,
    "MaskBatchCombiner": MaskBatchCombiner,
    "ListInputNode": ListInputNode,
    "StringConditionalNode": StringConditionalNode,
    "BoolConditionTF": BoolConditionTF,
    "S3ImgUploaderNodeImageNamePrefix": S3ImgUploaderNodeImageNamePrefix,
    "ImageBackMask": ImageBackMask,
    "test_node": test_node,
    "PrintNode": PrintNode,
    "MaskPasser": MaskPasser,
    "BoxMaskNode": BoxMaskNode,
    "ImageRemovePaddingss":ImageRemovePadding,
    "CUSTOM_OverlayTransparentImage":CUSTOM_OverlayTransparentImage,
    "UtilLoadImageFromUrlss":UtilLoadImageFromUrlss,
    "ShowTextss":ShowTextss
    }

NODE_DISPLAY_NAME_MAPPINGS = {
    "upload_video_to_s3": "Upload Video Files to S3"
}
