from setuptools import find_packages, setup

package_name = 'hw_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'pyserial'],
    zip_safe=True,
    maintainer='maxi',
    maintainer_email='monelosmaximo@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
            'pytest-mock',
        ],
    },
    entry_points={
        'console_scripts': [
            'uart_driver_node = hw_bridge.uart_driver:main',
            'protocol_handler_node = hw_bridge.protocol_handler_node:main'
        ],
    },
)
