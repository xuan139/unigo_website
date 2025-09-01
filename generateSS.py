import pandas as pd

# 模拟序列号数据
data = {
    "Serial": [
        "0AC3B7D0-0812-39AB-904C-4EF64288FBE0",
        "1B23C4D5-6789-123A-456B-789CDE123456",
        "ABCDEF12-3456-7890-ABCD-EF1234567890"
    ]
}

# 生成 DataFrame
df = pd.DataFrame(data)

# 保存为 Excel 文件
df.to_excel("test_serials.xlsx", index=False)
print("生成 Excel 文件: test_serials.xlsx")

# 也可以生成 CSV 文件
df.to_csv("test_serials.csv", index=False)
print("生成 CSV 文件: test_serials.csv")
