def test_lambda_post_create(monkeypatch):
    from app import lambda_handler

    def mock_put_task(task_id, description):
        return {}

    monkeypatch.setattr("utils.db.put_task", mock_put_task)

    event = {
        "httpMethod": "POST",
        "path": "/task",
        "body": '{"id": "123", "description": "Test task"}'
    }
    result = lambda_handler(event, None)
    assert result["statusCode"] == 201
