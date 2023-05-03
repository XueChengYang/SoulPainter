# -*- coding=utf-8 -*-
# Code version：0.1
# 更新用配置文件作为默认设置，增加缩放比例可调cfg_scale
import gradio as gr
import json
import io
from PIL import ImageOps,Image
import base64
import requests
import time

# def setargs(enable_hr, prompt, seed, steps, negative_prompt, control_weight, control_model, control_guessmodel):
def setargs(enable_hr, prompt, steps, cfg_scale,negative_prompt, control_weight, control_model, control_guessmodel):
    if enable_hr == False:
        payload["enable_hr"] = "false"
    else:
        payload["enable_hr"] = "true"
    payload["prompt"] = prompt
    # payload["seed"] = seed
    payload["steps"] = int(steps)
    payload["cfg_scale"] = int(cfg_scale)
    payload["negative_prompt"] = ','.join(['nude','sex','bloodiness',str(negative_prompt)])
    payload["controlnet_units"][0]["weight"] = control_weight
    payload["controlnet_units"][0]["model"] = control_model
    if control_guessmodel == False:
        payload["controlnet_units"][0]["guessmode"] = "false"
    else:
        payload["controlnet_units"][0]["guessmode"] = "true"
    print(payload)
    return payload


def startjob(img,payload):
    data = io.BytesIO()
    img.save(data,format='PNG')
    data = base64.b64encode(data.getvalue()).decode('utf-8')
    payload['controlnet_units'][0]['input_image'] = data
    # print('paint prompt:', payload['prompt'])
    response = requests.post(url=f'{url}/controlnet/txt2img', json=payload)
    r = response.json()
    return_img = r['images'][0]
    img_bytes = io.BytesIO(base64.b64decode(return_img))
    re_img = Image.open(img_bytes)
    return re_img



small_and_beautiful_theme = gr.themes.Soft(
    primary_hue=gr.themes.Color(
        c50="#02C160",
        c100="rgba(2, 193, 96, 0.2)",
        c200="#02C160",
        c300="rgba(2, 193, 96, 0.32)",
        c400="rgba(2, 193, 96, 0.32)",
        c500="rgba(2, 193, 96, 1.0)",
        c600="rgba(2, 193, 96, 1.0)",
        c700="rgba(2, 193, 96, 0.32)",
        c800="rgba(2, 193, 96, 0.32)",
        c900="#02C160",
        c950="#02C160",
    ),
    secondary_hue=gr.themes.Color(
        c50="#576b95",
        c100="#576b95",
        c200="#576b95",
        c300="#576b95",
        c400="#576b95",
        c500="#576b95",
        c600="#576b95",
        c700="#576b95",
        c800="#576b95",
        c900="#576b95",
        c950="#576b95",
    ),
    neutral_hue=gr.themes.Color(
        name="gray",
        c50="#f9fafb",
        c100="#f3f4f6",
        c200="#e5e7eb",
        c300="#d1d5db",
        c400="#B2B2B2",
        c500="#808080",
        c600="#636363",
        c700="#515151",
        c800="#393939",
        c900="#272727",
        c950="#171717",
    ),
    radius_size=gr.themes.sizes.radius_sm,
).set(
    button_primary_background_fill="#06AE56",
    button_primary_background_fill_dark="#06AE56",
    button_primary_background_fill_hover="#07C863",
    button_primary_border_color="#06AE56",
    button_primary_border_color_dark="#06AE56",
    button_primary_text_color="#FFFFFF",
    button_primary_text_color_dark="#FFFFFF",
    button_secondary_background_fill="#F2F2F2",
    button_secondary_background_fill_dark="#2B2B2B",
    button_secondary_text_color="#393939",
    button_secondary_text_color_dark="#FFFFFF",
    # background_fill_primary="#F7F7F7",
    # background_fill_primary_dark="#1F1F1F",
    block_title_text_color="*primary_500",
    block_title_background_fill="*primary_100",
    input_background_fill="#F6F6F6",
)

url = "127.0.0.1:7890"
# 读预设传参
with open("configs/payload.json", "r") as f:
    payload = json.load(f)

# 预读配置文件
with open("configs/sd_config.json", "r") as f:
    sd_conf = json.load(f)
url = sd_conf["server"] if sd_conf["server"] != "" else url
seed = sd_conf["seed"]


with gr.Blocks(theme=small_and_beautiful_theme,css="sty.css",title="SoulPainter") as demo:
    sdconfm = gr.State(sd_conf)
    payloadm = gr.State(payload)
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Row():
                with gr.Column(scale=7):
                    prompt = gr.Textbox(value=payload['prompt'], lines=2, max_lines=6, label="要画(请用英语输入):")
                with gr.Column(scale=1):
                    clear = gr.Button(value="清空提示").style(full_width=1)
                clear.click(lambda x: gr.Textbox.update(value=""), outputs=prompt)
            with gr.Row():
                with gr.Column(scale=7):
                    negative_prompt = gr.Textbox(value="", lines=2, max_lines=6, label="不画:")
                with gr.Column(scale=1):
                    clear = gr.Button(value="清空提示").style(full_width=1)
                clear.click(lambda x: gr.Textbox.update(value=""), outputs=negative_prompt)
            with gr.Row():
                with gr.Row():
                    #enable_hr = gr.Checkbox(value=payload['enable_hr'], label="是否启用高清")
                    #control_guessmodel = gr.Checkbox(value=payload['controlnet_units'][0]['guessmode'], label="是否启用画笔推理")
                    enable_hr = gr.Checkbox(value=False, label="是否启用高清")
                    control_guessmodel = gr.Checkbox(value=False, label="是否启用画笔推理")
                with gr.Row():
                    steps = gr.Number(value=payload['steps'], label="运算步数")
                    cfg_scale = gr.Number(value=payload['cfg_scale'], label="缩放比例")
            with gr.Row():
                with gr.Column():
                    control_weight = gr.Number(value=payload['controlnet_units'][0]['weight'], label="线条权重")
                with gr.Column():
                    control_model = gr.Dropdown(sd_conf['model'], value=sd_conf['model'][0], type="value", label="controlnet模型选择")
            with gr.Row():
                with gr.Column():
                    runbtn = gr.Button(value="提交")
            # runbtn.click(fn=setargs, inputs=[enable_hr, prompt, seed_gr, steps, negative_prompt, control_weight, control_model, control_guessmodel])
            runbtn.click(fn=setargs, inputs=[enable_hr, prompt, steps, cfg_scale,negative_prompt, control_weight, control_model, control_guessmodel], outputs=payloadm)
        with gr.Column(scale=5):
            gr.Markdown("Soul-Painter")
            with gr.Row():
                with gr.Column():
                    with gr.Row():
                        inImg = gr.Image(image_mode="L",source="canvas",type="pil",tool="color-sketch").style(height=512,width=512)
                    with gr.Row():
                        stopbtn = gr.Button(value="取消")
                        startbtn = gr.Button(value="画画",elem_id="button")
                with gr.Column():
                    outImg = gr.Image(interactive=False,show_progress=True).style(height=512,width=512)
                    resetbtn = gr.Button(value="清除画布")
        startbtn.click(fn = setargs, inputs=[enable_hr, prompt, steps, cfg_scale,negative_prompt, control_weight, control_model, control_guessmodel], outputs=payloadm)
        startbtn.click(fn = startjob,inputs=[inImg,payloadm],outputs=outImg)
        resetbtn.click(fn = lambda x:None,outputs=outImg)
demo.launch(server_name='0.0.0.0',server_port=8860)
