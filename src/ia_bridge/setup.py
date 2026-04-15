from setuptools import find_packages, setup

package_name = 'ia_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='maxi',
    maintainer_email='monelosmaximo@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'motor_status_node = ia_bridge.motor_topics_node:main',
            'motor_service_node = ia_bridge.motor_services_node:main',
            'motor_actions_node = ia_bridge.motor_actions_node:main',
        ],
    },
)
