import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

sidebar_col1,sidebar_col2=st.sidebar.columns(2)
year=sidebar_col1.slider("Year",min_value=2026,max_value=2030,value=2026)
month=sidebar_col2.selectbox("Month",["January", "February", "March", "April", "May", "June",
                                "July", "August", "September", "October", "November", "December"])
check_csv=month+str(year)+".csv"

try:
    df=pd.read_csv(check_csv)
except FileNotFoundError:
    df=pd.DataFrame(columns=["Name","Amount","Date"])
    df.to_csv(check_csv,index=False)

try:
    members=pd.read_csv("members.csv")
except FileNotFoundError:
    members=pd.DataFrame(columns=["Member"])
    members.to_csv("members.csv",index=False)
    st.dataframe(members)
st.set_page_config(layout="wide",page_title="Meal Track",page_icon="🍱")

st.sidebar.subheader("Add Details",text_alignment="center")
with st.sidebar.form("Add Expenses"):
    name=st.selectbox("Select member",members["Member"])
    amount=st.number_input("Enter amount")
    date=st.date_input("Enter date")
    if st.form_submit_button("Confirm",icon=(":material/check:"),type="primary"):
        bazar={"Name":name,"Amount":amount,"Date":date}
        df=pd.concat([df,pd.DataFrame([bazar])],ignore_index=True)
        df.to_csv(check_csv,index=False)
        st.toast("Expense added successfully",icon=(":material/check:"))

st.sidebar.subheader("Add New Member",text_alignment="center")
with st.sidebar.form("Add Member"):
    user_name=st.text_input("Enter Username")
    password=st.text_input("Enter password",type="password")
    member=st.text_input("Add Member",placeholder="Enter Name")
    if st.form_submit_button("Add",icon=(":material/add:")):
        if user_name=="admin" and password=="admin123":
                if member!="":
                    index=0
                    check=0
                    while 0<=index<len(members):
                        if members.loc[index,"Member"]==member:
                            check+=1
                        index+=1
                    if check>0:
                        st.error("Member already exists",icon=":material/error:")
                    else:
                        members_list={"Member":member}
                        members=pd.concat([members,pd.DataFrame([members_list])],ignore_index=True)
                        members.to_csv("members.csv",index=False)
                        st.rerun()
                else:
                    st.error("Please enter usernane",icon=":material/error:")  
        else:
            st.error("Invalid username or password",icon=":material/error:")         

col1,col2=st.columns(2)

col1.subheader("Expenses",text_alignment="center")
col2.subheader("Track Summary",text_alignment="center")
col1.dataframe(df)

st.markdown("Members",text_alignment="left")
index=0
while 0<=index<len(members):
    st.write(index+1,members['Member'][index])
    index+=1
