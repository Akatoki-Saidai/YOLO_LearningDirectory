from ultralytics import YOLO

pt_path = "./modelname.pt"
# モデル読み込み
model = YOLO(pt_path)

# 入力画像
results = model("/test_img.jpg",save=True)

# エクスポート.
# model.export()
