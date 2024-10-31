import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Metode Numerik",
    page_icon="📈",
    layout="wide",
)

st.markdown("""
    <h1 style="text-align: center;">
        KALKULATOR METODE NUMERIK : POSISI PALSU DAN JACOBI 🚀
    </h1>
""", unsafe_allow_html=True)


# ====================================== MENU APLIKASI ====================================== #
pilihan = option_menu(
    menu_title="MENU",  
    options=["HOME", "KALKULATOR", "ARTICLE"],  
    icons=["house", "bi bi-bar-chart-fill", "envelope"],  
    menu_icon="cast",  
    default_index=0,  
    orientation="horizontal",
)

def f(x):
    return x**3 - x - 2  # Sample equation with a root near x = 1.521

def g(x, y, z):
    return [4*x + y + z - 100, x + 5*y + z - 90, x + y + 6*z - 120]  # Sample system of linear equations

def false_position(a, b, tol=1e-6, max_iter=100):
    data = []
    for i in range(max_iter):
        fa = f(a)
        fb = f(b)
        c = b - (fb * (b - a)) / (fb - fa)
        fc = f(c)
        data.append([i+1, a, b, c, fa, fb, fc])

        if abs(fc) < tol:
            break
        if fa * fc < 0:
            b = c
        else:
            a = c

    df = pd.DataFrame(data, columns=['Iterasi', 'Nilai a', 'Nilai b', 'Nilai c', 'f(a)', 'f(b)', 'f(c)'])
    return c, df

def jacobi_method(a, b, tol, max_iter):
    n = len(b)
    x = [0.0] * n
    iterations = []

    for k in range(1, max_iter + 1):
        x_new = x.copy()
        max_change = 0.0

        for i in range(n):
            s = b[i]
            for j in range(n):
                if i != j:
                    s -= a[i][j] * x[j]
            s /= a[i][i]
            x_new[i] = s
            max_change = max(max_change, abs(x_new[i] - x[i]))

        iterations.append([k, x_new[0], x_new[1], x_new[2], max_change])
        x = x_new

        if max_change < tol:
            break

    return x, iterations

# Home section
if pilihan == "HOME":
    st.header("KALKULATOR METODE NUMERIK")
    st.success("""
    **KALKULATOR METODE NUMERIK** adalah aplikasi perhitungan numerik menggunakan metode 
    **False Position** dan **Jacobi** untuk mencari solusi dari persamaan tunggal atau 
    sistem persamaan linier.

    - **Metode False Position**: Digunakan untuk mencari akar dari suatu persamaan non-linier.
    - **Metode Jacobi**: Digunakan untuk menyelesaikan sistem persamaan linier melalui metode iterasi.
    """)

