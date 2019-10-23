import numpy as np 
import copy
import itertools

import torch 
import torch.nn as nn 
import torch.nn.functional as F 
import torch.optim as optim

from tensorboardX import SummaryWriter

from typing import List, Tuple, Generator, Dict

class Model(nn.Module):

    def __init__(self, config, model_type: str):
        
        self.model_type = model_type # 'teacher' or 'student'

        assert self.model_type == 'teacher' or 'student', "Unknown model type {} provided to network".format(self.model_type)

        # extract relevant parameters from config
        self.input_dimension = config.get(["model", "input_dimension"])
        self.output_dimension = config.get(["model", "output_dimension"])
        self.hidden_dimensions = config.get(["model", "{}_hidden_layers".format(self.model_type)])
        self.initialisation_std = config.get(["model", "{}_initialisation_std".format(self.model_type)])
        self.add_noise = config.get(["model", "{}_add_noise".format(self.model_type)])
        self.bias = config.get(["model", "bias_parameters"])
        self.soft_committee = config.get(["model", "soft_committee"])

        # initialise specified nonlinearity function
        self.nonlinearity_name = config.get(["model", "nonlinearity"])
        if self.nonlinearity_name == 'relu':
            self.nonlinear_function = F.relu
        elif self.nonlinearity_name == 'sigmoid':
            self.nonlinear_function = torch.sigmoid
        else:
            raise ValueError("Unknown non-linearity. Please use 'relu' or 'sigmoid'")

        super(Model, self).__init__()

        self._construct_layers()

        self._initialise_weights()

    def _construct_layers(self):

        self.layers = nn.ModuleList([])
        
        input_layer = nn.Linear(self.input_dimension, self.hidden_dimensions[0], bias=self.bias)
        self.layers.append(input_layer)

        for h in self.hidden_dimensions[:-1]:
            hidden_layer = nn.Linear(self.hidden_dimensions[h], self.hidden_dimensions[h + 1], bias=self.bias)
            self.layers.append(hidden_layer)

        output_layer = nn.Linear(self.hidden_dimensions[-1], self.output_dimension, bias=self.bias)
        if self.soft_committee:
            for param in output_layer.parameters():
                param.requires_grad = False
        self.layers.append(output_layer)

    def _get_model_type(self):
        """
        returns class attribute 'model type' i.e. 'teacher' or 'student'
        """
        return self.model_type

    def _initialise_weights(self):
        for layer in self.layers:
            if self.nonlinearity_name == 'relu':
                # std = 1 / np.sqrt(self.input_dimension)
                torch.nn.init.normal_(layer.weight, std=self.initialisation_std)
                # torch.nn.init.normal_(layer.bias, std=std)

            elif self.nonlinearity_name == 'sigmoid' or 'linear':
                torch.nn.init.normal_(layer.weight)
                # torch.nn.init.normal_(layer.bias)

    def freeze_weights(self):
        for param in self.parameters():
            param.requires_grad = False

    def forward(self, x):

        for layer in self.layers[:-1]:
            x = self.nonlinear_function(layer(x) / np.sqrt(self.input_dimension))

        y = self.layers[-1](x)

        if self.add_noise:
            noise = torch.randn(self.output_dimension)
            y = y + noise

        return y


