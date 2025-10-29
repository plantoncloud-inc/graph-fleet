from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class ImageBuildMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    image_build_method_unspecified: _ClassVar[ImageBuildMethod]
    dockerfile: _ClassVar[ImageBuildMethod]
    buildpacks: _ClassVar[ImageBuildMethod]

class PipelineProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    pipeline_provider_unspecified: _ClassVar[PipelineProvider]
    platform: _ClassVar[PipelineProvider]
    self: _ClassVar[PipelineProvider]
image_build_method_unspecified: ImageBuildMethod
dockerfile: ImageBuildMethod
buildpacks: ImageBuildMethod
pipeline_provider_unspecified: PipelineProvider
platform: PipelineProvider
self: PipelineProvider
