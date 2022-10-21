from pydantic import BaseModel


class InfoBbox(BaseModel):
    masked: int = None
    prob_masked: float = None
    bbox: list = None


def convert_output_2jsondumps(bbox_infos):
    list_info_bbox = []
    for bbox_info in bbox_infos:
        masked, prob_masked, bbox = bbox_info[0], bbox_info[1], bbox_info[2:]
        info_box = InfoBbox(masked=masked, prob_masked=prob_masked, bbox=bbox)
        list_info_bbox.append(info_box.__dict__)
    return list_info_bbox
