import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set up the app title
st.set_page_config(page_title="Interactive Data Dashboard", layout="wide", page_icon="📊")
# Refresh Button
if st.button("🔄 Refresh Dashboard"):
    st.experimental_set_query_params()

# Tooltip Message
tooltip_message = (
    "⚠️ The dataset is a working process. You cannot open the Excel file directly, "
    "and no modifications can be made. You can only add data to existing columns, "
    "and column names cannot be changed."
)
st.markdown(
    f'<p style="color: gray; font-size: 12px;">{tooltip_message}</p>',
    unsafe_allow_html=True
)
st.title("📊 Interactive Data Dashboard")

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Choose a page:", ["Data Table", "Visualizations"])

# Sidebar for file upload
st.sidebar.header("Upload your CSV or Excel file")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv", "xlsx"])

# Process the uploaded file
if uploaded_file is not None:
    # Load the file into a DataFrame
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Sidebar toggle for filters
    st.sidebar.header("Filters")
    show_filters = st.sidebar.checkbox("Enable Filters")

    # Apply filters if enabled
    if show_filters:
        st.sidebar.subheader("Filter Options")
        numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

        # Categorical filters
        for col in categorical_columns:
            unique_values = df[col].unique().tolist()
            selected_values = st.sidebar.multiselect(f"Filter by {col}", unique_values, default=unique_values)
            df = df[df[col].isin(selected_values)]

        # Numerical filters
        for col in numerical_columns:
            min_val = float(df[col].min())
            max_val = float(df[col].max())
            range_vals = st.sidebar.slider(f"Filter by {col}", min_val, max_val, (min_val, max_val))
            df = df[(df[col] >= range_vals[0]) & (df[col] <= range_vals[1])]

    # Page 1: Data Table
    if page == "Data Table":
        st.subheader("Uploaded Data with Statistics")

        # Data Preview
        st.dataframe(df.head())

        # Metrics Section
        st.markdown("### Key Statistics for Numerical Columns")
        numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        col1, col2, col3 = st.columns(3)

        for i, col in enumerate(numerical_columns):
            if i % 3 == 0:
                with col1:
                    st.metric(label=f"🔺 Max {col}", value=f"{df[col].max():,.2f}")
                    st.metric(label=f"🔻 Min {col}", value=f"{df[col].min():,.2f}")
                    st.metric(label=f"📊 Avg {col}", value=f"{df[col].mean():,.2f}")
            elif i % 3 == 1:
                with col2:
                    st.metric(label=f"🔺 Max {col}", value=f"{df[col].max():,.2f}")
                    st.metric(label=f"🔻 Min {col}", value=f"{df[col].min():,.2f}")
                    st.metric(label=f"📊 Avg {col}", value=f"{df[col].mean():,.2f}")
            else:
                with col3:
                    st.metric(label=f"🔺 Max {col}", value=f"{df[col].max():,.2f}")
                    st.metric(label=f"🔻 Min {col}", value=f"{df[col].min():,.2f}")
                    st.metric(label=f"📊 Avg {col}", value=f"{df[col].mean():,.2f}")

    # Page 2: Visualizations
    elif page == "Visualizations":
        st.subheader("Visualization Options")

        # Select Chart Type
        chart_type = st.selectbox(
            "Select Chart Type",
            ["Bar Chart", "Line Chart", "Pie Chart", "Gauge Chart", "Scatter Plot", "Area Chart"]
        )

        # Separate categorical and numerical columns for appropriate selection
        numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

        if not numerical_columns and not categorical_columns:
            st.warning("The dataset does not contain appropriate columns for visualizations.")
        else:
            # Select X, Y axes, and additional grouping
            x_axes = st.selectbox("Select X-axis", categorical_columns + numerical_columns)
            y_axes = st.selectbox("Select Y-axis", numerical_columns)
            group_by = st.selectbox("Group/Filter by (Optional)", ["None"] + categorical_columns)

            # Filter Data Based on Grouping (if selected)
            if group_by != "None":
                group_values = st.multiselect(f"Filter by {group_by}", df[group_by].unique().tolist())
                if group_values:
                    df = df[df[group_by].isin(group_values)]

            # Dynamic Chart Generation
            st.write(f"## {chart_type} Visualization")
            if chart_type == "Bar Chart":
                fig = px.bar(df, x=x_axes, y=y_axes, color=group_by if group_by != "None" else None,
                             title=f"{chart_type} of {y_axes} vs {x_axes}")
                st.plotly_chart(fig)

            elif chart_type == "Line Chart":
                fig = px.line(df, x=x_axes, y=y_axes, color=group_by if group_by != "None" else None,
                              title=f"{chart_type} of {y_axes} vs {x_axes}")
                st.plotly_chart(fig)

            elif chart_type == "Pie Chart" and x_axes in categorical_columns:
                fig = px.pie(df, values=y_axes, names=x_axes, title=f"{chart_type} of {x_axes}")
                st.plotly_chart(fig)

            elif chart_type == "Gauge Chart" and y_axes in numerical_columns:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=df[y_axes].mean(),
                    title={'text': f"Average {y_axes}"},
                    gauge={'axis': {'range': [0, df[y_axes].max()]}}
                ))
                st.plotly_chart(fig)

            elif chart_type == "Scatter Plot":
                fig = px.scatter(df, x=x_axes, y=y_axes, color=group_by if group_by != "None" else None,
                                 title=f"{chart_type} of {y_axes} vs {x_axes}")
                st.plotly_chart(fig)

            elif chart_type == "Area Chart":
                fig = px.area(df, x=x_axes, y=y_axes, color=group_by if group_by != "None" else None,
                              title=f"{chart_type} of {y_axes} vs {x_axes}")
                st.plotly_chart(fig)

else:
    st.write("Please upload a CSV or Excel file to begin.")
