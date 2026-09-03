# adding ui with streamlit
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# loading cleaned dataset
df = pd.read_csv('study.csv')


# page configuration
st.set_page_config(page_title='Student Dashboard', page_icon=':books:', layout='wide', initial_sidebar_state='expanded')
# adding title and description
st.title('Student Dashboard')
st.write('This dashboard provides insights into student performance and demographics.')
st.markdown('---')

# sidebar and filters
st.sidebar.title('Filters')
subject = st.sidebar.selectbox("Select Subject", ["Mathematics Score", "Reading Score", "Writing Score"])   
# displaying key metrics
avg_math = df['Mathematics Score'].mean()
avg_reading = df['Reading Score'].mean()
avg_writing = df['Writing Score'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Avg Maths", f"{avg_math:.1f}")
col2.metric("Avg Reading", f"{avg_reading:.1f}")
col3.metric("Avg Writing", f"{avg_writing:.1f}")
# visualizationss
st.subheader(f"📊 {subject.title()}  Distribution")
fig, ax = plt.subplots()
sns.histplot(df[subject],
              bins=20, ax=ax,
                color="steelblue",
                edgecolor="black",
                kde=True)
ax.set_xlabel("Score")
ax.set_ylabel("Number of Students")
st.pyplot(fig)

# parent engagement vs performances
st.subheader("👨‍👩‍👧 Parent Engagement vs Performance")
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.boxplot(data=df, x='Parental Level of Education', y=subject, hue='Preparation Course', ax=ax2)
ax2.set_xlabel('Parental Level of Education')
ax2.set_ylabel(subject.replace('_', ' ').title())
for label in ax2.get_xticklabels():
    label.set_rotation(45)
    label.set_ha('right')
fig2.tight_layout()
st.pyplot(fig2)
# gender distribution
st.subheader("👥 Gender Distribution")
fig3, ax3 = plt.subplots()
sns.countplot(data=df, x='Gender', ax=ax3)
ax3.set_xlabel('Gender')
ax3.set_ylabel('Number of Students')
st.pyplot(fig3)

#raw data display
if st.checkbox("Show raw data"):
    st.dataframe(df)