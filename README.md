# 📊 VizQ – Text to SQL & Data Visualization App

VizQ is a **GenAI-powered application** that converts **natural language queries into SQL** using **Google Gemini API** and visualizes results using **Streamlit, Pandas, and Matplotlib**.

---

## 🚀 Features

- 🧠 Convert **text → SQL queries** using Gemini API  
- 📊 Display query results in **tabular format**  
- 📈 Generate **data visualizations (charts)**  
- 📂 Upload your own dataset (CSV support)  
- 🏠 Built-in **default housing dataset** for instant usage  
- ⚡ Fast and interactive UI with Streamlit  

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **GenAI / NLP:** Google Gemini API (`google-generativeai` / `google-genai`)  
- **Database:** SQLite  
- **Data Processing:** Pandas  
- **Visualization:** Matplotlib  
- **Environment Management:** python-dotenv / Streamlit Secrets  

---

## 🔄 Workflow

```
User Input (Natural Language)
        ↓
Streamlit UI
        ↓
Gemini API (Text → SQL)
        ↓
SQLite Database Execution
        ↓
Pandas (Fetch Results)
        ↓
Table + Charts (Matplotlib)
```

---

## 📂 Project Structure

```
vizQ
│
├── app.py
├── housing.csv
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/vizQ.git
cd vizQ
```

---

### 2️⃣ Create virtual environment

```bash
python -m venv venv
```

Activate (Windows):

```bash
venv\Scripts\activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Add API Key

Create a `.env` file in the root directory:

```
GOOGLE_API_KEY=your_api_key_here
```

---

### 5️⃣ Run the app

```bash
python -m streamlit run app.py
```

---

## ▶️ How to Use

1. Run the application:
   ```bash
   python -m streamlit run app.py
   ```

2. Open in browser:
   ```
   http://localhost:8501
   ```

3. Choose one option:
   - Upload your own CSV dataset  
   - OR use the default housing dataset  

4. Enter your query in natural language  

5. Click **Generate**  

6. View:
   - Generated SQL query  
   - Table results  
   - Visualization (chart)  

---

## 📌 Example Query & Output

### 🧾 Input (User Query)

```
show median income and total rooms for houses with population 322
```

---

### 🧠 Generated SQL

```sql
SELECT median_income, total_rooms FROM housing WHERE population = 322;
```

---

### 📊 Output (Table)

| median_income | total_rooms |
|--------------|------------|
| 8.3252       | 880        |
| 4.7361       | 914        |
| 5.1831       | 440        |
| 4.2917       | 762        |

---

### 📈 Visualization

- Bar chart
<img width="537" height="530" alt="Screenshot 2026-03-17 193129" src="https://github.com/user-attachments/assets/205d35e3-1d75-4f54-9e9d-f878af167175" />

-pie chart
<img width="1172" height="521" alt="Screenshot 2026-03-17 193427" src="https://github.com/user-attachments/assets/0ea59168-0962-4839-b23f-d20e56731f1d" />

---

### 🧾 Another Example

**Input:**
```
Show top 5 most expensive houses
```

**Generated SQL:**
```sql
SELECT * FROM housing
ORDER BY price DESC
LIMIT 5;
```

---

## 💡 Tips

- Use simple natural language (like speaking to a human)
- Example:
  - "Show all houses with 3 bedrooms"
  - "Plot price vs area"
  - "Count houses by location"

---

## 💡 Future Enhancements

- 🔧 SQL query explanation  
- 📊 Advanced visualizations (Plotly)  
- 🤖 Query error correction  
- 📁 Support for multiple datasets  

---

## 👨‍💻 Author

**Rithwik Reddy Marla**

---



## 📌 Note

- API usage depends on Gemini quota limits  
- Ensure your API key is kept secure  
