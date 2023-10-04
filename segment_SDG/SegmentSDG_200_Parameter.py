"""Parameter 
"""

class Parameter:
    def __init__(self):
        self.gen_num = 250
        self.blender_exe_path = "C:/program Files/Blender Foundation/Blender 3.3/blender"
        self.asset_table_folder_path = "C:/Users/user/Documents/project/ArduinoSegment/Asset/TableModel"
        self.asset_board_folder_path = "C:/Users/user/Documents/project/ArduinoSegment/Asset/BoardModel"
        self.asset_table_texture_folder_path = "C:/Users/user/Documents/project/ArduinoSegment/Asset/TableTexture"
        self.asset_hdri_lighting_folder_path = "C:/Users/user/Documents/project/ArduinoSegment/Asset/HdriLighting"
        self.output_img_path = "C:/Users/user/Documents/project/ArduinoSegment/gen_data/images"
        self.output_label_path = "C:/Users/user/Documents/project/ArduinoSegment/gen_data/labels"
        self.camera_focal_length = 35
        self.camera_sensor_width = 36
        self.img_resolution_x = 4000
        self.img_resolution_y = 3000
        self.cycle_sample = 512
        self.borad_placement_area = {"x_min":-0.2, "x_max": 0.2, "y_min":-0.2, "y_max":0.2}
        self.texture_scale_range = {"min": 3 , "max": 7}
        self.hdri_lighting_strength_range = {"min": 0.5 , "max": 1.3}
        self.fibonacci_sphere_radius_range = {"min":0.15, "max":0.25}
        self.fibonacci_sphere_sample_area = 0.0001
        self.camera_normal_angle_range = {"min":70, "max": 90}
        self.camera_offset_location_range = {"min": - 0.003 , "max": 0.003}
        self.camera_offset_rotation_range = {"min":-5, "max":5}
        self.blur_probability = 0.5
        self.blur_value_range = {"min": 3, "max": 5}
        self.exposure_probability = 0.5
        self.exposure_value_range = {"min": 0, "max": 1}
        self.noise_probability = 0.5
        self.noise_value_range = {"min": 1.6, "max": 1.8}
        self.white_balance_probability = 0.5
        self.white_balance_value_range = {"min": 5500, "max": 7500}
        self.contrast_probability = 0.5
        self.contrast_value_range = {"min": -1, "max": 2}
        self.hue_probability = 0.5
        self.hue_value_range = {"min": 0.45, "max": 0.55}
        self.saturation_probability = 0.5
        self.saturation_value_range = {"min": 0.9, "max": 1.25}