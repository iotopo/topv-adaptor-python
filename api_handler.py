import logging
from datetime import datetime
from typing import List, Dict, Any
from models import ValueItem, DataItem, Result, HistoryResponse, TagPoint, Device

logger = logging.getLogger(__name__)


def find_last(data: Dict[str, Any]) -> Dict[str, Any]:
    """查询实时数据"""
    try:
        if not data:
            return {"error": "Invalid request body"}

        project_id = data.get("projectID")
        tag = data.get("tag")
        device = data.get("device", False)

        logger.info(f"find_last: projectID={project_id}, tag={tag}, device={device}")

        now = datetime.now()
        
        if device:
            # 查询设备标签下的所有测点
            response = [ValueItem(tag, now, "12.3", 1).to_dict()]
        else:
            # 查询单个测点
            response = ValueItem(tag, now, "12.3", 1).to_dict()

        return response

    except Exception as e:
        logger.error(f"Error in find_last: {e}")
        return {"error": str(e)}


def set_value(data: Dict[str, Any]) -> Dict[str, Any]:
    """设置值"""
    try:
        if not data:
            return {"error": "Invalid request body"}

        project_id = data.get("projectID")
        tag = data.get("tag")
        value = data.get("value")
        time = data.get("time")

        logger.info(f"set_value: projectID={project_id}, tag={tag}, value={value}, time={time}")

        response = {
            "code": "success",
            "msg": "Value set successfully"
        }

        return response

    except Exception as e:
        logger.error(f"Error in set_value: {e}")
        return {"error": str(e)}


def query_history(data: Dict[str, Any]) -> Dict[str, Any]:
    """查询历史数据"""
    try:
        if not data:
            return {"error": "Invalid request body"}

        project_id = data.get("projectID")
        tags = data.get("tag", [])
        interval = data.get("interval")
        start = data.get("start")
        end = data.get("end")
        offset = data.get("offset")
        limit = data.get("limit")
        order = data.get("order")

        logger.info(f"query_history: projectID={project_id}, tags={tags}, interval={interval}, "
                   f"start={start}, end={end}, offset={offset}, limit={limit}, order={order}")

        results = []
        if tags:
            # 为每个标签创建结果
            for tag in tags:
                data_item = DataItem("12.3", datetime.now())
                result = Result(tag, [data_item])
                results.append(result)

        response = HistoryResponse(results)
        return response.to_dict()

    except Exception as e:
        logger.error(f"Error in query_history: {e}")
        return {"error": str(e)}


def query_points(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """查询测点标签"""
    try:
        if not data:
            return [{"error": "Invalid request body"}]

        project_id = data.get("projectID")
        parent_tag = data.get("parentTag")

        logger.info(f"query_points: projectID={project_id}, parentTag={parent_tag}")

        points = [
            TagPoint(f"{parent_tag}.a", "a"),
            TagPoint(f"{parent_tag}.b", "b"),
            TagPoint(f"{parent_tag}.c", "c")
        ]

        response = [point.to_dict() for point in points]
        return response

    except Exception as e:
        logger.error(f"Error in query_points: {e}")
        return [{"error": str(e)}]


def query_devices(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """查询设备标签"""
    try:
        if not data:
            return [{"error": "Invalid request body"}]

        project_id = data.get("projectID")

        logger.info(f"query_devices: projectID={project_id}")

        devices = []

        # Group 1
        group1_children = [
            Device("group1.dev1", "dev1", [], True),
            Device("group1.dev2", "dev2", [], True),
            Device("group1.dev3", "dev3", [], True)
        ]
        devices.append(Device("group1", "group1", group1_children, False))

        # Group 2
        group2_children = [
            Device("group2.dev1", "dev1", [], True),
            Device("group2.dev2", "dev2", [], True),
            Device("group2.dev3", "dev3", [], True)
        ]
        devices.append(Device("group2", "group2", group2_children, False))

        # Group 3
        group3_children = [
            Device("group3.dev1", "dev1", [], True),
            Device("group3.dev2", "dev2", [], True),
            Device("group3.dev3", "dev3", [], True)
        ]
        devices.append(Device("group3", "group3", group3_children, False))

        response = [device.to_dict() for device in devices]
        return response

    except Exception as e:
        logger.error(f"Error in query_devices: {e}")
        return [{"error": str(e)}] 