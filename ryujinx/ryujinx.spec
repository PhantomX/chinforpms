%bcond_with bin
%bcond_without local_dotnet 1

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

# commit and Version must match https://github.com/Ryujinx/Ryujinx/wiki/Changelog
%global commit da073fce6127243fcd93b736cde951c4e835e508
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230314

%if %{without bin}
%bcond_with snapshot
%else
%bcond_without snapshot
%endif

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%else
%global shortcommit 0
%endif

%global local_dotnet_ver 8.0.203
%global local_dotnet_url_id 656a3402-6889-400f-927f-7f956856e58b/93750973d6eedd17c6d963658e7ec214

%global avalonia_angle_windows_natives_ver 2.1.0.2023020321
%global avalonia_ver 11.0.10
%global avalonia_ver2 11.0.4
%global avalonia_ver3 11.0.0
%global avalonia_build_services_ver 0.0.29
%global avalonia_svg_ver 11.0.0.18
%global concentus_ver 2.2.0
%global crc32_net_ver 1.2.0
%global discordrichpresence_ver 1.2.1.24
%global excss_ver 4.2.3
%global dynamicdata_ver 9.0.4
%global fluent_avalonia_ver 2.0.5
%global harfbuzzsharp_ver 7.3.0
%global harfbuzzsharp_ver2 2.8.2.3
%global libhac_ver 0.19.0
%global microcom_runtime_ver 0.11.0
# Must match dotnet
%global microsoft_aspnetcore_app_runtime_linux_x64_ver 8.0.3
%global microsoft_codeanalysis_analyzers_ver 3.3.4
%global microsoft_codeanalysis_analyzers_ver2 3.0.0
%global microsoft_codeanalysis_ver 4.9.2
%global microsoft_codeanalysis_ver2 3.8.0
%global microsoft_csharp_ver 4.5.0
%global microsoft_csharp_ver2 4.7.0
%global microsoft_csharp_ver3 4.3.0
%global microsoft_dotnet_platformabstractions_ver 3.1.6
%global microsoft_extensions_dependencymodel_ver 8.0.0
%global microsoft_identitymodel_ver 8.0.1
%global microsoft_io_recyclablememorystream_ver 3.0.1
# Must match dotnet
%global microsoft_netcore_app_runtime_linux_x64_ver 8.0.3
%global microsoft_netcore_platforms_ver 1.0.1
%global microsoft_netcore_platforms_ver2 1.1.0
%global microsoft_netcore_platforms_ver3 2.1.2
%global microsoft_netcore_platforms_ver4 2.0.0
%global microsoft_netcore_platforms_ver5 5.0.0
%global microsoft_netcore_targets_ver 1.0.1
%global microsoft_netcore_targets_ver2 1.1.0
%global microsoft_win32_primitives_ver 4.0.1
%global microsoft_win32_primitives_ver2 4.3.0
%global microsoft_win32_registry_ver 4.5.0
%global microsoft_win32_systemevents_ver 8.0.0
%global msgpack_cli_ver 1.0.1
%global netcoreserver_ver 8.0.7
%global netstandard_library_ver 1.6.0
%global netstandard_library_ver2 2.0.0
%global netstandard_library_ver3 2.0.3
%global newtonsoft_json_ver 13.0.1
%global opentk_ver 4.8.2
%global opentk_redist_glfw_ver 3.3.8.39
%global runtime_any_system_collections_ver 4.3.0
%global runtime_any_system_diagnostics_tools_ver 4.3.0
%global runtime_any_system_diagnostics_tracing_ver 4.3.0
%global runtime_any_system_globalization_ver 4.3.0
%global runtime_any_system_globalization_calendars_ver 4.3.0
%global runtime_any_system_io_ver 4.3.0
%global runtime_any_system_reflection_ver 4.3.0
%global runtime_any_system_reflection_extensions_ver 4.3.0
%global runtime_any_system_reflection_primitives_ver 4.3.0
%global runtime_any_system_resources_resourcemanager_ver 4.3.0
%global runtime_any_system_runtime_ver 4.3.0
%global runtime_any_system_runtime_handles_ver 4.3.0
%global runtime_any_system_runtime_interopservices_ver 4.3.0
%global runtime_any_system_text_encoding_ver 4.3.0
%global runtime_any_system_text_encoding_extensions_ver 4.3.0
%global runtime_any_system_threading_tasks_ver 4.3.0
%global runtime_any_system_threading_timer_ver 4.3.0
%global runtime_debian_8_x64_runtime_native_system_security_cryptography_openssl_ver 4.3.0
%global runtime_fedora_23_x64_runtime_native_system_security_cryptography_openssl_ver 4.3.0
%global runtime_fedora_24_x64_runtime_native_system_security_cryptography_openssl_ver 4.3.0
%global runtime_native_system_ver 4.0.0
%global runtime_native_system_ver2 4.3.0
%global runtime_native_system_io_compression_ver 4.1.0
%global runtime_native_system_net_http_ver 4.0.1
%global runtime_native_system_security_cryptography_ver 4.0.0
%global runtime_native_system_security_cryptography_openssl_ver 4.3.0
%global runtime_opensuse_13_2_x64_runtime_native_system_security_cryptography_openssl_ver 4.3.0
%global runtime_opensuse_42_1_x64_runtime_native_system_security_cryptography_openssl_ver 4.3.0
%global runtime_osx_10_10_x64_runtime_native_system_security_cryptography_openssl_ver 4.3.0
%global runtime_rhel_7_x64_runtime_native_system_security_cryptography_openssl_ver 4.3.0
%global runtime_ubuntu_14_04_x64_runtime_native_system_security_cryptography_openssl_ver 4.3.0
%global runtime_ubuntu_16_04_x64_runtime_native_system_security_cryptography_openssl_ver 4.3.0
%global runtime_ubuntu_16_10_x64_runtime_native_system_security_cryptography_openssl_ver 4.3.0
%global runtime_unix_microsoft_win32_primitives_ver 4.3.0
%global runtime_unix_system_console_ver 4.3.0
%global runtime_unix_system_diagnostics_debug_ver 4.3.0
%global runtime_unix_system_io_filesystem_ver 4.3.0
%global runtime_unix_system_net_primitives_ver 4.3.0
%global runtime_unix_system_net_sockets_ver 4.3.0
%global runtime_unix_system_private_uri_ver 4.3.0
%global runtime_unix_system_runtime_extensions_ver 4.3.0
%global ryujinx_audio_openal_dependencies_ver 1.21.0.1
%global ryujinx_graphics_nvdec_dependencies_ver 5.0.3-build14
%global ryujinx_graphics_nvdec_dependencies_osx_ver 5.0.1
%global ryujinx_graphics_vulkan_dependencies_moltenvk_ver 1.2.0
%global ryujinx_sdl2_cs_ver 2.30.0-build32
%global securifybv_ver 0.1.0
%global shaderc_net_ver 0.1.0
%global sharpziplib_ver 1.4.2
%global silk_net_ver 2.21.0
%global sixlabors_fonts_ver 1.0.0
%global sixlabors_imagesharp_ver 2.1.9
%global sixlabors_imagesharp_drawing_ver 1.0.0
%global skiasharp_ver 2.88.7
%global skiasharp_ver2 2.88.6
%global skiasharp_ver3 2.88.3
%global spb_ver 0.0.4-build32
%global svg_model_ver 1.0.0.18
%global system_appcontext_ver 4.1.0
%global system_buffers_ver 4.0.0
%global system_buffers_ver2 4.3.0
%global system_buffers_ver3 4.5.1
%global system_codedom_ver 4.4.0
%global system_codedom_ver2 8.0.0
%global system_collections_ver 4.0.11
%global system_collections_ver2 4.3.0
%global system_collections_concurrent_ver 4.0.12
%global system_collections_immutable_ver 8.0.0
%global system_collections_immutable_ver2 5.0.0
%global system_componentmodel_annotations_ver 4.5.0
%global system_console_ver 4.0.0
%global system_diagnostics_debug_ver 4.0.11
%global system_diagnostics_debug_ver2 4.3.0
%global system_diagnostics_diagnosticsource_ver 4.0.0
%global system_diagnostics_tools_ver 4.0.1
%global system_diagnostics_tracing_ver 4.1.0
%global system_diagnostics_tracing_ver2 4.3.0
%global system_drawing_common_ver 8.0.2
%global system_globalization_ver 4.0.11
%global system_globalization_ver2 4.3.0
%global system_globalization_calendars_ver 4.0.1
%global system_globalization_extensions_ver 4.0.1
%global system_io_ver 4.1.0
%global system_io_ver2 4.3.0
%global system_io_compression_ver 4.1.0
%global system_io_compression_zipfile_ver 4.0.1
%global system_io_filesystem_ver 4.0.1
%global system_io_filesystem_primitives_ver 4.0.1
%global system_io_hashing 8.0.0
%global system_io_pipelines_ver 6.0.0
%global system_linq_ver 4.1.0
%global system_linq_expressions_ver 4.1.0
%global system_management_ver 8.0.0
%global system_memory_ver 4.5.5
%global system_memory_ver2 4.5.4
%global system_net_http_ver 4.1.0
%global system_net_nameresolution_ver 4.3.0
%global system_net_primitives_ver 4.0.11
%global system_net_sockets_ver 4.1.0
%global system_numerics_vectors_ver 4.3.0
%global system_numerics_vectors_ver2 4.4.0
%global system_numerics_vectors_ver3 4.5.0
%global system_objectmodel_ver 4.0.12
%global system_private_uri_ver 4.3.0
%global system_reactive_ver 6.0.1
%global system_reflection_ver 4.1.0
%global system_reflection_ver2 4.3.0
%global system_reflection_emit_ver 4.0.1
%global system_reflection_emit_ver2 4.3.0
%global system_reflection_emit_ilgeneration_ver 4.0.1
%global system_reflection_emit_ilgeneration_ver2 4.3.0
%global system_reflection_emit_lightweight_ver 4.0.1
%global system_reflection_emit_lightweight_ver2 4.3.0
%global system_reflection_extensions_ver 4.0.1
%global system_reflection_metadata_ver 8.0.0
%global system_reflection_metadata_ver2 5.0.0
%global system_reflection_primitives_ver 4.0.1
%global system_reflection_primitives_ver2 4.3.0
%global system_reflection_typeextensions_ver 4.1.0
%global system_resources_resourcemanager_ver 4.0.1
%global system_resources_resourcemanager_ver2 4.3.0
%global system_runtime_ver 4.1.0
%global system_runtime_ver2 4.3.0
%global system_runtime_compilerservices_unsafe_ver 4.7.0
%global system_runtime_compilerservices_unsafe_ver2 5.0.0
%global system_runtime_compilerservices_unsafe_ver3 6.0.0
%global system_runtime_compilerservices_unsafe_ver4 4.7.1
%global system_runtime_extensions_ver 4.1.0
%global system_runtime_extensions_ver2 4.3.0
%global system_runtime_handles_ver 4.0.1
%global system_runtime_handles_ver2 4.3.0
%global system_runtime_interopservices_ver 4.1.0
%global system_runtime_interopservices_ver2 4.3.0
%global system_runtime_interopservices_runtimeinformation_ver 4.0.0
%global system_runtime_numerics_ver 4.0.1
%global system_security_accesscontrol_ver 4.5.0
%global system_security_claims_ver 4.3.0
%global system_security_cryptography_algorithms_ver 4.2.0
%global system_security_cryptography_cng_ver 4.2.0
%global system_security_cryptography_cng_ver2 4.5.0
%global system_security_cryptography_csp_ver 4.0.0
%global system_security_cryptography_encoding_ver 4.0.0
%global system_security_cryptography_openssl_ver 4.0.0
%global system_security_cryptography_primitives_ver 4.0.0
%global system_security_cryptography_x509certificates_ver 4.1.0
%global system_security_principal_ver 4.3.0
%global system_security_principal_windows_ver 4.3.0
%global system_security_principal_windows_ver2 4.5.0
%global system_text_encoding_ver 4.0.11
%global system_text_encoding_ver2 4.3.0
%global system_text_encoding_codepages_ver 8.0.0
%global system_text_encoding_codepages_ver2 5.0.0
%global system_text_encoding_codepages_ver3 4.5.1
%global system_text_encoding_extensions_ver 4.0.11
%global system_text_encodings_web_ver 8.0.0
%global system_text_encodings_web_ver2 4.7.2
%global system_text_json_ver 8.0.0
%global system_text_json_ver2 4.7.2
%global system_text_regularexpressions_ver 4.1.0
%global system_threading_ver 4.0.11
%global system_threading_ver2 4.3.0
%global system_threading_tasks_ver 4.0.11
%global system_threading_tasks_ver2 4.3.0
%global system_threading_tasks_extensions_ver 4.0.0
%global system_threading_tasks_extensions_ver2 4.5.4
%global system_threading_threadpool_ver 4.3.0
%global system_threading_timer_ver 4.0.1
%global system_xml_readerwriter_ver 4.0.11
%global system_xml_xdocument_ver 4.0.11
%global tmds_dbus_protocol_ver 0.15.0

