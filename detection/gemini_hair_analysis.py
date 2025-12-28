# # haircare/gemini_hair_analysis.py
# import google.generativeai as genai
# from django.conf import settings

# genai.configure(api_key=settings.GEMINI_API_KEY)

# # Use latest fast & smart model
# MODEL_NAME = "gemini-2.5-flash"  # or "gemini-1.5-pro" if you want better quality

# def analyze_hair_loss(symptoms: list[str]) -> str:
#     """
#     Takes list of selected symptoms and returns full AI analysis
#     """
#     symptoms_text = ", ".join(symptoms[:-1]) + f" and {symptoms[-1]}" if len(symptoms) > 1 else symptoms[0]

#     prompt = f"""
#     You are Dr. HairExpert, a world-class trichologist and hair loss specialist.
#     The user has selected these symptoms: {symptoms_text}.

#     Give a complete, caring, and professional response in this exact structure (use markdown):

#     ### Possible Causes
#     - Cause 1 with brief explanation
#     - Cause 2...
#     (Most likely first)

#     ### Recommended Treatments
#     - Medical options (minoxidil, finasteride, PRP, etc. when relevant)
#     - Natural/home remedies
#     - Lifestyle changes

#     ### Daily Hair Care Routine
#     Step-by-step gentle routine suitable for their condition

#     ### Product Suggestions (2025)
#     Suggest 3–5 real, currently popular products available in India/global (with short reason)
#     reason)
#     Example:
#     - Minimalist 5% Minoxidil → clinically proven, non-greasy
#     - Mamaearth Onion Shampoo → reduces fall, sulfate-free

#     ### When to See a Dermatologist
#     Red flags and advice

#     Keep tone empathetic, encouraging, and expert. Never scare the user.
#     Write in simple English/hinglish if needed, max 400 words.
#     """

#     model = genai.GenerativeModel(
#         MODEL_NAME,
#         system_instruction="You are a friendly Indian trichologist speaking to worried patients about hair loss."
#     )

#     response = model.generate_content(prompt)
#     return response.text.strip()


# haircare/gemini_hair_analysis.py

def analyze_hair_loss(symptoms: list[str]) -> dict:
    """
    Returns a single dict with cause, treatment, and suggestion based on selected symptoms
    """
    # Combine symptoms to generate a dummy analysis
    cause_list = []
    treatment_list = []
    suggestion_list = []

    for symptom in symptoms:
        if symptom == "Dandruff":
            cause_list.append("Fungal infection or dry scalp")
            treatment_list.append("Use anti-dandruff shampoo (zinc pyrithione/ketoconazole)")
            suggestion_list.append("Avoid scratching and maintain scalp hygiene")
        elif symptom == "Hair Thinning":
            cause_list.append("Genetics, stress, or poor nutrition")
            treatment_list.append("Topical minoxidil, protein-rich diet, stress management")
            suggestion_list.append("Avoid tight hairstyles and harsh chemicals")
        elif symptom == "Oily Scalp":
            cause_list.append("Overactive sebaceous glands or hormonal changes")
            treatment_list.append("Wash hair 2–3 times/week, avoid heavy oils")
            suggestion_list.append("Avoid greasy foods, maintain regular scalp cleaning")
        else:
            cause_list.append("Unknown symptom")
            treatment_list.append("Consult a dermatologist")
            suggestion_list.append("Follow gentle hair care routine")

    return {
        "cause": "; ".join(cause_list),
        "treatment": "; ".join(treatment_list),
        "suggestion": "; ".join(suggestion_list)
    }
