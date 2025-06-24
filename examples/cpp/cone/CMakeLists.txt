cmake_minimum_required(VERSION 3.29)
project(cone_main LANGUAGES C CXX)

# -----------------------------------------------------------------------------
# EMSCRIPTEN only
# -----------------------------------------------------------------------------

if (NOT EMSCRIPTEN)
  message("Skipping example: This needs to run inside an Emscripten build environment")
  return ()
endif ()

# -----------------------------------------------------------------------------
# Handle VTK dependency
# -----------------------------------------------------------------------------

find_package(VTK REQUIRED)

if (NOT VTK_FOUND)
  message("Skipping example: ${VTK_NOT_FOUND_MESSAGE}")
  return ()
endif ()

# -----------------------------------------------------------------------------
# Compile example code
# -----------------------------------------------------------------------------

add_executable(main main.cpp)
target_link_libraries(main PRIVATE ${VTK_LIBRARIES})

# -----------------------------------------------------------------------------
# Optimizations
# -----------------------------------------------------------------------------

set(emscripten_optimizations)
set(emscripten_debug_options)

# Set a default build type if none was specified
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to 'Debug' as none was specified.")
  set(CMAKE_BUILD_TYPE Debug CACHE STRING "Choose the type of build." FORCE)
  # Set the possible values of build type for cmake-gui
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release"
    "MinSizeRel" "RelWithDebInfo")
endif()

if (CMAKE_BUILD_TYPE STREQUAL "Release")
  set(wasm_optimize "BEST")
  set(wasm_debuginfo "NONE")
elseif (CMAKE_BUILD_TYPE STREQUAL "MinSizeRel")
  set(wasm_optimize "SMALLEST_WITH_CLOSURE")
  set(wasm_debuginfo "NONE")
elseif (CMAKE_BUILD_TYPE STREQUAL "RelWithDebInfo")
  set(wasm_optimize "MORE")
  set(wasm_debuginfo "PROFILE")
elseif (CMAKE_BUILD_TYPE STREQUAL "Debug")
  set(wasm_optimize "NO_OPTIMIZATION")
  set(wasm_debuginfo "DEBUG_NATIVE")
endif ()
set(wasm_optimize_NO_OPTIMIZATION "-O0")
set(wasm_optimize_LITTLE "-O1")
set(wasm_optimize_MORE "-O2")
set(wasm_optimize_BEST "-O3")
set(wasm_optimize_SMALLEST "-Os")
set(wasm_optimize_SMALLEST_WITH_CLOSURE "-Oz")
set(wasm_optimize_SMALLEST_WITH_CLOSURE_link "--closure=1")

set(emscripten_link_options
  "-lembind"
  "-sALLOW_MEMORY_GROWTH=1"
  "-sSINGLE_FILE=1")

if (DEFINED "wasm_optimize_${wasm_optimize}")
  list(APPEND emscripten_optimizations
    ${wasm_optimize_${wasm_optimize}})
  list(APPEND emscripten_link_options
    ${wasm_optimize_${wasm_optimize}_link})
else ()
  message (FATAL_ERROR "Unrecognized value for wasm_optimize=${wasm_optimize}")
endif ()

set(wasm_debuginfo_NONE "-g0")
set(wasm_debuginfo_READABLE_JS "-g1")
set(wasm_debuginfo_PROFILE "-g2")
set(wasm_debuginfo_DEBUG_NATIVE "-g3")
set(wasm_debuginfo_DEBUG_NATIVE_link "-sASSERTIONS=1")
if (DEFINED "wasm_debuginfo_${wasm_debuginfo}")
  list(APPEND emscripten_debug_options
    ${wasm_debuginfo_${wasm_debuginfo}})
  list(APPEND emscripten_link_options
    ${wasm_debuginfo_${wasm_debuginfo}_link})
else ()
  message (FATAL_ERROR "Unrecognized value for wasm_debuginfo=${wasm_debuginfo}")
endif ()

target_compile_options(main
  PRIVATE
    ${emscripten_compile_options}
    ${emscripten_optimizations}
    ${emscripten_debug_options})
target_link_options(main
  PRIVATE
    ${emscripten_link_options}
    ${emscripten_optimizations}
    ${emscripten_debug_options})

set(CMAKE_NINJA_FORCE_RESPONSE_FILE "ON" CACHE BOOL "Force Ninja to use response files.")

# -----------------------------------------------------------------------------
# VTK modules initialization
# -----------------------------------------------------------------------------

vtk_module_autoinit(
  TARGETS  main
  MODULES  ${VTK_LIBRARIES}
)

# Output the main.js file to the docs/public/demo/cpp-app-1 directory
# so that it can be used in the documentation.
set_target_properties(main PROPERTIES
  RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/../../../docs/public/demo/cpp-app-1"
)
