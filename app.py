import os
import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration & Aesthetic Setup
st.set_page_config(page_title="Agentic Buyer Demo", layout="wide")
st.title("Agentic Buyer Demo")
st.markdown("---")

# 2. Sidebar: Authentication & Environmental Control
api_key_input = st.sidebar.text_input("Gemini API Key", type="password", value=os.environ.get("GEMINI_API_KEY", ""))

if not api_key_input:
    st.sidebar.warning("Please enter your Gemini API Key to run the simulation.")
    st.stop()

# Initialize the modern Google GenAI Client
client = genai.Client(api_key=api_key_input)

# 3. UI Layout: Two-Column Control Panel
col1, col2 = st.columns(2)

with col1:
    st.header("Product Description")
    industry = st.text_input("Industry", "Luxury Horology & High-End Timepieces")
    choice_a = st.text_input("Product A", "Audemars Piguet Royal Oak")
    choice_b = st.text_input("Product B", "Vacheron Constantin Overseas")

with col2:
    st.header("Agentic Buyers")
    st.markdown("Describe your three agentic buyers.")
    
    # Pre-populate with your brilliant luxury watch personas
    agent_1_name = st.text_input("Agent 1 Name", "The Clout Chaser")
    agent_1_prompt = st.text_area("Agent 1 Core Psychology", 
        "You are obsessed with external validation, social hierarchy, and hype culture. You buy things strictly so people recognize the brand from across the room and know how rich you are. You care about aftermarket value and Instagram prestige over historical watchmaking craftsmanship.", height=70)
    
    agent_2_name = st.text_input("Agent 2 Name", "The Family Man")
    agent_2_prompt = st.text_area("Agent 2 Core Psychology", 
        "You value multi-generational legacy, understatement, durability, and versatility. You want an asset that can survive daily life with children, looks respectable at a parent-teacher association meeting, and can be passed down to your kids as a definitive heirloom without shouting for attention.", height=70)
    
    agent_3_name = st.text_input("Agent 3 Name", "The Yuppie")
    agent_3_prompt = st.text_area("Agent 3 Core Psychology", 
        "You are a young, upwardly mobile corporate professional. You care deeply about engineering excellence, mechanical movement specifications, horological history, and showing your peers that you are 'intellectual' and 'discerning' rather than just a victim of modern fashion trends.", height=70)

# Build the internal runtime data dictionary
PERSONAS = {
    agent_1_name: agent_1_prompt,
    agent_2_name: agent_2_prompt,
    agent_3_name: agent_3_prompt
}

st.markdown("---")

# 4. Simulation Execution Layer
if st.button("Query Agents", type="primary"):
    st.header("Outputs")
    
    # Create interactive display tabs for each agent's output
    tabs = st.tabs(list(PERSONAS.keys()))
    
    for index, (name, prompt) in enumerate(PERSONAS.items()):
        with tabs[index]:
            st.subheader(f"Response: {name}")
            
            # System instruction assembly using the new SDK configuration framework
            system_instruction = f"{prompt} Do not break character. Do not state you are an AI. Speak directly from your worldview."
            
            user_prompt = f"""
            You are evaluating two specific options in the context of the {industry} market:
            1. {choice_a}
            2. {choice_b}

            Based strictly on your core psychological traits, biases, and values, which option do you personally prefer and recommend? 
            Provide a short five-point explanation, including:
            - The specific brand proof points that appeal directly to you.
            - The structural flaws or psychological alignment failures of the opposing option.
            
            Be authentic, subjective, and fiercely opinionated, but above all be brief.
            """
            
            with st.spinner(f"Querying {name}..."):
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=user_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.4
                        )
                    )
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Execution Failure on {name}: {str(e)}")
