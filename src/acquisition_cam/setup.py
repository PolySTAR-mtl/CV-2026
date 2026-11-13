from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'acquisition_cam'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='codyd',
    maintainer_email='codyd@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'image_acquisition = acquisition_cam.image_acquisition:main',
            'imu_acquisition = acquisition_cam.imu_acquisition:main',
        ],
    },
)
