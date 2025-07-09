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
import io
import pandas as pd

import logging

def send_whatsapp_messages(numbers_file, image_path, message):
    logging.basicConfig(filename='whatsapp_errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')
    placeholder = st.empty()
    with placeholder:
        st.info("Please scan the QR code in WhatsApp Web.")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://web.whatsapp.com')
    WebDriverWait(driver, 60).until(
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
    MAX_RETRIES = 3
    for num in updated_list:

        success = False
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                link = f'https://web.whatsapp.com/send/?phone=91{num}'
                driver.get(link)

                try:

                    #this checks if any dialog box appears with this text if the number is not available
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Phone number shared via url is invalid")]'))
                    )
                    not_sent_list.append(num)
                    success = True
                    break
                except:

                    if image_path:
                        #this XPATH is of + sign to select the menu of sending multiple docs or images.
                        plus_icon_xpath = '//span[@aria-hidden="true" and @data-icon="plus-rounded"]/parent::button'
                        plus_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, plus_icon_xpath)))
                        plus_button.click()
                        time.sleep(1)



                        #this XPATh is of the accept of the images /videos             
                        image_input = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
                        )
                        image_input.send_keys(image_path)
                        time.sleep(random.uniform(1, 3))

                        #this xapth is of the caption pasted when there is an image selected.
                        caption_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[3]/div/div[2]/div[2]/span/div/div/div/div[2]/div/div[1]/div[3]/div/div/div[1]/div[1]/div[1]/p'))
    )
                        caption_box.click()
                        caption_box.send_keys(Keys.COMMAND, "v")
                        time.sleep(1)

                        #this is the xpath of the send button when an image or vide ois shared.
                        send_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[3]/div/div[2]/div[2]/span/div/div/div/div[2]/div/div[2]/div[2]/div/div/span'))
    )
                        send_btn.click()
                        sent_list.append(num)
                    else:

                        caption_box = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div/div[3]/div[1]/p'))
                        )
                        caption_box.click()
                        caption_box.send_keys(Keys.COMMAND, "v")
                        time.sleep(1)
                        send_btn = WebDriverWait(driver, 15).until(
                            EC.element_to_be_clickable((By.XPATH, '//footer//button[@aria-label="Send"]')))
                        send_btn.click()
                        sent_list.append(num)
                    success = True
                    time.sleep(random.uniform(1, 7))
                    break

            except Exception as e:
                logging.error(f"Attempt {attempt} failed for number {num}: {str(e)}")
                time.sleep(3)
        if not success:
            not_sent_list.append(num)
            st.warning(f"Failed to send to {num} after {MAX_RETRIES} attempts.")

    driver.quit()

    if len(not_sent_list)>0 or len(sent_list) > 0:
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')

        if len(sent_list) > 0:
            df_sent = pd.DataFrame({'Sent Numbers': sent_list})
            df_sent.to_excel(writer, sheet_name='Sent Numbers', index=False)

        if len(not_sent_list) > 0:
            df_not_sent = pd.DataFrame({'Not Sent Numbers': not_sent_list})
            df_not_sent.to_excel(writer, sheet_name='Not Sent Numbers', index=False)

        writer.close()
        processed_data = output.getvalue()

        st.download_button(
            label="Download Details",
            data=processed_data,
            file_name="whatsapp_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
            
           

