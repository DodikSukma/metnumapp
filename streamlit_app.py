import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

def f(x):
    return x**3 - 2*x + 1  # Sample equation 1: x^3 - 2x + 1 = 0

def g(x, y, z):
    return [4*x + y + z - 100, 
            x + 5*y + z - 90, 
            x + y + 6*z - 120]  # Sample system of linear equations

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

def main():
    st.title("Root Finding App ANJAY MANTAP CUI")

    st.subheader("Sample Equations:")
    st.write("1. Single equation: x^3 - 2x + 1 = 0")
    st.write("2. System of linear equations: ")
    st.write("4x + y + z = 100")
    st.write("x + y + 6z = 120")
    st.write("x + 5y + z = 90")

    method_choice = st.radio("Choose method", ["False Position", "Jacobi Method"])

    if method_choice == "False Position":
        st.subheader("False Position Solver")

        a = st.number_input("Enter initial value 'a'", value=1.0)
        b = st.number_input("Enter initial value 'b'", value=3.0)
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

        a = st.columns(3)
        with a[0]:
            a11 = st.number_input("a11", value=4.0)
            a12 = st.number_input("a12", value=1.0)
            a13 = st.number_input("a13", value=1.0)
        with a[1]:
            a21 = st.number_input("a21", value=1.0)
            a22 = st.number_input("a22", value=5.0)
            a23 = st.number_input("a23", value=1.0)
        with a[2]:
            a31 = st.number_input("a31", value=1.0)
            a32 = st.number_input("a32", value=1.0)
            a33 = st.number_input("a33", value=6.0)

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

if __name__ == "__main__":
    main()
