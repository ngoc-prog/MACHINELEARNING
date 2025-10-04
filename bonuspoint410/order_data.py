import pandas as pd

# Đọc dữ liệu từ file CSV
df = pd.read_csv('data/order_data.csv')


# Hàm lọc và sắp xếp dữ liệu
def filter_and_sort(df, minValue, maxValue, SortType):
    # Lọc các hóa đơn có tổng giá trị nằm trong khoảng [minValue, maxValue]
    filtered_df = df[(df['Sum'] >= minValue) & (df['Sum'] <= maxValue)]

    # Sắp xếp theo SortType
    if SortType:
        sorted_df = filtered_df.sort_values(by='Sum', ascending=True)
    else:
        sorted_df = filtered_df.sort_values(by='Sum', ascending=False)

    # Trả về DataFrame đã lọc và sắp xếp
    return sorted_df


# Gọi hàm với ví dụ
minValue = 500
maxValue = 900
SortType = True
result_df = filter_and_sort(df, minValue, maxValue, SortType)

# Hiển thị kết quả dưới dạng bảng
print(result_df)
