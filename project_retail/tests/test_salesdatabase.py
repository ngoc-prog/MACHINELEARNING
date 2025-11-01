import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
from project_retail.connectors.connector import Connector

# Kết nối database
conn = Connector(database="salesdatabase")
conn.connect()

# Lấy dữ liệu
sql = "select * from customer"
df = conn.queryDataset(sql)
print(df)

sql2 = ("select distinct customer.CustomerId, Age, Annual_Income, Spending_Score from customer, customer_spend_score "
        "where customer.CustomerId = customer_spend_score.CustomerID")
df2 = conn.queryDataset(sql2)
print(df2)

print(df2.head())
print(df2.describe())

# Kiểm tra và xử lý dữ liệu null
print(f"\nShape of df2: {df2.shape}")
print(f"Null values:\n{df2.isnull().sum()}")
df2 = df2.dropna()  # Xóa các dòng có giá trị null

def showHistogram(df, columns):
    plt.figure(figsize=(7, 8))
    n = 0
    for column in columns:
        n += 1
        plt.subplot(3, 1, n)
        plt.subplots_adjust(hspace=0.5, wspace=0.5)
        sns.histplot(df[column], bins=32)
        plt.title(f'Histogram of {column}')
    plt.show()

showHistogram(df2, df2.columns[1:])

def elbowMethod(df, columnsForElbow):
    X = df.loc[:, columnsForElbow].values
    inertia = []
    for n in range(1, 11):
        model = KMeans(n_clusters=n,
                       init='k-means++',
                       max_iter=500,
                       random_state=42)
        model.fit(X)
        inertia.append(model.inertia_)

    plt.figure(figsize=(15, 6))
    plt.plot(np.arange(1, 11), inertia, 'o')
    plt.plot(np.arange(1, 11), inertia, '-', alpha=0.5)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Cluster sum of squared distances')
    plt.show()

columns = ['Age', 'Spending_Score']
elbowMethod(df2, columns)

def runKMeans(X, cluster):
    model = KMeans(n_clusters=cluster,
                   init='k-means++',
                   max_iter=500,
                   random_state=42)
    model.fit(X)
    labels = model.labels_
    centroids = model.cluster_centers_
    y_kmeans = model.fit_predict(X)
    return y_kmeans, centroids, labels

X = df2.loc[:, columns].values
print(f"\nX shape: {X.shape}")
print(f"X sample:\n{X[:5]}")

cluster = 5  # Chỉnh số lượng cluster phù hợp
colors = ["red", "green", "blue", "purple", "orange"]  # Cập nhật mảng màu

y_kmeans, centroids, labels = runKMeans(X, cluster)
print(f"\ny_kmeans: {y_kmeans}")
print(f"Centroids:\n{centroids}")
print(f"Labels: {labels}")

df2["cluster"] = labels

def visualizeKMeans(X, y_kmeans, cluster, title, xlabel, ylabel, colors):
    plt.figure(figsize=(10, 8))
    for i in range(cluster):
        plt.scatter(X[y_kmeans == i, 0],
                    X[y_kmeans == i, 1],
                    s=100,
                    c=colors[i],
                    label=f'Cluster {i + 1}')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

visualizeKMeans(X,
                y_kmeans,
                cluster,
                "Clusters of Customers - Age X Spending Score",
                "Age",
                "Spending Score",
                colors)

# Xử lý thêm một tập dữ liệu khác với cột 'Annual_Income' và 'Spending_Score'
columns = ['Annual_Income', 'Spending_Score']
elbowMethod(df2, columns)

X = df2.loc[:, columns].values
cluster = 5  # Chỉnh số lượng cluster phù hợp

y_kmeans, centroids, labels = runKMeans(X, cluster)

print(f"\ny_kmeans: {y_kmeans}")
print(f"Centroids:\n{centroids}")
print(f"Labels: {labels}")

df2["cluster"] = labels

visualizeKMeans(X,
                y_kmeans,
                cluster,
                "Clusters of Customers - Annual Income X Spending Score",
                "Annual Income",
                "Spending Score",
                colors)

columns = ['Age', 'Annual_Income', 'Spending_Score']
elbowMethod(df2, columns)

X = df2.loc[:, columns].values
cluster = 6

y_kmeans, centroids, labels = runKMeans(X, cluster)

print(y_kmeans)
print(centroids)
print(labels)

df2["cluster"] = labels
print(df2)

# Hàm vẽ 3D KMeans
import plotly.express as px
def visualize3DKmeans(df, columns, hover_data, cluster):
    fig = px.scatter_3d(
        df,
        x=columns[0],
        y=columns[1],
        z=columns[2],
        color='cluster',
        hover_data=hover_data,
        category_orders={"cluster": range(0, cluster)},
    )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig.show()

hover_data = df2.columns
visualize3DKmeans(df2, columns, hover_data, cluster)


