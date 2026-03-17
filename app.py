import streamlit as st
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import google.genai as genai
import dotenv

# Load environment variables
dotenv.load_dotenv()
genai.api_key = os.environ['GOOGLE_API_KEY']

# Configure Streamlit for better performance
st.set_page_config(page_title="VizQ", layout="wide", initial_sidebar_state="collapsed")

# Clean up old custom tables on app start (keep housing.csv and current selected table)
def cleanup_custom_tables():
    db_name = "dataset.db"
    try:
        current_table = None
        if 'table' in st.session_state and st.session_state['table'] is not None:
            current_table = st.session_state['table'].lower()
        
        tables = get_table_names_early(db_name)
        if tables:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            for table in tables:
                if table.lower() != 'housing' and table.lower() != current_table:
                    cursor.execute(f"DROP TABLE IF EXISTS {table}")
            conn.commit()
            conn.close()
    except:
        pass

def get_table_names_early(db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
        conn.close()
        return [table[0] for table in tables]
    except:
        return []

cleanup_custom_tables()

# Create uploads folder
os.makedirs('uploads', exist_ok=True)

# Function to load Google Gemini Model and provide queries as response
@st.cache_data(ttl=3600)
def get_gemini_response(question, prompt):
    try:
        client = genai.Client()
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, question]
        )
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

# Function to retrieve and execute query from the database
def execute_sql_query(sql_query, db_name):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        conn.close()
        return rows, columns
    except sqlite3.Error as e:
        print(f"SQLite error while executing query: {e}")
        return None, None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None, None

# Function to plot bar chart
@st.cache_resource
def plot_bar_chart(columns, values, xlabel, ylabel):
    try:
        # Convert values to numeric
        numeric_values = []
        valid_columns = []
        for i, v in enumerate(values):
            try:
                numeric_values.append(float(v))
                valid_columns.append(columns[i])
            except (ValueError, TypeError):
                pass
        
        if not numeric_values:
            return None
        
        fig, ax = plt.subplots(figsize=(2, 2))
        ax.bar(valid_columns, numeric_values, color='steelblue')
        ax.set_xlabel(xlabel, fontsize=10)
        ax.set_ylabel(ylabel, fontsize=10)
        ax.set_title('Bar Chart', fontsize=12, fontweight='bold')
        ax.tick_params(axis='x', rotation=45, labelsize=9)
        plt.tight_layout()
        return fig
    except Exception as e:
        st.error(f"Bar chart error: {str(e)}")
        return None
    finally:
        plt.close('all')

# Function to plot pie chart
@st.cache_resource
def plot_pie_chart(labels, sizes, title):
    try:
        # Convert sizes to numeric
        numeric_sizes = []
        valid_labels = []
        for i, s in enumerate(sizes):
            try:
                numeric_sizes.append(float(s))
                valid_labels.append(labels[i])
            except (ValueError, TypeError):
                pass
        
        if not numeric_sizes or sum(numeric_sizes) <= 0:
            st.error("No valid numeric values for pie chart")
            return None
        
        fig, ax = plt.subplots(figsize=(2, 2))
        colors = plt.cm.Set3(range(len(numeric_sizes)))
        ax.pie(numeric_sizes, labels=valid_labels, autopct='%1.1f%%', startangle=140, colors=colors)
        ax.set_title(title, fontsize=12, fontweight='bold')
        plt.tight_layout()
        return fig
    except Exception as e:
        st.error(f"Pie chart error: {str(e)}")
        return None
    finally:
        plt.close('all')

# Function to create a SQLite database from a CSV file
def create_db_from_csv(csv_file, db_name):
    try:
        df = pd.read_csv(csv_file)
        table_name = os.path.splitext(os.path.basename(csv_file))[0]
        conn = sqlite3.connect(db_name)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        return table_name
    except Exception as e:
        print(f"Error creating database from CSV: {e}")
        return None

