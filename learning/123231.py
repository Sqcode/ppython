
s = "【1【1【3【1【】23】"
left_value = s[:s.find("【")].strip()

auxPropertyId = 100001
result = '尺码' if auxPropertyId == 100001 else ('款型' if auxPropertyId == 100002 else '其他')



print(result)  # 输出 "11【1【】"