from common.interfaces import SkeletonDataAccessInterface, FeatureSelectionPresenterInterface
from common.object_factory import ObjectFactory

class DisplaySkeletonsSelectorUseCase(object):
    def __init__(self):
        pass

    def run(self):
        data_access = ObjectFactory.build_instance(SkeletonDataAccessInterface)
        features = data_access.get_features()
        presenter = ObjectFactory.build_instance(FeatureSelectionPresenterInterface, features)
        presenter.show()
