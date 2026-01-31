from flask import Blueprint, current_app, jsonify
import re

bp = Blueprint("endpoints", __name__, url_prefix="/api/endpoints")

@bp.get("")
def list_endpoints():
    """
    列出所有注册的 API 接口及其用法信息。
    返回格式包括路径、允许的方法、Endpoint 名称、文档说明等。
    """
    output = []
    
    for rule in current_app.url_map.iter_rules():
        # 过滤掉静态文件路由和内部路由
        if rule.endpoint == 'static':
            continue
            
        # 获取视图函数
        view_func = current_app.view_functions.get(rule.endpoint)
        docstring = view_func.__doc__ if view_func else None
        
        # 清理 docstring (去除多余空白)
        description = ""
        if docstring:
            description = "\n".join([line.strip() for line in docstring.strip().split("\n") if line.strip()])

        # 提取参数
        arguments = list(rule.arguments)
        
        output.append({
            "path": str(rule),
            "methods": list(rule.methods - {"HEAD", "OPTIONS"}) if rule.methods else [],
            "endpoint": rule.endpoint,
            "description": description,
            "arguments": arguments,
        })
    
    # 按路径排序
    output.sort(key=lambda x: x["path"])
    
    return jsonify({
        "count": len(output),
        "endpoints": output
    })