%global appname Ryujinx
%global vc_url  https://github.com/%{appname}
%global nuget_url https://globalcdn.nuget.org/packages

Name:           ryujinx
Version:        1.1.1400
Release:        1%{?dist}
Summary:        Experimental Nintendo Switch Emulator

License:        MIT
URL:            https://ryujinx.org/

%if %{with bin}
Source0:        %{vc_url}/release-channel-master/releases/download/%{version}/%{name}-%{version}-linux_x64.tar.gz
Source1:        %{vc_url}/%{appname}/raw/%{commit}/LICENSE.txt
Source2:        %{vc_url}/%{appname}/raw/%{commit}/README.md
Source3:        %{vc_url}/%{appname}/raw/%{commit}/distribution/linux/%{name}.desktop
Source4:        %{vc_url}/%{appname}/raw/%{commit}/distribution/misc/Logo.svg#/%{name}-Logo.svg
%else
%if %{with snapshot}
Source0:        %{vc_url}/%{appname}/archive/%{commit}/%{appname}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/%{appname}/archive/%{version}/%{appname}-%{version}.tar.gz
%endif
%if %{with local_dotnet}
Source199:      https://download.visualstudio.microsoft.com/download/pr/%{local_dotnet_url_id}/dotnet-sdk-%{local_dotnet_ver}-linux-x64.tar.gz
%endif
Source200:      %{nuget_url}/avalonia.angle.windows.natives.%{avalonia_angle_windows_natives_ver}.nupkg
Source201:      %{nuget_url}/avalonia.%{avalonia_ver}.nupkg
Source202:      %{nuget_url}/avalonia.buildservices.%{avalonia_build_services_ver}.nupkg
Source203:      %{nuget_url}/avalonia.controls.colorpicker.%{avalonia_ver2}.nupkg
Source204:      %{nuget_url}/avalonia.controls.colorpicker.%{avalonia_ver}.nupkg
Source205:      %{nuget_url}/avalonia.controls.datagrid.%{avalonia_ver}.nupkg
Source206:      %{nuget_url}/avalonia.controls.itemsrepeater.%{avalonia_ver2}.nupkg
Source207:      %{nuget_url}/avalonia.desktop.%{avalonia_ver}.nupkg
Source208:      %{nuget_url}/avalonia.diagnostics.%{avalonia_ver}.nupkg
Source209:      %{nuget_url}/avalonia.freedesktop.%{avalonia_ver}.nupkg
Source210:      %{nuget_url}/avalonia.markup.xaml.loader.%{avalonia_ver}.nupkg
Source211:      %{nuget_url}/avalonia.native.%{avalonia_ver}.nupkg
Source212:      %{nuget_url}/avalonia.remote.protocol.%{avalonia_ver2}.nupkg
Source213:      %{nuget_url}/avalonia.remote.protocol.%{avalonia_ver}.nupkg
Source214:      %{nuget_url}/avalonia.skia.%{avalonia_ver2}.nupkg
Source215:      %{nuget_url}/avalonia.skia.%{avalonia_ver3}.nupkg
Source216:      %{nuget_url}/avalonia.skia.%{avalonia_ver}.nupkg
Source217:      %{nuget_url}/avalonia.svg.%{avalonia_svg_ver}.nupkg
Source218:      %{nuget_url}/avalonia.svg.skia.%{avalonia_svg_ver}.nupkg
Source219:      %{nuget_url}/avalonia.themes.simple.%{avalonia_ver2}.nupkg
Source220:      %{nuget_url}/avalonia.themes.simple.%{avalonia_ver}.nupkg
Source221:      %{nuget_url}/avalonia.win32.%{avalonia_ver}.nupkg
Source222:      %{nuget_url}/avalonia.x11.%{avalonia_ver}.nupkg
Source223:      %{nuget_url}/concentus.%{concentus_ver}.nupkg
Source224:      %{nuget_url}/discordrichpresence.%{discordrichpresence_ver}.nupkg
Source225:      %{nuget_url}/dynamicdata.%{dynamicdata_ver}.nupkg
Source226:      %{nuget_url}/excss.%{excss_ver}.nupkg
Source227:      %{nuget_url}/fluentavaloniaui.%{fluent_avalonia_ver}.nupkg
Source228:      %{nuget_url}/harfbuzzsharp.%{harfbuzzsharp_ver2}.nupkg
Source229:      %{nuget_url}/harfbuzzsharp.%{harfbuzzsharp_ver}.nupkg
Source230:      %{nuget_url}/harfbuzzsharp.nativeassets.linux.%{harfbuzzsharp_ver2}.nupkg
Source231:      %{nuget_url}/harfbuzzsharp.nativeassets.linux.%{harfbuzzsharp_ver}.nupkg
Source232:      %{nuget_url}/harfbuzzsharp.nativeassets.macos.%{harfbuzzsharp_ver2}.nupkg
Source233:      %{nuget_url}/harfbuzzsharp.nativeassets.macos.%{harfbuzzsharp_ver}.nupkg
Source234:      %{nuget_url}/harfbuzzsharp.nativeassets.webassembly.%{harfbuzzsharp_ver2}.nupkg
Source235:      %{nuget_url}/harfbuzzsharp.nativeassets.webassembly.%{harfbuzzsharp_ver}.nupkg
Source236:      %{nuget_url}/harfbuzzsharp.nativeassets.win32.%{harfbuzzsharp_ver2}.nupkg
Source237:      %{nuget_url}/harfbuzzsharp.nativeassets.win32.%{harfbuzzsharp_ver}.nupkg
Source238:      %{nuget_url}/libhac.%{libhac_ver}.nupkg
Source239:      %{nuget_url}/microcom.codegenerator.msbuild.%{microcom_runtime_ver}.nupkg
Source240:      %{nuget_url}/microcom.runtime.%{microcom_runtime_ver}.nupkg
Source241:      %{nuget_url}/microsoft.aspnetcore.app.runtime.linux-x64.%{microsoft_aspnetcore_app_runtime_linux_x64_ver}.nupkg
Source242:      %{nuget_url}/microsoft.codeanalysis.analyzers.%{microsoft_codeanalysis_analyzers_ver2}.nupkg
Source243:      %{nuget_url}/microsoft.codeanalysis.analyzers.%{microsoft_codeanalysis_analyzers_ver}.nupkg
Source244:      %{nuget_url}/microsoft.codeanalysis.common.%{microsoft_codeanalysis_ver2}.nupkg
Source245:      %{nuget_url}/microsoft.codeanalysis.common.%{microsoft_codeanalysis_ver}.nupkg
Source246:      %{nuget_url}/microsoft.codeanalysis.csharp.%{microsoft_codeanalysis_ver2}.nupkg
Source247:      %{nuget_url}/microsoft.codeanalysis.csharp.%{microsoft_codeanalysis_ver}.nupkg
Source248:      %{nuget_url}/microsoft.codeanalysis.csharp.scripting.%{microsoft_codeanalysis_ver2}.nupkg
Source249:      %{nuget_url}/microsoft.codeanalysis.scripting.common.%{microsoft_codeanalysis_ver2}.nupkg
Source250:      %{nuget_url}/microsoft.csharp.%{microsoft_csharp_ver2}.nupkg
Source251:      %{nuget_url}/microsoft.csharp.%{microsoft_csharp_ver3}.nupkg
Source252:      %{nuget_url}/microsoft.csharp.%{microsoft_csharp_ver}.nupkg
Source253:      %{nuget_url}/microsoft.dotnet.platformabstractions.%{microsoft_dotnet_platformabstractions_ver}.nupkg
Source254:      %{nuget_url}/microsoft.extensions.dependencymodel.%{microsoft_extensions_dependencymodel_ver}.nupkg
Source255:      %{nuget_url}/microsoft.identitymodel.abstractions.%{microsoft_identitymodel_ver}.nupkg
Source256:      %{nuget_url}/microsoft.identitymodel.jsonwebtokens.%{microsoft_identitymodel_ver}.nupkg
Source257:      %{nuget_url}/microsoft.identitymodel.logging.%{microsoft_identitymodel_ver}.nupkg
Source258:      %{nuget_url}/microsoft.identitymodel.tokens.%{microsoft_identitymodel_ver}.nupkg
Source259:      %{nuget_url}/microsoft.io.recyclablememorystream.%{microsoft_io_recyclablememorystream_ver}.nupkg
Source260:      %{nuget_url}/microsoft.netcore.app.runtime.linux-x64.%{microsoft_netcore_app_runtime_linux_x64_ver}.nupkg
Source261:      %{nuget_url}/microsoft.netcore.platforms.%{microsoft_netcore_platforms_ver2}.nupkg
Source262:      %{nuget_url}/microsoft.netcore.platforms.%{microsoft_netcore_platforms_ver3}.nupkg
Source263:      %{nuget_url}/microsoft.netcore.platforms.%{microsoft_netcore_platforms_ver4}.nupkg
Source264:      %{nuget_url}/microsoft.netcore.platforms.%{microsoft_netcore_platforms_ver}.nupkg
Source265:      %{nuget_url}/microsoft.netcore.targets.%{microsoft_netcore_targets_ver2}.nupkg
Source266:      %{nuget_url}/microsoft.netcore.targets.%{microsoft_netcore_targets_ver}.nupkg
Source267:      %{nuget_url}/microsoft.win32.primitives.%{microsoft_win32_primitives_ver2}.nupkg
Source268:      %{nuget_url}/microsoft.win32.primitives.%{microsoft_win32_primitives_ver}.nupkg
Source269:      %{nuget_url}/microsoft.win32.registry.%{microsoft_win32_registry_ver}.nupkg
Source270:      %{nuget_url}/microsoft.win32.systemevents.%{microsoft_win32_systemevents_ver}.nupkg
Source271:      %{nuget_url}/msgpack.cli.%{msgpack_cli_ver}.nupkg
Source272:      %{nuget_url}/netcoreserver.%{netcoreserver_ver}.nupkg
Source273:      %{nuget_url}/netstandard.library.%{netstandard_library_ver2}.nupkg
Source274:      %{nuget_url}/netstandard.library.%{netstandard_library_ver3}.nupkg
Source275:      %{nuget_url}/netstandard.library.%{netstandard_library_ver}.nupkg
Source276:      %{nuget_url}/newtonsoft.json.%{newtonsoft_json_ver}.nupkg
Source277:      %{nuget_url}/opentk.audio.openal.%{opentk_ver}.nupkg
Source278:      %{nuget_url}/opentk.core.%{opentk_ver}.nupkg
Source279:      %{nuget_url}/opentk.graphics.%{opentk_ver}.nupkg
Source280:      %{nuget_url}/opentk.mathematics.%{opentk_ver}.nupkg
Source281:      %{nuget_url}/opentk.redist.glfw.%{opentk_redist_glfw_ver}.nupkg
Source282:      %{nuget_url}/opentk.windowing.graphicslibraryframework.%{opentk_ver}.nupkg
Source283:      %{nuget_url}/runtime.any.system.collections.%{runtime_any_system_collections_ver}.nupkg
Source284:      %{nuget_url}/runtime.any.system.diagnostics.tools.%{runtime_any_system_diagnostics_tools_ver}.nupkg
Source285:      %{nuget_url}/runtime.any.system.diagnostics.tracing.%{runtime_any_system_diagnostics_tracing_ver}.nupkg
Source286:      %{nuget_url}/runtime.any.system.globalization.calendars.%{runtime_any_system_globalization_calendars_ver}.nupkg
Source287:      %{nuget_url}/runtime.any.system.globalization.%{runtime_any_system_globalization_ver}.nupkg
Source288:      %{nuget_url}/runtime.any.system.io.%{runtime_any_system_io_ver}.nupkg
Source289:      %{nuget_url}/runtime.any.system.reflection.extensions.%{runtime_any_system_reflection_extensions_ver}.nupkg
Source290:      %{nuget_url}/runtime.any.system.reflection.primitives.%{runtime_any_system_reflection_primitives_ver}.nupkg
Source291:      %{nuget_url}/runtime.any.system.reflection.%{runtime_any_system_reflection_ver}.nupkg
Source292:      %{nuget_url}/runtime.any.system.resources.resourcemanager.%{runtime_any_system_resources_resourcemanager_ver}.nupkg
Source293:      %{nuget_url}/runtime.any.system.runtime.handles.%{runtime_any_system_runtime_handles_ver}.nupkg
Source294:      %{nuget_url}/runtime.any.system.runtime.interopservices.%{runtime_any_system_runtime_interopservices_ver}.nupkg
Source295:      %{nuget_url}/runtime.any.system.runtime.%{runtime_any_system_runtime_ver}.nupkg
Source296:      %{nuget_url}/runtime.any.system.text.encoding.extensions.%{runtime_any_system_text_encoding_extensions_ver}.nupkg
Source297:      %{nuget_url}/runtime.any.system.text.encoding.%{runtime_any_system_text_encoding_ver}.nupkg
Source298:      %{nuget_url}/runtime.any.system.threading.tasks.%{runtime_any_system_threading_tasks_ver}.nupkg
Source299:      %{nuget_url}/runtime.any.system.threading.timer.%{runtime_any_system_threading_timer_ver}.nupkg
Source300:      %{nuget_url}/runtime.debian.8-x64.runtime.native.system.security.cryptography.openssl.%{runtime_debian_8_x64_runtime_native_system_security_cryptography_openssl_ver}.nupkg
Source301:      %{nuget_url}/runtime.fedora.23-x64.runtime.native.system.security.cryptography.openssl.%{runtime_fedora_23_x64_runtime_native_system_security_cryptography_openssl_ver}.nupkg
Source302:      %{nuget_url}/runtime.fedora.24-x64.runtime.native.system.security.cryptography.openssl.%{runtime_fedora_24_x64_runtime_native_system_security_cryptography_openssl_ver}.nupkg
Source303:      %{nuget_url}/runtime.native.system.io.compression.%{runtime_native_system_io_compression_ver}.nupkg
Source304:      %{nuget_url}/runtime.native.system.net.http.%{runtime_native_system_net_http_ver}.nupkg
Source305:      %{nuget_url}/runtime.native.system.%{runtime_native_system_ver2}.nupkg
Source306:      %{nuget_url}/runtime.native.system.%{runtime_native_system_ver}.nupkg
Source307:      %{nuget_url}/runtime.native.system.security.cryptography.openssl.%{runtime_native_system_security_cryptography_openssl_ver}.nupkg
Source308:      %{nuget_url}/runtime.native.system.security.cryptography.%{runtime_native_system_security_cryptography_ver}.nupkg
Source309:      %{nuget_url}/runtime.opensuse.13.2-x64.runtime.native.system.security.cryptography.openssl.%{runtime_opensuse_13_2_x64_runtime_native_system_security_cryptography_openssl_ver}.nupkg
Source310:      %{nuget_url}/runtime.opensuse.42.1-x64.runtime.native.system.security.cryptography.openssl.%{runtime_opensuse_42_1_x64_runtime_native_system_security_cryptography_openssl_ver}.nupkg
Source311:      %{nuget_url}/runtime.osx.10.10-x64.runtime.native.system.security.cryptography.openssl.%{runtime_osx_10_10_x64_runtime_native_system_security_cryptography_openssl_ver}.nupkg
Source312:      %{nuget_url}/runtime.rhel.7-x64.runtime.native.system.security.cryptography.openssl.%{runtime_rhel_7_x64_runtime_native_system_security_cryptography_openssl_ver}.nupkg
Source313:      %{nuget_url}/runtime.ubuntu.14.04-x64.runtime.native.system.security.cryptography.openssl.%{runtime_ubuntu_14_04_x64_runtime_native_system_security_cryptography_openssl_ver}.nupkg
Source314:      %{nuget_url}/runtime.ubuntu.16.04-x64.runtime.native.system.security.cryptography.openssl.%{runtime_ubuntu_16_04_x64_runtime_native_system_security_cryptography_openssl_ver}.nupkg
Source315:      %{nuget_url}/runtime.ubuntu.16.10-x64.runtime.native.system.security.cryptography.openssl.%{runtime_ubuntu_16_10_x64_runtime_native_system_security_cryptography_openssl_ver}.nupkg
Source316:      %{nuget_url}/runtime.unix.microsoft.win32.primitives.%{runtime_unix_microsoft_win32_primitives_ver}.nupkg
Source317:      %{nuget_url}/runtime.unix.system.console.%{runtime_unix_system_console_ver}.nupkg
Source318:      %{nuget_url}/runtime.unix.system.diagnostics.debug.%{runtime_unix_system_diagnostics_debug_ver}.nupkg
Source319:      %{nuget_url}/runtime.unix.system.io.filesystem.%{runtime_unix_system_io_filesystem_ver}.nupkg
Source320:      %{nuget_url}/runtime.unix.system.net.primitives.%{runtime_unix_system_net_primitives_ver}.nupkg
Source321:      %{nuget_url}/runtime.unix.system.net.sockets.%{runtime_unix_system_net_sockets_ver}.nupkg
Source322:      %{nuget_url}/runtime.unix.system.private.uri.%{runtime_unix_system_private_uri_ver}.nupkg
Source323:      %{nuget_url}/runtime.unix.system.runtime.extensions.%{runtime_unix_system_runtime_extensions_ver}.nupkg
Source324:      %{nuget_url}/ryujinx.audio.openal.dependencies.%{ryujinx_audio_openal_dependencies_ver}.nupkg
Source325:      %{nuget_url}/ryujinx.graphics.nvdec.dependencies.%{ryujinx_graphics_nvdec_dependencies_ver}.nupkg
Source326:      %{nuget_url}/ryujinx.graphics.vulkan.dependencies.moltenvk.%{ryujinx_graphics_vulkan_dependencies_moltenvk_ver}.nupkg
Source327:      %{nuget_url}/ryujinx.sdl2-cs.%{ryujinx_sdl2_cs_ver}.nupkg
Source328:      %{nuget_url}/securifybv.propertystore.%{securifybv_ver}.nupkg
Source329:      %{nuget_url}/securifybv.shelllink.%{securifybv_ver}.nupkg
Source330:      %{nuget_url}/shaderc.net.%{shaderc_net_ver}.nupkg
Source331:      %{nuget_url}/sharpziplib.%{sharpziplib_ver}.nupkg
Source332:      %{nuget_url}/shimskiasharp.%{svg_model_ver}.nupkg
Source333:      %{nuget_url}/silk.net.core.%{silk_net_ver}.nupkg
Source334:      %{nuget_url}/silk.net.vulkan.extensions.ext.%{silk_net_ver}.nupkg
Source335:      %{nuget_url}/silk.net.vulkan.extensions.khr.%{silk_net_ver}.nupkg
Source336:      %{nuget_url}/silk.net.vulkan.%{silk_net_ver}.nupkg
Source337:      %{nuget_url}/sixlabors.fonts.%{sixlabors_fonts_ver}.nupkg
Source338:      %{nuget_url}/sixlabors.imagesharp.drawing.%{sixlabors_imagesharp_drawing_ver}.nupkg
Source339:      %{nuget_url}/sixlabors.imagesharp.%{sixlabors_imagesharp_ver}.nupkg
Source340:      %{nuget_url}/skiasharp.harfbuzz.%{skiasharp_ver2}.nupkg
Source341:      %{nuget_url}/skiasharp.nativeassets.linux.%{skiasharp_ver3}.nupkg
Source342:      %{nuget_url}/skiasharp.nativeassets.linux.%{skiasharp_ver}.nupkg
Source343:      %{nuget_url}/skiasharp.nativeassets.macos.%{skiasharp_ver2}.nupkg
Source344:      %{nuget_url}/skiasharp.nativeassets.macos.%{skiasharp_ver3}.nupkg
Source345:      %{nuget_url}/skiasharp.nativeassets.macos.%{skiasharp_ver}.nupkg
Source346:      %{nuget_url}/skiasharp.nativeassets.webassembly.%{skiasharp_ver3}.nupkg
Source347:      %{nuget_url}/skiasharp.nativeassets.webassembly.%{skiasharp_ver}.nupkg
Source348:      %{nuget_url}/skiasharp.nativeassets.win32.%{skiasharp_ver2}.nupkg
Source349:      %{nuget_url}/skiasharp.nativeassets.win32.%{skiasharp_ver3}.nupkg
Source350:      %{nuget_url}/skiasharp.nativeassets.win32.%{skiasharp_ver}.nupkg
Source351:      %{nuget_url}/skiasharp.%{skiasharp_ver2}.nupkg
Source352:      %{nuget_url}/skiasharp.%{skiasharp_ver3}.nupkg
Source353:      %{nuget_url}/skiasharp.%{skiasharp_ver}.nupkg
Source354:      %{nuget_url}/spb.%{spb_ver}.nupkg
Source355:      %{nuget_url}/svg.custom.%{svg_model_ver}.nupkg
Source356:      %{nuget_url}/svg.model.%{svg_model_ver}.nupkg
Source357:      %{nuget_url}/svg.skia.%{svg_model_ver}.nupkg
Source358:      %{nuget_url}/system.appcontext.%{system_appcontext_ver}.nupkg
Source359:      %{nuget_url}/system.buffers.%{system_buffers_ver2}.nupkg
Source360:      %{nuget_url}/system.buffers.%{system_buffers_ver3}.nupkg
Source361:      %{nuget_url}/system.buffers.%{system_buffers_ver}.nupkg
Source362:      %{nuget_url}/system.codedom.%{system_codedom_ver2}.nupkg
Source363:      %{nuget_url}/system.codedom.%{system_codedom_ver}.nupkg
Source364:      %{nuget_url}/system.collections.concurrent.%{system_collections_concurrent_ver}.nupkg
Source365:      %{nuget_url}/system.collections.immutable.%{system_collections_immutable_ver2}.nupkg
Source366:      %{nuget_url}/system.collections.immutable.%{system_collections_immutable_ver}.nupkg
Source367:      %{nuget_url}/system.collections.%{system_collections_ver2}.nupkg
Source368:      %{nuget_url}/system.collections.%{system_collections_ver}.nupkg
Source369:      %{nuget_url}/system.componentmodel.annotations.%{system_componentmodel_annotations_ver}.nupkg
Source370:      %{nuget_url}/system.console.%{system_console_ver}.nupkg
Source371:      %{nuget_url}/system.diagnostics.debug.%{system_diagnostics_debug_ver2}.nupkg
Source372:      %{nuget_url}/system.diagnostics.debug.%{system_diagnostics_debug_ver}.nupkg
Source373:      %{nuget_url}/system.diagnostics.diagnosticsource.%{system_diagnostics_diagnosticsource_ver}.nupkg
Source374:      %{nuget_url}/system.diagnostics.tools.%{system_diagnostics_tools_ver}.nupkg
Source375:      %{nuget_url}/system.diagnostics.tracing.%{system_diagnostics_tracing_ver2}.nupkg
Source376:      %{nuget_url}/system.diagnostics.tracing.%{system_diagnostics_tracing_ver}.nupkg
Source377:      %{nuget_url}/system.drawing.common.%{system_drawing_common_ver}.nupkg
Source378:      %{nuget_url}/system.globalization.calendars.%{system_globalization_calendars_ver}.nupkg
Source379:      %{nuget_url}/system.globalization.extensions.%{system_globalization_extensions_ver}.nupkg
Source380:      %{nuget_url}/system.globalization.%{system_globalization_ver2}.nupkg
Source381:      %{nuget_url}/system.globalization.%{system_globalization_ver}.nupkg
Source382:      %{nuget_url}/system.io.compression.%{system_io_compression_ver}.nupkg
Source383:      %{nuget_url}/system.io.compression.zipfile.%{system_io_compression_zipfile_ver}.nupkg
Source384:      %{nuget_url}/system.io.filesystem.primitives.%{system_io_filesystem_primitives_ver}.nupkg
Source385:      %{nuget_url}/system.io.filesystem.%{system_io_filesystem_ver}.nupkg
Source386:      %{nuget_url}/system.io.hashing.%{system_io_hashing}.nupkg
Source387:      %{nuget_url}/system.io.pipelines.%{system_io_pipelines_ver}.nupkg
Source388:      %{nuget_url}/system.io.%{system_io_ver2}.nupkg
Source389:      %{nuget_url}/system.io.%{system_io_ver}.nupkg
Source390:      %{nuget_url}/system.linq.expressions.%{system_linq_expressions_ver}.nupkg
Source391:      %{nuget_url}/system.linq.%{system_linq_ver}.nupkg
Source392:      %{nuget_url}/system.management.%{system_management_ver}.nupkg
Source393:      %{nuget_url}/system.memory.%{system_memory_ver2}.nupkg
Source394:      %{nuget_url}/system.memory.%{system_memory_ver}.nupkg
Source395:      %{nuget_url}/system.net.http.%{system_net_http_ver}.nupkg
Source396:      %{nuget_url}/system.net.nameresolution.%{system_net_nameresolution_ver}.nupkg
Source397:      %{nuget_url}/system.net.primitives.%{system_net_primitives_ver}.nupkg
Source398:      %{nuget_url}/system.net.sockets.%{system_net_sockets_ver}.nupkg
Source399:      %{nuget_url}/system.numerics.vectors.%{system_numerics_vectors_ver2}.nupkg
Source400:      %{nuget_url}/system.numerics.vectors.%{system_numerics_vectors_ver3}.nupkg
Source401:      %{nuget_url}/system.numerics.vectors.%{system_numerics_vectors_ver}.nupkg
Source402:      %{nuget_url}/system.objectmodel.%{system_objectmodel_ver}.nupkg
Source403:      %{nuget_url}/system.private.uri.%{system_private_uri_ver}.nupkg
Source404:      %{nuget_url}/system.reactive.%{system_reactive_ver}.nupkg
Source405:      %{nuget_url}/system.reflection.emit.ilgeneration.%{system_reflection_emit_ilgeneration_ver2}.nupkg
Source406:      %{nuget_url}/system.reflection.emit.ilgeneration.%{system_reflection_emit_ilgeneration_ver}.nupkg
Source407:      %{nuget_url}/system.reflection.emit.lightweight.%{system_reflection_emit_lightweight_ver2}.nupkg
Source408:      %{nuget_url}/system.reflection.emit.lightweight.%{system_reflection_emit_lightweight_ver}.nupkg
Source409:      %{nuget_url}/system.reflection.emit.%{system_reflection_emit_ver2}.nupkg
Source410:      %{nuget_url}/system.reflection.emit.%{system_reflection_emit_ver}.nupkg
Source411:      %{nuget_url}/system.reflection.extensions.%{system_reflection_extensions_ver}.nupkg
Source412:      %{nuget_url}/system.reflection.metadata.%{system_reflection_metadata_ver2}.nupkg
Source413:      %{nuget_url}/system.reflection.metadata.%{system_reflection_metadata_ver}.nupkg
Source414:      %{nuget_url}/system.reflection.primitives.%{system_reflection_primitives_ver2}.nupkg
Source415:      %{nuget_url}/system.reflection.primitives.%{system_reflection_primitives_ver}.nupkg
Source416:      %{nuget_url}/system.reflection.%{system_reflection_ver2}.nupkg
Source417:      %{nuget_url}/system.reflection.%{system_reflection_ver}.nupkg
Source418:      %{nuget_url}/system.reflection.typeextensions.%{system_reflection_typeextensions_ver}.nupkg
Source419:      %{nuget_url}/system.resources.resourcemanager.%{system_resources_resourcemanager_ver2}.nupkg
Source420:      %{nuget_url}/system.resources.resourcemanager.%{system_resources_resourcemanager_ver}.nupkg
Source421:      %{nuget_url}/system.runtime.compilerservices.unsafe.%{system_runtime_compilerservices_unsafe_ver2}.nupkg
Source422:      %{nuget_url}/system.runtime.compilerservices.unsafe.%{system_runtime_compilerservices_unsafe_ver3}.nupkg
Source423:      %{nuget_url}/system.runtime.compilerservices.unsafe.%{system_runtime_compilerservices_unsafe_ver4}.nupkg
Source424:      %{nuget_url}/system.runtime.compilerservices.unsafe.%{system_runtime_compilerservices_unsafe_ver}.nupkg
Source425:      %{nuget_url}/system.runtime.extensions.%{system_runtime_extensions_ver2}.nupkg
Source426:      %{nuget_url}/system.runtime.extensions.%{system_runtime_extensions_ver}.nupkg
Source427:      %{nuget_url}/system.runtime.handles.%{system_runtime_handles_ver2}.nupkg
Source428:      %{nuget_url}/system.runtime.handles.%{system_runtime_handles_ver}.nupkg
Source429:      %{nuget_url}/system.runtime.interopservices.runtimeinformation.%{system_runtime_interopservices_runtimeinformation_ver}.nupkg
Source430:      %{nuget_url}/system.runtime.interopservices.%{system_runtime_interopservices_ver2}.nupkg
Source431:      %{nuget_url}/system.runtime.interopservices.%{system_runtime_interopservices_ver}.nupkg
Source432:      %{nuget_url}/system.runtime.numerics.%{system_runtime_numerics_ver}.nupkg
Source433:      %{nuget_url}/system.runtime.%{system_runtime_ver2}.nupkg
Source434:      %{nuget_url}/system.runtime.%{system_runtime_ver}.nupkg
Source435:      %{nuget_url}/system.security.accesscontrol.%{system_security_accesscontrol_ver}.nupkg
Source436:      %{nuget_url}/system.security.claims.%{system_security_claims_ver}.nupkg
Source437:      %{nuget_url}/system.security.cryptography.algorithms.%{system_security_cryptography_algorithms_ver}.nupkg
Source438:      %{nuget_url}/system.security.cryptography.cng.%{system_security_cryptography_cng_ver2}.nupkg
Source439:      %{nuget_url}/system.security.cryptography.cng.%{system_security_cryptography_cng_ver}.nupkg
Source440:      %{nuget_url}/system.security.cryptography.csp.%{system_security_cryptography_csp_ver}.nupkg
Source441:      %{nuget_url}/system.security.cryptography.encoding.%{system_security_cryptography_encoding_ver}.nupkg
Source442:      %{nuget_url}/system.security.cryptography.openssl.%{system_security_cryptography_openssl_ver}.nupkg
Source443:      %{nuget_url}/system.security.cryptography.primitives.%{system_security_cryptography_primitives_ver}.nupkg
Source444:      %{nuget_url}/system.security.cryptography.x509certificates.%{system_security_cryptography_x509certificates_ver}.nupkg
Source445:      %{nuget_url}/system.security.principal.%{system_security_principal_ver}.nupkg
Source446:      %{nuget_url}/system.security.principal.windows.%{system_security_principal_windows_ver2}.nupkg
Source447:      %{nuget_url}/system.security.principal.windows.%{system_security_principal_windows_ver}.nupkg
Source448:      %{nuget_url}/system.text.encoding.codepages.%{system_text_encoding_codepages_ver2}.nupkg
Source449:      %{nuget_url}/system.text.encoding.codepages.%{system_text_encoding_codepages_ver}.nupkg
Source450:      %{nuget_url}/system.text.encoding.extensions.%{system_text_encoding_extensions_ver}.nupkg
Source451:      %{nuget_url}/system.text.encodings.web.%{system_text_encodings_web_ver2}.nupkg
Source452:      %{nuget_url}/system.text.encodings.web.%{system_text_encodings_web_ver}.nupkg
Source453:      %{nuget_url}/system.text.encoding.%{system_text_encoding_ver2}.nupkg
Source454:      %{nuget_url}/system.text.encoding.%{system_text_encoding_ver}.nupkg
Source455:      %{nuget_url}/system.text.json.%{system_text_json_ver2}.nupkg
Source456:      %{nuget_url}/system.text.json.%{system_text_json_ver}.nupkg
Source457:      %{nuget_url}/system.text.regularexpressions.%{system_text_regularexpressions_ver}.nupkg
Source458:      %{nuget_url}/system.threading.%{system_threading_ver2}.nupkg
Source459:      %{nuget_url}/system.threading.%{system_threading_ver}.nupkg
Source460:      %{nuget_url}/system.threading.tasks.extensions.%{system_threading_tasks_extensions_ver2}.nupkg
Source461:      %{nuget_url}/system.threading.tasks.extensions.%{system_threading_tasks_extensions_ver}.nupkg
Source462:      %{nuget_url}/system.threading.tasks.%{system_threading_tasks_ver2}.nupkg
Source463:      %{nuget_url}/system.threading.tasks.%{system_threading_tasks_ver}.nupkg
Source464:      %{nuget_url}/system.threading.threadpool.%{system_threading_threadpool_ver}.nupkg
Source465:      %{nuget_url}/system.threading.timer.%{system_threading_timer_ver}.nupkg
Source466:      %{nuget_url}/system.xml.readerwriter.%{system_xml_readerwriter_ver}.nupkg
Source467:      %{nuget_url}/system.xml.xdocument.%{system_xml_xdocument_ver}.nupkg
Source468:      %{nuget_url}/tmds.dbus.protocol.%{tmds_dbus_protocol_ver}.nupkg
Source469:      %{nuget_url}/system.text.encoding.codepages.%{system_text_encoding_codepages_ver3}.nupkg
Source470:      %{nuget_url}/microsoft.netcore.platforms.%{microsoft_netcore_platforms_ver5}.nupkg