# Hàm 1: Lọc customers theo từng cluster (giữ nguyên)
def getCustomersByCluster(df, cluster_number):
    """
    Lọc ra danh sách customers thuộc một cluster cụ thể

    Parameters:
    df: DataFrame chứa dữ liệu customers và cluster
    cluster_number: Số thứ tự cluster cần lọc (0, 1, 2, ...)

    Returns:
    DataFrame chứa thông tin customers của cluster đó
    """
    cluster_df = df[df['cluster'] == cluster_number].copy()
    cluster_df = cluster_df.sort_values('CustomerId')
    return cluster_df


# Hàm 2: Tạo HTML với nút chọn cluster
def exportClustersToHTML(df, total_clusters, output_file='customer_clusters.html'):
    """
    Tạo file HTML hiển thị danh sách customers theo từng cluster với nút chọn

    Parameters:
    df: DataFrame chứa dữ liệu customers và cluster
    total_clusters: Tổng số clusters
    output_file: Tên file HTML output
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Customer Clusters Analysis</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }

            .container {
                max-width: 1400px;
                margin: 0 auto;
                background-color: white;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                overflow: hidden;
            }

            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }

            .header h1 {
                font-size: 36px;
                margin-bottom: 10px;
            }

            .summary {
                display: flex;
                justify-content: center;
                gap: 40px;
                margin-top: 20px;
            }

            .summary-item {
                text-align: center;
            }

            .summary-value {
                font-size: 32px;
                font-weight: bold;
            }

            .summary-label {
                font-size: 14px;
                opacity: 0.9;
                margin-top: 5px;
            }

            .controls {
                padding: 30px;
                background-color: #f8f9fa;
                border-bottom: 2px solid #e9ecef;
            }

            .controls h2 {
                color: #333;
                margin-bottom: 20px;
                font-size: 24px;
            }

            .button-group {
                display: flex;
                flex-wrap: wrap;
                gap: 15px;
            }

            .cluster-btn {
                padding: 12px 24px;
                border: 2px solid #667eea;
                background-color: white;
                color: #667eea;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
                transition: all 0.3s ease;
                min-width: 120px;
            }

            .cluster-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
            }

            .cluster-btn.active {
                background-color: #667eea;
                color: white;
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }

            .show-all-btn {
                padding: 12px 30px;
                border: none;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
                transition: all 0.3s ease;
                min-width: 150px;
            }

            .show-all-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(245, 87, 108, 0.4);
            }

            .content {
                padding: 30px;
            }

            .cluster-section {
                background-color: white;
                margin: 20px 0;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.1);
                border-left: 5px solid;
                display: none;
            }

            .cluster-section.show {
                display: block;
                animation: fadeIn 0.5s ease;
            }

            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .cluster-section.cluster-0 { border-left-color: #FF6B6B; }
            .cluster-section.cluster-1 { border-left-color: #4ECDC4; }
            .cluster-section.cluster-2 { border-left-color: #45B7D1; }
            .cluster-section.cluster-3 { border-left-color: #96CEB4; }
            .cluster-section.cluster-4 { border-left-color: #FFEAA7; }
            .cluster-section.cluster-5 { border-left-color: #DFE6E9; }

            .cluster-header {
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 20px;
                padding: 15px;
                border-radius: 8px;
                color: white;
                display: inline-block;
            }

            .cluster-0 .cluster-header { background-color: #FF6B6B; }
            .cluster-1 .cluster-header { background-color: #4ECDC4; }
            .cluster-2 .cluster-header { background-color: #45B7D1; }
            .cluster-3 .cluster-header { background-color: #96CEB4; }
            .cluster-4 .cluster-header { background-color: #FFEAA7; color: #333; }
            .cluster-5 .cluster-header { background-color: #DFE6E9; color: #333; }

            .stats {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
            }

            .stats-item {
                text-align: center;
            }

            .stats-label {
                font-weight: bold;
                color: #555;
                font-size: 14px;
                display: block;
                margin-bottom: 5px;
            }

            .stats-value {
                color: #667eea;
                font-size: 24px;
                font-weight: bold;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                background-color: white;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }

            th {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px;
                text-align: left;
                font-weight: bold;
                font-size: 14px;
                text-transform: uppercase;
            }

            td {
                padding: 12px 15px;
                border-bottom: 1px solid #f0f0f0;
                font-size: 14px;
            }

            tr:hover {
                background-color: #f8f9fa;
            }

            tr:last-child td {
                border-bottom: none;
            }

            .no-data {
                text-align: center;
                padding: 60px 20px;
                color: #999;
                font-size: 18px;
            }

            .no-data-icon {
                font-size: 64px;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎯 Customer Segmentation Analysis</h1>
                <div class="summary">
                    <div class="summary-item">
                        <div class="summary-value">""" + str(len(df)) + """</div>
                        <div class="summary-label">Total Customers</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">""" + str(total_clusters) + """</div>
                        <div class="summary-label">Clusters</div>
                    </div>
                </div>
            </div>

            <div class="controls">
                <h2>📊 Select Cluster to View</h2>
                <div class="button-group">
                    <button class="show-all-btn" onclick="showAllClusters()">Show All Clusters</button>
    """

    # Tạo nút cho từng cluster
    for i in range(total_clusters):
        html_content += f"""
                    <button class="cluster-btn" onclick="showCluster({i})">Cluster {i + 1}</button>
        """

    html_content += """
                </div>
            </div>

            <div class="content">
                <div class="no-data" id="noDataMessage">
                    <div class="no-data-icon">👆</div>
                    <div>Please select a cluster above to view customer details</div>
                </div>
    """

    # Tạo nội dung cho từng cluster
    for i in range(total_clusters):
        cluster_data = getCustomersByCluster(df, i)
        count = len(cluster_data)

        # Tính toán statistics cho cluster
        avg_age = cluster_data['Age'].mean()
        avg_income = cluster_data['Annual_Income'].mean()
        avg_spending = cluster_data['Spending_Score'].mean()

        html_content += f"""
                <div class="cluster-section cluster-{i}" id="cluster-{i}">
                    <div class="cluster-header">
                        Cluster {i + 1}
                    </div>
                    <div class="stats">
                        <div class="stats-item">
                            <span class="stats-label">Total Customers</span> 
                            <span class="stats-value">{count}</span>
                        </div>
                        <div class="stats-item">
                            <span class="stats-label">Average Age</span> 
                            <span class="stats-value">{avg_age:.1f}</span>
                        </div>
                        <div class="stats-item">
                            <span class="stats-label">Average Income</span> 
                            <span class="stats-value">${avg_income:,.0f}</span>
                        </div>
                        <div class="stats-item">
                            <span class="stats-label">Avg Spending Score</span> 
                            <span class="stats-value">{avg_spending:.1f}</span>
                        </div>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>Customer ID</th>
                                <th>Age</th>
                                <th>Annual Income</th>
                                <th>Spending Score</th>
                            </tr>
                        </thead>
                        <tbody>
        """

        # Thêm dữ liệu customers vào bảng
        for _, row in cluster_data.iterrows():
            html_content += f"""
                            <tr>
                                <td>{row['CustomerId']}</td>
                                <td>{row['Age']}</td>
                                <td>${row['Annual_Income']:,.0f}</td>
                                <td>{row['Spending_Score']}</td>
                            </tr>
            """

        html_content += """
                        </tbody>
                    </table>
                </div>
        """

    html_content += """
            </div>
        </div>

        <script>
            function showCluster(clusterIndex) {
                // Ẩn tất cả clusters
                const allClusters = document.querySelectorAll('.cluster-section');
                allClusters.forEach(cluster => {
                    cluster.classList.remove('show');
                });

                // Ẩn thông báo no data
                document.getElementById('noDataMessage').style.display = 'none';

                // Hiện cluster được chọn
                const selectedCluster = document.getElementById('cluster-' + clusterIndex);
                selectedCluster.classList.add('show');

                // Update button states
                const allButtons = document.querySelectorAll('.cluster-btn');
                allButtons.forEach((btn, index) => {
                    if (index === clusterIndex) {
                        btn.classList.add('active');
                    } else {
                        btn.classList.remove('active');
                    }
                });

                // Scroll to content
                selectedCluster.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }

            function showAllClusters() {
                // Hiện tất cả clusters
                const allClusters = document.querySelectorAll('.cluster-section');
                allClusters.forEach(cluster => {
                    cluster.classList.add('show');
                });

                // Ẩn thông báo no data
                document.getElementById('noDataMessage').style.display = 'none';

                // Remove active state from all buttons
                const allButtons = document.querySelectorAll('.cluster-btn');
                allButtons.forEach(btn => {
                    btn.classList.remove('active');
                });

                // Scroll to content
                document.querySelector('.content').scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        </script>
    </body>
    </html>
    """

    # Ghi file HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Đã xuất file HTML: {output_file}")
    return output_file


# Sử dụng các hàm
print("\n" + "=" * 80)
print("PHÂN TÍCH CUSTOMERS THEO TỪNG CLUSTER")
print("=" * 80)

# In ra thông tin từng cluster
for i in range(cluster):
    cluster_customers = getCustomersByCluster(df2, i)
    print(f"\n📊 CLUSTER {i + 1}:")
    print(f"   - Số lượng customers: {len(cluster_customers)}")
    print(f"   - Tuổi trung bình: {cluster_customers['Age'].mean():.1f}")
    print(f"   - Thu nhập trung bình: ${cluster_customers['Annual_Income'].mean():,.0f}")
    print(f"   - Spending Score trung bình: {cluster_customers['Spending_Score'].mean():.1f}")
    print(f"\n   Top 5 customers:")
    print(cluster_customers.head()[['CustomerId', 'Age', 'Annual_Income', 'Spending_Score']])

# Xuất ra file HTML
html_file = exportClustersToHTML(df2, cluster)
print(f"\n🌐 Mở file '{html_file}' trong trình duyệt để xem chi tiết!")

# Tự động mở file HTML trong trình duyệt
import webbrowser
import os

webbrowser.open('file://' + os.path.realpath(html_file))