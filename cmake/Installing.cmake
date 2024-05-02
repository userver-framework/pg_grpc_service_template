include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

function(template_add_library)
    set(options)
    set(one_value_args LIB_NAME LIB_NAMESPACE)
    set(multi_value_args PUBLIC_HDRS SRCS)
    cmake_parse_arguments(TEMPLATE "${options}" "${one_value_args}" "${multi_value_args}" ${ARGN})
    
    add_library(${TEMPLATE_LIB_NAME})
    target_sources(${TEMPLATE_LIB_NAME} PRIVATE ${TEMPLATE_SRCS})
    target_include_directories(${TEMPLATE_LIB_NAME}
        PRIVATE
            # where the library itself will look for its internal headers
            ${CMAKE_CURRENT_SOURCE_DIR}/src
        PUBLIC
            # where top-level project will look for the library's public headers
            $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
            # where external projects will look for the library's public headers
            $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
    )
    set_target_properties(${TEMPLATE_LIB_NAME} PROPERTIES DEBUG_POSTFIX "-d")

    set_target_properties(${TEMPLATE_LIB_NAME} PROPERTIES PUBLIC_HEADER "${TEMPLATE_PUBLIC_HDRS}")

    install(TARGETS ${TEMPLATE_LIB_NAME}
        EXPORT "${TEMPLATE_LIB_NAME}Targets"
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${TEMPLATE_LIB_NAME}
        INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    )

    install(EXPORT "${TEMPLATE_LIB_NAME}Targets"
        FILE "${TEMPLATE_LIB_NAME}Targets.cmake"
        NAMESPACE ${TEMPLATE_LIB_NAMESPACE}::
        DESTINATION cmake
    )

    write_basic_package_version_file(
        "${CMAKE_CURRENT_BINARY_DIR}/${TEMPLATE_LIB_NAME}ConfigVersion.cmake"
        COMPATIBILITY AnyNewerVersion
    )
    configure_package_config_file(${PROJECT_SOURCE_DIR}/cmake/Config.cmake.in
        "${CMAKE_CURRENT_BINARY_DIR}/${TEMPLATE_LIB_NAME}Config.cmake"
        INSTALL_DESTINATION cmake
    )

    install(FILES
        "${CMAKE_CURRENT_BINARY_DIR}/${TEMPLATE_LIB_NAME}Config.cmake"
        "${CMAKE_CURRENT_BINARY_DIR}/${TEMPLATE_LIB_NAME}ConfigVersion.cmake"
        DESTINATION cmake
    )
endfunction()