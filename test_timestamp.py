#!/usr/bin/env python3
"""
时间戳格式测试脚本
"""

from datetime import datetime
from models import ValueItem, DataItem
import json


def test_timestamp_format():
    """测试时间戳格式"""
    print("=== Testing Timestamp Format ===")
    
    now = datetime.now()
    print(f"Original datetime: {now}")
    print(f"ISO format: {now.isoformat()}")
    print(f"RFC3339 format: {now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')}")
    
    # 测试 ValueItem
    value_item = ValueItem("test.tag", now, 123.45, 1)
    value_dict = value_item.to_dict()
    print(f"\nValueItem timestamp: {value_dict['timestamp']}")
    
    # 测试 DataItem
    data_item = DataItem(123.45, now)
    data_dict = data_item.to_dict()
    print(f"DataItem time: {data_dict['time']}")
    
    # 测试 JSON 序列化
    value_json = value_item.to_json()
    print(f"\nValueItem JSON: {value_json}")
    
    data_json = data_item.to_json()
    print(f"DataItem JSON: {data_json}")
    
    print("\nTimestamp format test completed!")


if __name__ == "__main__":
    test_timestamp_format() 