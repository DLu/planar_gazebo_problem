from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    empty_world_launch = IncludeLaunchDescription(
        [FindPackageShare('gazebo_ros'), '/launch/gzserver.launch.py'],
        launch_arguments={
            'pause': 'true',
            'verbose': 'true',
        }.items(),
    )

    gzclient_launch = IncludeLaunchDescription(
        [FindPackageShare('gazebo_ros'), '/launch/gzclient.launch.py'],
    )

    package_dir = FindPackageShare('frucking_friction')

    robot_description_content1 = ParameterValue(
        Command(['xacro ', PathJoinSubstitution([package_dir, 'urdf/box.urdf'])]), value_type=str)
    robot_description_content2 = ParameterValue(
        Command(['xacro ', PathJoinSubstitution([package_dir, 'urdf/wheels.urdf'])]), value_type=str)

    robot_state_publisher_node1 = Node(name='robot_state_publisher1',  package='robot_state_publisher',
                                       executable='robot_state_publisher',
                                       parameters=[{
                                           'robot_description': robot_description_content1,
                                       }],
                                       remappings=[('/robot_description', '/robot_description1')]
                                       )

    robot_state_publisher_node2 = Node(name='robot_state_publisher2',
                                       package='robot_state_publisher',
                                       executable='robot_state_publisher',
                                       parameters=[{
                                           'robot_description': robot_description_content2,
                                       }],
                                       remappings=[('/robot_description', '/robot_description2')]
                                       )

    # push robot_description to factory and spawn robot in gazebo
    urdf_spawner_node1 = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='urdf_spawner1',
        arguments=['-topic', '/robot_description1', '-entity', 'robot1', '-z', '1.5',],
        output='screen',
    )
    urdf_spawner_node2 = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='urdf_spawner2',
        arguments=['-topic', '/robot_description2', '-entity', 'robot2', '-x', '2.0', '-z', '1.5', '-unpause'],
        output='screen',
    )

    return LaunchDescription([
        empty_world_launch,
        gzclient_launch,
        robot_state_publisher_node1,
        robot_state_publisher_node2,
        urdf_spawner_node1,
        urdf_spawner_node2,
    ])
