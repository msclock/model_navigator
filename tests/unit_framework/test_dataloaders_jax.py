# Copyright (c) 2021-2022, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# pytype: disable=import-error

import tempfile
from pathlib import Path

import jax.numpy as jnp
import numpy
import tensorflow

import model_navigator as nav
from model_navigator.framework_api.commands.performance import ProfilerConfig

# pytype: enable=import-error

gpus = tensorflow.config.experimental.list_physical_devices("GPU")
for gpu in gpus:
    tensorflow.config.experimental.set_memory_growth(gpu, True)


def check_model_dir(model_dir: Path) -> bool:
    if not model_dir.is_dir():
        return False
    if not Path(model_dir / "config.yaml").is_file():
        return False
    if not Path(model_dir / "model.savedmodel").exists():
        return False
    return True


dataloader = [numpy.random.rand(1, 10, 10) for _ in range(10)]
params = numpy.random.rand(1, 10, 10)


def predict(inputs, params):
    outputs = jnp.dot(inputs, params)
    return outputs


def test_np_dict_dataloader():
    with tempfile.TemporaryDirectory() as tmp_dir:
        model_name = "navigator_model"

        workdir = Path(tmp_dir) / "navigator_workdir"
        package_dir = workdir / f"{model_name}.nav.workspace"
        status_file = package_dir / "status.yaml"
        model_input_dir = package_dir / "model_input"
        model_output_dir = package_dir / "model_output"
        navigator_log_file = package_dir / "navigator.log"

        nav.jax.export(
            model=predict,
            model_params=params,
            dataloader=dataloader,
            workdir=workdir,
            model_name=model_name,
            override_workdir=True,
            profiler_config=ProfilerConfig(measurement_interval=100),
            batch_dim=None,
        )
        assert status_file.is_file()
        assert model_input_dir.is_dir()
        assert all(
            [path.suffix == ".npz" for samples_dir in model_input_dir.iterdir() for path in samples_dir.iterdir()]
        )
        assert model_output_dir.is_dir()
        assert all(
            [path.suffix == ".npz" for samples_dir in model_output_dir.iterdir() for path in samples_dir.iterdir()]
        )
        assert navigator_log_file.is_file()

        # Output formats
        assert check_model_dir(model_dir=package_dir / "tf-savedmodel")


def test_np_sequence_dataloader():
    with tempfile.TemporaryDirectory() as tmp_dir:
        model_name = "navigator_model"

        workdir = Path(tmp_dir) / "navigator_workdir"
        package_dir = workdir / f"{model_name}.nav.workspace"
        status_file = package_dir / "status.yaml"
        model_input_dir = package_dir / "model_input"
        model_output_dir = package_dir / "model_output"
        navigator_log_file = package_dir / "navigator.log"

        nav.jax.export(
            model=predict,
            model_params=params,
            dataloader=dataloader,
            workdir=workdir,
            model_name=model_name,
            override_workdir=True,
            profiler_config=ProfilerConfig(measurement_interval=100),
            batch_dim=None,
        )
        assert status_file.is_file()
        assert model_input_dir.is_dir()
        assert all(
            [path.suffix == ".npz" for samples_dir in model_input_dir.iterdir() for path in samples_dir.iterdir()]
        )
        assert model_output_dir.is_dir()
        assert all(
            [path.suffix == ".npz" for samples_dir in model_output_dir.iterdir() for path in samples_dir.iterdir()]
        )
        assert navigator_log_file.is_file()

        # Output formats
        assert check_model_dir(model_dir=package_dir / "tf-savedmodel")