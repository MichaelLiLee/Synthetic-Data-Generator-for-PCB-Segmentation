""" Initializer
Cleans up the whole scene at first and then initializes basic blender settings, the world, the renderer and
the camera.

reference:
https://github.com/DLR-RM/BlenderProc/blob/ea934e1b5df747dfcb5faf177092e156e5ca3356/blenderproc/python/utility/Initializer.py

"""
import bpy

class Initializer:
    def __init__(self,
                camera_focal_length = 35,
                camera_sensor_width = 36,
                img_resolution_x = 2000,
                img_resolution_y = 1500,
                cycle_samples = 256
                ):
        self.__render_engine = "CYCLES"
        self.__render_device = "GPU"
        self.__collection_need_create = ["TableCollection", "BoardCollection"]
        self.__camera_location = (0, 0, 1)
        self.camera_focal_length = camera_focal_length
        self.camera_sensor_width = camera_sensor_width
        self.img_resolution_x = img_resolution_x
        self.img_resolution_y = img_resolution_y
        self.cycle_samples = cycle_samples

    def __remove_all_data(self):
        """ Remove all data blocks except opened scripts and scene.
        """
        ## Go through all attributes of bpy.data
        for collection in dir(bpy.data):
            data_structure = getattr(bpy.data, collection)
            ## Check that it is a data collection
            if isinstance(data_structure, bpy.types.bpy_prop_collection) and hasattr(data_structure, "remove") \
                    and collection not in ["texts"]:
                ## Go over all entities in that collection
                for block in data_structure:
                    ## Skip the default scene
                    if isinstance(block, bpy.types.Scene) and block.name == "Scene":
                        continue
                    data_structure.remove(block)

    def __remove_custom_properties(self):
        """ Remove all custom properties registered at global entities like the scene.
        """
        for key in bpy.context.scene.keys():
            del bpy.context.scene[key]

    def init(self):
        """ Resets the scene to its clean state.
        This method removes all objects, camera poses and cleans up the world background.
        """
        ## Switch to right context
        if bpy.context.object is not None and bpy.context.object.mode != "OBJECT":
            bpy.ops.object.mode_set(mode='OBJECT')

        ## Clean up data in blender file
        self.__remove_all_data()
        self.__remove_custom_properties()

        ## Create new world
        new_world = bpy.data.worlds.new("World")
        bpy.context.scene.world = new_world
        new_world["category_id"] = 0

        ## Create the camera
        cam = bpy.data.cameras.new("Camera")
        cam_ob = bpy.data.objects.new("Camera", cam)
        bpy.context.scene.collection.objects.link(cam_ob)
        bpy.context.scene.camera = cam_ob
        cam_ob.location = self.__camera_location
        ## set camera focal length 
        bpy.data.cameras['Camera'].lens = self.camera_focal_length
        ## set camera sensor width
        bpy.data.cameras['Camera'].sensor_width = self.camera_sensor_width
        ## set img resolution
        bpy.data.scenes['Scene'].render.resolution_x = self.img_resolution_x
        bpy.data.scenes['Scene'].render.resolution_y = self.img_resolution_y
        ## set render max samples num
        bpy.data.scenes['Scene'].cycles.preview_samples = self.cycle_samples
        bpy.data.scenes['Scene'].cycles.samples = self.cycle_samples

        ## Create new synthdet collections
        for collection in self.__collection_need_create:
            bpy.context.scene.collection.children.link(bpy.data.collections.new(collection))

        ## Set rendering setting
        bpy.context.scene.render.engine = self.__render_engine
        bpy.context.scene.cycles.device = self.__render_device

        print("INITIALIZE COMPLERED !!!")

if __name__ == '__main__':
    initializer = Initializer()
    initializer.init()