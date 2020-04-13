from common.entities import FeatureEntity
from common.interfaces import FeaturePresenterInterface
from common.object_factory import ObjectFactory


class DisplaySkeletonUseCase(object):
    def __init__(self, feature: FeatureEntity) -> None:
        self.feature = feature

    def run(self):
        presenter = ObjectFactory.build_instance(FeaturePresenterInterface, self.feature)
        presenter.show()
