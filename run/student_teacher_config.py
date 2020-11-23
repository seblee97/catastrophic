from typing import Union, Dict

from config_manager import base_configuration
from config_manager import config_template

import constants


class StudentTeacherConfiguration(base_configuration.BaseConfiguration):
    def __init__(self, config: Union[str, Dict], template: config_template.Template):
        super().__init__(configuration=config, template=template)
        self._validate_configuration()

    def _validate_configuration(self):
        """Method to check for non-trivial associations
        in the configuration.
        """
        if self.teacher_configuration == constants.Constants.BOTH_ROTATION:
            assert self.scale_forward_by_hidden == True, (
                "In both rotation regime, i.e. mean field limit, "
                "need to scale forward by 1/K."
            )
        else:
            assert self.scale_forward_by_hidden == False, (
                "When not in both rotation regime, i.e. mean field limit, "
                "no need to scale forward by 1/K."
            )
