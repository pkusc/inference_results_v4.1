# MLPerf Inference v4.1 NVIDIA-Optimized Inference on Jetson Systems
This is a repository of NVIDIA-optimized implementations for the [MLPerf](https://mlcommons.org/en/) Inference Benchmark.
This README is a quickstart tutorial on how to setup the the Jetson systems as a public / external user.
Please also read README.md for general instructions on how to run the code.

---

NVIDIA Jetson is a platform for AI at the edge. Its high-performance, low-power computing for deep learning and computer vision makes it the ideal platform for compute-intensive projects. The Jetson platform includes a variety of Jetson modules together with NVIDIA JetPack™ SDK.
Each Jetson module is a computing system packaged as a plug-in unit (a System on Module (SOM)). NVIDIA offers a variety of Jetson modules with different capabilities.
JetPack bundles all of the Jetson platform software, starting with NVIDIA Jetson Linux. Jetson Linux provides the Linux kernel, bootloader, NVIDIA drivers, flashing utilities, sample file system, and more for the Jetson platform.

## NVIDIA Submissions

For v4.1 round, please start with a Jetson AGX Orin 64GB board, and here is the list of benchmarks NVIDIA supports:

- Stable Diffusion XL (Offline, Single Stream)
- GPT-J (Offline and Single Stream), at 99% of FP16 accuracy target

*Note: power submission is not supported in MLPerf Inference v4.1*

## Setup the Jetson AGX Orin System

### Flash the board
Follow the the [Jetson Developer Guide](https://docs.nvidia.com/jetson/archives/r36.3/DeveloperGuide/IN/QuickStart.html#quick-start) to flash the board with the r36.3.0 L4T

Make sure the following dependencies are installed on your host system

`sudo apt update && sudo apt install -y libxml2-utils & sudo apt install -y qemu-user-static`

```
wget https://developer.nvidia.com/downloads/embedded/l4t/r36_release_v3.0/release/jetson_linux_r36.3.0_aarch64.tbz2

export L4T_RELEASE_PACKAGE=jetson_linux_r36.3.0_aarch64.tbz2

wget https://developer.nvidia.com/downloads/embedded/l4t/r36_release_v3.0/release/tegra_linux_sample-root-filesystem_r36.3.0_aarch64.tbz2

export SAMPLE_FS_PACKAGE=tegra_linux_sample-root-filesystem_r36.3.0_aarch64.tbz2

tar xf ${L4T_RELEASE_PACKAGE}
sudo tar xpf ${SAMPLE_FS_PACKAGE} -C Linux_for_Tegra/rootfs/
cd Linux_for_Tegra/
sudo ./tools/l4t_flash_prerequisites.sh
sudo ./apply_binaries.sh

sudo tools/board_automation/boardctl -t topo recovery
sudo ./flash.sh jetson-agx-orin-devkit-maxn mmcblk0p1
```

if you have an external display, follow the prompts on the display to set up a user account and log in. otherwise, use minicom to proceed

`sudo minicom -w -D /dev/ttyACM0` 
### Install nvidia container toolkit:
Install [docker](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) and [nvidia container toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installing-with-apt) following the instructions in the links.

Note: for nvidia container toolkit installation, follow **Installing with Apt** and **Configuring Docker** sections in the link provided above.



### Lock the max clocks

The best ML performance can be achieved with highest power settings. In NVIDIA published Orin benchmarks, the board were configured to use MAXN power profile. The MAXN mode unlock GPU/DLA/CPU/EMC TDP restrictions and is available through flash config switch.

Run the following command under closed/NVIDIA/ to lock the max clocks
```
sudo /usr/sbin/nvpmodel -m 0
sudo jetson_clocks
sudo jetson_clocks --show
```

After this step, you have **finished** the system setup for Orin AGX. 


### USB-C Power Adapters

For performance submission systems, Dell 130.0W Adapter (HA130PM170) were used for Jetson AGX.


## Download Data, Model and Preprocess the data

The data downloading, model downloading and data preprocessing have to be done on **a x86 system**. Please follow the section **Setting up the Scratch Spaces**, **Download the Datasets**, **Downloading the Model files**, **Preprocessing the datasets for inferences** described in [README.md](README.md) to perform the procedure. Note that in MLPerf v4.1, only GPTJ and SDXL benchmarks are supported. 


## Running a Benchmark

As noted in [README.md](README.md) all benchmarks need to run inside a docker container. Follow the steps in **Running your first benchmark** and **Launching the environment on Jetson Orin systems** in the main [README.md](README.md) for instructions on running the benchmarks. And for GPTJ, SDXL, there are also detailed per benchmark instruction located in: `closed/NVIDIA/code/gptj/tensorrt/README.md` and `closed/NVIDIA/code/stable-diffusion-xl/tensorrt/README.md`

By default, Orin will be automatically detected by our system detection algorithm, in case it doesn't, you need to follow **Adding a New or Custom System** as well.

## FAQ
- **Q**: I ran `nvidia-smi` inside the container and the result is 
```
(mlperf) nvidia@mlperf-inference-nvidia-aarch64-15632:/work$ nvidia-smi
NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver. Make sure that the latest NVIDIA driver is installed and running.
```
but the command works outside of container.

**A**: please run `sudo su` once you are inside the container.

- **Q**: I encountered the error below when launching docker:
```
docker: Error response from daemon: failed to create task for container: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: error during container init: error setting rlimits for ready process: error setting rlimit type 8: operation not permitted: unknown.
```
**A**: remove the `--ulimit memlock=-1` from target **launch_docker** in Makefile.docker



- **Q**: I encountered error when launching the docker. The code throws error `Error response from daemon: could not select device driver "" with capabilities: [[gpu]].
nvidia docker is not installed`

**A**: Please make sure you install [NVIDIA container Toolkit](https://github.com/NVIDIA/nvidia-docker) and set it as the default container runtime. You can also set the container runtime by adding `--runtime=nvidia` to the `DOCKER_ARGS`. E.g. `DOCKER_ARGS="--runtime=nvidia"`

- **Q**: I encountered cpu permission error when launching the docker. The code throws error `docker: Error response from daemon: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: unable to apply cgroup configuration: failed to write "0-11"`

**A**: Please check the value of `/sys/fs/cgroup/cpuset/docker/cpuset.cpus` and `/sys/fs/cgroup/cpuset/cpuset.cpus`. You need to reset the value of `/sys/fs/cgroup/cpuset/docker/cpuset.cpus` with the value of `/sys/fs/cgroup/cpuset/cpuset.cpus`. E.g. `sudo echo "0-11" > /sys/fs/cgroup/cpuset/docker/cpuset.cpus`
