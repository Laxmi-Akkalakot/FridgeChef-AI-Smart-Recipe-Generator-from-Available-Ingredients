from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_recipe(ingredients, diet_type="any"):
    diet_note = f"The recipe must be {diet_type}." if diet_type != "any" else ""

    prompt = f"""
    I have these ingredients in my fridge: {', '.join(ingredients)}.
    {diet_note}

    Give me a creative recipe with exactly this format:

    RECIPE NAME: <name here>

    INGREDIENTS NEEDED:
    - ingredient 1
    - ingredient 2

    STEP-BY-STEP INSTRUCTIONS:
    Step 1: ...
    Step 2: ...
    Step 3: ...

    COOKING TIME: <time>
    DIFFICULTY: <Easy/Medium/Hard>
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )

    return response.choices[0].message.content
def get_nutrition(ingredients, recipe_text):
    prompt = f"""
    Based on this recipe using ingredients: {ingredients}
    
    Recipe: {recipe_text[:500]}
    
    Give estimated nutrition per serving in EXACTLY this format, numbers only:
    CALORIES: <number>
    PROTEIN: <number>g
    CARBS: <number>g
    FAT: <number>g
    FIBER: <number>g
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    
    return response.choices[0].message.content