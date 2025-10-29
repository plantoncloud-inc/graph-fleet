from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StackOutputsTestEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STACK_OUTPUTS_TEST_ENUM_UNSPECIFIED: _ClassVar[StackOutputsTestEnum]
    STACK_OUTPUTS_TEST_ENUM_VALUE_ONE: _ClassVar[StackOutputsTestEnum]
    STACK_OUTPUTS_TEST_ENUM_VALUE_TWO: _ClassVar[StackOutputsTestEnum]
STACK_OUTPUTS_TEST_ENUM_UNSPECIFIED: StackOutputsTestEnum
STACK_OUTPUTS_TEST_ENUM_VALUE_ONE: StackOutputsTestEnum
STACK_OUTPUTS_TEST_ENUM_VALUE_TWO: StackOutputsTestEnum

class TestStackOutputsPrimitives(_message.Message):
    __slots__ = ("field_one", "field_two", "field_three", "field_four", "enum_field")
    FIELD_ONE_FIELD_NUMBER: _ClassVar[int]
    FIELD_TWO_FIELD_NUMBER: _ClassVar[int]
    FIELD_THREE_FIELD_NUMBER: _ClassVar[int]
    FIELD_FOUR_FIELD_NUMBER: _ClassVar[int]
    ENUM_FIELD_FIELD_NUMBER: _ClassVar[int]
    field_one: str
    field_two: int
    field_three: bool
    field_four: float
    enum_field: StackOutputsTestEnum
    def __init__(self, field_one: _Optional[str] = ..., field_two: _Optional[int] = ..., field_three: bool = ..., field_four: _Optional[float] = ..., enum_field: _Optional[_Union[StackOutputsTestEnum, str]] = ...) -> None: ...

class TestStackOutputsRepeatedString(_message.Message):
    __slots__ = ("repeated_strings",)
    REPEATED_STRINGS_FIELD_NUMBER: _ClassVar[int]
    repeated_strings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, repeated_strings: _Optional[_Iterable[str]] = ...) -> None: ...

class TestStackOutputsRepeatedInt(_message.Message):
    __slots__ = ("repeated_integers",)
    REPEATED_INTEGERS_FIELD_NUMBER: _ClassVar[int]
    repeated_integers: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, repeated_integers: _Optional[_Iterable[int]] = ...) -> None: ...

class TestStackOutputsRepeatedFloat(_message.Message):
    __slots__ = ("repeated_floats",)
    REPEATED_FLOATS_FIELD_NUMBER: _ClassVar[int]
    repeated_floats: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, repeated_floats: _Optional[_Iterable[float]] = ...) -> None: ...

class TestStackOutputsRepeatedEnum(_message.Message):
    __slots__ = ("repeated_enum",)
    REPEATED_ENUM_FIELD_NUMBER: _ClassVar[int]
    repeated_enum: _containers.RepeatedScalarFieldContainer[StackOutputsTestEnum]
    def __init__(self, repeated_enum: _Optional[_Iterable[_Union[StackOutputsTestEnum, str]]] = ...) -> None: ...

class TestStackOutputsRepeatedObjects(_message.Message):
    __slots__ = ("repeated_objects",)
    REPEATED_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    repeated_objects: _containers.RepeatedCompositeFieldContainer[StackOutputsRepeatedTestObject]
    def __init__(self, repeated_objects: _Optional[_Iterable[_Union[StackOutputsRepeatedTestObject, _Mapping]]] = ...) -> None: ...

class TestStackOutputsMixed(_message.Message):
    __slots__ = ("simple_string", "simple_int", "simple_bool", "simple_float", "simple_enum", "repeated_strings", "repeated_integers", "repeated_enum", "repeated_objects")
    SIMPLE_STRING_FIELD_NUMBER: _ClassVar[int]
    SIMPLE_INT_FIELD_NUMBER: _ClassVar[int]
    SIMPLE_BOOL_FIELD_NUMBER: _ClassVar[int]
    SIMPLE_FLOAT_FIELD_NUMBER: _ClassVar[int]
    SIMPLE_ENUM_FIELD_NUMBER: _ClassVar[int]
    REPEATED_STRINGS_FIELD_NUMBER: _ClassVar[int]
    REPEATED_INTEGERS_FIELD_NUMBER: _ClassVar[int]
    REPEATED_ENUM_FIELD_NUMBER: _ClassVar[int]
    REPEATED_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    simple_string: str
    simple_int: int
    simple_bool: bool
    simple_float: float
    simple_enum: StackOutputsTestEnum
    repeated_strings: _containers.RepeatedScalarFieldContainer[str]
    repeated_integers: _containers.RepeatedScalarFieldContainer[int]
    repeated_enum: _containers.RepeatedScalarFieldContainer[StackOutputsTestEnum]
    repeated_objects: _containers.RepeatedCompositeFieldContainer[StackOutputsRepeatedTestObject]
    def __init__(self, simple_string: _Optional[str] = ..., simple_int: _Optional[int] = ..., simple_bool: bool = ..., simple_float: _Optional[float] = ..., simple_enum: _Optional[_Union[StackOutputsTestEnum, str]] = ..., repeated_strings: _Optional[_Iterable[str]] = ..., repeated_integers: _Optional[_Iterable[int]] = ..., repeated_enum: _Optional[_Iterable[_Union[StackOutputsTestEnum, str]]] = ..., repeated_objects: _Optional[_Iterable[_Union[StackOutputsRepeatedTestObject, _Mapping]]] = ...) -> None: ...

