import win32com.client
import pythoncom

def cut_three_gaps():
    try:
        pythoncom.CoInitialize()
        # 连接 AutoCAD
        acad = win32com.client.Dispatch("AutoCAD.Application")
        doc = acad.ActiveDocument

        print("[DEBUG] AutoCAD 已连接")

        # 选择对象：返回 (对象, 点坐标)
        obj, pick_point = doc.Utility.GetEntity("选择要切割的对象：")

        # 强制转换类型（解决 COM 类型不匹配问题）
        obj = win32com.client.CastTo(obj, obj.ObjectName)

        # 检查对象类型
        print(f"[DEBUG] 选择的对象类型: {obj.ObjectName}")

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        pythoncom.CoUninitialize()

if __name__ == "__main__":
    cut_three_gaps()
