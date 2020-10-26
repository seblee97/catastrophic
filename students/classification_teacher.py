import torch

from students import base_teacher


class ClassificationTeacher(base_teacher.BaseTeacher):
    """Classification - threshold output"""

    def _output_forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Override teacher output forward, add sign output
        """
        y = self.output_layer(x)

        if self.noisy:
            y = self.add_output_noise(y)

        # threshold differently depending on nonlinearity to
        # ensure even class distributions
        if self.nonlinearity_name == "relu":
            labels = torch.abs(y) > 0
        elif self.nonlinearity_name == "linear":
            tanh_y = torch.tanh(y)
            labels = tanh_y > 0
        else:
            raise NotImplementedError(
                "Teacher thresholding for {} nonlinearity not yet \
                implemented".format(
                    self.nonlinearity_name
                )
            )

        return labels.long().reshape(
            len(labels),
        )