import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

try:
    df=pd.read_csv("bazar.csv")
except FileNotFoundError:
    df=pd.DataFrame(columns=["Name","Amount","Date"])
    df.to_csv("bazar.csv",index=False)
st.set_page_config(layout="wide",page_title="Meal Track",page_icon="🍱")
with st.sidebar.form("Add Expenses"):
    name=st.selectbox("Select member",["member1","member2"])
    amount=st.number_input("Enter amount")
    date=st.date_input("Enter date")
    if st.form_submit_button("Confirm",icon=(":material/check:")):
        bazar={"Name":name,"Amount":amount,"Date":date}
        df=pd.concat([df,pd.DataFrame([bazar])],ignore_index=True)
        df.to_csv("bazar.csv",index=False)
        st.toast("Expense added successfully",icon=(":material/check:"))


col1,col2=st.columns(2)
col1.subheader("Expenses",text_alignment="center")
col2.subheader("Track Summary",text_alignment="center")
col1.dataframe(df)