%global nuget_files1 %{SOURCE200} %{SOURCE201} %{SOURCE202} %{SOURCE203} %{SOURCE204} %{SOURCE205} %{SOURCE206} %{SOURCE207} %{SOURCE208} %{SOURCE209} %{SOURCE210} %{SOURCE211} %{SOURCE212} %{SOURCE213} %{SOURCE214} %{SOURCE215} %{SOURCE216} %{SOURCE217} %{SOURCE218} %{SOURCE219} %{SOURCE220} %{SOURCE221} %{SOURCE222} %{SOURCE223} %{SOURCE224} %{SOURCE225} %{SOURCE226} %{SOURCE227} %{SOURCE228} %{SOURCE229} %{SOURCE230} %{SOURCE231} %{SOURCE232} %{SOURCE233} %{SOURCE234} %{SOURCE235} %{SOURCE236} %{SOURCE237} %{SOURCE238} %{SOURCE239} %{SOURCE240} %{SOURCE241} %{SOURCE242} %{SOURCE243} %{SOURCE244} %{SOURCE245} %{SOURCE246} %{SOURCE247} %{SOURCE248} %{SOURCE249}
%global nuget_files2 %{SOURCE250} %{SOURCE251} %{SOURCE252} %{SOURCE253} %{SOURCE254} %{SOURCE255} %{SOURCE256} %{SOURCE257} %{SOURCE258} %{SOURCE259} %{SOURCE260} %{SOURCE261} %{SOURCE262} %{SOURCE263} %{SOURCE264} %{SOURCE265} %{SOURCE266} %{SOURCE267} %{SOURCE268} %{SOURCE269} %{SOURCE270} %{SOURCE271} %{SOURCE272} %{SOURCE273} %{SOURCE274} %{SOURCE275} %{SOURCE276} %{SOURCE277} %{SOURCE278} %{SOURCE279} %{SOURCE280} %{SOURCE281} %{SOURCE282} %{SOURCE283} %{SOURCE284} %{SOURCE285} %{SOURCE286} %{SOURCE287} %{SOURCE288} %{SOURCE289} %{SOURCE290} %{SOURCE291} %{SOURCE292} %{SOURCE293} %{SOURCE294} %{SOURCE295} %{SOURCE296} %{SOURCE297} %{SOURCE298} %{SOURCE299}
%global nuget_files3 %{SOURCE300} %{SOURCE301} %{SOURCE302} %{SOURCE303} %{SOURCE304} %{SOURCE305} %{SOURCE306} %{SOURCE307} %{SOURCE308} %{SOURCE309} %{SOURCE310} %{SOURCE311} %{SOURCE312} %{SOURCE313} %{SOURCE314} %{SOURCE315} %{SOURCE316} %{SOURCE317} %{SOURCE318} %{SOURCE319} %{SOURCE320} %{SOURCE321} %{SOURCE322} %{SOURCE323} %{SOURCE324} %{SOURCE325} %{SOURCE326} %{SOURCE327} %{SOURCE328} %{SOURCE329} %{SOURCE330} %{SOURCE331} %{SOURCE332} %{SOURCE333} %{SOURCE334} %{SOURCE335} %{SOURCE336} %{SOURCE337} %{SOURCE338} %{SOURCE339} %{SOURCE340} %{SOURCE341} %{SOURCE342} %{SOURCE343} %{SOURCE344} %{SOURCE345} %{SOURCE346} %{SOURCE347} %{SOURCE348} %{SOURCE349}
%global nuget_files4 %{SOURCE350} %{SOURCE351} %{SOURCE352} %{SOURCE353} %{SOURCE354} %{SOURCE355} %{SOURCE356} %{SOURCE357} %{SOURCE358} %{SOURCE359} %{SOURCE360} %{SOURCE361} %{SOURCE362} %{SOURCE363} %{SOURCE364} %{SOURCE365} %{SOURCE366} %{SOURCE367} %{SOURCE368} %{SOURCE369} %{SOURCE370} %{SOURCE371} %{SOURCE372} %{SOURCE373} %{SOURCE374} %{SOURCE375} %{SOURCE376} %{SOURCE377} %{SOURCE378} %{SOURCE379} %{SOURCE380} %{SOURCE381} %{SOURCE382} %{SOURCE383} %{SOURCE384} %{SOURCE385} %{SOURCE386} %{SOURCE387} %{SOURCE388} %{SOURCE389} %{SOURCE390} %{SOURCE391} %{SOURCE392} %{SOURCE393} %{SOURCE394} %{SOURCE395} %{SOURCE396} %{SOURCE397} %{SOURCE398} %{SOURCE399}
%global nuget_files5 %{SOURCE400} %{SOURCE401} %{SOURCE402} %{SOURCE403} %{SOURCE404} %{SOURCE405} %{SOURCE406} %{SOURCE407} %{SOURCE408} %{SOURCE409} %{SOURCE410} %{SOURCE411} %{SOURCE412} %{SOURCE413} %{SOURCE414} %{SOURCE415} %{SOURCE416} %{SOURCE417} %{SOURCE418} %{SOURCE419} %{SOURCE420} %{SOURCE421} %{SOURCE422} %{SOURCE423} %{SOURCE424} %{SOURCE425} %{SOURCE426} %{SOURCE427} %{SOURCE428} %{SOURCE429} %{SOURCE430} %{SOURCE431} %{SOURCE432} %{SOURCE433} %{SOURCE434} %{SOURCE435} %{SOURCE436} %{SOURCE437} %{SOURCE438} %{SOURCE439} %{SOURCE440} %{SOURCE441} %{SOURCE442} %{SOURCE443} %{SOURCE444} %{SOURCE445} %{SOURCE446} %{SOURCE447} %{SOURCE448} %{SOURCE449}
%global nuget_files6 %{SOURCE450} %{SOURCE451} %{SOURCE452} %{SOURCE453} %{SOURCE454} %{SOURCE455} %{SOURCE456} %{SOURCE457} %{SOURCE458} %{SOURCE459} %{SOURCE460} %{SOURCE461} %{SOURCE462} %{SOURCE463} %{SOURCE464} %{SOURCE465} %{SOURCE466} %{SOURCE467} %{SOURCE468} %{SOURCE469} %{SOURCE470}
%endif