class StudentTeacher:

    def __init__(self, config):
        """
        Experiment
        """
        # extract relevant parameters from config
        self._extract_parameters(config)

        # initialise student network
        self.student_network = Model(config=config, model_type='student')

        # initialise teacher networks, freeze
        self.teachers = []
        for _ in range(self.num_teachers):
            teacher = Model(config=config, model_type='teacher')
            teacher.freeze_weights()
            self.teachers.append(teacher)

        # extract curriculum from config
        self._set_curriculum(config)
        
        trainable_parameters = filter(lambda param: param.requires_grad, self.student_network.parameters())

        # initialise optimiser with trainable parameters of student        
        self.optimiser = optim.SGD(trainable_parameters, lr=self.learning_rate)
        
        # initialise loss function
        if config.get(["training", "loss_function"]) == 'mse':
            self.loss_function = nn.MSELoss()
        else:
            raise NotImplementedError("{} is not currently supported, please use mse loss".format(config.get("loss")))

        # generate fixed test data
        self.test_input_data = torch.randn(self.test_batch_size, self.input_dimension)
        self.test_teacher_outputs = [teacher(self.test_input_data) for teacher in self.teachers]

        # initialise general tensorboard writer
        self.writer = SummaryWriter(self.checkpoint_path)
        # initialise separate tb writers for each teacher
        self.teacher_writers = [SummaryWriter("{}/teacher_{}".format(self.checkpoint_path, t)) for t in range(self.num_teachers)]

        # initialise objects containing metrics of interest
        self._initialise_metrics()

    def _extract_parameters(self, config):

        self.verbose = config.get("verbose")
        self.checkpoint_path = config.get("checkpoint_path")

        self.total_training_steps = config.get(["training", "total_training_steps"])

        self.input_dimension = config.get(["model", "input_dimension"])
        self.output_dimension = config.get(["model", "output_dimension"])
        self.nonlinearity = config.get(["model", "nonlinearity"])
        self.soft_committee = config.get(["model", "soft_committee"])

        self.train_batch_size = config.get(["training", "train_batch_size"])
        self.test_batch_size = config.get(["training", "test_batch_size"])
        self.learning_rate = config.get(["training", "learning_rate"])

        self.test_all_teachers = config.get(["testing", "test_all_teachers"])
        self.test_frequency = config.get(["testing", "test_frequency"])
        self.overlap_frequency = config.get(["testing", "overlap_frequency"])

        self.num_teachers = config.get(["training", "num_teachers"])

    def _initialise_metrics(self):
        self.generalisation_errors = {i: [] for i in range(len(self.teachers))}

    def _set_curriculum(self, config: Dict):
        curriculum_type = config.get(["curriculum", "type"])
        self.curriculum_stopping_condition = config.get(["curriculum", "stopping_condition"])
        self.curriculum_period = config.get(["curriculum", "fixed_period"])

        if curriculum_type == "custom":
            self.curriculum = itertools.cycle((config.get(["curriculum", "custom"])))
        elif curriculum_type == "standard":
            self.curriculum_selection_type = config.get(["curriculum", "selection_type"])
            if self.curriculum_selection_type == "cyclical":
                self.curriculum = itertools.cycle(list(range(self.num_teachers)))
            elif self.curriculum_selection_type == "random":
                raise NotImplementedError
            else:
                raise ValueError("You have specified a standard curriculum (as opposed to custom)," 
                                 "but the selection type is not recognised. Please choose between"
                                 "'cyclical' and 'random'")
        else:
            raise ValueError("Curriculum type {} not recognised".format(curriculum_type))

    def train(self):

        training_losses = []
        total_step_count = 0

        # import pdb; pdb.set_trace()

        while total_step_count < self.total_training_steps:
            
            teacher_index = next(self.curriculum)
            task_step_count = 0
            latest_task_generalisation_error = np.inf

            while True:

                random_input = torch.randn(self.train_batch_size, self.input_dimension)
    
                teacher_output = self.teachers[teacher_index](random_input)
                student_output = self.student_network(random_input)

                if self.verbose and task_step_count % 1000 == 0:
                    print("Training step {}".format(task_step_count))

                # training iteration
                self.optimiser.zero_grad()
                loss = self._compute_loss(student_output, teacher_output)
                training_losses.append(float(loss))
                loss.backward()
                self.optimiser.step()

                # log training loss
                self.writer.add_scalar('training_loss', float(loss), total_step_count)

                # test
                if total_step_count % self.test_frequency == 0 and total_step_count != 0:
                    latest_task_generalisation_error = self._perform_test_loop(teacher_index, task_step_count, total_step_count)

                # overlap matrices
                if total_step_count % self.overlap_frequency == 0 and total_step_count != 0:
                    self._compute_overlap_matrices()

                total_step_count += 1
                task_step_count += 1

                if self._switch_task(step=task_step_count, generalisation_error=latest_task_generalisation_error):
                    break

    def _switch_task(self, step, generalisation_error):
        if self.curriculum_stopping_condition == "fixed_period":
            if step == self.curriculum_period:
                return True
            else:
                return False
        elif self.curriculum_stopping_condition == "threshold":
            if generalisation_error < self.curriculum_loss_threshold:
                return True
            else:
                return False
        else:
            raise ValueError("curriculum stopping condition {} unknown".format(self.curriculum_stopping_condition))

    def _perform_test_loop(self, teacher_index, task_step_count, total_step_count):
        with torch.no_grad():

            if self.test_all_teachers:
                teachers_to_test = list(range(len(self.teachers)))
            else:
                teachers_to_test = [teacher_index]

            generalisation_error_per_teacher = self._compute_generalisation_errors(teachers_to_test)

            # log average generalisation losses over teachers
            self.writer.add_scalar(
                'mean_generalisation_error/linear', np.mean(generalisation_error_per_teacher), total_step_count
                )
            self.writer.add_scalar(
                'mean_generalisation_error/log', np.log10(np.mean(generalisation_error_per_teacher)), total_step_count
                )

            for i, error in enumerate(generalisation_error_per_teacher):
                self.generalisation_errors[i].append(error)
                # log generalisation loss per teacher
                self.teacher_writers[i].add_scalar('generalisation_error/linear', error, total_step_count)
                self.teacher_writers[i].add_scalar('generalisation_error/log', np.log10(error), total_step_count)

            if self.verbose and total_step_count % 100 == 0:
                print("Generalisation errors @ step {} ({}'th step training on teacher {}):".format(total_step_count, task_step_count, teacher_index))
                for i, error in enumerate(generalisation_error_per_teacher):
                    print(
                        "{}Teacher {}: {}".format("".rjust(10), i, error),
                        sep="\n"
                    )

            return generalisation_error_per_teacher[teacher_index]

    def _compute_overlap_matrices(self):
        raise NotImplementedError

    def _compute_generalisation_errors(self, teacher_indices: List) -> List:
        # import pdb; pdb.set_trace()
        with torch.no_grad():
            student_outputs = self.student_network(self.test_input_data)
            if self.test_all_teachers:
                generalisation_errors = [float(self._compute_loss(student_outputs, teacher_output)) for teacher_output in self.test_teacher_outputs]
            else:
                generalisation_errors = [float(self._compute_loss(student_outputs, self.test_teacher_outputs[teacher_index])) for teacher_index in teacher_indices]
            return generalisation_errors

    def _compute_loss(self, prediction, target):
        loss = 0.5 * self.loss_function(prediction, target)
        return loss


        
