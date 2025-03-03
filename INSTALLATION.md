# 🚀 Installation Guide – AutoGPT  

Follow this guide to set up and run AutoGPT seamlessly.  

## 🔹 Prerequisites 
✅ **Python 3.8+**  
✅ **pip** (Latest Version)  
✅ **CUDA 11+** (For GPU acceleration)  
✅ **Docker** (For containerized deployment)  
✅ **Google Cloud Account** (For scalable AI deployment)  

## 🔧 Setup Instructions  

### 1️⃣ Clone the Repository  
```sh
git clone https://github.com/SaurabhCodesAI/AutoGPT.git
cd AutoGPT

2️⃣ Create a Virtual Environment
python3 -m venv env
source env/bin/activate  # (On Windows: env\Scripts\activate)

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run AutoGPT
python main.py

5️⃣ Docker Setup (Optional)
docker build -t autogpt .
docker run -p 8080:8080 autogpt

For further customization, refer to CONTRIBUTING.md.
