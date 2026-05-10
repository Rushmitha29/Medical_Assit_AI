
# =========================================================
# MEDASSIST PRO MAX
# Advanced Doctor AI Assistant
# Google Colab + Gemini + Gradio
# =========================================================

!pip install -q gradio google-genai pillow

import gradio as gr
from google import genai
from PIL import Image
import tempfile
import os

# =========================================================
# GEMINI API
# =========================================================

API_KEY = "YOUR_API_KEY"

client = genai.Client(api_key='YOUR_API_KEY')

# =========================================================
# AI SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are MedAssist Pro AI.

You are designed ONLY for medical doctors and healthcare professionals.

Your job:
- Analyze clinical questions
- Interpret uploaded medical images
- Generate concise medical insights
- Help in diagnosis support
- Provide structured outputs

VERY IMPORTANT RESPONSE RULES:

DO NOT generate overly descriptive responses.

KEEP RESPONSES SHORT, CLEAR, STRUCTURED, AND CLINICAL.

ALWAYS FOLLOW THIS FORMAT:

================================================
🩺 CLINICAL SUMMARY
- Short summary in 2-3 lines

🔍 KEY FINDINGS
- Bullet points only

⚠ POSSIBLE CONDITIONS
- Top likely differentials only

🧪 RECOMMENDED TESTS
- Only essential tests

💊 SUGGESTED NEXT STEP
- Short actionable recommendation

🚨 RED FLAGS
- Mention emergency concerns only if present
================================================

Rules:
- Avoid paragraphs
- Avoid unnecessary explanation
- Use bullet points
- Maximum concise output
- Professional tone
- Mention uncertainty if needed
"""

# =========================================================
# MAIN FUNCTION
# =========================================================

def med_assistant(
    image,
    question,
    specialty,
    response_mode,
    urgency,
    output_style
):

    try:

        contents = [SYSTEM_PROMPT]

        clinical_context = f"""
Specialty: {specialty}

Urgency Level: {urgency}

Response Style: {output_style}

Response Mode:
{response_mode}
"""

        contents.append(clinical_context)

        # Upload image if exists
        if image is not None:

            temp = tempfile.NamedTemporaryFile(
                suffix=".png",
                delete=False
            )

            image.save(temp.name)

            uploaded_file = client.files.upload(file=temp.name)

            contents.append(uploaded_file)

        contents.append(question)

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=contents
        )

        return response.text

    except Exception as e:
        return f"❌ Error: {str(e)}"

# =========================================================
# QUICK PROMPTS
# =========================================================

quick_prompts = {
    "Chest X-Ray Analysis":
    "Analyze this chest X-ray and provide concise findings.",

    "ECG Interpretation":
    "Interpret this ECG and identify abnormalities.",

    "Differential Diagnosis":
    "Provide likely differential diagnoses.",

    "MRI Review":
    "Summarize MRI findings briefly.",

    "Lab Report Summary":
    "Summarize abnormal lab findings.",

    "Emergency Triage":
    "Identify emergency red flags and urgency.",

    "Prescription Analysis":
    "Extract medications and explain briefly."
}

# =========================================================
# LOAD QUICK PROMPT
# =========================================================

def load_prompt(choice):
    return quick_prompts.get(choice, "")

# =========================================================
# CUSTOM CSS
# =========================================================

custom_css = """
body {
    background: #0b1220;
}

.gradio-container {
    font-family: 'Segoe UI';
}

.main-title {
    text-align:center;
    color:white;
    padding:20px;
}

.section-card {
    background:#111827;
    border-radius:18px;
    padding:15px;
    border:1px solid #374151;
}

.output-box textarea {
    font-size:16px !important;
    line-height:1.6 !important;
    background:#0f172a !important;
    color:#00ffcc !important;
}

