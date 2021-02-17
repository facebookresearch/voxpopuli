cmake_minimum_required(VERSION 3.10)

project(voxpopuli_wav2letter++ CXX C)

# C++ 14 is required
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(flashlight CONFIG REQUIRED)
if (FL_USE_CUDA)
  enable_language(CUDA)
endif()

if (NOT TARGET flashlight::flashlight-app-asr)
  message(FATAL_ERROR "flashlight must be build with app/asr for wav2letter++")
endif ()


# ------------------------- Dedicated SSL Train executable --------------------------
add_executable(
  Train_cpc
  CPCCriterion.cpp
  Train.cpp
)

add_executable(
  Decode_cpc
  CPCCriterion.cpp
  Decode.cpp
)

target_link_libraries(
  Train_cpc
  flashlight::flashlight-app-asr
)

target_link_libraries(
  Decode_cpc
  flashlight::flashlight-app-asr
)