# ARTICLE section
elif pilihan == "ARTICLE":
    st.markdown("""
        <h2 style="text-align: center;">Tentang Metode Posisi Palsu dan Metode Jacobi</h2>
        
        <h3>Metode Posisi Palsu</h3>
        <p>
            Metode Posisi Palsu atau False Position Method adalah metode numerik yang digunakan untuk mencari akar dari
            sebuah fungsi non-linier <em>f(x) = 0</em>. Metode ini bekerja dengan cara mengambil dua titik awal, 
            <strong>a</strong> dan <strong>b</strong>, yang terletak di sekitar akar (di mana <em>f(a)</em> dan <em>f(b)</em> 
            memiliki tanda yang berlawanan). Posisi akar kemudian diestimasi berdasarkan pendekatan linier antara kedua 
            titik tersebut. Proses ini diulangi hingga hasil mendekati nilai akar yang diinginkan sesuai toleransi yang 
            telah ditetapkan.
        </p>
        
        <ul>
            <li><strong>Kelebihan</strong>: Konvergen pada interval yang diketahui mengandung akar.</li>
            <li><strong>Kekurangan</strong>: Terkadang membutuhkan banyak iterasi untuk mencapai solusi yang akurat.</li>
        </ul>
        
        <h3>Langkah-Langkah Metode Posisi Palsu:</h3>
        <ol>
            <li>Menentukan dua titik awal <strong>a</strong> dan <strong>b</strong> di sekitar akar, dengan syarat <em>f(a)</em> dan <em>f(b)</em> memiliki tanda yang berlawanan.</li>
            <li>Menghitung nilai <em>c</em> sebagai pendekatan akar: <em>c = b - f(b) * (b - a) / (f(b) - f(a))</em>.</li>
            <li>Memperbarui nilai <strong>a</strong> atau <strong>b</strong> berdasarkan nilai <em>f(c)</em>.</li>
            <li>Mengulangi langkah 2 dan 3 hingga hasilnya memenuhi toleransi yang diinginkan.</li>
        </ol>
        
        <hr>
        
        <h3>Metode Jacobi</h3>
        <p>
            Metode Jacobi adalah metode iteratif yang digunakan untuk menyelesaikan sistem persamaan linier dalam bentuk 
            matriks <em>Ax = b</em>. Dalam metode ini, setiap variabel diisolasi, dan setiap iterasi menghasilkan 
            perkiraan yang semakin mendekati solusi yang sebenarnya. Metode Jacobi bekerja dengan memisahkan persamaan untuk 
            setiap variabel dan menggunakan perkiraan nilai dari iterasi sebelumnya untuk menghitung nilai variabel yang 
            baru.
        </p>
        
        <ul>
            <li><strong>Kelebihan</strong>: Cocok untuk sistem yang memiliki matriks diagonal dominan.</li>
            <li><strong>Kekurangan</strong>: Tidak selalu konvergen untuk semua jenis matriks.</li>
        </ul>
        
        <h3>Langkah-Langkah Metode Jacobi:</h3>
        <ol>
            <li>Menulis sistem persamaan linier dalam bentuk <em>Ax = b</em>.</li>
            <li>Memisahkan setiap persamaan untuk mencari variabel-variabel secara individu.</li>
            <li>Menggunakan nilai variabel dari iterasi sebelumnya untuk menghitung nilai variabel yang baru.</li>
            <li>Melakukan iterasi hingga perubahan antara nilai baru dan lama cukup kecil (memenuhi toleransi yang diinginkan).</li>
        </ol>
        
        <hr>
        
        <p style="text-align: center;">
            Kedua metode ini penting dalam pemecahan masalah numerik, khususnya dalam kasus di mana metode analitik
            sulit diterapkan. Mereka memberikan solusi mendekati yang dapat dihitung dengan efisien melalui pemrograman
            komputer.
        </p>
    """, unsafe_allow_html=True)

