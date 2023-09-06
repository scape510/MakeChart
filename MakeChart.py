import streamlit as st
import pytesseract
from PIL import Image
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# pytesseractの設定（ローカル環境での実行の場合）
# pytesseract.pytesseract.tesseract_cmd = r'/path/to/tesseract'

def extract_text_from_image(image):
    return pytesseract.image_to_string(image, lang='jpn')

def extract_date_and_code(text):
    import re
    date_pattern = r"(\d{4}年\d{1,2}月\d{1,2}日)"
    code_pattern = r"(\d{4})"
    
    date_match = re.search(date_pattern, text)
    code_match = re.search(code_pattern, text)
    
    if date_match and code_match:
        date_str = date_match.group(1)
        code = code_match.group(1) + ".T"
        return date_str, code
    return None, None

def fetch_stock_data(code, target_date):
    start_date = (target_date - timedelta(days=90)).strftime('%Y-%m-%d')
    end_date = (target_date + timedelta(days=90)).strftime('%Y-%m-%d')
    stock_data = yf.download(code, start=start_date, end=end_date)
    return stock_data

def plot_chart(stock_data, code, target_date):
    stock_data['Close'].plot(figsize=(12,6))
    plt.axvline(x=target_date, color='red', linestyle='--')
    plt.title(f'Stock Price of {code}')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.grid(True)
    st.pyplot()

# StreamlitのUI部分
st.title('Stock Price Visualization from Tweet Screenshot')

uploaded_file = st.file_uploader("Upload a screenshot", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Screenshot.', use_column_width=True)
    
    text = extract_text_from_image(image)
    st.write("Extracted Text:")
    st.write(text)
    
    date_str, code = extract_date_and_code(text)
    if date_str and code:
        target_date = datetime.strptime(date_str, '%Y年%m月%d日')
        stock_data = fetch_stock_data(code, target_date)
        plot_chart(stock_data, code, target_date)
    else:
        st.write("Failed to extract date or stock code from the screenshot.")
