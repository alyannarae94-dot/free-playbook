import os
import requests

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def generate_ai_post():
    # Pinalitan ng gemini-pro para unibersal at walang 404 error
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    prompt_text = (
        "Write a high-converting, professional, and engaging Facebook page post for 'Nexus Automations PH'. "
        "Our core mission is: 'We build autonomous 24/7 AI Agents and custom workflows for businesses.' "
        "Focus on business automation, intelligent routing, lead capture engines, and scaling operations without increasing headcount. "
        "Every post must include a call-to-action (CTA) to get our Free AI Automation Playbook. "
        "Include engaging emojis, a clean paragraph structure, and professional industry hashtags. "
        "Do not use placeholders."
    )

    payload = {
        "contents": [{
            "parts": [{
                "text": prompt_text
            }]
        }]
    }
    
    response = requests.post(gemini_url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        post_content = data['candidates'][0]['content']['parts'][0]['text']
        return post_content
    else:
        raise Exception(f"Gemini API Error: {response.text}")

def save_to_supabase(content):
    supabase_url = f"{SUPABASE_URL}/rest/v1/posts"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    payload = {
        "content": content,
        "status": "pending"
    }
    response = requests.post(supabase_url, json=payload, headers=headers)
    if response.status_code in [200, 201]:
        print("Successfully saved targeted AI post to Supabase!")
    else:
        raise Exception(f"Supabase Error: {response.text}")

if __name__ == "__main__":
    post = generate_ai_post()
    save_to_supabase(post)
