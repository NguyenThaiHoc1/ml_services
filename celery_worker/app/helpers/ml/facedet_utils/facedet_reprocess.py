import cv2
import logging
import numpy as np
from PIL import Image
from helpers.ml.facedet_utils import (
    anchor_generator, anchor_decode, nms
)


def preprocess_image(image):
    logging.info("\tPreprocess image ...")
    image = image.resize((260, 260))
    np_array = np.asarray(image)
    np_image_preprocess = np_array.astype(np.float32) / 255.
    np_image_preprocess = np.expand_dims(np_image_preprocess, axis=0)
    logging.info("\tPreprocess image done.")
    return np_image_preprocess


def read_image_from_path_to_numpy(path):
    logging.info("\tReading image ...")
    image = Image.open(path)
    width, height = image.size
    image = image.convert('RGB')
    logging.info("\tReading image done.")
    return image, width, height


def decode_all_boxes(image,
                     y_bboxes_output, y_cls_output,
                     width, height,
                     conf_thresh=0.5,
                     iou_thresh=0.4,
                     target_shape=(160, 160),
                     draw_result=True):
    image = np.asarray(image)
    output_info = []
    feature_map_sizes = [[33, 33], [17, 17], [9, 9], [5, 5], [3, 3]]
    anchor_sizes = [[0.04, 0.056], [0.08, 0.11], [0.16, 0.22], [0.32, 0.45], [0.64, 0.72]]
    anchor_ratios = [[1, 0.62, 0.42]] * 5
    id2class = {0: 'Mask', 1: 'NoMask'}
    anchors = anchor_generator.generate_anchors(feature_map_sizes, anchor_sizes, anchor_ratios)
    anchors_exp = np.expand_dims(anchors, axis=0)

    y_bboxes = anchor_decode.decode_bbox(anchors_exp, y_bboxes_output)[0]
    y_cls = y_cls_output[0]

    # To speed up, do single class NMS, not multiple classes NMS.
    bbox_max_scores = np.max(y_cls, axis=1)
    bbox_max_score_classes = np.argmax(y_cls, axis=1)

    # keep_idx is the alive bounding box after nms.
    keep_idxs = nms.single_class_non_max_suppression(y_bboxes,
                                                     bbox_max_scores,
                                                     conf_thresh=conf_thresh,
                                                     iou_thresh=iou_thresh)
    for idx in keep_idxs:
        conf = float(bbox_max_scores[idx])
        class_id = bbox_max_score_classes[idx]
        bbox = y_bboxes[idx]
        # clip the coordinate, avoid the value exceed the image boundary.
        xmin = max(0, int(bbox[0] * width))
        ymin = max(0, int(bbox[1] * height))
        xmax = min(int(bbox[2] * width), width)
        ymax = min(int(bbox[3] * height), height)

        if draw_result:
            if class_id == 0:
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)
            cv2.putText(image, "%s: %.2f" % (id2class[class_id], conf), (xmin + 2, ymin - 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color)
        output_info.append([class_id, conf, xmin, ymin, xmax, ymax])

    img_output = Image.fromarray(image)
    return output_info, img_output
