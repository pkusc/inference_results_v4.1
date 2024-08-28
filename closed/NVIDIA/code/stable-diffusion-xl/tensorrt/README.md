# Stable Diffusion XL Benchmark

This benchmark performs object detection using the [Stable Diffusion XL](https://huggingface.co/docs/diffusers/using-diffusers/sdxl) network and a subset of COCO2014 dataset.

:warning: **IMPORTANT**: Please use [closed/NVIDIA](closed/NVIDIA) as the working directory when
running the below commands. :warning:

## Downloading / obtaining the dataset

The dataset used for this benchmark is [5K subset of COCO2014](https://github.com/mlcommons/inference/blob/master/text_to_image/coco2014/captions/captions_source.tsv). You can run `BENCHMARKS=stable-diffusion-xl make download_data` to download the data to `$MLPERF_SCRATCH_PATH/data`.

## Downloading / obtaining the model

The pytorch model is downloaded from the [Hugging Face snapshot](https://cloud.mlcommons.org/index.php/s/DjnCSGyNBkWA4Ro) provided by the MLCommon. The Pytorch model is subsequently processed into 4 onnx models under `$MLPERF_SCRATCH_PATH/models/SDXL/onnx_models`.

Please run `BENCHMARKS=stable-diffusion-xl make download_model` for the download and post-processing.

### Alternative way to download to model when wget links from MLCommons are broken

If 404 is reported during `BENCHMARKS=stable-diffusion-xl make download_model`, you can use the following commands **outside** of the container to download the model weights

```
python3 -m pip install cmind
cm pull repo mlcommons@ck
cm run script --tags=get,ml-model,sdxl,_fp16,_rclone -j
```

NVIDIA's SDXL model weights structure and md5sums look as follows. **You need to move the downloaded fp16 weights in your scratch space following the same structure**.

```
$MLPERF_SCRATCH_PATH/models/SDXL/official_pytorch/fp16/
├── stable_diffusion_fp16
│   ├── checkpoint_pipe
│   │   ├── model_index.json
│   │   ├── scheduler
│   │   │   └── scheduler_config.json
│   │   ├── text_encoder
│   │   │   ├── config.json
│   │   │   └── model.safetensors (81b87e641699a4cd5985f47e99e71eeb)
│   │   ├── text_encoder_2
│   │   │   ├── config.json
│   │   │   └── model.safetensors (5e540a9d92f6f88d3736189fd28fa6cd)
│   │   ├── tokenizer
│   │   │   ├── merges.txt
│   │   │   ├── special_tokens_map.json
│   │   │   ├── tokenizer_config.json
│   │   │   └── vocab.json
│   │   ├── tokenizer_2
│   │   │   ├── merges.txt
│   │   │   ├── special_tokens_map.json
│   │   │   ├── tokenizer_config.json
│   │   │   └── vocab.json
│   │   ├── unet
│   │   │   ├── config.json
│   │   │   └── diffusion_pytorch_model.safetensors (edfa956683fb6121f717d095bf647f53)
│   │   └── vae
│   │       ├── config.json
│   │       └── diffusion_pytorch_model.safetensors (25fe90074af9a0fe36d4a713ad5a3a29)
│   └── checkpoint_scheduler
│       └── scheduler_config.json
```

## Preprocessing the dataset for usage

To process the input captions to numpy files and download the initial noist latent generated by mlcommons, please run `BENCHMARKS=stable-diffusion-xl make prepreocess_data`. The preprocessed data will be saved to `$MLPERF_SCRATCH_PATH/preprocessed_data/coco2014-tokenized-sdxl/5k_dataset_final`.

## Optimizations

### Lower Precision

To further optimize performance, with minimal impact on classification accuracy, we run the UNetXL computations in FP8-INT8-FP16-FP32 mixed precision. Specifically, UNet is quantized to FP8-FP16 and VAE is quantized to INT8-FP32 on datacenter systems.

Note: on Orin for edge submission, we use FP32 VAE engine instead of INT8 VAE engine, and we use INT8 Unet instead of FP8.

### Calibration

UNetXL FP8-INT8-FP16-FP32 mixed precision is calibrated on the [official calibration dataset](https://github.com/mlcommons/inference/blob/master/calibration/COCO-2014/coco_cal_captions_list.txt) using NVIDIA ModelOpt v0.13.1. The quantized models can be found under `${MODEL_DIR}/SDXL/modelopt_models/` after `BENCHMARKS=stable-diffusion-xl make download_model` finishes successfully

## Run Inference through LoadGen

Run the following commands from within the container to run inference through LoadGen:

```
make build
make generate_engines RUN_ARGS="--benchmarks=stable-diffusion-xl --scenarios=<SCENARIO>"
make run_harness RUN_ARGS="--benchmarks=stable-diffusion-xl --scenarios=<SCENARIO> --test_mode=PerformanceOnly"
make run_harness RUN_ARGS="--benchmarks=stable-diffusion-xl --scenarios=<SCENARIO> --test_mode=AccuracyOnly"
```

The performance and the accuracy results will be printed to stdout, and the LoadGen logs can be found in `build/logs`.