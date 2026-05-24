import os
import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration & Aesthetic Setup
st.set_page_config(page_title="Agentic Buyer Demo", layout="wide")
st.title("Agentic Buyer Demo")
st.markdown("---")

# 2. Sidebar: Authentication & Environmental Control
api_key_input = st.sidebar.text_input("API Key (Optional)", type="password", value=os.environ.get("GEMINI_API_KEY", ""))

if api_key_input:
    st.sidebar.success("Live mode activated")
    client = genai.Client(api_key=api_key_input)
    is_demo_mode = False
else:
    st.sidebar.warning("Live mode inactive")
    is_demo_mode = True

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

BAKED_RESPONSES = {
    "The Clout Chaser": """
    ### 🏆 Recommendation: Audemars Piguet Royal Oak
    
    **Why I choose this:** The Royal Oak is an absolute cultural monolith. From across a dimly lit room in Miami or a restaurant in SF, *everyone* recognizes the octagonal bezel and the tapisserie dial. It screams liquidity and cultural relevance. Jay-Z talks about it. It has the hype premium.
    
    **Flaws of the VC Overseas:** The Vacheron Constantin Overseas is a beautiful 'if you know, you know' watch, but that's exactly the problem—*not enough people know.* If I'm spending $30k+, I don't want to explain horological history to someone; I want them to look at my wrist and instantly know where I sit on the social ladder. The Overseas is too quiet.
    """,
    
    "The Family Man": """
    ### 👨‍👩‍👧‍👦 Recommendation: Vacheron Constantin Overseas
    
    **Why I choose this:** The Overseas is the ultimate elegant daily driver. It features an incredible quick-change bracelet system (swapping from steel to rubber to alligator leather in 5 seconds), meaning I can wear it to the beach with the kids and then straight to a formal dinner. It’s Holy Trinity watchmaking without the obnoxious 'look at me' vanity. It represents quiet, generational wealth that I will happily pass down to my son.
    
    **Flaws of the Royal Oak:** The Royal Oak has become a magnet for crypto flippers, influencers, and aggressive modern clout. It’s an scratch-magnet that flashes too brightly under a cuff. It paints a target on your back and lacks the understated dignity required for everyday family life.
    """,
    
    "The Yuppie": """
    ### 📈 Recommendation: Vacheron Constantin Overseas (Ref. 4500V)
    
    **Why I choose this:** From a pure horological perspective, the in-house Calibre 5100 movement with the Hallmark of Geneva finishing completely out-classes modern mass-produced AP movements. The Maltese cross integration into the bezel and bracelet links shows highly disciplined, geometric industrial design. It signals that I understand independent execution and mechanical heritage.
    
    **Flaws of the Royal Oak:** The Royal Oak is a victim of its own success. It hasn't fundamentally changed its cognitive footprint since Gérald Genta designed it in 1972, and the market is saturated with people who bought it purely because of an Instagram algorithm. It lacks intellectual differentiation.
    """
}

st.markdown("---")

st.markdown("---")

# 4. Simulation Execution Layer
if st.button("Query Agents", type="primary"):
    st.header("Outputs")
    
    # Create interactive display tabs for each agent's output
    tabs = st.tabs(list(PERSONAS.keys()))
    
    for index, (name, prompt) in enumerate(PERSONAS.items()):
        with tabs[index]:
            st.subheader(f"Response: {name}")
            
            if is_demo_mode:
                with st.spinner("Fetching pre-computed responses..."):
                    fallback_text = f"### 🔵 Sandbox Mode Active\nTo analyze a customized run for **{choice_a}** vs **{choice_b}**, please enter a live Gemini API Key in the sidebar. In Sandbox mode, we showcase the default pre-baked evaluation architecture."
                    output_text = BAKED_RESPONSES.get(name, fallback_text)
                    st.markdown(output_text)
            else: 
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
