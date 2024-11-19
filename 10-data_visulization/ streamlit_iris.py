import streamlit as st
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(layout="wide")
st.title('Iris Dataset Analysis')

# Load and prepare data
@st.cache_data
def load_data():
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['Species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
    return df, iris.feature_names

df, feature_names = load_data()
X = df[feature_names].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Sidebar controls
st.sidebar.header('Analysis Controls')
clusters = st.sidebar.slider('Select Number of Clusters:', 1, 6, 3)



# 1. Feature Distribution Analysis
st.header('1. Feature Distributions by Species')
option_with_no_species = [col for col in df.columns if col != "Species"]
selected_option = st.selectbox(label="Select Feature for Box Plot:",options=option_with_no_species)
# Colors for species
colors = {'setosa': '#FF4B4B', 'versicolor': '#4B4BFF', 'virginica': '#4BFF4B'}
st.text(f'Distribution of {selected_option} by Species')
# Feature selection for box plot
mydf = px.data.tips()
fig = px.box(df,x="Species", y=selected_option, color="Species", color_discrete_map=colors  )
st.plotly_chart(fig)



# 2. Feature Relationships
st.header('2. Feature Relationships')
st.write("Feature Relationships by Species")
fig = px.scatter_matrix(df, dimensions=option_with_no_species, color="Species", color_discrete_map=colors)
st.plotly_chart(fig)



# 3. Feature Correlations
st.header('3. Feature Correlations')
correlation = df[feature_names].corr().round(2)
# Create correlation heatmap
st.write("Draw a correlation heatmap here")
fig = px.imshow(correlation, text_auto=True,color_continuous_scale='RdBu')
st.plotly_chart(fig)



# 4. Elbow Analysis
st.header('4. Elbow Analysis')
@st.cache_data
def perform_elbow_analysis(X, max_clusters=10):
    inertias = []
    for k in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)
    return inertias
inertias = perform_elbow_analysis(X_scaled)
fig = px.line(x=[int(i) for i in range(len(inertias))], y=inertias, markers=True, title="Elbow Method Analysis").update_layout(
    xaxis_title="Number of Clusters", yaxis_title="Inertia"
)
st.plotly_chart(fig, use_container_width=True)



# 5. Clustering Analysis
st.header('5. Clustering Analysis')
# Perform clustering
kmeans = KMeans(n_clusters=clusters, random_state=42)
cluster_labels = kmeans.fit_predict(X_scaled)
df['Cluster'] = cluster_labels.astype(str)
# Create comparison plots
col1, col2 = st.columns(2)
with col1:
    st.subheader('Clustering Result')
    fig = px.scatter(df, x="petal width (cm)", y="petal length (cm)", color="Cluster", title="KMeans Clustering Result")
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.subheader('Actual Species')
    fig = px.scatter(df, x="petal width (cm)", y="petal length (cm)",color="Species", color_discrete_map=colors, title="Actual Species Distribution")
    st.plotly_chart(fig, use_container_width=True)



# 6. Clustering Performance Analysis
st.header('6. Clustering Performance')
confusion_df = pd.crosstab(df['Species'], df['Cluster'], margins=True)
st.write("Confusion Matrix (Species vs Clusters):")
st.write(confusion_df)



# 7. Additional Statistics
st.header('7. Feature Statistics')
col3, col4 = st.columns(2)

with col3:
    st.subheader('Statistics by Species')
    species_stats = df.groupby('Species')[feature_names].agg(['mean', 'std']).round(2)
    st.write(species_stats)
with col4:
    st.subheader('Statistics by Cluster')
    cluster_stats = df.groupby('Cluster')[feature_names].agg(['mean', 'std']).round(2)
    st.write(cluster_stats)