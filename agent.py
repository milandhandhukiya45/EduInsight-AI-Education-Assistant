from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

# Load your API key from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
print("API KEY:", api_key)

# Set up Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash-latest",
    temperature=0.2,
    google_api_key=api_key
)

# === Core LangGraph Functions for Quality Education ===

def get_education_input(dictionary):
    """This will be filled by Flask form."""
    return dictionary

def analyze_education_data(dictionary):
    prompt = f"""
    You are an education policy expert. Analyze the following student or school education data and provide:
    1. Learning level summary (e.g., foundational, intermediate, advanced)
    2. Strengths and weaknesses in learning
    3. Accessibility or inclusion gaps (if any)
    4. Quality indicators: teaching method, infrastructure, technology use
    
    Input: {dictionary['education_input']}
    
    Provide a structured and detailed analysis.
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    dictionary["education_analysis"] = response.content.strip()
    return dictionary

def classify_learning_quality(dictionary):
    prompt = f"""
    Based on this analysis, categorize the overall education quality as one of the following:
    - "needs_improvement"
    - "adequate"
    - "excellent"
    
    Analysis: {dictionary['education_analysis']}
    
    Respond with only one word: needs_improvement, adequate, or excellent.
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    category = response.content.strip().lower()
    dictionary["education_category"] = category
    return dictionary

def education_router(dictionary):
    cat = dictionary["education_category"]
    if "needs_improvement" in cat:
        return "needs_improvement"
    elif "adequate" in cat:
        return "adequate"
    elif "excellent" in cat:
        return "excellent"
    else:
        return "adequate"

def improvement_recommendations(dictionary):
    prompt = f"""
    The education analysis shows a need for improvement. Please provide:
    1. 4-5 practical suggestions to improve education quality
    2. Tools, technologies, or platforms that can help
    3. Teacher or parental involvement strategies
    4. Personalized learning methods if applicable

    Analysis: {dictionary['education_analysis']}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    dictionary["recommendations"] = f"🔴 EDUCATION NEEDS IMPROVEMENT\n\n{response.content.strip()}"
    return dictionary

def adequate_recommendations(dictionary):
    prompt = f"""
    The education input shows adequate quality. Provide:
    1. Suggestions for maintaining current quality
    2. Tips to enhance student engagement or personalization
    3. Technology/tools to make learning more effective

    Analysis: {dictionary['education_analysis']}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    dictionary["recommendations"] = f"🟡 ADEQUATE EDUCATION QUALITY\n\n{response.content.strip()}"
    return dictionary

def excellence_recommendations(dictionary):
    prompt = f"""
    The analysis shows excellent education quality. Please:
    1. Highlight what is working well
    2. Suggest innovations or advanced tools to go further
    3. Recommend ways to share this model with others (e.g., teachers, schools)

    Analysis: {dictionary['education_analysis']}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    dictionary["recommendations"] = f"✅ EXCELLENT EDUCATION QUALITY\n\n{response.content.strip()}"
    return dictionary

def generate_learning_plan(dictionary):
    prompt = f"""
    Based on the education analysis and recommendations, create a learning plan for tomorrow:
    
    - Morning: (topics, duration)
    - Afternoon: (activities, tools)
    - Evening: (review, parent/teacher suggestions)
    
    Use personalized strategies wherever possible.

    Analysis: {dictionary['education_analysis']}
    Recommendations: {dictionary['recommendations']}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    dictionary["learning_plan"] = response.content.strip()
    return dictionary

# 👇 Wrapper function to be called from Flask
def run_education_agent(user_input):
    # Step 1: Build the graph
    builder = StateGraph(dict)
    builder.set_entry_point("get_education_input")
    builder.add_node("get_education_input", get_education_input)
    builder.add_node("analyze_education_data", analyze_education_data)
    builder.add_node("classify_learning_quality", classify_learning_quality)
    builder.add_node("needs_improvement", improvement_recommendations)
    builder.add_node("adequate", adequate_recommendations)
    builder.add_node("excellent", excellence_recommendations)
    builder.add_node("learning_plan", generate_learning_plan)

    builder.add_edge("get_education_input", "analyze_education_data")
    builder.add_edge("analyze_education_data", "classify_learning_quality")
    builder.add_conditional_edges("classify_learning_quality", education_router, {
        "needs_improvement": "needs_improvement",
        "adequate": "adequate",
        "excellent": "excellent"
    })

    builder.add_edge("needs_improvement", "learning_plan")
    builder.add_edge("adequate", "learning_plan")
    builder.add_edge("excellent", "learning_plan")
    builder.add_edge("learning_plan", END)

    # Step 2: Run the graph
    graph = builder.compile()
    final_state = graph.invoke({"education_input": user_input})

    return final_state["recommendations"], final_state["learning_plan"]


