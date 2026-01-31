def test_list_endpoints(client):
    response = client.get("/api/endpoints")
    assert response.status_code == 200
    
    data = response.json
    assert "count" in data
    assert "endpoints" in data
    assert isinstance(data["endpoints"], list)
    
    # 验证是否包含我们已知的接口
    endpoints = data["endpoints"]
    paths = [e["path"] for e in endpoints]
    
    assert "/health" in paths
    assert "/api/users" in paths
    assert "/api/posts" in paths
    assert "/api/tags" in paths
    assert "/api/endpoints" in paths
    
    # 验证详情
    health_endpoint = next(e for e in endpoints if e["path"] == "/health")
    assert "GET" in health_endpoint["methods"]
    assert health_endpoint["endpoint"] == "health.health"
    
    # 验证 docstring 提取
    endpoints_endpoint = next(e for e in endpoints if e["path"] == "/api/endpoints")
    assert "列出所有注册的 API 接口" in endpoints_endpoint["description"]
