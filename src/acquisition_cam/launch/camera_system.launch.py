
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # Paramètres de la caméra
    camera_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('realsense2_camera'),
            '/launch/rs_launch.py'
        ]),
        launch_arguments={
            'align_depth.enable': 'true',
            'enable_sync': 'true',
            'enable_gyro': 'true',
            'enable_accel': 'true',
            'rgb_camera.enable_auto_exposure': 'false',  
            'rgb_camera.color_profile': '640x480x15',
            'depth_module.depth_profile': '640x480x15',
        }.items()
    )

    # Node d'acquisition des images
    image_node = Node(
        package='acquisition_cam',
        executable='image_acquisition',
        name='image_acquisition',
        output='screen',
        parameters=[{
            'rgb_topic': LaunchConfiguration('rgb_topic'),
            'depth_topic': LaunchConfiguration('depth_topic')
        }]
    )

    # Node d'acquisition de l'IMU
    imu_node = Node(
        package='acquisition_cam',
        executable='imu_acquisition',
        name='imu_acquisition',
        output='screen',
        parameters=[{
            'gyro_topic': LaunchConfiguration('gyro_topic'),
            'accel_topic': LaunchConfiguration('accel_topic')
        }]
    )

    return LaunchDescription([

        # DeclareLaunchArgument(
        #     'rgb_exposure',
        #     default_value='80.0'
        # ),

        # DeclareLaunchArgument(
        #     'rgb_gain',
        #     default_value='64.0'
        # ),

        DeclareLaunchArgument(
            'rgb_topic',
            default_value='/camera/camera/color/image_raw'
        ),

        DeclareLaunchArgument(
            'depth_topic',
            default_value='/camera/camera/aligned_depth_to_color/image_raw'
        ),

        DeclareLaunchArgument(
            'gyro_topic',
            default_value='/camera/gyro/sample'
        ),

        DeclareLaunchArgument(
            'accel_topic',
            default_value='/camera/accel/sample'
        ),

        camera_launch,
        image_node,
        imu_node
    ])
