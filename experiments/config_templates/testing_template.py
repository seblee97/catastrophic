from context import utils

from typing import List

class TestingTemplate(utils._Template):

    LEVELS = ["testing"]

    # Testing level fields
    TEST_FREQUENCY = utils.Field(
        name="test_frequency", types=(int), reqs=[lambda x: x > 0]
    )

    OVERLAP_FREQUENCY = utils.Field(
        name="overlap_frequency", types=(int), reqs=[lambda x: x > 0]
    )
    
    TEST_ALL_TEACHERS = utils.Field(
        name="test_all_teachers", types=(bool), reqs=None
    )

    @classmethod
    def get_fields(cls) -> List:
        return [
            cls.TEST_FREQUENCY,
            cls.OVERLAP_FREQUENCY,
            cls.TEST_ALL_TEACHERS
        ]