from typing import NamedTuple, List

ResourceEntity = NamedTuple('ResourceEntity', [('name', str), ('description', str), ('file_path', str),
                                               ('target_route', str), ('content', str)])

VariableEntity = NamedTuple('VariableEntity', [('name', str), ('type', str), ('description', str),
                                               ('variable_name', str), ('autofill', str), ('depends_on', str)])

FeatureEntity = NamedTuple('FeatureEntity', [('name', str), ('description', str), ('resources', List[ResourceEntity]),
                                             ('variables', List[VariableEntity])])

FileEntity = NamedTuple('FileEntity', [('name', str), ('description', str), ('absolute_path', str), ('content', str)])
