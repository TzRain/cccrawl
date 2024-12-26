import os
import torch
from PIL import Image

try:
    from ultralytics import YOLO
    from OmniParser.utils import get_som_labeled_img, check_ocr_box, get_caption_model_processor, get_yolo_model
except:
    print('Please install ultralytics and OmniParser')

from transformers import AutoModelForImageClassification, AutoImageProcessor

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

class OmniParserModel:

    caption_model_dict = {
        "florence2":{
            'model_name': 'florence2',
            'model_path': 'icon_caption_florence',
        },
        "blip2":{
            'model_name': 'blip2',
            'model_path': 'icon_caption_blip2',
        }
    }

    som_model_dict = {
        "icon_detect_v1_5":{
            'model_name': 'icon_detect_v1_5',
            'model_path': 'icon_detect_v1_5/model_v1_5.pt',
        },
        "icon_detect":{
            'model_name': 'icon_detect',
            'model_path': 'icon_detect/model.pt',
        }
    }

    def __init__(
            self,
            som_model='icon_detect_v1_5',
            caption_model='florence2',
            weigth_root = 'OmniParser/weights'
        ):
        self.weigth_root = weigth_root
        self.load_models(som_model,caption_model)

    def load_models(self,som_model,caption_model):
        
        self.som_model = get_yolo_model(os.path.join(self.weigth_root, self.som_model_dict[som_model]['model_path']))
        self.som_model.to(DEVICE)

        self.caption_model_processor = get_caption_model_processor(
            model_name=self.caption_model_dict[caption_model]['model_name'], 
            model_name_or_path=os.path.join(self.weigth_root, self.caption_model_dict[caption_model]['model_path']),
            device=DEVICE
        )

    def process_image(self, image_path, box_threshold=0.05, text_threshold=0.5):

        # image_path = 'imgs/google_page.png'
        # image_path = 'imgs/windows_home.png'
        # # image_path = 'imgs/windows_multitab.png'
        # # image_path = 'imgs/omni3.jpg'
        # # image_path = 'imgs/ios.png'
        # image_path = 'imgs/word.png'
        # # image_path = 'imgs/excel2.png'

        image = Image.open(image_path)
        # image_rgb = image.convert('RGB')

        box_overlay_ratio = max(image.size) / 3200

        draw_bbox_config = {
            'text_scale': 0.8 * box_overlay_ratio,
            'text_thickness': max(int(2 * box_overlay_ratio), 1),
            'text_padding': max(int(3 * box_overlay_ratio), 1),
            'thickness': max(int(3 * box_overlay_ratio), 1),
        }

        ocr_bbox_rslt, is_goal_filtered = check_ocr_box(
            image_path, display_img = False, 
            output_bb_format='xyxy', 
            goal_filtering=None, 
            easyocr_args={'paragraph': False, 'text_threshold': text_threshold}, 
            use_paddleocr=True
        )
        text, ocr_bbox = ocr_bbox_rslt

        dino_labled_img, label_coordinates, parsed_content_list = get_som_labeled_img(
            image_path, self.som_model, BOX_TRESHOLD = box_threshold, 
            output_coord_in_ratio=True, ocr_bbox=ocr_bbox,draw_bbox_config=draw_bbox_config, 
            caption_model_processor=self.caption_model_processor, ocr_text=text,use_local_semantics=True, 
            iou_threshold=0.7, scale_img=False,
        batch_size=128)

        return {
            'dino_labled_img': dino_labled_img,
            'label_coordinates': label_coordinates,
            'parsed_content_list': parsed_content_list,
            'image_size': image.size # (w,h)
        }
# label_coordinates is a list of dictionaries with the following format:
# {
# 'type': 'text',
# 'bbox': [0.17,0.01,0.21,0.03], # [v[0]/w, v[1]/h, v[2]/w, v[3]/h]
# 'interactivity': False,
# 'content': 'storage'
# },


class ScreenshotChecker:
    def __init__(self , device='cpu'):
        print('[ScreenshotChecker] : Loading model...')
        self.model = AutoModelForImageClassification.from_pretrained("al-css/Screenshots_detection_to_classification")
        self.processor = AutoImageProcessor.from_pretrained("openai/clip-vit-base-patch32")
        self.model.to(device)
        self.model.eval()
        print('[ScreenshotChecker] : Model loaded')

    def predict(self,image):
        with torch.no_grad():
            inputs = self.processor(images=image, return_tensors="pt")
            outputs = self.model(**inputs)
            probs = outputs[-1][0]
            return float(probs.softmax(dim=0)[-1])

if __name__ == '__main__':
    model = OmniParserModel()
    image_path = 'imgs/google_page.png'
    dino_labled_img, label_coordinates, parsed_content_list = model.process_image(image_path)
    dino_labled_img.show()
    print(label_coordinates)
    print(parsed_content_list)