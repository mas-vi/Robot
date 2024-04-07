from setuptools import find_packages, setup

package_name = 'robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/launch.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vboxuser',
    maintainer_email='opreaionut035@gmail.com',
    description='TODO: Package description',
    license='Apace-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'motor_controller = robot.motor_controller:main',
            'image_publisher=robot.image_publisher:main',
            'image_subscriber=robot.image_subscriber:main',
            'dht11_publisher=robot.dht11_publisher:main'
        ],
    },
)
