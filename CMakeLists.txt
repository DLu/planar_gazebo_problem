cmake_minimum_required(VERSION 3.5)
project(frucking_friction)
find_package(ament_cmake REQUIRED)
install(DIRECTORY urdf/
        DESTINATION share/${PROJECT_NAME}/urdf
)
install(DIRECTORY launch/
        DESTINATION share/${PROJECT_NAME}/launch
)
ament_package()
