from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

# Load your API key from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Set up Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash-latest",
    temperature=0.2,
    google_api_key=api_key
)

# Core LangGraph Functions

def get_food_intake(dictionary):
    """This will be filled by Flask form."""
    return dictionary

def analyze_nutrition(dictionary):
    prompt = f"""
    You are an expert nutritionist. Analyze the following food intake and provide:
    1. Estimated total calories
    2. Macronutrient breakdown (protein, carbs, fats in grams)
    3. Key vitamins and minerals present
    4. Overall nutritional quality assessment
    
    Food intake: {dictionary['food_intake']}
    
    Provide your analysis in a structured format with specific numbers where possible.
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    dictionary["nutrition_analysis"] = response.content.strip()
    return dictionary

def identify_gaps(dictionary):
    prompt = f"""
    Based on this nutritional analysis, identify the main nutritional gaps or concerns and categorize as one of the following:
    - "deficient"
    - "balanced"
    - "excessive"
    
    Analysis: {dictionary['nutrition_analysis']}
    
    Respond with only one word: deficient, balanced, or excessive
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    category = response.content.strip().lower()
    dictionary["nutrition_category"] = category
    return dictionary

def nutrition_router(dictionary):
    cat = dictionary["nutrition_category"]
    if "deficient" in cat:
        return "deficient"
    elif "balanced" in cat:
        return "balanced"
    elif "excessive" in cat:
        return "excessive"
    else:
        return "balanced"

def deficient_recommendations(dictionary):
    prompt = f"""
    Based on this nutritional analysis showing deficiencies, provide specific recommendations:
    1. List 5-7 specific foods to add to the diet
    2. Suggest meal ideas for tomorrow
    3. Highlight critical nutrients that need attention
    4. Provide portion size guidance

    Analysis: {dictionary['nutrition_analysis']}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    dictionary["recommendations"] = f"🔴 NUTRITIONAL DEFICIENCIES DETECTED\n\n{response.content.strip()}"
    return dictionary

def balanced_recommendations(dictionary):
    prompt = f"""
    Based on this well-balanced nutritional intake, provide maintenance recommendations:
    1. Suggest 3-4 foods to maintain variety
    2. Recommend one optimization for tomorrow
    3. Highlight what they're doing well
    4. Suggest any minor improvements

    Analysis: {dictionary['nutrition_analysis']}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    dictionary["recommendations"] = f"✅ WELL-BALANCED NUTRITION\n\n{response.content.strip()}"
    return dictionary

def excessive_recommendations(dictionary):
    prompt = f"""
    Based on this nutritional analysis showing excessive intake, provide balancing recommendations:
    1. Suggest 5-6 foods to reduce or replace
    2. Recommend lighter meal options for tomorrow
    3. Highlight areas of concern (calories, sugar, sodium, etc.)
    4. Provide portion control tips

    Analysis: {dictionary['nutrition_analysis']}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    dictionary["recommendations"] = f"🟡 EXCESSIVE INTAKE DETECTED\n\n{response.content.strip()}"
    return dictionary

def generate_meal_plan(dictionary):
    prompt = f"""
    Based on the nutritional analysis and recommendations, create a simple meal plan for tomorrow:

    Breakfast: (one option)
    Lunch: (one option)  
    Dinner: (one option)
    Snacks: (1-2 healthy options)

    Current analysis: {dictionary['nutrition_analysis']}
    Recommendations: {dictionary['recommendations']}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    dictionary["meal_plan"] = response.content.strip()
    return dictionary

# 👇 Wrapper function to be called from Flask
def run_nutrition_agent(food_input):
    # Step 1: Build graph
    builder = StateGraph(dict)
    builder.set_entry_point("get_food_intake")
    builder.add_node("get_food_intake", get_food_intake)
    builder.add_node("analyze_nutrition", analyze_nutrition)
    builder.add_node("identify_gaps", identify_gaps)
    builder.add_node("deficient", deficient_recommendations)
    builder.add_node("balanced", balanced_recommendations)
    builder.add_node("excessive", excessive_recommendations)
    builder.add_node("meal_plan", generate_meal_plan)

    builder.add_edge("get_food_intake", "analyze_nutrition")
    builder.add_edge("analyze_nutrition", "identify_gaps")
    builder.add_conditional_edges("identify_gaps", nutrition_router, {
        "deficient": "deficient",
        "balanced": "balanced",
        "excessive": "excessive"
    })

    builder.add_edge("deficient", "meal_plan")
    builder.add_edge("balanced", "meal_plan")
    builder.add_edge("excessive", "meal_plan")
    builder.add_edge("meal_plan", END)

    # Step 2: Run the graph
    graph = builder.compile()
    final_state = graph.invoke({"food_intake": food_input})

    return final_state["recommendations"], final_state["meal_plan"]