.footer {
    text-align:center;
    color:gray;
    margin-top:20px;
}
"""

# =========================================================
# UI
# =========================================================

with gr.Blocks(
    theme=gr.themes.Base(
        primary_hue="blue",
        secondary_hue="cyan",
        neutral_hue="slate"
    ),
    css=custom_css,
    title="MedAssist Pro Max"
) as demo:

    # =====================================================
    # HEADER
    # =====================================================

    gr.HTML("""
    <div class="main-title">
        <h1>🩺 MedAssist Pro Max</h1>
        <h3>Advanced AI Assistant for Medical Professionals</h3>
        <p>Radiology • Diagnosis • Clinical AI • Emergency Support</p>
    </div>
    """)

    # =====================================================
    # MAIN LAYOUT
    # =====================================================

    with gr.Row():

        # =================================================
        # LEFT PANEL
        # =================================================

        with gr.Column(scale=1):

            gr.Markdown("## 📥 Patient / Clinical Inputs")

            specialty = gr.Dropdown(
                choices=[
                    "General Medicine",
                    "Radiology",
                    "Cardiology",
                    "Neurology",
                    "Dermatology",
                    "Pulmonology",
                    "Orthopedics",
                    "Pediatrics",
                    "Emergency Medicine",
                    "Oncology",
                    "ICU/Critical Care"
                ],
                value="General Medicine",
                label="🏥 Specialty"
            )

            urgency = gr.Radio(
                choices=[
                    "Routine",
                    "Urgent",
                    "Emergency"
                ],
                value="Routine",
                label="🚨 Urgency Level"
            )

            output_style = gr.Dropdown(
                choices=[
                    "Concise Clinical",
                    "Bullet Summary",
                    "Diagnostic Focus",
                    "Emergency Focus",
                    "Treatment Focus"
                ],
                value="Concise Clinical",
                label="📋 Output Style"
            )

            response_mode = gr.CheckboxGroup(
                choices=[
                    "Differential Diagnosis",
                    "Treatment Suggestions",
                    "Lab Interpretation",
                    "Radiology Findings",
                    "Red Flag Detection",
                    "Clinical Summary"
                ],
                value=["Clinical Summary"],
                label="🧠 AI Tasks"
            )

            image_input = gr.Image(
                type="pil",
                label="🖼 Upload Medical Image"
            )

            quick_menu = gr.Dropdown(
                choices=list(quick_prompts.keys()),
                label="⚡ Quick Clinical Prompt"
            )

            question_input = gr.Textbox(
                label="❓ Clinical Question",
                lines=7,
                placeholder="""
Example:
- Analyze this CT scan
- Possible diagnosis?
- Explain abnormalities
- Is this emergency?
"""
            )

            quick_menu.change(
                fn=load_prompt,
                inputs=quick_menu,
                outputs=question_input
            )

            with gr.Row():

                analyze_btn = gr.Button(
                    "🚀 Analyze",
                    variant="primary"
                )

                clear_btn = gr.Button("🗑 Clear")

        # =================================================
        # RIGHT PANEL
        # =================================================

        with gr.Column(scale=2):

            gr.Markdown("## 🧠 AI Clinical Response")

            output_box = gr.Textbox(
                label="📋 Medical Analysis",
                lines=26,
                max_lines=40,
                elem_classes="output-box",
                show_copy_button=True
            )

            # =============================================
            # MINI DASHBOARD
            # =============================================

            with gr.Row():

                gr.Markdown("""
### ✅ Features
- X-Ray Analysis
- ECG Interpretation
- Differential Diagnosis
- Emergency Detection
""")

                gr.Markdown("""
### ⚡ AI Modes
- Concise Output
- Treatment Focus
- Bullet Summary
- Clinical Insights
""")

    # =====================================================
    # TABS
    # =====================================================

    with gr.Tabs():

        # =================================================
        # TAB 1
        # =================================================

        with gr.Tab("📚 Clinical Templates"):

            gr.Markdown("""
# Example Clinical Queries

## Radiology
- Analyze chest infiltrates
- Detect fractures
- Identify lung abnormalities

## Cardiology
- ECG interpretation
- Cardiac risk findings

## Neurology
- Stroke indicators
- MRI lesion review

## Emergency
- Triage severity
- Emergency warning signs
""")

        # =================================================
        # TAB 2
        # =================================================

        with gr.Tab("🧪 Lab Assistant"):

            gr.Markdown("""
# Supported Lab Analysis

✅ CBC  
✅ LFT  
✅ KFT  
✅ Thyroid Profile  
✅ ABG  
✅ Electrolytes  
✅ Cardiac Markers  
""")

        # =================================================
        # TAB 3
        # =================================================

        with gr.Tab("📈 Clinical Workflow"):

            gr.Markdown("""
# Suggested Workflow

1. Upload image/report
2. Select specialty
3. Choose urgency
4. Select AI task
5. Ask clinical question
6. Review concise AI output
""")

        # =================================================
        # TAB 4
        # =================================================

        with gr.Tab("⚠ Disclaimer"):

            gr.Markdown("""
# Medical Disclaimer

This system is ONLY for healthcare professionals.

- Not a replacement for clinical judgment
- Verify all AI outputs
- Use institutional guidelines
- Emergency decisions require physician review
""")

    # =====================================================
    # BUTTON EVENTS
    # =====================================================

    analyze_btn.click(
        fn=med_assistant,
        inputs=[
            image_input,
            question_input,
            specialty,
            response_mode,
            urgency,
            output_style
        ],
        outputs=output_box
    )

    clear_btn.click(
        fn=lambda: (
            None,
            "",
            "General Medicine",
            [],
            "Routine",
            "Concise Clinical",
            ""
        ),
        outputs=[
            image_input,
            question_input,
            specialty,
            response_mode,
            urgency,
            output_style,
            output_box
        ]
    )

    # =====================================================
    # FOOTER
    # =====================================================

    gr.HTML("""
    <div class="footer">
    🩺 MedAssist Pro Max © 2026 | Clinical AI Platform
    </div>
    """)

# =========================================================
# LAUNCH
# =========================================================

demo.launch(
    share=True,
    debug=True
)
\
