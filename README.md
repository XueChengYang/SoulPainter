# SoulPainter
Generating Beautiful Images Through Sketching with a Paintbrush.

Enabling the Function of Generating Images by Mouse Drawing Black and White Line Sketches using Stable Diffusion and Controlnet Plugins.Before use, please ensure that you have deployed StableDiffusion, enabled the Controlnet plugin, and loaded the basic generation model and control_v11p_sd15_scribble model.

## 1.Deploy stable diffusion and ensure that the base model has been loaded.Please refer to the [Stable-Diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) project for this step.

## 2.Please install the Controlnet plugin for SD and make sure that the available models include control_v11p_sd15_scribble. Please refer to the [Controlnet](https://github.com/Mikubill/sd-webui-controlnet) project for this step.

## 3.Edit the configuration files for Soulpainter. sd_config.json is related to StableDiffusion API, while payload.json is about default configuration.

## 4.run app

```bash
python appv0.py
```

## 5.Access http://localhost:8860 in your browser and embark on your painting journey.

If the program prompts that there is a lack of dependent libraries during its execution,please:

```bash
pip install -r requirements.txt
```

![2023-05-03 14-01-41](https://github.com/XueChengYang/SoulPainter/blob/main/img/2023-05-03%2014-01-41.jpg)
