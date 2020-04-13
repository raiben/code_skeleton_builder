from typing import List

from common.entities import FeatureEntity, FileEntity


class SkeletonDataAccessInterface(object):
    def __init__(self):
        pass

    def get_features(self) -> List[FeatureEntity]:
        return


class FeatureSelectionPresenterInterface(object):
    def __init__(self, features: List[FeatureEntity]) -> None:
        self.features = features

    def show(self):
        pass


class FeaturePresenterInterface(object):
    def __init__(self, feature: FeatureEntity) -> object:
        pass

    def show(self):
        pass


class FilesPresenterInterface(object):
    def __init__(self, feature: FeatureEntity, files: List[FileEntity]) -> None:
        pass

    def show(self):
        pass


class VelocityTemplateEngineInterface(object):
    def __init__(self):
        pass

    def translate(self, code: str, dictionary: dict) -> str:
        pass
