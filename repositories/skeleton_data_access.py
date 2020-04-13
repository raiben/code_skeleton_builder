import json

from common.entities import ResourceEntity, FeatureEntity, VariableEntity
from common.interfaces import SkeletonDataAccessInterface
import os


class SkeletonDataAccess(SkeletonDataAccessInterface):
    def __init__(self):
        self.root_path = '/'.join(__file__.split('/')[:-2] + ['skeletons'])

    def get_features(self):
        features = []
        for child in os.listdir(self.root_path):
            skeleton_path = '/'.join([self.root_path, child])
            if os.path.isdir(skeleton_path):
                feature = self._get_feature_from_skeleton(skeleton_path)
                features.append(feature)
        return features

    def _get_feature_from_skeleton(self, skeleton_path):
        name = skeleton_path.split('/')[-1]
        definition_file = '/'.join([skeleton_path, 'skeleton.json'])
        if os.path.exists(definition_file):
            with open(definition_file, 'r') as file_handler:
                definition = json.load(file_handler)

        description = definition['description']
        resources = [ResourceEntity(resource['name'], resource['description'], resource['file_path'],
                                    resource['target_route'], self._get_content(skeleton_path, resource))
                     for resource in definition['resources']]
        variables = [VariableEntity(resource['name'], resource['type'], resource['description'],
                                    resource['variable_name'], resource['autofill'], resource['depends_on'])
                     for resource in definition['variables']]
        return FeatureEntity(name, description, resources, variables)

    def _get_content(self, skeleton_path, resource):
        resource_path = '/'.join([skeleton_path, resource['file_path']])
        with open(resource_path, 'r') as handler:
            content = handler.read()
        return content

