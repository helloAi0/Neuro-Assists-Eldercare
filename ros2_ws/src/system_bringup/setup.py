from setuptools import find_packages, setup

package_name = 'system_bringup'

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
    maintainer='user_taha5253',
    maintainer_email='you@example.com',
    description='System-wide bringup, launch files, and heartbeat/health signaling.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'heartbeat_publisher = system_bringup.heartbeat_publisher:main',
            'heartbeat_listener = system_bringup.heartbeat_listener:main',
        ],
    },
)