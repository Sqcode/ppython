data = [
    {
        "Visible": True,
        "Key": "FBillNo",
        "ColIndex": 3,
        "Caption": [
            {
                "Value": "单据编号"
            }
        ],
        "FieldName": "FBILLNO",
        "RealKey": "FBillNo"
    },
    {
        "Visible": True,
        "Key": "FDocumentStatus",
        "ColIndex": 4,
        "Caption": [
            {
                "Value": "单据状态"
            }
        ],
        "FieldName": "FDOCUMENTSTATUS",
        "RealKey": "FDocumentStatus"
    },
    {
        "Visible": True,
        "Key": "FMaterialID.FNumber",
        "ColIndex": 5,
        "Caption": [
            {
                "Value": "商品编码"
            }
        ],
        "RealKey": "FMaterialID"
    },
    {
        "Visible": True,
        "Key": "FMateriaName",
        "ColIndex": 6,
        "Caption": [
            {
                "Value": "商品名称"
            }
        ],
        "RealKey": "FMateriaName"
    }
]


# 按照"ColIndex"升序排序
sorted_data = sorted(data, key=lambda item: item["ColIndex"])

# 提取"Key"和相应"Caption"里的"Value"
key_value_dict = {item["RealKey"]: item["Caption"][0]["Value"] for item in sorted_data}


print(key_value_dict)
