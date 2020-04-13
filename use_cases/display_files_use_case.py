from common.entities import FeatureEntity, FileEntity, ResourceEntity
from common.interfaces import FilesPresenterInterface, VelocityTemplateEngineInterface
from common.object_factory import ObjectFactory


class DisplayFilesUseCase(object):
    def __init__(self, feature: FeatureEntity, values: dict) -> None:
        self.feature = feature
        self.values = values
        self.files = []

    def run(self):
        # TODO: build the files
        self._retrieve_files()

        presenter = ObjectFactory.build_instance(FilesPresenterInterface, self.feature, self.files)
        presenter.show()

    def _retrieve_files(self):
        for resource in self.feature.resources:
            file = self._retrieve_file(resource)
            self.files.append(file)

    def _retrieve_file(self, resource: ResourceEntity) -> FileEntity:
        relative_path = eval(resource.target_route, globals(), self.values)
        content = resource.content

        template_engine = ObjectFactory.build_instance(VelocityTemplateEngineInterface)
        code = template_engine.translate(content, self.values)

        return FileEntity(name=resource.name, description=resource.description, absolute_path=relative_path,
                          content=code)
