"""YoloSegmentLabeler

"""

import bpy
import numpy as np
import datetime
import os
import cv2

class YoloSegmentLabeler:
    def __init__(self,
                 output_img_path = "C:/Users/user/Documents/project/ArduinoSegment/gen_data/images",
                 output_label_path = "C:/Users/user/Documents/project/ArduinoSegment/gen_data/labels"
                 ):

        self.output_img_path = output_img_path
        self.output_label_path = output_label_path
        self.__obj_name_and_id_dict = {}
        self.__obj_name_and_polygon_dict = {}
        self.__target_obj_collection = bpy.data.collections["BoardCollection"]
        self.__minimum_obj_pixel = 1 * 1
        self.__gen_img_id = None
        self.__render_machine_id = "a"
        self.__output_yolo_segmentation_txt_str = ""
        self.__obj_name_and_class_id_mapping = {
            "usb_connector" : 28,
            "power_connector" : 16,
            "analog_input_pins" : 10,
            "digital_pins_01" : 13,
            "digital_pins_02" : 14,
            "power_pins" : 17,
            "capacitor_01" : 11,
            "capacitor_02" : 11,
            "ICSP_pins_01" : 6,
            "ICSP_pins_02" : 6,
            "ATMEGA16U2_USB_TTL_converter" : 4,
            "oscillator" : 15,
            "ATMEGA328P_microcontroller" : 5,
            "5V_regulator" : 3,
            "LMV358LIST_IC" : 9,
            "reset" : 21,
            "resistor102_01" : 22,
            "resistor102_02" : 22,
            "resistor103" : 23,
            "resistor220" : 25,
            "JP2_pins_01" : 7,
            "JP2_pins_02" : 7,
            "JP2_pins_03" : 7,
            "JP2_pins_04" : 7,
            "L_LED" : 8,
            "ON_LED" : 8,
            "RX_LED" : 8,
            "TX_LED" : 8,
            "chip_capacitor" : 12,
            "rectifier_D1" : 18,
            "rectifier_D2" : 19,
            "rectifier_D3" : 20,
            "0603_capacitor_01" : 0,
            "0603_capacitor_02" : 0,
            "0603_capacitor_03" : 0,
            "0603_capacitor_04" : 0,
            "0603_capacitor_05" : 0,
            "0603_capacitor_06" : 0,
            "0603_capacitor_07" : 0,
            "0603_capacitor_08" : 0,
            "0603_capacitor_09" : 0,
            "resistor105_01" : 24,
            "resistor105_02" : 24,
            "resistor105_03" : 24,
            "3V_regulator" : 2,
            "transistor" : 27,
            "resonator" : 26,
            "0805_capacitor" : 1,
            "resistor105_04" : 24,
            "0603_capacitor_10" : 0
}

    def __create_and_switch_annotation_scene(self):
        """
        """
        scene_list = []
        for scene in bpy.data.scenes:
            scene_list.append(scene.name)

        if ("Scene_Annot" not in scene_list):
            bpy.data.scenes['Scene'].copy()
            bpy.data.scenes["Scene.001"].name = "Scene_Annot"

        bpy.context.window.scene = bpy.data.scenes["Scene_Annot"]

    def __create_gen_img_id(self):
        """ 
        """
        now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
        time_id = now.strftime("%Y%m%d%H%M%S").zfill(15)
        render_machine_id = self.__render_machine_id
        self.__gen_img_id = render_machine_id + time_id

        return id
    
    def  __create_id_mask_nodes(self):
        """ 
        """
        ## active compositing nodes
        bpy.data.scenes['Scene_Annot'].use_nodes = True

        ## clear all nodes
        bpy.data.scenes['Scene_Annot'].node_tree.nodes.clear()

        ## activate object index pass
        bpy.data.scenes['Scene_Annot'].view_layers["ViewLayer"].use_pass_object_index = True

        ## add new nodes
        node_RenderLayers = bpy.data.scenes['Scene_Annot'].node_tree.nodes.new("CompositorNodeRLayers")
        node_Composite = bpy.data.scenes['Scene_Annot'].node_tree.nodes.new("CompositorNodeComposite")
        node_Viewer = bpy.data.scenes['Scene_Annot'].node_tree.nodes.new("CompositorNodeViewer")
  
        node_RenderLayers.location = (-100,0)
        node_Composite.location = (250,0)
        node_Viewer.location = (600,-200)

        ## link nodes
        links = bpy.data.scenes['Scene_Annot'].node_tree.links
        links.new(node_RenderLayers.outputs["Image"], node_Composite.inputs["Image"])
        links.new(node_RenderLayers.outputs["IndexOB"], node_Viewer.inputs["Image"])

    def __add_pass_index(self):
        """ 
        """ 
        bpy.data.scenes['Scene_Annot'].view_layers["ViewLayer"].use_pass_object_index = True

        for index, obj in enumerate(self.__target_obj_collection.objects, start=1): 
            obj.pass_index = index
            self.__obj_name_and_id_dict[obj.name] = index

    def __annotation_render(self):
        """ 
        """
        ## render using Cycle
        bpy.data.scenes['Scene_Annot'].render.engine = "CYCLES"
        bpy.data.scenes['Scene_Annot'].cycles.device = "GPU"
        bpy.data.scenes['Scene_Annot'].cycles.samples = 128
        bpy.data.scenes['Scene_Annot'].cycles.use_denoising = False
        print("Start Render Annot")
        bpy.ops.render.render(scene='Scene_Annot')
        print("End Render Annot")

    def __mask_to_polygon(self, mask: np.array) -> list[int]:
        """ 
        """ 
        contour, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour = np.vstack(contour).squeeze()
        polygon = list()

        for point in contour:
            coords = list()
            coords.append(int(point[0]))
            coords.append(int(point[1]))
            polygon.append(coords)
        
        print(f"Number of points = {len(polygon)}")
        
        return polygon

    def __find_all_parts_contour(self):
        """ 
        """ 
        self.__annotation_render()
        for obj_name, id in self.__obj_name_and_id_dict.items():
            S = bpy.data.scenes['Scene_Annot']
            width  = int(S.render.resolution_x * S.render.resolution_percentage / 100)
            height = int(S.render.resolution_y * S.render.resolution_percentage / 100)
            depth  = 4

            img = np.array( bpy.data.images['Viewer Node'].pixels[:] ).reshape( [height, width, depth] ) #img shape : (h,w,d)
            ## Keep only one value for each pixel
            # img = np.array( [ [ img[0] for img in row ] for row in img] ) #img shape : (h,w)
            img = img[:, :, 0] # faster than for loop ??
           
            img = img.astype(int) #covert float to int
            ## print count pixel by id
            # print("Count Pixel By ID : ")
            # unique, counts = np.unique(img, return_counts=True)
            # print(dict(zip(unique, counts)))
            
            print(f'id:{id} obj_name:{obj_name}')
            if img.max() == 0: # no object in view
                continue
            print(f'id {id} pixel_sum: {(img == int(id)).sum()}')
            if (img == int(id)).sum() <= self.__minimum_obj_pixel: # object too small in view
                continue
            
            # threshold img (id to 255, else to 0) 
            img[img != int(id)] = 0
            img[img == int(id)] = 255
            img = img.astype(np.uint8) #convert to CV_8UC2 img
            # flip img
            img = np.flip(img,0)

            # get contour
            polygon = self.__mask_to_polygon(img)
            self.__obj_name_and_polygon_dict[obj_name] = polygon

            print(f"Find {obj_name} polygon")
            print(f"Remain Obj Num: {len(self.__obj_name_and_id_dict) - id}")

    def __get_obj_class_id(self, obj_name):
        """ 
        """ 
        obj_class_id = None
        for key in self.__obj_name_and_class_id_mapping:
            if key in obj_name:
                obj_class_id = self.__obj_name_and_class_id_mapping[key]
                return obj_class_id

    def  __format_coordinates(self, coordinates, obj_class_id):
        """
        """
        if coordinates and obj_class_id != None:
            ## Figure out the rendered image size
            render = bpy.data.scenes['Scene_Annot'].render
            fac = render.resolution_percentage * 0.01
            dw = 1./(render.resolution_x * fac)
            dh = 1./(render.resolution_y * fac)
        ## Formulate line corresponding to the segmentation polygon of one class
            txt_coordinates = str(obj_class_id)
            for coord in coordinates:
                x = coord[0]*dw
                y = coord[1]*dh
                txt_coordinates = txt_coordinates + ' '  + str(x) + ' ' + str(y) 
            txt_coordinates = txt_coordinates + '\n'

            return txt_coordinates
            ## If the current class isn't in view of the camera, then pass
        else:
            pass        

    def __convert_to_yolo_segmentation_format(self):
        """
        """ 
        main_text_coordinates = ""

        for obj_name in self.__obj_name_and_polygon_dict:
            obj_class_id = self.__get_obj_class_id(obj_name)
            coordinates = self.__obj_name_and_polygon_dict[obj_name]
            ## Reformat coordinates to YOLO segmentation format
            text_coordinates = self.__format_coordinates(coordinates, obj_class_id)

            if text_coordinates:
                main_text_coordinates = main_text_coordinates + text_coordinates
        
        splitted_main_text_coordinates = main_text_coordinates.split('\n')[:-1]# Delete last '\n' in coordinates
        self.__output_yolo_segmentation_txt_str = splitted_main_text_coordinates                                                           
        #return main_text_coordinates 

    def __render_img_and_save_annotation(self):
        """ 
        """ 
        ##　save png img
        img_file_path = os.path.join(self.output_img_path,  str(self.__gen_img_id)+".png")
        bpy.data.scenes["Scene"].render.filepath = img_file_path 
        print("Start Render Image")         
        bpy.ops.render.render(write_still=True, scene='Scene')
        print("End Render Image")

        ## save labels
        text_file_path = os.path.join(self.output_label_path, str(self.__gen_img_id)+".txt")
        text_file = open(text_file_path, 'w+') # Open .txt file of the label
        text_file.write('\n'.join(self.__output_yolo_segmentation_txt_str))
        text_file.close()

        print("SAVE IMG AT {}".format(img_file_path))
        print("SAVE LABLE AT {}".format(text_file_path))

    def test(self):
        """ 
        """
        self.__create_gen_img_id()
        self.__create_and_switch_annotation_scene()
        self.__create_id_mask_nodes()
        self.__add_pass_index()
        self.__find_all_parts_contour()
        text_coordinates = self.__convert_to_yolo_segmentation_format()
        print('text_coordinates')
        print(text_coordinates)
        splitted_coordinates = text_coordinates.split('\n')[:-1]# Delete last '\n' in coordinates
        print('splitted_coordinates')
        print(splitted_coordinates)

        ##　save png img
        img_file_path = os.path.join(self.output_img_path,  str(self.__gen_img_id)+".png")
        bpy.data.scenes["Scene"].render.filepath = img_file_path 
        print("Start Render Image")         
        bpy.ops.render.render(write_still=True, scene='Scene')
        print("End Render Image")

        ## save labels
        text_file_path = os.path.join(self.output_label_path, str(self.__gen_img_id)+".txt")
        text_file = open(text_file_path, 'w+') # Open .txt file of the label
        text_file.write('\n'.join(splitted_coordinates))
        text_file.close()

        print("SAVE IMG AT {}".format(img_file_path))
        print("SAVE LABLE AT {}".format(text_file_path))
        print("Auto Labeling COMPLERED !!!")

        print("test ok !!!")

    def rendering_and_labeling(self):
        """
        """
        self.__create_gen_img_id()
        self.__create_and_switch_annotation_scene()
        self.__create_id_mask_nodes()
        self.__add_pass_index()
        self.__find_all_parts_contour()
        self.__convert_to_yolo_segmentation_format()
        self.__render_img_and_save_annotation()
        print("Rendering and Labeling COMPLERED !!!")

if __name__ == '__main__':
    yolo_labeler = YoloSegmentLabeler()
    yolo_labeler.rendering_and_labeling()   