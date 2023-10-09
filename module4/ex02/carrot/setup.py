from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'carrot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='nastya',
    maintainer_email='nastasapervaa@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'static_turtle_tf2_broadcaster = carrot.static_turtle_tf2_broadcaster:main',
        'turtle_tf2_broadcaster = carrot.turtle_tf2_broadcaster:main',
        'turtle_tf2_listener = carrot.turtle_tf2_listener:main',
        'turtles_carrot = carrot.turtles_carrot:main',
        ],
    },
)
