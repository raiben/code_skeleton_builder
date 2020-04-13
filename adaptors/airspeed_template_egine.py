import airspeed as airspeed

from common.interfaces import VelocityTemplateEngineInterface


class AirspeedTemplateEngine(VelocityTemplateEngineInterface):
    def __init__(self):
        pass

    def translate(self, code: str, variables: dict) -> str:
        template = airspeed.Template(code)
        return template.merge(variables)
