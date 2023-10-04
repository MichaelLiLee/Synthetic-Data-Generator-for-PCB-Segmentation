"""SceneGenerateRandomizer

"""
import bpy
import random
import glob
import os
from mathutils import Euler
import math

class SceneGenerateRandomizer:
    def __init__(self,
                asset_board_folder_path = "C:/Users/user/Documents/project/ArduinoSegment/Asset/BoardModel",
                asset_table_folder_path = "C:/Users/user/Documents/project/ArduinoSegment/Asset/TableModel",
                borad_placement_area = {"x_min":-0.2, "x_max": 0.2, "y_min":-0.2, "y_max":0.2}
                ):

        self.asset_table_folder_path = asset_table_folder_path
        self.asset_board_folder_path = asset_board_folder_path
        self.borad_placement_area = borad_placement_area
        self.__table_object_collection = bpy.data.collections["TableCollection"]
        self.__board_object_collection = bpy.data.collections["BoardCollection"]
        self.__board_coordinate = [0,0,0]
        self.__board_pose = [0,0,0]

    def __load_object(self, filepath, collection):
        """ Asset Linking
        """
        ## append object from .blend file
        with bpy.data.libraries.load(filepath, link = False,assets_only = True) as (data_from, data_to):
            data_to.objects = data_from.objects
        ## link object to current scene
        for obj in data_to.objects:
            if obj is not None:
                collection.objects.link(obj)

    def __import_table_and_board_asset(self):
        """ 
        """ 
        ## get table object asset path
        table_object_path_list = glob.glob(os.path.join(self.asset_table_folder_path, "*.blend"))
        ## link table asset to current scene
        table_asset_path = random.sample(table_object_path_list, 1)[0]
        self.__load_object(filepath = table_asset_path, collection = self.__table_object_collection)

        ## get board object asset path
        board_object_path_list = glob.glob(os.path.join(self.asset_board_folder_path, "*.blend"))
        ## link board asset to current scene
        board_asset_path =  random.sample(board_object_path_list, 1)[0]
        self.__load_object(filepath = board_asset_path, collection = self.__board_object_collection)

    def __randomly_place_board(self):
        """ 
        """
        ## place board
        self.__board_coordinate[0] = random.uniform(self.borad_placement_area["x_min"], self.borad_placement_area["x_max"])
        self.__board_coordinate[1] = random.uniform(self.borad_placement_area["y_min"], self.borad_placement_area["y_max"])
        for board_obj in self.__board_object_collection.objects:
            if board_obj.parent == None: #main board is the parent of other parts
                board_obj.location = self.__board_coordinate

        ## rotate board
        self.__board_pose = [0, 0 , random.random() * 2 * math.pi]
        for board_obj in self.__board_object_collection.objects:
            if board_obj.parent == None: #main board is the parent of other parts
                board_obj.rotation_euler = Euler(self.__board_pose, 'XYZ')

    def scene_generate(self):
        """ 
        """ 
        self.__import_table_and_board_asset()
        self.__randomly_place_board()
        print("Scene Generate COMPLERED !!!")

if __name__ == '__main__':
    randomizer = SceneGenerateRandomizer()
    randomizer.scene_generate()