"""CameraPoseRandomizer

reference:
camera_point_to_a_point, https://blender.stackexchange.com/questions/150697/center-point-in-camera-view 
"""

import bpy
import math
import random
import mathutils
from mathutils import Euler

class CameraPoseRandomizer:
    def __init__(self,
                fibonacci_sphere_radius_range = {"min":0.12, "max":0.2},
                fibonacci_sphere_sample_area = 0.0001,
                camera_normal_angle_range = {"min":75, "max": 90},
                camera_offset_location_range = {"min": - 0.003 , "max": 0.003},
                camera_offset_rotation_range = {"min":-5, "max":5}
                ):

        self.__object_camera_need_to_point = bpy.data.objects["arduino_board"]
        self.fibonacci_sphere_radius_range = fibonacci_sphere_radius_range
        self.__fibonacci_sphere_radius = 5 #random change by __create_random_fibonacci_sphere
        self.fibonacci_sphere_sample_area = fibonacci_sphere_sample_area
        self.__fibonacci_sphere_sample_num = 10 #random change by __create_random_fibonacci_sphere
        self.__sphere_points = list()
        self.__random_camera_coordinate = None
        self.camera_normal_angle_range = camera_normal_angle_range
        self.camera_offset_location_range = camera_offset_location_range
        self.camera_offset_rotation_range = camera_offset_rotation_range

    def __fibonacci_sphere(self, r = 1, samples = 100):
        """
        """
        points = []
        phi = math.pi * (3. - math.sqrt(5.))  # golden angle in radians

        for i in range(samples):
            y = 1 - (i / float(samples - 1)) * 2  # y goes from 1 to -1
            radius = math.sqrt(1 - y * y)  # radius at y
            theta = phi * i  # golden angle increment
            x = math.cos(theta) * radius
            z = math.sin(theta) * radius

            ## just return upper sphere points
            if z <= 0:
                continue

            ## check camera_normal_angle
            angle = math.asin(z) * (180/math.pi)
            if (angle > self.camera_normal_angle_range["max"] or angle < self.camera_normal_angle_range["min"]):
                continue

            x,y,z=r*x,r*y,r*z
            points.append((x, y, z))

        return points

    def __create_random_fibonacci_sphere(self):
        """
        1.random select fibonacci_sphere_radius
        2.caculate sphere_area
        3.caculate fibonacci_sphere_sample_num accroding to fibonacci_sphere_sample_area
        4.return fibonacci_sphere points coordinate
        """
        ## 1.random select fibonacci_sphere_radius
        fibonacci_sphere_radius_max = self.fibonacci_sphere_radius_range["max"]
        fibonacci_sphere_radius_min = self.fibonacci_sphere_radius_range["min"]
        self.__fibonacci_sphere_radius = random.uniform(fibonacci_sphere_radius_min, fibonacci_sphere_radius_max)

        ##2.caculate sphere_area
        sphere_area = 4 * math.pi * self.__fibonacci_sphere_radius * self.__fibonacci_sphere_radius

        ## 3.caculate fibonacci_sphere_sample_num accroding to fibonacci_sphere_sample_area
        self.__fibonacci_sphere_sample_num = round(sphere_area/self.fibonacci_sphere_sample_area)

        ## 4.return fibonacci_sphere points coordinate
        self.__sphere_points = self.__fibonacci_sphere(r = self.__fibonacci_sphere_radius, samples = self.__fibonacci_sphere_sample_num)

        print(f'fibonacci_sphere_radius : {self.__fibonacci_sphere_radius}')
        print(f'fibonacci_sphere_sample_num : {self.__fibonacci_sphere_sample_num}')
        print(f'sphere_points_num : {len(self.__sphere_points)}')

    def __randomly_place_camera(self):
        """
        """
        cam = bpy.data.objects["Camera"]
        object = self.__object_camera_need_to_point

        self.__create_random_fibonacci_sphere()
        random_point = random.sample(self.__sphere_points, 1)[0]
        self.__random_camera_coordinate = (random_point[0] + object.location.x, random_point[1] + object.location.y, random_point[2])
        cam.location = self.__random_camera_coordinate
        
    def __point_camera_at_object(self):
        """ 
        """ 
        cam = bpy.data.objects["Camera"]
        object = self.__object_camera_need_to_point

        direction = cam.location - object.location

        rot = direction.to_track_quat('Z', 'Y').to_matrix().to_4x4()
        loc = mathutils.Matrix.Translation(cam.location)

        cam.matrix_world = loc @ rot

    def __random_camera_offset(self):
        """ 
        """ 
        cam = bpy.data.objects["Camera"]

        ## randomly adjust camera location
        camera_offset_location_x = random.uniform(self.camera_offset_location_range["min"], self.camera_offset_location_range["max"])
        camera_offset_location_y = random.uniform(self.camera_offset_location_range["min"], self.camera_offset_location_range["max"])
        cam.location.x = cam.location.x + camera_offset_location_x
        cam.location.y = cam.location.y + camera_offset_location_y

        ## randomly adjust camera rotation
        camera_offset_rotation_x = random.uniform(self.camera_offset_rotation_range["min"]/360, self.camera_offset_rotation_range["max"]/360) * 2 * math.pi
        camera_offset_rotation_y = random.uniform(self.camera_offset_rotation_range["min"]/360, self.camera_offset_rotation_range["max"]/360) * 2 * math.pi
        cam.rotation_euler.x = cam.rotation_euler.x + camera_offset_rotation_x
        cam.rotation_euler.x = cam.rotation_euler.x + camera_offset_rotation_y

    def camera_pose_randomize(self):
        """ 
        """
        self.__randomly_place_camera()
        self.__point_camera_at_object()
        self.__random_camera_offset()

        print("Camera Pose Randomize COMPLERED !!!")

if __name__ == '__main__':
    randomizer = CameraPoseRandomizer()
    randomizer.camera_pose_randomize()   
