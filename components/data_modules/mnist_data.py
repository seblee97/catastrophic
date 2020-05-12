from abc import ABC, abstractmethod

from .base_data_module import _BaseData

from typing import Dict, List

import os

import torch
import torchvision 

from utils import custom_torch_transforms, get_pca

class _MNISTData(_BaseData, ABC):

    """Class for dealing with data generated from MNIST images"""

    def __init__(self, config: Dict):
        _BaseData.__init__(self, config)

        self._data_path = config.get(["mnist_data", "data_path"])
        
        self._pca_input = config.get(["mnist_data", "pca_input"])
        self._standardise = config.get(["mnist_data", "standardise"])
        self._noise = config.get(["mnist_data", "noise"])

        self._load_mnist_data()

    def _load_mnist_data(self) -> None:

        self._get_transforms()
        self._generate_dataloaders()

    @abstractmethod
    def _generate_dataloaders(self) -> None:
        raise NotImplementedError("Base class method")

    def _get_transforms(self) -> None:

        # TODO: Docs

        file_path = os.path.dirname(os.path.realpath(__file__))
        self._full_data_path = os.path.join(file_path, self._data_path)

        # transforms to add to data
        transform_list = [
            torchvision.transforms.Grayscale(),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize((0.1307,), (0.3081,)),
            custom_torch_transforms.CustomFlatten(),
            custom_torch_transforms.ToFloat()                   
        ]

        base_transform = torchvision.transforms.Compose(transform_list)

        if self._pca_input > 0:
            # note always using train data to generate pca
            mnist_data = torchvision.datasets.MNIST(self._full_data_path, transform=base_transform, train=True)
            raw_data = next(iter(mnist_data))[0].reshape((len(mnist_data), -1))
            pca_output = get_pca(raw_data, num_principal_components=self._pca_input)

            # add application of pca to transforms
            pca_transform = custom_torch_transforms.ApplyPCA(pca_output)

            transform_list.append(pca_transform)
            base_transform = torchvision.transforms.Compose(transform_list)

        if self._standardise:
            # load dataset to compute channel statistics
            mnist_train_data = torchvision.datasets.MNIST(self._full_data_path, transform=base_transform, train=True)
            mnist_train_dataloader = torch.utils.data.DataLoader(mnist_train_data, batch_size=len(mnist_train_data))

            # import pdb; pdb.set_trace()

            # evaluate channel mean and std (note MNIST small enough to load all in memory rather than computing over smaller batches)
            data_mu = torch.mean(next(iter(mnist_train_dataloader))[0], axis=0)
            data_sigma = torch.std(next(iter(mnist_train_dataloader))[0], axis=0)
            # import pdb; pdb.set_trace()

            # add normalisation to transforms
            normalise_transform = custom_torch_transforms.Standardize(data_mu, data_sigma)
            transform_list.append(normalise_transform)

        if self._noise is not None:
            add_noise_transform = custom_torch_transforms.AddGaussianNoise(self._noise)
            transform_list.append(normalise_transform)

        transform = torchvision.transforms.Compose(transform_list)

        self.transform = torchvision.transforms.Compose(transform_list)
    
    @abstractmethod
    def get_test_set(self) -> (torch.Tensor, List[torch.Tensor]):
        """
        returns fixed test data set (data and labels)
        
        return data: test data inputs
        return labels: corresponding labels for test data inputs
        """
        raise NotImplementedError("Base class method")

    @abstractmethod
    def get_batch(self) -> Dict[str, torch.Tensor]:
        raise NotImplementedError("Base class method")

    @abstractmethod        
    def signal_task_boundary_to_data_generator(self, new_task: int) -> None:
        """for use in cases where data generation changes with task (e.g. pure MNIST)"""
        raise NotImplementedError("Base class method")