import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(layout="wide",page_title="Meal Track",page_icon="🍱")

sidebar_col1,sidebar_col2=st.sidebar.columns(2)
year=sidebar_col1.slider("Year",min_value=2026,max_value=2030,value=2026)
month=sidebar_col2.selectbox("Month",["January", "February", "March", "April", "May", "June",
                                "July", "August", "September", "October", "November", "December"])
check_csv="bazar"+month+str(year)+".csv"
check_csv_meal="meal"+month+str(year)+".csv"
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

try:
    meal=pd.read_csv(check_csv_meal)
except FileNotFoundError:
    meal=pd.DataFrame(columns=["Name","Meals","Date"])
    meal.to_csv(check_csv_meal,index=False)

st.sidebar.subheader("Add Bazar",text_alignment="center")
with st.sidebar.form("Add Expenses"):
    name=st.selectbox("Select member",members["Member"])
    amount=st.number_input("Enter amount")
    date=st.date_input("Enter date")
    if st.form_submit_button("Confirm",icon=(":material/check:"),type="primary"):
        bazar={"Name":name,"Amount":amount,"Date":date}
        df=pd.concat([df,pd.DataFrame([bazar])],ignore_index=True)
        df.to_csv(check_csv,index=False)
        st.success("Expense added successfully",icon=(":material/check:"))

st.sidebar.subheader("Add Daily Meal",text_alignment="center")
with st.sidebar.form("Add Daily Meal"):
    name=st.selectbox("Select member",members["Member"])
    meal_count=st.slider("Enter meal",max_value=3,min_value=0)
    date=st.date_input("Enter date")
    if st.form_submit_button("Confirm",icon=(":material/check:"),type="primary"):
        meals_list={"Name":name,"Meals":meal_count,"Date":date}
        meal=pd.concat([meal,pd.DataFrame([meals_list])],ignore_index=True)
        meal.to_csv(check_csv_meal,index=False)
        st.success("Meal added successfully",icon=(":material/check:"))

st.sidebar.subheader("Add New Member",text_alignment="center")
with st.sidebar.form("Add Member"):
    user_name=st.text_input("Enter Username")
    password=st.text_input("Enter password",type="password")
    member=st.text_input("Add Member",placeholder="Enter Name")
    if st.form_submit_button("Add",icon=(":material/add:"),type="primary"):
        if user_name=="admin" and password=="admin123":
                if member!="":
                    index=0
                    check=0
                    if member in members["Member"].values:
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

col1,col2,col3=st.columns(3)

col1.subheader("Log Bazar",text_alignment="center")
col2.subheader("Log Meal",text_alignment="center")
col1.dataframe(df)
col2.dataframe(meal)

index=0
with col3:
    st.markdown("### Members")
    while 0<=index<len(members):
        st.write(index+1,members['Member'][index])
        index+=1
