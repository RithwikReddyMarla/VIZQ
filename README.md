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

## 📸 Example Use Cases

- “Show all houses with price > 500000”  
- “Average price by location”  
- “Plot price vs area”  

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
