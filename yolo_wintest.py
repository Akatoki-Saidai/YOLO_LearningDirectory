import time
from ultralytics import YOLO
import cv2
import numpy as np

# 同じディレクトリに重みを置く
pt_path = "./modelname.pt"

class Camera:
    def yolo_detect(self, frame):
        # YOLOによる画像認識
        try:
            yolo_xylist = None
            center_x = 0
            
            # YOLOv10nモデルをロード
            model = YOLO(pt_path)
            # 推論
            yolo_results = model.predict(frame, save = False, show = False)
            # print(type(yolo_results))
            # print(yolo_results)

            confidence_best = 0
            # 最も信頼性の高いBounding Boxを取得
            yolo_result = yolo_results[0]
            # print("yolo_result: ",yolo_result)
            # バウンディングボックス情報を NumPy 配列で取得
            Bounding_box = yolo_result.boxes.xyxy.numpy()
            # print("Bounding_box: ", Bounding_box)
            confidences = yolo_result.boxes.conf.numpy()
            # print("confidences: ", confidences)

            if len(Bounding_box) == 0:
                print("No objects detected.")

            else:
                for i in range(len(Bounding_box)):
                    confidence = confidences[i]
                    if confidence < confidence_best:
                        continue
                    else:
                        confidence_best = confidence
                    xmin, ymin, xmax, ymax = Bounding_box[i]

                center_x = int(xmin + (xmax - xmin) / 2)
                yolo_xylist = [xmin, ymin, xmax, ymax, confidence]

            return yolo_xylist, center_x
        except Exception as e:
            print(f"An error occured in reasoning by yolo: {e}")
            

if __name__ == '__main__':
    try:
        # カメラをセットアップ
        cam = Camera()
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480) # カメラ画像の横幅
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320) # カメラ画像の縦幅

    except Exception as e:
        print(f"An error occured in setup camera: {e}")

    while(cap.isOpened()):
        try:
            # フレームを取得
            ret, frame = cap.read()

            # 画像がRGBAの場合はRGBに変換
            if frame.shape[2] == 4:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)  # BGRA → BGR(RGBと等価)

        except Exception as e:
            print(f"An error occured in getting camera frame: {e}")

        try:
            # YOLOによって画像認識
            yolo_xylist = None
            frame_center_x = frame.shape[1] // 2
            colorcone_x = 0
            
            yolo_xylist, yolo_center_x = cam.yolo_detect(frame)
            print(f"yolo_xylist: {yolo_xylist}, yolo_center_x: {yolo_center_x}")
            
            colorcone_x = yolo_center_x - frame_center_x
            
        except Exception as e:
            print(f"An error occured in yolo_detect: {e}")

        try:
            # カラーコーンが画像内のどの部分にあるかを判断
            # camera_order: 0:不明, 1:直進, 2:右へ, 3:左へ
            if -50 <= colorcone_x <= 50:
                print("The yolo object is in the center")
                camera_order = 1
            elif colorcone_x > 50:
                print("The yolo object is in the right")
                camera_order = 2
            elif colorcone_x < -50:
                print("The yolo object is in the left")
                camera_order = 3
            else:
                print("The yolo object is none")
                camera_order = 0
                 
        except Exception as e:
            print(f"An error occured in result: {e}")
            
        try:
            # バウンディングボックスを表示する
            if yolo_xylist is not None:
                cv2.rectangle(frame, (int(yolo_xylist[0]), int(yolo_xylist[1])), (int(yolo_xylist[2]), int(yolo_xylist[3])), (255, 0, 0), 2)
                cv2.putText(frame, str(yolo_xylist[4]), (int(yolo_xylist[0]), int(yolo_xylist[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0))

            # 結果表示
            cv2.imshow('kekka', frame)
            time.sleep(0.5)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                print("pressed q interrupted")

        except Exception as e:
            print(f"An error occured in showing Bounding Box: {e}")
                    
        


