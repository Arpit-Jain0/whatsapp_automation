import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
import random

def send_whatsapp_messages(numbers_file, image_path, message):
    placeholder = st.empty()
    with placeholder:
        st.info("Please scan the QR code in WhatsApp Web.") 
     
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://web.whatsapp.com')
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="textbox"]'))
    )
    placeholder.empty()

    if numbers_file:
        numbers_text = numbers_file.read().decode("utf-8")
        numbers_list = [num.strip() for num in numbers_text.split("\n") if num.strip()]
        updated_list=[]
        for i in numbers_list:
            if len(i)>10:
                if str(i).startswith('+91'):
                    i=str(i).replace("+91","")
                    updated_list.append(int(i))
                if str(i).startswith('0'):
                    updated_list.append(int(i))
                if str(i).startswith('91'):
                    updated_list.append(int(str(i)[2:12]))
            else:
                i=int(i)
                updated_list.append(i)

    pyperclip.copy(message)
    sent_list=[]
    not_sent_list=[]
    for num in updated_list:
        try:
            if image_path:
                link = f'https://web.whatsapp.com/send/?phone=91{num}'
                driver.get(link)
                WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="textbox"]')))
                attach_btn = WebDriverWait(driver, 2).until(EC.element_to_be_clickable
                    ((By.CSS_SELECTOR, 'span[data-icon="plus"]')))
                attach_btn.click()
                image_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
                )
                image_input.send_keys(image_path)
                time.sleep(random.uniform(1, 4))
                caption_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
                )
                caption_box.click()
                caption_box.send_keys(Keys.COMMAND, "v")
                time.sleep(1)
                send_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="send"]'))
                )
                send_btn.click()
                sent_list.append(num)
            else:
                link = f'https://web.whatsapp.com/send/?phone=91{num}'
                driver.get(link)
                caption_box=WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="textbox"]')))
                caption_box.click()
                caption_box.send_keys(Keys.COMMAND, "v")
                send_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'span[data-icon="send"]')))
                send_button.click()
                sent_list.append(num)
            
            time.sleep(random.uniform(2, 5))
    
        except Exception as e:
            st.error(f"Time Limit exceeded! Please check your internet connection")
            not_sent_list.append(num)

    st.success("Messages sent successfully!")
    driver.quit()
    