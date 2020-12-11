cmake_minimum_required(VERSION 3.6)
project(BaseCv)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
        CPP/ssq.cpp
        ../../LICENSE
        ../../README.md)

find_package(Qt5Core REQUIRED)
find_package(Qt5Widgets REQUIRED)
find_package(Qt5Gui REQUIRED)

add_executable(BaseCV ${SOURCE_FILES})