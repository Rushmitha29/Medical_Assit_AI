# 🌍 EcoSort AI 
> **AI Powered • Eco Focused • Future Ready**

EcoSort AI is an intelligent, multi-lingual waste segregation assistant built to promote a cleaner Earth through smart waste management. Utilizing deep learning image classification, the application automatically scans waste items, evaluates their environmental impact, delivers precise disposal recommendations, and displays real-time data metrics via an analytical dashboard.

---

## ⚡ Core Features

* **🔬 Real-Time Waste Analysis:** Upload images or leverage a live webcam feed to instantly classify waste categories (Plastic, Paper, Glass, Metal, Cardboard, and General Trash).
* **🌐 Trilingual Interface:** Fully localized UI and audio output supporting **English**, **Telugu (తెలుగు)**, and **Hindi (हिंदी)**, automatically updating all dashboard labels and contextual information upon language selection.
* **🔊 Voice AI Integration:** Built-in Browser Speech Synthesis (TTS) that automatically reads out detection results, confidence scores, and eco-friendly disposal methods in the selected language.
* **📊 Analytics Dashboard:** A futuristic, dark-mode analytical suite featuring:
    * 🍩 **Confidence Breakdown:** A Matplotlib-generated donut chart displaying classification probabilities.
    * 🌱 **Eco Score Gauge:** A dynamic environmental safety meter that scales based on item metrics and model confidence.
    * 📈 **Scan History Distribution:** A real-time tracking bar graph reflecting localized waste distribution trends.
* **🌱 Eco-Educational Guide:** A dedicated modular reference deck detailing decomposition timelines, bin colors, and high/low pollution risk indicators.

---

## ⚙️ Tech Stack

* **Frontend UI:** [Gradio](https://github.com/gradio-app/gradio) (Custom stylized dark UI matching an obsidian-emerald aesthetic)
* **Machine Learning Pipeline:** [Hugging Face Transformers](https://github.com/huggingface/transformers)
* **Core Model:** `yangy50/garbage-classification` (ViT/Image Classification Pipeline)
* **Deep Learning Frameworks:** PyTorch & Torchvision
* **Data Visualization:** Matplotlib & NumPy
* **Image Processing:** Pillow (PIL)

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.8+ installed along with `pip`.

### 2. Installation
Clone the repository and install the required packages:
```bash
git clone [https://github.com/Rushmitha29/Eco_Sort_AI.git](https://github.com/Rushmitha29/Eco_Sort_AI.git)
cd Eco_Sort_AI
pip install gradio transformers pillow matplotlib torch torchvision
