import pandas as pd
import streamlit as st

st.set_page_config(layout="wide",page_title="Meal Track",page_icon="🍱")

st.markdown("""
<style>
.title-box {
    background-color: #1f3b5c;
    padding: 20px;
    border-radius: 8px;
    text-align: center;        
}

.title-text {
    color: white;
    font-size: 36px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""<div class="title-box"><div class="title-text">Meal Track</div></div>""",unsafe_allow_html=True)

st.sidebar.subheader("Select Date",text_alignment="center")
sidebar_col1,sidebar_col2=st.sidebar.columns(2)
year=sidebar_col1.slider("Year",min_value=2026,max_value=2030,value=2026)
month=sidebar_col2.selectbox("Month",["January", "February", "March", "April", "May", "June",
                                "July", "August", "September", "October", "November", "December"])
check_csv="bazar"+month+str(year)+".csv"
check_csv_meal="meal"+month+str(year)+".csv"
check_csv_deposit="deposit"+month+str(year)+".csv"
try:
    df=pd.read_csv(check_csv)
except FileNotFoundError:
    df=pd.DataFrame(columns=["Bazar","Amount","Date"])
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

try:
    deposit=pd.read_csv(check_csv_deposit)
except FileNotFoundError:
    deposit=pd.DataFrame(columns=["Name","Amount","Date"])
    deposit.to_csv(check_csv_deposit,index=False)

st.sidebar.subheader("Make Deposit",text_alignment="center")
with st.sidebar.form("Make Deposit"):
    name=st.selectbox("Select member",members["Member"])
    amount=st.number_input("Enter amount (taka)")
    date=st.date_input("Enter date")
    if st.form_submit_button("Confirm",icon=(":material/check:")):
        deposit_list={"Name":name,"Amount":amount,"Date":date}
        deposit=pd.concat([deposit,pd.DataFrame([deposit_list])],ignore_index=True)
        deposit.to_csv(check_csv_deposit,index=False)
        st.success("Deposit added successfully",icon=(":material/check:"))

st.sidebar.subheader("Add Bazar",text_alignment="center")
with st.sidebar.form("Add Expenses"):
    bazar_details=st.text_input("Enter details")
    amount=st.number_input("Enter amount (taka)")
    date=st.date_input("Enter date")
    if st.form_submit_button("Confirm",icon=(":material/check:")):
        bazar={"Bazar":bazar_details,"Amount":amount,"Date":date}
        df=pd.concat([df,pd.DataFrame([bazar])],ignore_index=True)
        df.to_csv(check_csv,index=False)
        st.success("Expense added successfully",icon=(":material/check:"))

st.sidebar.subheader("Add Daily Meal",text_alignment="center")
with st.sidebar.form("Add Daily Meal"):
    name=st.selectbox("Select member",members["Member"])
    meal_count=st.slider("Enter meal",max_value=3,min_value=0)
    date=st.date_input("Enter date")
    if st.form_submit_button("Confirm",icon=(":material/check:")):
        meals_list={"Name":name,"Meals":meal_count,"Date":date}
        meal=pd.concat([meal,pd.DataFrame([meals_list])],ignore_index=True)
        meal.to_csv(check_csv_meal,index=False)
        st.success("Meal added successfully",icon=(":material/check:"))

st.sidebar.subheader("Members",text_alignment="center")
with st.sidebar:
    st.dataframe(members,hide_index=True)
    delete_member=st.selectbox("Select member to delete",members["Member"])
    if st.button("Delete",type="primary",icon=":material/delete:"):
        members=members[members["Member"]!=delete_member]
        members.to_csv("members.csv",index=False)
        st.rerun()

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

if members.empty:
    st.warning("No members added yet")

col1,col2,col3=st.columns(3)

col1.subheader("Log Bazar",text_alignment="center")
col2.subheader("Log Meal",text_alignment="center")
col3.subheader("Log Deposit",text_alignment="center")

col1.dataframe(df)
col2.dataframe(meal)
col3.dataframe(deposit)

delete_bazar=col1.number_input("Enter Index to Delete ",min_value=0)
with col1:
    if st.button(" Delete",type="primary",icon=":material/delete:"):
        if 0<=delete_bazar<len(df.index):
            df=df.drop(delete_bazar)
            df.to_csv(check_csv,index=False)
            st.rerun()
        else:
            st.error("Invalid index",icon=":material/error:")

delete_meal=col2.number_input("Enter Index to Delete  ",min_value=0)
with col2:
    if st.button("Delete ",type="primary",icon=":material/delete:"):
        if 0<=delete_meal<len(meal.index):
            meal=meal.drop(delete_meal)
            meal.to_csv(check_csv_meal,index=False)
            st.rerun()
        else:
            st.error("Invalid index",icon=":material/error:")

delete_deposit=col3.number_input("Enter Index to Delete",min_value=0)
with col3:
    if st.button(" Delete ",type="primary",icon=":material/delete:"):
        if 0<=delete_deposit<len(deposit.index):
            deposit=deposit.drop(delete_deposit)
            deposit.to_csv(check_csv_deposit,index=False)
            st.rerun()
        else:
            st.error("Invalid index",icon=":material/error:")

st.subheader("Monthly Summery",text_alignment="center")

col4,col5,col6,col7,col8=st.columns(5)  

col4.metric("Total Expense",round(df["Amount"].sum(),1),"Taka")

col5.metric("Total Meal",meal["Meals"].sum(),"Plates")

col6.metric("Total Deposit",round(deposit["Amount"].sum(),1),"Taka")

col7.metric("Remaining Balance",round((deposit["Amount"].sum()-df["Amount"].sum()),1),"Taka")

selected_member=st.selectbox("Select Member",members["Member"],width=250)

col9,col10,col11,col12,col13=st.columns(5)

with col8:
    try:
        meal_rate=(df["Amount"].sum())/(meal["Meals"].sum())
    except ZeroDivisionError:
        meal_rate=0
    st.metric("Meal Rate",round(meal_rate,1),"Taka")    

with col9:
    st.metric("Expense",round(((meal_rate)*(meal[meal["Name"]==selected_member]["Meals"].sum())),1),"Taka")

with col10:
    st.metric("Meal",meal[meal["Name"]==selected_member]["Meals"].sum(),"Plates")

with col11:
    st.metric("Deposit",round((deposit[deposit["Name"]==selected_member]["Amount"].sum()),1),"Taka")    

with col12:
    pay=(meal_rate*(meal[meal["Name"]==selected_member]["Meals"].sum()))-deposit[deposit["Name"]==selected_member]["Amount"].sum()
    if pay>0:
        st.metric("Pay Amount",round(pay,1),"Taka")
    else:
        st.metric("Pay Amount",0.0,"Taka")
    
with col13:
    due=deposit[deposit["Name"]==selected_member]["Amount"].sum()-(meal_rate*(meal[meal["Name"]==selected_member]["Meals"].sum()))
    if due>0:
        st.metric("Refund Due",round(due,1),"Taka")
    else:
        st.metric("Refund Due",0.0,"Taka")
