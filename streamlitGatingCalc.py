
import streamlit as st
from calArea import CalcArea, CalcRiser
import numpy as np
import csv
import pandas as pd

gating_header = ['Head', 'LossFactor', 'FlowRate', 'CastingHeight_P', 'TotalCasting_C', 'Name', 'Area', 'Width', 'Height']
riser_header = ['Material','CastingWt','CastingMod','ColdRiser',
                            'NeckMod','RiserMod',
                            'NeckW','NeckH','NeckL',
                            'RiserBase','RiserTop','RiserH','RiserWt','RiserFeed']

def savecsv_gating(filename,data):
    # writing to csv file 
    with open(filename, 'w', encoding='UTF8', newline='') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
        # writing the fields 
        csvwriter.writerow(gating_header)
        csvwriter.writerows(data)

def savecsv_riser(riser_file,riser_data):
    with open(riser_file, 'w', encoding='UTF8', newline='') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(riser_header)
        csvwriter.writerows(riser_data)

ch = st.radio("รายการคำนวณ",("CalcGating","CalcRiser","Other"))

if ch == "CalcGating":
    h = st.number_input("กรุณาเลือกตัวเลขความสูง",min_value=0,max_value=400,value=200,step=5)
    f = st.number_input("กรุณาเลือกตัวเลข f",min_value=0.0,max_value=0.9,value=0.4,step=0.1)
    q = st.number_input("กรุณาเลือกตัวเลข flowrate",min_value=0.0,max_value=10.0,value=1.0,step=0.1)
    p = st.number_input("กรุณาเลือกตัวเลขความสูงงานด้านบน",min_value=0,max_value=200,value=30,step=10)
    c = st.number_input("กรุณาเลือกตัวเลขความสูงงานทั้งหมด",min_value=0,max_value=250,value=100,step=10)
    th = st.number_input("กรุณาเลือกความหนา ingate",min_value=0.0,max_value=10.0,value=4.0,step=0.1)
    name = st.text_input("กรอกชื่อ runner_n/choke_n/ingate_n")

    fname = st.text_input("กรอกชื่อไฟล์ที่จะบันทึก")

    st.text("ข้อมูลของคุณ คือ : " + f'h={h:.0f} f={f:0.2f} q={q:0.2f} p={p:0.1f} c={c:0.1f} name={name} gateTH={th:.1f}')
    c1 = CalcArea(h=h,f=f,q=q,p=p,c=c,name=name,gthickness=th)

    calc = st.button("คำนวณ gating")
    label_res = st.empty()
    label_res.text("คุณยังไม่ได้กดปุ่มcalc")
    save = st.button("บันทึกลงไฟล์")
    label_save = st.empty()
    label_save.text("คุณยังไม่ได้กดปุ่มsave")

    if calc:
        result = c1.save()
        label_res.text("ผลการคำนวณ: "+f'name:{result[5]} , area:{result[6]:.0f} mm2 , width:{result[7]:.0f} mm , height:{result[8]:.1f} mm')
        df = pd.DataFrame(
                CalcArea.data,
                columns=gating_header)
        st.write(df)
    if save:
        savecsv_gating(fname,CalcArea.data)
        label_save.text("บันทึกผลคำนวณลงไฟล์ "+ fname + "เรียบร้อยแล้ว")
        with open(fname) as f:
            btn = st.download_button('Download File CSV',
                            data=f,
                            file_name=fname, 
                            mime='text/csv'
                            )  # Defaults to 'text/plain'

if ch == "CalcRiser":

    mat = st.text_input("กรอกชื่อ mat FC25/FCD45")
    cwt = st.number_input("กรุณาเลือกน้ำหนักชิ้นงาน",min_value=0.0,max_value=30.0,value=4.0,step=0.5)
    cmd = st.number_input("กรุณาเลือก Casting mod",min_value=0.0,max_value=2.0,value=1.0,step=0.1)
    nh = st.number_input("กรุณาเลือก ความหนา neck",min_value=0.0,max_value=30.0,value=0.0,step=0.5)
    cold = st.text_input("กรอกชนิดColdriser True/False")
    fname = st.text_input("กรอกชื่อไฟล์ที่จะบันทึก")
    
    st.text("ข้อมูลของคุณ คือ : " + f'mat={mat} wt={cwt:.2f} mod={cmd} cold riser={cold} neck th={nh:.2f}')
    r1 = CalcRiser(mat,cwt,cmd,cold,nh)

    calc = st.button("คำนวณ gating")
    label_res = st.empty()
    label_res.text("คุณยังไม่ได้กดปุ่มcalc")
    save = st.button("บันทึกลงไฟล์")
    label_save = st.empty()
    label_save.text("คุณยังไม่ได้กดปุ่มsave")
    # dwload = st.button("Dow load file")
    
    if calc:
        result = r1.save()
        label_res.text("ผลการคำนวณ: "+f'mat:{result[0]} , mod:{result[5]:.3f} cm , base:{result[9]:.0f} mm , top:{result[10]:.1f} mm, Height:{result[11]:.1f} mm, Weight:{result[12]:.3f} kg ,ratio:{result[13]:.1f} time')
        df = pd.DataFrame(
                CalcRiser.data,
                columns=riser_header)
        st.write(df)
    if save:
        savecsv_riser(fname,CalcRiser.data)
        label_save.text("บันทึกผลคำนวณลงไฟล์ "+ fname + "เรียบร้อยแล้ว")
        with open(fname) as f:
            btn = st.download_button('Download File CSV',
                                data=f,
                                file_name=fname, 
                                mime='text/csv'
                                )  # Defaults to 'text/plain'



