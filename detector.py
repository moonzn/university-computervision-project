from ultralytics.models.yolo.detect import DetectionPredictor

args = dict(model='yolo\\yolov8n-face.pt', source="assets")
predictor = DetectionPredictor(overrides=args)
predictor.predict_cli()
