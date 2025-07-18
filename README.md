```bash
# EduInsight - AI-Powered Education Assistant

EduInsight is an AI-powered assistant built with Flask and Google Gemini (via LangChain) that analyzes nutritional input and generates personalized recommendations and meal plans for students. It aims to support **Quality Education (UN SDG 4)** by improving students' well-being through better nutrition insights.
```

```bash
## Features

- Accepts natural language input of meals or food items.
- Uses Google Gemini AI via LangChain to analyze nutritional content.
- Provides:
  - Estimated total calories
  - Macronutrient breakdown (proteins, carbs, fats)
  - Personalized health suggestions
  - Daily meal plan generation
- Clean and intuitive web UI using Flask and HTML.
```

```bash
## Tech Stack

- **Frontend:** HTML (Flask templates)
- **Backend:** Python, Flask
- **AI Model:** Google Gemini (via LangChain)
- **Env Management:** Python `dotenv`
- **LLM Agent Flow:** LangGraph
```

```bash
## Project Structure

EduInsight-AI-Education-Assistant/
├── .gitignore
├── AUTHORS.txt
├── LICENSE.txt
├── EduInsight_Index.html
├── index.html
├── __init__.py
├── __main__.py
├── __pip-runner__.py
├── agent.py
├── agent.cpython-313.pyc
├── app.py
├── neww.env
├── activate
├── activate.bat
├── activate.fish
├── deactivate.bat
├── dotenv.exe
├── filetype.exe
├── flask.exe
├── httpx.exe
├── pip.exe
├── pip3.exe
├── pip3.13.exe
├── py.typed
├── python.exe
├── pythonw.exe
├── pyvenv.cfg
```

```bash
2. Set Up Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Requirements
commands
python -m venv venv
venv\Scripts\activate
pip install flask langchain langgraph langchain-google-genai python-dotenv
pip install flask langchain langgraph python-dotenv

4. Add Google API Key
GOOGLE_API_KEY=your_gemini_api_key_here

5. Run the App
python app.py #to run
```

```bash
AUTHOR
Milan Dhandhukiya
```bash

