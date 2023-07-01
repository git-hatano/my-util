import subprocess

# setting
# model
# model_name = "yolox-s"
# model_name = "yolox-x"
model_name = "yolox-tiny"

# weight
# ckpt_path = "./model/yolox_s.pth"
# ckpt_path = "model/yolox_x.pth"
ckpt_path = "model/yolox_tiny.pth"

# input
input_type = "image" #"video"
# input_path = "assets/dog.jpg"
input_path = "image/test"

conf = 0.5 #0.25
nms = 0.45
tsize = 640
device = "cpu" #"gpu"


# 実行コマンド
cmd = [
    "python", "tools/demo.py", 
    input_type, 
    "-n", model_name,
    "-c", ckpt_path,
    "--path", input_path,
    "--conf", str(conf),
    "--nms", str(nms),
    "--tsize", str(tsize),
    "--save_result",
    "--device", device,
]

# コマンド実行
subprocess.run(cmd)