Patch0:         %{vc_url}/%{appname}/pull/7285.patch#/%{name}-gh-pr7285.patch

Patch11:        0001-Use-system-SDL_GameControllerDB.patch
Patch12:        0001-Modify-default-settings.patch

ExclusiveArch:  x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  librsvg2-tools
%if %{without bin}
%if %{without local_dotnet}
BuildRequires:  dotnet >= 8.0.100
%endif
BuildRequires:  libicu-devel
BuildRequires:  pkgconfig(zlib)
%endif
Requires:       gtk3%{?_isa}
Requires:       libglvnd-glx%{?_isa}
Requires:       libicu%{?_isa}
Requires:       libsoundio%{?_isa}
Requires:       openssl%{?_isa}
Requires:       SDL2%{?_isa}
Requires:       sdl_gamecontrollerdb
Requires:       vulkan-loader%{?_isa}
Requires:       hicolor-icon-theme

%global __provides_exclude_from ^%{_libdir}/%{name}/.*.so.*

%global __requires_exclude ^libavutil\\.so.*$


%description
Ryujinx is an open-source Nintendo Switch emulator, written in C#. This emulator
aims at providing excellent accuracy and performance, a user-friendly interface
and consistent builds.


%prep
%if %{with bin}
%autosetup -N -c
%else
%autosetup -n %{appname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1
%endif

%if %{with bin}

cp -p %{S:1} %{S:2} %{S:3} %{S:4} .

%else

cp distribution/linux/*.desktop distribution/legal/THIRDPARTY.md .
mv distribution/misc/Logo.svg %{name}-Logo.svg
cp -a distribution/linux/mime .

%if %{with local_dotnet}
mkdir dotnetbin
tar xvf %{S:199} -C dotnetbin
%endif

mkdir -p nuget/{cache,packages}
install -pm0644 %{nuget_files1} %{nuget_files2} %{nuget_files3} %{nuget_files4} \
  %{nuget_files5} %{nuget_files6} \
  nuget/cache/

sed \
  -e 's|_RPM_GCDB_|%{_datadir}/SDL_GameControllerDB/gamecontrollerdb.txt|g' \
  -i src/Ryujinx.SDL2.Common/SDL2Driver.cs
%endif

sed \
  -e 's|\%\%RYUJINX_BUILD_VERSION\%\%|%{version}|g' \
  -e 's|\%\%RYUJINX_BUILD_GIT_HASH\%\%|%{shortcommit}|g' \
  -e 's|\%\%RYUJINX_TARGET_RELEASE_CHANNEL_NAME\%\%|master|g' \
  -e 's|\%\%RYUJINX_TARGET_RELEASE_CHANNEL_OWNER\%\%|Ryujinx|g' \
  -e 's|\%\%RYUJINX_TARGET_RELEASE_CHANNEL_REPO\%\%|chinforpms|g' \
  -i src/Ryujinx.Common/ReleaseInformation.cs

cat > %{appname}.sh <<'EOF'
#!/usr/bin/bash
export DOTNET_EnableAlternateStackCheck=1
exec "%{_libdir}/%{name}/%{appname}" "$@"
EOF


%build
%if %{without bin}
%if %{with local_dotnet}
export PATH=$PATH:$(pwd)/dotnetbin
%endif

export \
  DOTNET_CLI_TELEMETRY_OPTOUT=1 \
  DOTNET_NOLOGO=1 \
  MSBUILDDISABLENODEREUSE=1 \
  NO_COLOR=1

dotnet restore \
  -maxcpucount:%{_smp_build_ncpus} \
  --runtime linux-x64 \
  --no-cache \
  --packages "$(pwd)/nuget/packages" \
  --source "$(pwd)/nuget/cache" \
  src/%{appname} \
%{nil}

dotnet publish \
  -maxcpucount:%{_smp_build_ncpus} \
  --nologo \
  --no-restore \
  --configuration Release \
  --runtime linux-x64 \
  -p:Version="%{version}" \
  -p:SourceRevisionId="%{shortcommit}" \
  -p:ExtraDefineConstants=DISABLE_UPDATER \
  -p:DebugType=embedded \
  -p:UseSharedCompilation=False \
  --self-contained true \
  -o publish \
  src/%{appname} \
%{nil}
%endif

chrpath --delete publish/%{appname}


%install

pushd publish
mkdir -p %{buildroot}%{_libdir}/%{name}
install -pm0755 %{appname} %{buildroot}%{_libdir}/%{name}/

install -pm0755 libav{codec,util}.so.* %{buildroot}%{_libdir}/%{name}/
install -pm0755 libglfw*.so.3.3 %{buildroot}%{_libdir}/%{name}/
install -pm0755 libHarfBuzzSharp.so %{buildroot}%{_libdir}/%{name}/
install -pm0755 libSkiaSharp.so %{buildroot}%{_libdir}/%{name}/
install -pm0644 OpenAL32.dll %{buildroot}%{_libdir}/%{name}/

install -pm0644 Ryujinx.SDL2.Common.dll.config %{buildroot}%{_libdir}/%{name}/
popd

# Ugly hack to use system libraries
ln -sf ../libSDL2-2.0.so.0 %{buildroot}%{_libdir}/%{name}/libSDL2.so
ln -sf ../libsoundio.so.2 %{buildroot}%{_libdir}/%{name}/libsoundio.so

%if %{with bin}
ln -sf ../../share/SDL_GameControllerDB/gamecontrollerdb.txt \
  %{buildroot}%{_libdir}/%{name}/SDL_GameControllerDB.txt

ln -sf ../../../tmp %{buildroot}%{_libdir}/%{name}/Logs
%endif

mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{appname}.sh %{buildroot}%{_bindir}/%{appname}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key=Exec \
  --set-value="%{appname} %%f" \
  %{appname}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -pm0644 %{name}-Logo.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{appname}.svg

for res in 16 22 24 32 36 48 64 72 96 128 192 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  rsvg-convert %{name}-Logo.svg -h ${res} -w ${res} \
    -o ${dir}/%{appname}.png
done

mkdir -p %{buildroot}%{_datadir}/mime/packages
install -pm0644 mime/%{appname}.xml %{buildroot}%{_datadir}/mime/packages/


%files
%license LICENSE.txt THIRDPARTY.md
%doc README.md
%{_bindir}/%{appname}
%{_libdir}/%{name}/%{appname}
%{_libdir}/%{name}/*.so*
%{_libdir}/%{name}/*.config
%{_libdir}/%{name}/*.dll
%if %{with bin}
%{_libdir}/%{name}/*.txt
%{_libdir}/%{name}/Logs
%endif
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{appname}.*
%{_datadir}/mime/packages/%{appname}.xml


%changelog
* Mon Mar 04 2024 Phantom X <megaphantomx at hotmail dot com> - 1.1.1217-1
- 1.1.1217
- Avalonia

* Fri Mar 24 2023 Phantom X <megaphantomx at hotmail dot com> - 1.1.680-1
- 1.1.680 tag release

* Tue Nov 01 2022 Phantom X <megaphantomx at hotmail dot com> - 1.1.335-2
- Support build from source

* Thu Oct 27 2022 Phantom X <megaphantomx at hotmail dot com> - 1.1.328-1
- Initial spec

