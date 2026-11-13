
import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Imu
from rclpy.qos import qos_profile_sensor_data


class ImuAcquisition(Node):

    def __init__(self):
        super().__init__('imu_acquisition')

        self.declare_parameter(
            'gyro_topic',
            '/camera/gyro/sample'
        )

        self.declare_parameter(
            'accel_topic',
            '/camera/accel/sample'
        )

        gyro_topic = self.get_parameter(
            'gyro_topic'
        ).value

        accel_topic = self.get_parameter(
            'accel_topic'
        ).value

        # Stockage des dernières mesures
        self.last_gyro = None
        self.last_accel = None

        # Abonnement au gyroscope
        self.gyro_sub = self.create_subscription(
            Imu,
            gyro_topic,
            self.gyro_callback,
            qos_profile_sensor_data
        )

        # Abonnement à l'accéléromètre
        self.accel_sub = self.create_subscription(
            Imu,
            accel_topic,
            self.accel_callback,
            qos_profile_sensor_data
        )

        self.get_logger().info(
            f'Abonnement Gyroscope : {gyro_topic}'
        )

        self.get_logger().info(
            f'Abonnement Accéléromètre : {accel_topic}'
        )

    def gyro_callback(self, msg):

        self.last_gyro = msg

        angular_velocity = msg.angular_velocity

        # Vitesse angulaire en rad/s
        gx = angular_velocity.x
        gy = angular_velocity.y
        gz = angular_velocity.z

        self.get_logger().debug(
            f'Gyro : x={gx:.3f}, y={gy:.3f}, z={gz:.3f}'
        )

    def accel_callback(self, msg):

        self.last_accel = msg

        acceleration = msg.linear_acceleration

        # Accélération en m/s²
        ax = acceleration.x
        ay = acceleration.y
        az = acceleration.z

        self.get_logger().debug(
            f'Accel : x={ax:.3f}, y={ay:.3f}, z={az:.3f}'
        )


def main(args=None):

    rclpy.init(args=args)

    node = ImuAcquisition()
    
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
