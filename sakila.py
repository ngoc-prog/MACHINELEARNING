from flask import Flask, render_template_string
import mysql.connector
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings('ignore')

app = Flask(__name__)


# Kết nối database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="ngot",
        password="Obama@123",
        database="sakila"
    )


# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Phân tích Database Sakila</title>
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
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }

        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }

        .nav-tabs {
            display: flex;
            background: #f8f9fa;
            padding: 0;
            border-bottom: 3px solid #667eea;
            overflow-x: auto;
        }

        .nav-tab {
            flex: 1;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            border: none;
            background: #f8f9fa;
            font-size: 16px;
            font-weight: 600;
            color: #666;
            transition: all 0.3s;
            min-width: 200px;
        }

        .nav-tab:hover {
            background: #e9ecef;
            color: #667eea;
        }

        .nav-tab.active {
            background: white;
            color: #667eea;
            border-bottom: 3px solid #667eea;
        }

        .content {
            padding: 40px;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
            animation: fadeIn 0.5s;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }

        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }

        .stat-card h3 {
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
        }

        .stat-card .number {
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .stat-card .label {
            font-size: 0.85em;
            opacity: 0.8;
        }

        .section {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
        }

        .section h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 2em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }

        .section h3 {
            color: #764ba2;
            margin: 25px 0 15px 0;
            font-size: 1.5em;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }

        td {
            padding: 12px 15px;
            border-bottom: 1px solid #e9ecef;
        }

        tr:hover {
            background: #f8f9fa;
        }

        .chart-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .info-box {
            background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #667eea;
        }

        .info-box h4 {
            color: #333;
            margin-bottom: 10px;
        }

        .info-box p {
            color: #555;
            line-height: 1.6;
        }

        .cluster-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            color: white;
            font-weight: 600;
            font-size: 0.9em;
        }

        .cluster-0 { background: #10b981; }
        .cluster-1 { background: #3b82f6; }
        .cluster-2 { background: #f59e0b; }
        .cluster-3 { background: #ef4444; }

        .footer {
            background: #2d3748;
            color: white;
            text-align: center;
            padding: 20px;
        }
    </style>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 Phân tích Database Sakila</h1>
            <p>K-Means Clustering & Customer Analysis</p>
        </div>

        <div class="nav-tabs">
            <button class="nav-tab active" onclick="showTab(0)">📊 Tổng quan</button>
            <button class="nav-tab" onclick="showTab(1)">🎬 Câu 1: Theo Phim</button>
            <button class="nav-tab" onclick="showTab(2)">🏆 Câu 2: Theo Category</button>
            <button class="nav-tab" onclick="showTab(3)">👥 K-Means Clustering</button>
        </div>

        <div class="content">
            {{ content | safe }}
        </div>

        <div class="footer">
            <p>© 2025 Sakila Database Analysis | K-Means Clustering Project</p>
        </div>
    </div>

    <script>
        function showTab(index) {
            const tabs = document.querySelectorAll('.nav-tab');
            const contents = document.querySelectorAll('.tab-content');

            tabs.forEach((tab, i) => {
                if (i === index) {
                    tab.classList.add('active');
                } else {
                    tab.classList.remove('active');
                }
            });

            contents.forEach((content, i) => {
                if (i === index) {
                    content.classList.add('active');
                } else {
                    content.classList.remove('active');
                }
            });
        }
    </script>
</body>
</html>
'''


@app.route('/')
def index():
    try:
        conn = get_db_connection()

        # Lấy thống kê tổng quan
        stats = get_statistics(conn)

        # Câu 1: Phim
        film_data, film_chart = analyze_films(conn)

        # Câu 2: Category
        category_data, category_charts = analyze_categories(conn)

        # K-Means Clustering
        cluster_data, cluster_charts = perform_clustering(conn)

        conn.close()

        # Tạo nội dung HTML
        content = f'''
        <!-- Tab 0: Tổng quan -->
        <div class="tab-content active">
            <h2 style="color: #667eea; margin-bottom: 30px;">📊 Tổng quan phân tích</h2>

            <div class="stats-grid">
                <div class="stat-card">
                    <h3>Tổng khách hàng</h3>
                    <div class="number">{stats['customers']}</div>
                    <div class="label">Database Sakila</div>
                </div>
                <div class="stat-card">
                    <h3>Tổng phim</h3>
                    <div class="number">{stats['films']}</div>
                    <div class="label">Phim có sẵn</div>
                </div>
                <div class="stat-card">
                    <h3>Thể loại</h3>
                    <div class="number">{stats['categories']}</div>
                    <div class="label">Categories</div>
                </div>
                <div class="stat-card">
                    <h3>Tổng lượt thuê</h3>
                    <div class="number">{stats['rentals']:,}</div>
                    <div class="label">Rental records</div>
                </div>
            </div>

            <div class="info-box">
                <h4>🎯 Mục tiêu phân tích:</h4>
                <p><strong>1.</strong> Phân loại khách hàng theo Tên phim đã thuê</p>
                <p><strong>2.</strong> Phân loại khách hàng theo Category (xác minh 1 Category có nhiều Film)</p>
                <p><strong>3.</strong> Áp dụng K-Means Clustering để gom cụm khách hàng theo mức độ quan tâm Film và Inventory</p>
            </div>
        </div>

        <!-- Tab 1: Theo Phim -->
        <div class="tab-content">
            <div class="section">
                <h2>🎬 Câu 1: Phân loại khách hàng theo Tên phim</h2>

                <div class="info-box">
                    <h4>📋 Mô tả:</h4>
                    <p>Truy vấn từ các bảng: <strong>Customer, Rental, Inventory, Film</strong></p>
                    <p>Mục đích: Xác định khách hàng nào đã thuê phim nào và bao nhiêu lần</p>
                </div>

                <h3>Top 20 khách hàng và phim đã thuê:</h3>
                {film_data}

                <div class="chart-container">
                    {film_chart}
                </div>
            </div>
        </div>

        <!-- Tab 2: Theo Category -->
        <div class="tab-content">
            <div class="section">
                <h2>🏆 Câu 2: Phân loại khách hàng theo Category</h2>

                <div class="info-box">
                    <h4>📋 Mô tả:</h4>
                    <p>Truy vấn từ các bảng: <strong>Customer, Rental, Inventory, Film, Film_Category, Category</strong></p>
                    <p style="color: #10b981; font-weight: bold;">✓ Xác nhận: Thiết kế này loại bỏ dữ liệu trùng lặp vì 1 Category chứa nhiều Film khác nhau</p>
                </div>

                <h3>Số lượng phim trong mỗi thể loại:</h3>
                {category_data}

                <div class="chart-container">
                    <h3 style="margin-bottom: 20px;">Biểu đồ phân tích Category:</h3>
                    {category_charts}
                </div>
            </div>
        </div>

        <!-- Tab 3: K-Means -->
        <div class="tab-content">
            <div class="section">
                <h2>👥 K-Means Clustering: Gom cụm khách hàng</h2>

                <div class="info-box">
                    <h4>🎯 Mục đích:</h4>
                    <p>Gom cụm khách hàng dựa trên mức độ quan tâm đến Film và Inventory</p>
                    <p><strong>Features sử dụng:</strong> Tổng lượt thuê, Số phim unique, Số inventory items, Avg rental rate, Avg film length</p>
                </div>

                {cluster_charts}

                <h3 style="margin-top: 30px;">Chi tiết phân cụm khách hàng (Top 30):</h3>
                {cluster_data}
            </div>
        </div>
        '''

        return render_template_string(HTML_TEMPLATE, content=content)

    except Exception as e:
        return f"<h1>Lỗi: {str(e)}</h1><p>Vui lòng kiểm tra kết nối database!</p>"


def get_statistics(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM customer")
    customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM film")
    films = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM category")
    categories = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM rental")
    rentals = cursor.fetchone()[0]

    cursor.close()

    return {
        'customers': customers,
        'films': films,
        'categories': categories,
        'rentals': rentals
    }


def analyze_films(conn):
    query = """
    SELECT 
        c.customer_id,
        CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
        f.title AS film_title,
        COUNT(*) AS rental_count
    FROM customer c
    JOIN rental r ON c.customer_id = r.customer_id
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f ON i.film_id = f.film_id
    GROUP BY c.customer_id, f.film_id
    ORDER BY rental_count DESC, c.customer_id
    LIMIT 20
    """

    df = pd.read_sql(query, conn)

    # Tạo bảng HTML
    table_html = df.to_html(index=False, classes='data-table', border=0)

    # Tạo biểu đồ
    fig = px.bar(df, x='film_title', y='rental_count',
                 title='Top 20 phim được thuê nhiều nhất',
                 labels={'film_title': 'Tên phim', 'rental_count': 'Số lượt thuê'},
                 color='rental_count',
                 color_continuous_scale='Viridis')
    fig.update_layout(xaxis_tickangle=-45, height=500)
    chart_html = fig.to_html(full_html=False, include_plotlyjs=False)

    return table_html, chart_html


def analyze_categories(conn):
    query = """
    SELECT 
        cat.name AS category_name,
        COUNT(DISTINCT f.film_id) AS film_count,
        COUNT(r.rental_id) AS total_rentals
    FROM category cat
    JOIN film_category fc ON cat.category_id = fc.category_id
    JOIN film f ON fc.film_id = f.film_id
    LEFT JOIN inventory i ON f.film_id = i.film_id
    LEFT JOIN rental r ON i.inventory_id = r.inventory_id
    GROUP BY cat.category_id
    ORDER BY film_count DESC
    """

    df = pd.read_sql(query, conn)

    # Tạo bảng HTML
    table_html = df.to_html(index=False, classes='data-table', border=0)

    # Tạo 2 biểu đồ
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Số lượng phim theo thể loại', 'Tổng lượt thuê theo thể loại')
    )

    fig.add_trace(
        go.Bar(x=df['category_name'], y=df['film_count'], name='Số phim',
               marker_color='rgb(102, 126, 234)'),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(x=df['category_name'], y=df['total_rentals'], name='Lượt thuê',
               marker_color='rgb(118, 75, 162)'),
        row=1, col=2
    )

    fig.update_layout(height=500, showlegend=False)
    fig.update_xaxes(tickangle=-45)

    chart_html = fig.to_html(full_html=False, include_plotlyjs=False)

    return table_html, chart_html


def perform_clustering(conn):
    query = """
    SELECT 
        c.customer_id,
        CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
        COUNT(DISTINCT r.rental_id) AS total_rentals,
        COUNT(DISTINCT f.film_id) AS unique_films_rented,
        COUNT(DISTINCT i.inventory_id) AS unique_inventory_items,
        COALESCE(AVG(f.rental_rate), 0) AS avg_rental_rate,
        COALESCE(AVG(f.length), 0) AS avg_film_length
    FROM customer c
    LEFT JOIN rental r ON c.customer_id = r.customer_id
    LEFT JOIN inventory i ON r.inventory_id = i.inventory_id
    LEFT JOIN film f ON i.film_id = f.film_id
    GROUP BY c.customer_id
    """

    df = pd.read_sql(query, conn)

    # Chuẩn bị dữ liệu cho K-Means
    features = ['total_rentals', 'unique_films_rented', 'unique_inventory_items',
                'avg_rental_rate', 'avg_film_length']
    X = df[features].fillna(0)

    # Chuẩn hóa
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Elbow Method
    inertias = []
    K_range = range(2, 11)
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)

    # K-Means với k=4
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(X_scaled)

    # Gắn nhãn cụm
    cluster_labels = {0: 'VIP', 1: 'Trung bình', 2: 'Ít thuê', 3: 'Mới'}
    df['cluster_label'] = df['cluster'].map(cluster_labels)

    # Tạo bảng HTML với badge màu
    df_display = df[['customer_id', 'customer_name', 'total_rentals', 'unique_films_rented', 'cluster_label']].head(30)

    table_rows = ""
    for _, row in df_display.iterrows():
        table_rows += f"""
        <tr>
            <td>{row['customer_id']}</td>
            <td>{row['customer_name']}</td>
            <td>{row['total_rentals']}</td>
            <td>{row['unique_films_rented']}</td>
            <td><span class="cluster-badge cluster-{df[df['customer_id'] == row['customer_id']]['cluster'].values[0]}">{row['cluster_label']}</span></td>
        </tr>
        """

    table_html = f"""
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Tên khách hàng</th>
                <th>Tổng lượt thuê</th>
                <th>Phim unique</th>
                <th>Phân loại</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
    """

    # Biểu đồ Elbow
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=list(K_range), y=inertias, mode='lines+markers',
                              marker=dict(size=10, color='rgb(102, 126, 234)'),
                              line=dict(width=3, color='rgb(102, 126, 234)')))
    fig1.update_layout(title='Elbow Method - Xác định số cụm tối ưu',
                       xaxis_title='Số cụm (K)',
                       yaxis_title='Inertia',
                       height=400)

    # Biểu đồ phân bố cụm
    cluster_counts = df['cluster_label'].value_counts()
    fig2 = px.pie(values=cluster_counts.values, names=cluster_counts.index,
                  title='Phân bố khách hàng theo cụm',
                  color_discrete_sequence=['#10b981', '#3b82f6', '#f59e0b', '#ef4444'])
    fig2.update_layout(height=400)

    # Biểu đồ scatter
    fig3 = px.scatter(df, x='total_rentals', y='unique_films_rented',
                      color='cluster_label',
                      title='Phân cụm khách hàng theo mức độ quan tâm Film',
                      labels={'total_rentals': 'Tổng lượt thuê', 'unique_films_rented': 'Số phim unique'},
                      color_discrete_map={'VIP': '#10b981', 'Trung bình': '#3b82f6',
                                          'Ít thuê': '#f59e0b', 'Mới': '#ef4444'},
                      hover_data=['customer_name'])
    fig3.update_layout(height=500)

    # Kết hợp các biểu đồ
    charts_html = f"""
    <div class="chart-container">
        {fig1.to_html(full_html=False, include_plotlyjs=False)}
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        <div class="chart-container">
            {fig2.to_html(full_html=False, include_plotlyjs=False)}
        </div>
        <div class="chart-container">
            <h3 style="margin-bottom: 15px;">Đặc điểm từng cụm:</h3>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px;">
                <p><span class="cluster-badge cluster-0">VIP</span> - Khách hàng thuê nhiều, đa dạng phim ({len(df[df['cluster'] == 0])} người)</p>
                <p style="margin-top: 10px;"><span class="cluster-badge cluster-1">Trung bình</span> - Khách hàng ổn định ({len(df[df['cluster'] == 1])} người)</p>
                <p style="margin-top: 10px;"><span class="cluster-badge cluster-2">Ít thuê</span> - Khách hàng ít hoạt động ({len(df[df['cluster'] == 2])} người)</p>
                <p style="margin-top: 10px;"><span class="cluster-badge cluster-3">Mới</span> - Khách hàng mới hoặc không hoạt động ({len(df[df['cluster'] == 3])} người)</p>
            </div>
        </div>
    </div>
    <div class="chart-container">
        {fig3.to_html(full_html=False, include_plotlyjs=False)}
    </div>
    """

    return table_html, charts_html


if __name__ == '__main__':
    print("=" * 80)
    print("🚀 Starting Sakila Analysis Web Server...")
    print("=" * 80)
    print("📊 Mở trình duyệt và truy cập: http://localhost:5000")
    print("⏹️  Nhấn Ctrl+C để dừng server")
    print("=" * 80)
    app.run(debug=True, host='0.0.0.0', port=5000)