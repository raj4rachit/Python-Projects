import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40],
}))

df = pd.DataFrame(
    np.random.randn(200, 3),
    columns=['a', 'b', 'c'])

c = alt.Chart(df).mark_circle().encode(
    x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

st.write(c)

st.write("""
# My first APP
Welcome to the *my world!*
""")
st.divider()
# title
st.title('A title with _italics_ :blue[colors] and emojis :sunglasses:')
st.divider()
# text
st.text('This is some text.')
st.divider()
# slider
st.slider("This is a slider", 0, 100, (25, 75))
st.divider()
# code
code = '''def hello():
    print("Hello, Streamlit!")'''
st.code(code, language='python')
st.divider()
# Markdown
st.markdown('Streamlit is **_really_ cool**.')
st.markdown("This text is :red[colored red], and this is **:blue[colored]** and bold.")
st.markdown(":green[$\sqrt{x^2+y^2}=1$] is a Pythagorean identity. :pencil:")
st.divider()
# mathematical expressions latex
st.latex(r'''
    a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    \sum_{k=0}^{n-1} ar^k =
    a \left(\frac{1-r^{n}}{1-r}\right)
    ''')
st.divider()