elif pilihan == "KALKULATOR":
    method_choice = st.selectbox("Pilih Metode", ["False Position", "Jacobi Method"])

    if method_choice == "False Position":
        st.subheader("False Position Method Solver")
        st.markdown("""
            <h3>Metode Posisi Palsu</h3>
            <h3>Sample Soal : </h3>
            <h4><i>x<sup>3</sup> - x - 2 = 0</i></h4>
        """, unsafe_allow_html=True)
        
        # Alert message with usage instructions
        st.info("""
            **Cara Penggunaan:**
            - Masukkan nilai awal a dan b yang mendekati akar dari persamaan.
            - Nilai a dan b harus menghasilkan tanda fungsi yang berlawanan.
            - Tentukan toleransi sebagai batas kesalahan yang diinginkan. Semakin kecil nilai toleransi, semakin presisi hasilnya.
        """, icon="ℹ️")

        a = st.number_input("Enter initial value 'a'", value=1.0)
        b = st.number_input("Enter initial value 'b'", value=2.0)
        tol = st.number_input("Enter tolerance", min_value=0.0, step=0.01, value=1e-6)

        if st.button("Solve"):
            root, result_table = false_position(a, b, tol)
            st.subheader("Iteration Results")
            st.write(result_table)
            st.subheader("Final Solution")
            st.write(f"Root: {root:.6f}")

            plot_fig = go.Figure()
            plot_fig.add_trace(go.Scatter(x=result_table['Iterasi'], y=result_table['Nilai c'], mode='lines+markers',
                                        name="Nilai c (pendekatan akar)", line=dict(color='blue')))
            plot_fig.add_hline(y=root, line=dict(color='red', dash='dash'),
                            annotation_text=f"Root: {root:.4f}", annotation_position="bottom right")

            plot_fig.update_layout(
                title="False Position Method Convergence",
                xaxis_title="Iteration",
                yaxis_title="Value of c",
                template="plotly_white"
            )

            st.subheader("Visualization")
            st.plotly_chart(plot_fig)


    elif method_choice == "Jacobi Method":
        st.subheader("Jacobi Method Solver")
        st.markdown("""
            <h3>Metode Jacobi</h3>
            <h3>Sample Soal:</h3>
            <p>Menyelesaikan sistem persamaan linear berikut:</p>
            <ul>
                <li>4x + y + z = 100</li>
                <li>x + 5y + z = 90</li>
                <li>x + y + 6z = 120</li>
            </ul>
        """, unsafe_allow_html=True)
        
        # Alert message with usage instructions
        st.info("""
            **Cara Penggunaan:**
            - Masukkan nilai koefisien untuk setiap elemen matriks A (a11 hingga a33).
            - Masukkan nilai konstanta pada sisi kanan persamaan (b1, b2, dan b3).
            - Tentukan toleransi sebagai batas konvergensi yang diinginkan. Semakin kecil toleransi, semakin presisi solusi.
            - Tentukan batas maksimal iterasi untuk mencegah perulangan tak terbatas jika solusi tidak ditemukan.
        """, icon="ℹ️")

        
        # Input fields organized in 4 columns
        a_col1 = st.columns(4)
        with a_col1[0]:
            st.markdown("**Matrix A**")
        with a_col1[3]:
            st.markdown("**Vector b**")

        a_col = st.columns(4)
        with a_col[0]:
            st.markdown("****")
            a11 = st.number_input("a11", value=4.0)
            a21 = st.number_input("a21", value=1.0)
            a31 = st.number_input("a31", value=1.0)
        with a_col[1]:
            st.markdown("****")
            a12 = st.number_input("a12", value=1.0)
            a22 = st.number_input("a22", value=5.0)
            a32 = st.number_input("a32", value=1.0)
        with a_col[2]:
            st.markdown("****")
            a13 = st.number_input("a13", value=1.0)
            a23 = st.number_input("a23", value=1.0)
            a33 = st.number_input("a33", value=6.0)
        with a_col[3]:
            st.markdown("****")
            b1 = st.number_input("b1", value=100.0)
            b2 = st.number_input("b2", value=90.0)
            b3 = st.number_input("b3", value=120.0)

        tol = st.number_input("Tolerance", min_value=0.0, step=0.01, value=0.01)
        max_iter = st.number_input("Maximum Iterations", min_value=1, step=1, value=20)

        if st.button("Solve"):
            a_np = [[a11, a12, a13], [a21, a22, a23], [a31, a32, a33]]
            b_np = [b1, b2, b3]
            x, iterations = jacobi_method(a_np, b_np, tol, max_iter)

            df_iterations = pd.DataFrame(iterations, columns=["Iteration", "x", "y", "z", "Max Change"])

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_iterations['Iteration'], y=df_iterations['x'], mode='lines+markers', name='x', line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=df_iterations['Iteration'], y=df_iterations['y'], mode='lines+markers', name='y', line=dict(color='green')))
            fig.add_trace(go.Scatter(x=df_iterations['Iteration'], y=df_iterations['z'], mode='lines+markers', name='z', line=dict(color='red')))
            fig.add_trace(go.Scatter(x=df_iterations['Iteration'], y=df_iterations['Max Change'], mode='lines+markers', name='Max Change', line=dict(color='orange')))

            fig.update_layout(
                title='Jacobi Method Iteration Values',
                xaxis_title='Iteration',
                yaxis_title='Value',
                template='plotly_white'
            )

            st.subheader("Iteration Results")
            st.write(df_iterations)

            st.subheader("Final Solution")
            st.write(f"x = {x[0]:.4f}")
            st.write(f"y = {x[1]:.4f}")
            st.write(f"z = {x[2]:.4f}")

            st.subheader("Visualization")
            st.plotly_chart(fig)