class TestStackOutputsMixedWithRepeatNested(_message.Message):
    __slots__ = ("simple_string", "simple_int", "simple_bool", "simple_float", "simple_enum", "repeated_strings", "repeated_integers", "repeated_enum", "repeated_objects", "repeated_objects_with_nested_objects")
    SIMPLE_STRING_FIELD_NUMBER: _ClassVar[int]
    SIMPLE_INT_FIELD_NUMBER: _ClassVar[int]
    SIMPLE_BOOL_FIELD_NUMBER: _ClassVar[int]
    SIMPLE_FLOAT_FIELD_NUMBER: _ClassVar[int]
    SIMPLE_ENUM_FIELD_NUMBER: _ClassVar[int]
    REPEATED_STRINGS_FIELD_NUMBER: _ClassVar[int]
    REPEATED_INTEGERS_FIELD_NUMBER: _ClassVar[int]
    REPEATED_ENUM_FIELD_NUMBER: _ClassVar[int]
    REPEATED_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    REPEATED_OBJECTS_WITH_NESTED_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    simple_string: str
    simple_int: int
    simple_bool: bool
    simple_float: float
    simple_enum: StackOutputsTestEnum
    repeated_strings: _containers.RepeatedScalarFieldContainer[str]
    repeated_integers: _containers.RepeatedScalarFieldContainer[int]
    repeated_enum: _containers.RepeatedScalarFieldContainer[StackOutputsTestEnum]
    repeated_objects: _containers.RepeatedCompositeFieldContainer[StackOutputsRepeatedTestObject]
    repeated_objects_with_nested_objects: _containers.RepeatedCompositeFieldContainer[StackOutputsRepeatedTestObjectContainingNestedObject]
    def __init__(self, simple_string: _Optional[str] = ..., simple_int: _Optional[int] = ..., simple_bool: bool = ..., simple_float: _Optional[float] = ..., simple_enum: _Optional[_Union[StackOutputsTestEnum, str]] = ..., repeated_strings: _Optional[_Iterable[str]] = ..., repeated_integers: _Optional[_Iterable[int]] = ..., repeated_enum: _Optional[_Iterable[_Union[StackOutputsTestEnum, str]]] = ..., repeated_objects: _Optional[_Iterable[_Union[StackOutputsRepeatedTestObject, _Mapping]]] = ..., repeated_objects_with_nested_objects: _Optional[_Iterable[_Union[StackOutputsRepeatedTestObjectContainingNestedObject, _Mapping]]] = ...) -> None: ...

class StackOutputsRepeatedTestObject(_message.Message):
    __slots__ = ("object_name", "object_id")
    OBJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    object_name: str
    object_id: int
    def __init__(self, object_name: _Optional[str] = ..., object_id: _Optional[int] = ...) -> None: ...

class StackOutputsRepeatedTestObjectContainingNestedObject(_message.Message):
    __slots__ = ("object_name", "object_id", "repeated_nested_objects")
    OBJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    REPEATED_NESTED_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    object_name: str
    object_id: int
    repeated_nested_objects: _containers.RepeatedCompositeFieldContainer[StackOutputsNestedRepeatedTestObject]
    def __init__(self, object_name: _Optional[str] = ..., object_id: _Optional[int] = ..., repeated_nested_objects: _Optional[_Iterable[_Union[StackOutputsNestedRepeatedTestObject, _Mapping]]] = ...) -> None: ...

class StackOutputsNestedRepeatedTestObject(_message.Message):
    __slots__ = ("nested_name", "nested_object_id")
    NESTED_NAME_FIELD_NUMBER: _ClassVar[int]
    NESTED_OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    nested_name: str
    nested_object_id: int
    def __init__(self, nested_name: _Optional[str] = ..., nested_object_id: _Optional[int] = ...) -> None: ...

class TestStackOutputsWithMapField(_message.Message):
    __slots__ = ("string_map",)
    class StringMapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    STRING_MAP_FIELD_NUMBER: _ClassVar[int]
    string_map: _containers.ScalarMap[str, str]
    def __init__(self, string_map: _Optional[_Mapping[str, str]] = ...) -> None: ...

class TestStackOutputsWithIntMapField(_message.Message):
    __slots__ = ("int_map",)
    class IntMapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    INT_MAP_FIELD_NUMBER: _ClassVar[int]
    int_map: _containers.ScalarMap[str, int]
    def __init__(self, int_map: _Optional[_Mapping[str, int]] = ...) -> None: ...

class TestStackOutputsWithBooleanMap(_message.Message):
    __slots__ = ("boolean_map",)
    class BooleanMapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: bool
        def __init__(self, key: _Optional[str] = ..., value: bool = ...) -> None: ...
    BOOLEAN_MAP_FIELD_NUMBER: _ClassVar[int]
    boolean_map: _containers.ScalarMap[str, bool]
    def __init__(self, boolean_map: _Optional[_Mapping[str, bool]] = ...) -> None: ...