# Function to get table names from the database
def get_table_names(db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
        conn.close()
        return [table[0] for table in tables]
    except Exception as e:
        print(f"Error fetching table names: {e}")
        return []

# Function to get column names for a specific table
def get_column_names(db, table_name):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({table_name});")
        columns = cur.fetchall()
        conn.close()
        return [column[1] for column in columns]
    except Exception as e:
        print(f"Error fetching column names: {e}")
        return []

# Define Prompts
custom_prompt_template = """
You are an expert in converting English text to SQL query.
I have a database with table named {table_name} & have columns {columns}. 
Please help me with this task. Provide only the SQL query without any additional text or formatting.
"""

# Streamlit App
st.title("VizQ: English to SQL Query Converter")

db_name = "dataset.db"

# Initialize session state
if 'page' not in st.session_state:
    st.session_state['page'] = 1
if 'table' not in st.session_state:
    st.session_state['table'] = None
    st.session_state['db_name'] = None
    st.session_state['results'] = None
    st.session_state['result_columns'] = None

# ============== PAGE 1: DATASET SELECTION ==============
if st.session_state['page'] == 1:
    st.header("Dataset Selection")
    
    dataset_choice = st.radio(
        "Do you have your own dataset?",
        ("No, use housing dataset", "Yes, I have a dataset"),
        horizontal=True
    )
    
    st.divider()
    
    # Option 1: Use Housing Dataset
    if dataset_choice == "No, use housing dataset":
        if os.path.exists("housing.csv"):
            create_db_from_csv("housing.csv", db_name)
            available_tables = get_table_names(db_name)
            
            if available_tables:
                selected_table = st.selectbox("Select table:", available_tables, key="table_selector_1")
                if st.button("Select Table", type="primary", use_container_width=True):
                    st.session_state['table'] = selected_table
                    st.session_state['db_name'] = db_name
                    st.success(f"✓ Table '{selected_table}' selected!")
        else:
            st.warning("⚠️ housing.csv not found. Please upload a dataset instead.")
    
    # Option 2: Upload Custom Dataset
    else:
        uploaded_file = st.file_uploader("Upload your CSV file", type="csv", key="csv_uploader")
        
        if uploaded_file is not None:
            file_path = os.path.join("uploads", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            custom_table_name = create_db_from_csv(file_path, db_name)
            if custom_table_name:
                st.success(f"✓ File '{uploaded_file.name}' uploaded!")
                
                # Clear cache to show newly uploaded table
                # st.cache_data.clear()
                
                # Show table dropdown after upload
                available_tables = get_table_names(db_name)
                if available_tables:
                    selected_table = st.selectbox("Select table:", available_tables, key="table_selector_2")
                    if st.button("Select Table", type="primary", use_container_width=True):
                        st.session_state['table'] = selected_table
                        st.session_state['db_name'] = db_name
                        st.success(f"✓ Table '{selected_table}' selected!")
            else:
                st.error("Failed to process file.")
    
    # Next button
    st.divider()
    if st.session_state['table'] is not None:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col3:
            if st.button("Next →", type="primary", key="next_page"):
                st.session_state['page'] = 2
                st.rerun()

# ============== PAGE 2: QUERY & VISUALIZATION ==============
elif st.session_state['page'] == 2:
    if st.session_state['table'] is None:
        st.warning("⚠️ Please select a dataset first.")
    else:
        table = st.session_state['table']
        db = st.session_state['db_name']
        columns = get_column_names(db, table)
        
        st.header("Query & Visualization")
        st.write(f"**Table:** {table}")
        st.write(f"**Columns:** {', '.join(columns)}")
        
        st.subheader("Ask a Question")
        question = st.text_area("Enter your question in English:", height=100, placeholder="E.g., Show me average prices by region")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Generate Query", type="primary", use_container_width=True):
                if question.strip():
                    columns_str = ", ".join(columns)
                    custom_prompt = custom_prompt_template.format(table_name=table, columns=columns_str)
                    response = get_gemini_response(question, custom_prompt)
                    
                    if response:
                        sql_query = response.strip().replace('```', '').strip()
                        if sql_query.lower().startswith('sql'):
                            sql_query = sql_query[3:].strip()
                        
                        st.subheader("Generated SQL Query:")
                        st.code(sql_query, language="sql")
                        
                        result, result_columns = execute_sql_query(sql_query, db)
                        
                        if result and result_columns:
                            st.session_state['results'] = result
                            st.session_state['result_columns'] = result_columns
                            
                            df = pd.DataFrame(result, columns=result_columns)
                            st.subheader("Results:")
                            st.caption(f"📊 Rows: {len(df)} | Columns: {len(df.columns)}")
                            st.dataframe(df, use_container_width=True)
                            st.success("✓ Query executed!")
                        else:
                            st.error("No results found or query execution failed.")
                    else:
                        st.error("Failed to generate SQL query.")
                else:
                    st.warning("Please enter a question.")
        
        with col2:
            if st.button("← Back", use_container_width=True):
                st.session_state['page'] = 1
                st.rerun()
        
        # Visualization section
        if st.session_state['results'] is not None:
            st.subheader("Visualization")
            
            result = st.session_state['results']
            result_columns = st.session_state['result_columns']
            
            if len(result_columns) >= 2 and len(result) > 0:
                graph_type = st.selectbox(
                    "Select visualization type:",
                    ["Bar Chart", "Pie Chart", "Both"],
                    key="graph_selectbox"
                )
                
                if st.button("Generate Visualization", type="primary", use_container_width=True):
                    try:
                        x_values = [str(row[0]) for row in result]
                        y_values = [row[1] for row in result]
                        
                        st.info(f"📊 Plotting {len(result)} data points")
                        
                        if graph_type in ["Bar Chart", "Both"]:
                            fig_bar = plot_bar_chart(x_values, y_values, result_columns[0], result_columns[1])
                            if fig_bar:
                                st.pyplot(fig_bar)
                                st.success("✓ Bar chart generated!")
                            else:
                                st.error("Failed to generate bar chart.")
                        
                        if graph_type in ["Pie Chart", "Both"]:
                            fig_pie = plot_pie_chart(x_values, y_values, f"{result_columns[0]} vs {result_columns[1]}")
                            if fig_pie:
                                st.pyplot(fig_pie)
                                st.success("✓ Pie chart generated!")
                            else:
                                st.error("Failed to generate pie chart.")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.error("❌ Cannot generate graphs: At least 2 columns are required for visualization!")
    
