# DocQuest - AI-Powered PDF Study Question Generator

DocQuest is a modern web application that allows students, educators, and lifelong learners to upload PDF study materials and generate customized study questions. Powered by Google's Gemini AI, the app extracts text from documents and creates high-quality Multiple Choice Questions (MCQs) and Short Answer questions adjusted to the selected difficulty level.

## 🚀 Features

- 📑 **PDF Parser**: Seamlessly extracts raw text content from uploaded PDF documents.
- 🤖 **Gemini AI Integration**: Uses the advanced `gemini-2.5-flash` model to analyze content and craft relevant, context-aware study questions.
- ⚙️ **Customizable Settings**:
  - Select the number of questions to generate (3, 5, 10, or 15).
  - Adjust the difficulty level (Easy, Medium, or Hard) to match your study goals.
- 🎨 **Premium Modern UI**: Built with rich aesthetics, smooth CSS animations, dark-themed styling, and an intuitive drag-and-drop zone.
- ⚡ **Fast API Backend**: Powered by FastAPI for highly performant and asynchronous file upload and response delivery.

---

## 📂 Project Structure

```text
pdf-analyzer/
├── backend/
│   ├── services/
│   │   ├── ai_generator.py   # Interface to Google Gemini API
│   │   └── pdf_parser.py     # PDF text extraction logic (using pypdf)
│   ├── main.py               # FastAPI server and static files mount
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── index.html            # Webpage layout structure
│   ├── script.js             # API interaction and dynamic UI updates
│   └── styles.css            # Custom CSS styles, loaders, and layout
├── .gitignore                # Git ignoring patterns (venv, .env, etc.)
└── README.md                 # Project documentation
```

---

## 🛠️ Setup & Installation

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system. You will also need a **Google Gemini API Key** which you can get from the [Google AI Studio](https://aistudio.google.com/).

### 2. Clone/Navigate to the Repository
Navigate to the root directory of the project:
```bash
cd pdf-analyzer
```

### 3. Create a Virtual Environment
Create and activate a Python virtual environment:
```powershell
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
Install all required packages from `requirements.txt`:
```bash
pip install -r backend/requirements.txt
```

### 5. Setup Environment Variables
Create a file named `.env` in the `backend/` directory:
```text
GEMINI_API_KEY=your_google_gemini_api_key_here
```
*(Replace `your_google_gemini_api_key_here` with your actual API key.)*

---

## 🖥️ Running the Application

Start the FastAPI application by running:
```bash
python backend/main.py
```

The application will start, and the console will output:
```text
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Open your web browser and navigate to **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** to access the DocQuest interface.

---

## 💡 How It Works
1. **Upload**: Drag and drop a PDF file or select one from your computer.
2. **Choose Settings**: Select the desired number of questions and difficulty level from the dropdown menus.
3. **Analyze**: The backend extracts text from the PDF using `pypdf` and passes it to the Google Gemini AI.
4. **Solve**: The generated MCQ and Short Answer questions are rendered in an interactive card list directly on your screen. You can expand/reveal answers to check your knowledge!
