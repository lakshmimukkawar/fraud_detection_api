import pytest


class TestFraudDetectionEndpoint:
    def test_fraud_detection_endpoint_should_succeed(self, client, input_examples):
        response = client.post("/fraud_detection", json=[input_examples])
        assert response.status_code == 200

    def test_fraud_detection_endpoint_should_return_400_when_input_params_are_different(
        self, client, wrong_input
    ):
        response = client.post("/fraud_detection", json=wrong_input)
        assert response.status_code == 422
