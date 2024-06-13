# 手动设置 Qhull 的包含目录和库目录
set(Qhull_INCLUDE_DIRS "usr/include/qhull/include")
set(Qhull_LIBRARY_DIRS "usr/lib/x86_64-linux-gnu/libqhullcpp.a")

# 包含头文件目录
include_directories(${Qhull_INCLUDE_DIRS})

# 添加可执行文件
add_executable(planar_detector_test planar_detector_test.cpp)

# 链接 Qhull 库
target_link_libraries(planar_detector_test ${Qhull_LIBRARY_DIRS}/libqhullcpp.a ${Qhull_LIBRARY_DIRS}/libqhull_r.a)