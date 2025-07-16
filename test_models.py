#!/usr/bin/env python3
"""
模型测试脚本
"""

from datetime import datetime
from models import ValueItem, DataItem, Result, HistoryResponse, TagPoint, Device
import json


def test_value_item():
    """测试 ValueItem 模型"""
    print("=== Testing ValueItem ===")
    now = datetime.now()
    item = ValueItem("test.tag", now, 123.45, 1)
    
    print(f"Original: {item.__dict__}")
    print(f"To dict: {item.to_dict()}")
    print(f"To JSON: {item.to_json()}")
    print()


def test_data_item():
    """测试 DataItem 模型"""
    print("=== Testing DataItem ===")
    now = datetime.now()
    item = DataItem(123.45, now)
    
    print(f"Original: {item.__dict__}")
    print(f"To dict: {item.to_dict()}")
    print(f"To JSON: {item.to_json()}")
    print()


def test_result():
    """测试 Result 模型"""
    print("=== Testing Result ===")
    now = datetime.now()
    data_items = [DataItem(123.45, now), DataItem(67.89, now)]
    result = Result("test.tag", data_items)
    
    print(f"Original: {result.__dict__}")
    print(f"To dict: {result.to_dict()}")
    print(f"To JSON: {result.to_json()}")
    print()


def test_history_response():
    """测试 HistoryResponse 模型"""
    print("=== Testing HistoryResponse ===")
    now = datetime.now()
    data_items = [DataItem(123.45, now)]
    result = Result("test.tag", data_items)
    response = HistoryResponse([result], "Success", "200")
    
    print(f"Original: {response.__dict__}")
    print(f"To dict: {response.to_dict()}")
    print(f"To JSON: {response.to_json()}")
    print()


def test_tag_point():
    """测试 TagPoint 模型"""
    print("=== Testing TagPoint ===")
    point = TagPoint("test.tag", "Test Point")
    
    print(f"Original: {point.__dict__}")
    print(f"To dict: {point.to_dict()}")
    print(f"To JSON: {point.to_json()}")
    print()


def test_device():
    """测试 Device 模型"""
    print("=== Testing Device ===")
    children = [
        Device("device1", "Device 1", [], True),
        Device("device2", "Device 2", [], True)
    ]
    device = Device("group1", "Group 1", children, False)
    
    print(f"Original: {device.__dict__}")
    print(f"To dict: {device.to_dict()}")
    print(f"To JSON: {device.to_json()}")
    print()


def main():
    """主测试函数"""
    print("TopV Adaptor Python - Model Tests")
    print("=" * 50)
    
    test_value_item()
    test_data_item()
    test_result()
    test_history_response()
    test_tag_point()
    test_device()
    
    print("All tests completed!")


if __name__ == "__main__":
    main() 