""" DataGenerator
"""

## add SynthDet related python files path to system path
import sys
import os
module_path = os.path.dirname(os.path.abspath(__file__))
sys_path_list = []
for p in sys.path:
    sys_path_list.append(p)
if module_path not in sys_path_list:
    sys.path.append(module_path)
## prevent create __pycache__ file
sys.dont_write_bytecode = True

import bpy 
from SegmentSDG_000_Initializer import Initializer
from SegmentSDG_010_SceneGenerateRandomizer import SceneGenerateRandomizer
from SegmentSDG_020_TableTextureRandomizer import TableTextureRandomizer
from segmentSDG_030_LightRandomizer import LightRandomizer
from SegmentSDG_040_CameraPoseRandomizer import CameraPoseRandomizer
from SegmentSDG_050_CameraEffectRandomizer import CameraEffectRandomizer
from SegmentSDG_100_YOLOSegmentLabeler import YoloSegmentLabeler
from SegmentSDG_200_Parameter import Parameter

class DataGenerator:

    def gen_one_data(self):
        """
        main data generate flow
        """ 
        ## blender env init
        initializer = Initializer()
        parameter = Parameter()
        initializer.camera_focal_length = parameter.camera_focal_length
        initializer.camera_sensor_width = parameter.camera_sensor_width
        initializer.img_resolution_x = parameter.img_resolution_x
        initializer.img_resolution_y = parameter.img_resolution_y
        initializer.cycle_samples = parameter.cycle_sample
        initializer.init()
        
        ## scene generate
        scene_generate_randomizer = SceneGenerateRandomizer()
        scene_generate_randomizer.asset_board_folder_path = parameter.asset_board_folder_path # passing params
        scene_generate_randomizer.asset_table_folder_path = parameter.asset_table_folder_path
        scene_generate_randomizer.borad_placement_area = parameter.borad_placement_area
        scene_generate_randomizer.scene_generate()

        ## table texture randomize
        table_texture_randomizer = TableTextureRandomizer()
        table_texture_randomizer.asset_table_texture_folder_path = parameter.asset_table_texture_folder_path # passing params
        table_texture_randomizer.texture_scale_range = parameter.texture_scale_range
        table_texture_randomizer.table_texture_randomize()

        ## light randomize
        light_randomizer = LightRandomizer()
        light_randomizer.asset_hdri_lighting_folder_path = parameter.asset_hdri_lighting_folder_path # passing params
        light_randomizer.hdri_lighting_strength_range = parameter.hdri_lighting_strength_range
        light_randomizer.light_randomize()

        ## camera pose randomize
        camera_pose_randomizer = CameraPoseRandomizer()
        camera_pose_randomizer.fibonacci_sphere_radius_range = parameter.fibonacci_sphere_radius_range # passing params
        camera_pose_randomizer.fibonacci_sphere_sample_area = parameter.fibonacci_sphere_sample_area
        camera_pose_randomizer.camera_normal_angle_range = parameter.camera_normal_angle_range
        camera_pose_randomizer.camera_offset_location_range = parameter.camera_offset_location_range
        camera_pose_randomizer.camera_offset_rotation_range = parameter.camera_offset_rotation_range
        camera_pose_randomizer.camera_pose_randomize()

        ## camera effect randomize
        camera_effect_randomizer = CameraEffectRandomizer()
        camera_effect_randomizer.camera_focal_length = parameter.camera_focal_length # passing params
        camera_effect_randomizer.img_resolution_x = parameter.img_resolution_x
        camera_effect_randomizer.img_resolution_y = parameter.img_resolution_y
        camera_effect_randomizer.max_samples = parameter.cycle_sample
        camera_effect_randomizer.blur_probability = parameter.blur_probability
        camera_effect_randomizer.exposure_probability = parameter.exposure_probability
        camera_effect_randomizer.noise_probability = parameter.noise_probability
        camera_effect_randomizer.white_balance_probability = parameter.white_balance_probability
        camera_effect_randomizer.contrast_probability = parameter.contrast_probability
        camera_effect_randomizer.hue_probability = parameter.hue_probability
        camera_effect_randomizer.saturation_probability = parameter.saturation_probability
        camera_effect_randomizer.blur_value_range = parameter.blur_value_range
        camera_effect_randomizer.exposure_value_range = parameter.exposure_value_range
        camera_effect_randomizer.noise_value_range = parameter.noise_value_range
        camera_effect_randomizer.white_balance_value_range = parameter.white_balance_value_range
        camera_effect_randomizer.contrast_value_range = parameter.contrast_value_range
        camera_effect_randomizer.hue_value_range = parameter.hue_value_range
        camera_effect_randomizer.saturation_value_range = parameter.saturation_value_range
        camera_effect_randomizer.camera_effect_randomize()

        ## Update blender env view layer 
        bpy.data.scenes["Scene"].view_layers.update()

        ## rendering & labeling image
        yolo_segment_labeler = YoloSegmentLabeler()
        yolo_segment_labeler.output_img_path = parameter.output_img_path
        yolo_segment_labeler.output_label_path = parameter.output_label_path
        yolo_segment_labeler.rendering_and_labeling()

        print("One Data Generating Cylce Completed!!!")

        sys.exit()

if __name__ == '__main__':
    datagen = DataGenerator()
    datagen.gen_one_data()