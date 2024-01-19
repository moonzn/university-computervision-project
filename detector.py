from ultralytics.models.yolo.detect import DetectionPredictor

DATASET_FOLDER = ".crown_dataset_filtered"

args = dict(model='yolo\\yolov8n-face.pt', source=DATASET_FOLDER)
predictor = DetectionPredictor(overrides=args)
predictor.predict_cli()
