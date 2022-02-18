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
import torch
import torch.nn as nn

import model_navigator.framework_api as nav


def dataloader():
    yield torch.randn(1)


class MyModule(nn.Module):
    def forward(self, x):
        return x + 10


model = MyModule()


nav.torch.export(
    model=model,
    dataloader=dataloader,
    override_workdir=True,
    target_formats=(nav.Format.ONNX,),
)
