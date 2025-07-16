from datetime import datetime
from typing import List, Optional, Any, Dict
import json


class ValueItem:
    def __init__(self, tag: str, timestamp: datetime, value: Any, quality: int = 1):
        self.tag = tag
        self.timestamp = timestamp
        self.value = value
        self.quality = quality

    def to_dict(self) -> Dict:
        return {
            "tag": self.tag,
            "timestamp": self.timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "value": self.value,
            "quality": self.quality
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class DataItem:
    def __init__(self, value: Any = None, time: Optional[datetime] = None):
        self.value = value
        self.time = time

    def to_dict(self) -> Dict:
        result = {}
        if self.value is not None:
            result["value"] = self.value
        if self.time is not None:
            result["time"] = self.time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return result

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class Result:
    def __init__(self, tag: str, values: List[DataItem]):
        self.tag = tag
        self.values = values

    def to_dict(self) -> Dict:
        return {
            "tag": self.tag,
            "values": [item.to_dict() for item in self.values]
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class HistoryResponse:
    def __init__(self, results: List[Result], msg: Optional[str] = None, code: Optional[str] = None):
        self.results = results
        self.msg = msg
        self.code = code

    def to_dict(self) -> Dict:
        result = {
            "results": [item.to_dict() for item in self.results]
        }
        if self.msg is not None:
            result["msg"] = self.msg
        if self.code is not None:
            result["code"] = self.code
        return result

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class TagPoint:
    def __init__(self, tag: Optional[str] = None, name: Optional[str] = None):
        self.tag = tag
        self.name = name

    def to_dict(self) -> Dict:
        result = {}
        if self.tag is not None:
            result["tag"] = self.tag
        if self.name is not None:
            result["name"] = self.name
        return result

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class Device:
    def __init__(self, tag: Optional[str] = None, name: Optional[str] = None, 
                 children: Optional[List['Device']] = None, is_device: bool = False):
        self.parent_tag = None  # 内部使用，不序列化
        self.tag = tag
        self.name = name
        self.children = children or []
        self.is_device = is_device

    def to_dict(self) -> Dict:
        result = {}
        if self.tag is not None:
            result["tag"] = self.tag
        if self.name is not None:
            result["name"] = self.name
        if self.children:
            result["children"] = [child.to_dict() for child in self.children]
        result["isDevice"] = self.is_device
        return result

    def to_json(self) -> str:
        return json.dumps(self.to_dict()) 