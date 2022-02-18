# Copyright (c) 2021, NVIDIA CORPORATION. All rights reserved.
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

import logging

LOGGER = logging.getLogger(__name__)


try:
    import torch  # pytype: disable=import-error

    _TORCH_VERSION = torch.__version__
    _TORCH_AVAILABLE = True
    LOGGER.info(f"PyTorch version {_TORCH_VERSION} available.")
except ModuleNotFoundError:
    _TORCH_AVAILABLE = False
    LOGGER.info("PyTorch is not available.")

try:
    import tensorflow  # pytype: disable=import-error

    _TF_VERSION = tensorflow.__version__
    _TF_AVAILABLE = True
    LOGGER.info(f"Tensorflow version {_TF_VERSION} available.")
except ModuleNotFoundError:
    _TF_AVAILABLE = False
    LOGGER.info("Tensorflow is not available.")

try:
    import transformers  # pytype: disable=import-error

    _HF_VERSION = transformers.__version__
    _HF_AVAILABLE = True
    LOGGER.info(f"Huggingface Transformers version {_HF_VERSION} available.")
except ModuleNotFoundError:
    _HF_AVAILABLE = False
    LOGGER.info("Huggingface Transformers is not available.")


def is_torch_available() -> bool:
    return _TORCH_AVAILABLE


def is_tf_available() -> bool:
    return _TF_AVAILABLE


def is_hf_available() -> bool:
    return _HF_AVAILABLE
