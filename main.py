from adaptors.airspeed_template_egine import AirspeedTemplateEngine
from common.interfaces import SkeletonDataAccessInterface, FeatureSelectionPresenterInterface, \
    FeaturePresenterInterface, FilesPresenterInterface, VelocityTemplateEngineInterface
from common.object_factory import ObjectFactory
from presenters.feature_presenter import FeaturePresenter
from presenters.files_presenter import FilesPresenter
from repositories.skeleton_data_access import SkeletonDataAccess
from presenters.feature_selection_presenter import FeatureSelectionPresenter
from use_cases.display_skeletons_selector_use_case import DisplaySkeletonsSelectorUseCase

if __name__ == "__main__":

    ObjectFactory.add_implementation(SkeletonDataAccessInterface, SkeletonDataAccess)
    ObjectFactory.add_implementation(FeatureSelectionPresenterInterface, FeatureSelectionPresenter)
    ObjectFactory.add_implementation(FeaturePresenterInterface, FeaturePresenter)
    ObjectFactory.add_implementation(FilesPresenterInterface, FilesPresenter)
    ObjectFactory.add_implementation(VelocityTemplateEngineInterface, AirspeedTemplateEngine)

    use_case = DisplaySkeletonsSelectorUseCase()
    use_case.run()
