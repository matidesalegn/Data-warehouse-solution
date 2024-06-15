import pytest
from detect_objects import run_object_detection

@pytest.fixture
def mock_yolo(mocker):
    # Mock the YOLO detection model
    mock_yolo_model = mocker.patch('detect_objects.YOLO')
    return mock_yolo_model

def test_run_object_detection(mock_yolo):
    mock_yolo.return_value.detect.return_value = [
        {'label': 'object1', 'confidence': 0.9},
        {'label': 'object2', 'confidence': 0.8}
    ]

    run_object_detection('images/test_image.jpg')

    # Check if the detection results were saved correctly
    assert os.path.exists('detection_results/results.csv')

    with open('detection_results/results.csv', 'r') as file:
        content = file.read()
        assert 'object1' in content
        assert 'object2' in content