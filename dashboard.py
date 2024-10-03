import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns

# Mengimpor dataset
day_data = pd.read_csv('./data/day.csv')
hour_data = pd.read_csv('./data/hour.csv')

# Menggabungkan dataset menjadi satu
bike_df = hour_data.merge(day_data, on='dteday', how='inner', suffixes=('_hour', '_day'))

# Sidebar - Pilihan untuk memilih komponen analisis
st.sidebar.header('Dashboard Filters')
selected_view = st.sidebar.radio("Select Analysis View:", ["Daily Trends", "Hourly Trends", "Holiday & Weather Impact", "Correlation Analysis"])

# Judul dan Header untuk Dashboard
st.title('Dashboard Analisis Data Penyewaan Sepeda')
st.markdown("### Dashboard Interaktif untuk Menganalisis Tren Penyewaan Sepeda")

# Bagian Analisis Tren Harian
if selected_view == "Daily Trends":
    st.header("Tren Penggunaan Sepeda Harian dari Waktu ke Waktu")
    
    # Menghitung level stok optimal sepeda (rata-rata + standar deviasi)
    daily_mean_cnt = bike_df['cnt_day'].mean()  
    daily_std_cnt = bike_df['cnt_day'].std()  
    daily_optimal_stock = int(daily_mean_cnt + daily_std_cnt)  


    fig = go.Figure()

    # Menambahkan garis jumlah penyewaan sepeda harian
    fig.add_trace(go.Scatter(
        x=bike_df['dteday'],
        y=bike_df['cnt_day'],
        mode='lines',
        name='Daily Rentals',
        line=dict(color='blue')
    ))

    # Menambahkan garis level stok optimal
    fig.add_trace(go.Scatter(
        x=bike_df['dteday'],
        y=[daily_optimal_stock] * len(bike_df),  
        mode='lines',
        name='Optimal Stock Level',
        line=dict(color='red', dash='dash'),  
        hovertemplate='Optimal Stock Level: %{y}<extra></extra>'
    ))

    # Update layout figure untuk tampilan yang lebih baik
    fig.update_layout(
        title='Daily Bike Rentals and Optimal Stock Level',
        xaxis_title='Date',
        yaxis_title='Total Bike Rentals',
        hovermode='x',  
        legend_title="Legend",
        xaxis=dict(tickformat="%Y-%m-%d"),
        template='plotly_white'
    )

    # Menampilkan grafik di Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Menampilkan informasi level stok optimal di bawah grafik
    st.markdown(f"**Jumlah stok sepeda optimal setiap hari adalah: {daily_optimal_stock}**")

    # Insight tambahan
    st.markdown("""
    **Insight:**
    - Grafik di atas menunjukkan tren penyewaan sepeda setiap hari dari waktu ke waktu.
    - Garis merah menunjukkan level stok optimal yang disarankan, dihitung berdasarkan rata-rata harian dan deviasi standar.
    - Ini membantu dalam memastikan cukupnya jumlah sepeda untuk memenuhi permintaan harian.
    """)

# Bagian Analisis Tren Per Jam
elif selected_view == "Hourly Trends":
    st.header("Tren Penggunaan Sepeda Per Jam")
    # Memilih hari tertentu untuk melihat tren hourly
    selected_day = st.sidebar.selectbox("Pilih Hari untuk Analisis Tren Per Jam:", bike_df['dteday'].unique())
    filtered_data = bike_df[bike_df['dteday'] == selected_day]

    # Membuat grafik untuk tren penggunaan sepeda per jam pada hari tertentu
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_data['hr'],
        y=filtered_data['cnt_hour'],
        mode='lines+markers',
        name='Hourly Rentals',
        line=dict(color='green')
    ))

    # Update layout grafik
    fig.update_layout(
        title=f'Hourly Bike Rentals on {selected_day}',
        xaxis_title='Hour of the Day',
        yaxis_title='Total Bike Rentals',
        hovermode='x',
        legend_title="Legend",
        template='plotly_white'
    )

    # Menampilkan grafik di Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Insight
    st.markdown("""
    **Insight:**
    - Grafik ini menunjukkan penggunaan sepeda sepanjang hari untuk hari yang dipilih.
    - Puncak penggunaan biasanya terjadi pada jam sibuk seperti pagi atau sore hari.
    """)

# Bagian Dampak Hari Libur dan Cuaca
elif selected_view == "Holiday & Weather Impact":
    st.header("Dampak Hari Libur dan Cuaca pada Penggunaan Sepeda")
    
    # Membuat boxplot dampak hari libur vs bukan hari libur
    st.subheader("Perbandingan Penyewaan Sepeda: Hari Libur vs Bukan Hari Libur")
    fig, ax = plt.subplots()
    sns.boxplot(data=bike_df, x='holiday_day', y='cnt_day', palette=['lightblue', 'lightgreen'], ax=ax)
    ax.set_title('Perbandingan Penyewaan Sepeda: Hari Libur vs Bukan Hari Libur')
    ax.set_xlabel('Holiday (1=Yes, 0=No)')
    ax.set_ylabel('Total Bike Rentals')
    st.pyplot(fig)

    # Insight
    st.markdown("""
    **Insight:**
    - Grafik boxplot menunjukkan perbedaan rata-rata penyewaan sepeda pada hari libur dan bukan hari libur.
    - Jumlah penyewaan cenderung lebih rendah pada hari libur, karena kebanyakan orang tidak bepergian untuk bekerja.
    """)

    # Membuat boxplot dampak kondisi cuaca pada penyewaan sepeda
    st.subheader("Dampak Kondisi Cuaca pada Penyewaan Sepeda")
    fig, ax = plt.subplots()
    sns.boxplot(data=bike_df, x='weathersit_day', y='cnt_day', palette='Set2', ax=ax)
    ax.set_title('Dampak Kondisi Cuaca pada Penyewaan Sepeda')
    ax.set_xlabel('Weather Situation (1: Clear, 2: Mist, 3: Light Snow/Rain, 4: Heavy Rain)')
    ax.set_ylabel('Total Bike Rentals')
    st.pyplot(fig)

    # Insight
    st.markdown("""
    **Insight:**
    - Penyewaan sepeda cenderung lebih tinggi saat cuaca cerah dan menurun saat cuaca buruk hujan atau salju ringan
    """)

# Bagian Analisis Korelasi
elif selected_view == "Correlation Analysis":
    st.header("Analisis Korelasi Antar Variabel")
    # Matriks korelasi antara fitur
    correlation_daily = bike_df[['temp_day', 'atemp_day', 'hum_day', 'windspeed_day', 'casual_day', 'registered_day', 'cnt_day']].corr()

    # Membuat heatmap untuk matriks korelasi
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(correlation_daily, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Matriks Korelasi (Data Harian)')
    st.pyplot(fig)

    # Insight tambahan
    st.markdown("""
    **Insight:**
    - Matriks korelasi memberikan wawasan tentang hubungan antara variabel seperti suhu, kelembaban, dan jumlah penyewaan sepeda.
    - terdapat korelasi positif antara suhu dan jumlah penyewaan sepeda, yang menunjukkan bahwa lebih banyak orang menggunakan sepeda saat suhu lebih tinggi.
    """)