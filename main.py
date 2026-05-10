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
    amount=st.number_input("Enter amount (taka)")
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

col1,col2=st.columns(2)

col1.subheader("Log Bazar",text_alignment="center")
col2.subheader("Log Meal",text_alignment="center")
col1.dataframe(df)
col2.dataframe(meal,height="stretch")

col4,col5=st.columns([1,8])
col6,col7,col8,col9,col10,col11,col12,col13=st.columns(8)

col4.subheader("Members",text_alignment="center")
col5.subheader("Monthly Summery",text_alignment="center")

col6.dataframe(members,width="content")
col7.metric("Total Bazar",df["Amount"].sum(),"Taka")
with col8:
    specific_bazar=st.selectbox("Select Member(Bazar)",members["Member"])
    st.metric("Specific Bazar",df[df["Name"]==specific_bazar]["Amount"].sum(),"taka")
col9.metric("Total Meal",meal["Meals"].sum())
with col10:
    specific_meal=st.selectbox("Select Member(Meal)",members["Member"])
    st.metric("Specific Meal",meal[meal["Name"]==specific_meal]["Meals"].sum())

with col11:
    try:
        meal_rate=(df["Amount"].sum()/meal["Meals"].sum())
    except ZeroDivisionError:
        meal_rate=0
    st.metric("Meal Rate",meal_rate,"Taka")    

with col12:
    specific_due=st.selectbox("Select Member(Due Amount)",members["Member"])
    due=df[df["Name"]==specific_due]["Amount"].sum()-(meal_rate*(meal[meal["Name"]==specific_due]["Meals"].sum()))
    if due>=0:
        st.metric("Due Amount",due,"taka")
    else:
        st.metric("Due Amount",0,"taka")

with col13:
    specific_pay=st.selectbox("Select Member(Pay Amount)",members["Member"])
    pay=(meal_rate*(meal[meal["Name"]==specific_pay]["Meals"].sum()))-df[df["Name"]==specific_pay]["Amount"].sum()
    if pay>=0:
        st.metric("Pay Amount",pay,"taka")
    else:
        st.metric("Pay Amount",0,"taka")
