# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
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

import os
import sys
sys.path.insert(0, os.getcwd())
from importlib import import_module

from code.common.constants import Benchmark, Scenario
from code.common.systems.system_list import KnownSystem
from configs.configuration import *
GPUBaseConfig = import_module("configs.stable-diffusion-xl").GPUBaseConfig


class OfflineGPUBaseConfig(GPUBaseConfig):
    scenario = Scenario.Offline
    precision = "fp8"

    use_graphs = False
    gpu_inference_streams = 1
    gpu_copy_streams = 1


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class GH200_96GB_aarch64x1(OfflineGPUBaseConfig):
    system = KnownSystem.GH200_96GB_ARMx1
    gpu_batch_size = {'clip1': 32 * 2, 'clip2': 32 * 2, 'unet': 32 * 2, 'vae': 8}
    offline_expected_qps = 2
    use_graphs = False


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class D54U_3U_H100_PCIe_80GBx4(OfflineGPUBaseConfig):
    system = KnownSystem.D54U_3U_H100_PCIe_80GBx4
    gpu_batch_size = {'clip1': 8 * 2, 'clip2': 8 * 2, 'unet': 8 * 2, 'vae': 8}
    offline_expected_qps = 5
    use_graphs = False

