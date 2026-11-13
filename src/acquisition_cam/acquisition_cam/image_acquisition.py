
import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

from message_filters import Subscriber, ApproximateTimeSynchronizer
from rclpy.qos import qos_profile_sensor_data


class ImageAcquisition(Node):

    def __init__(self):
        super().__init__('image_acquisition')

        # Paramètres configurables
        self.declare_parameter(
            'rgb_topic',
            '/camera/color/image_raw'
        )

        self.declare_parameter(
            'depth_topic',
            '/camera/aligned_depth_to_color/image_raw'
        )

        self.rgb_topic = self.get_parameter(
            'rgb_topic'
        ).value

        self.depth_topic = self.get_parameter(
            'depth_topic'
        ).value

        self.bridge = CvBridge()

        # Abonnements aux deux topics
        self.rgb_sub = Subscriber(
            self,
            Image,
            self.rgb_topic,
            qos_profile=qos_profile_sensor_data
        )

        self.depth_sub = Subscriber(
            self,
            Image,
            self.depth_topic,
            qos_profile=qos_profile_sensor_data
        )

        # Synchronisation des images
        self.sync = ApproximateTimeSynchronizer(
            [self.rgb_sub, self.depth_sub],
            queue_size=10,
            slop=0.05
        )

        self.sync.registerCallback(self.image_callback)

        self.get_logger().info(
            f'Abonnement RGB : {self.rgb_topic}'
        )

        self.get_logger().info(
            f'Abonnement Depth : {self.depth_topic}'
        )

    def image_callback(self, rgb_msg, depth_msg):

        # Conversion ROS -> OpenCV / NumPy
        rgb_image = self.bridge.imgmsg_to_cv2(
            rgb_msg,
            desired_encoding='bgr8'
        )

        depth_image = self.bridge.imgmsg_to_cv2(
            depth_msg,
            desired_encoding='passthrough'
        )

        # Informations utiles
        height, width, _ = rgb_image.shape

        self.get_logger().debug(
            f'Images reçues : {width}x{height}'
        )

        # Les deux tableaux sont maintenant disponibles.
        # rgb_image : image BGR pour OpenCV / YOLO
        # depth_image : image de profondeur (encodage d'origine)
        
        # cv2.imshow('RealSense RGB', rgb_image)

        # depth_vis = cv2.convertScaleAbs(
        #     depth_image,
        #     alpha=0.03
        # )

        # cv2.imshow(
        #     'RealSense Depth',
        #     depth_vis
        # )
        
        # depth_colormap = cv2.applyColorMap(
        #     cv2.convertScaleAbs(depth_image, alpha=0.03),
        #     cv2.COLORMAP_JET
        # )

        # cv2.imshow('RealSense Depth', depth_colormap)

        # Nécessaire pour actualiser les fenêtres
        # cv2.waitKey(1)

        self.get_logger().debug(
                f'Images reçues : {width}x{height} '
                f'| Depth encoding : {depth_msg.encoding}'
            )
        
    def destroy_node(self):

        cv2.destroyAllWindows()
        super().destroy_node()



def main(args=None):

    rclpy.init(args=args)

    node = ImageAcquisition()

    
    rclpy.spin(node)

    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
