cmake_minimum_required(VERSION 3.2)

project(AdventOfCode VERSION 0.1.0 LANGUAGES C)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -std=c17")

if (MSVC)
    # warning level 4 and all warnings as errors
    add_compile_options(/W4 /WX)
else()
    # lots of warnings and all warnings as errors
    add_compile_options(-Wall -Wextra -pedantic -Werror)
endif()

include_directories(include)

#add_subdirectory(aoc2015)
#add_subdirectory(aoc2016)
add_subdirectory(aoc2021)

enable_testing()

add_executable(hashing tests/hash.c)
add_test(hashing hashing)

add_executable(queuing tests/queuing.c)
add_test(queuing queuing)