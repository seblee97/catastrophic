from models import MetaStudent

from .base_learner import _BaseLearner

from typing import Dict

class MetaLearner(_BaseLearner):

    def __init__(self, config):
        _BaseLearner.__init__(self, config)

    def _setup_student(self, config: Dict) -> None:
        """Instantiate student"""
        self._student_network = MetaStudent(config=config).to(self._device)

    def signal_task_boundary_to_learner(self, new_task: int) -> None:
        self._student_network.set_task(new_task)

    def signal_step_boundary_to_learner(self, step: int, current_task: int) -> None:
        pass
