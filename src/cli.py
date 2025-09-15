import sys
import json

def main():
    # Ensure Unicode characters like 🔥 print correctly
    sys.stdout.reconfigure(encoding='utf-8')

    response = {
        "status": "success",
        "message": "🔥 VertexAutoGPT CLI is alive! 🔥",
        "python_executable": sys.executable,
        "version_info": sys.version
    }

    # ✅ Ensure proper JSON output
    print(json.dumps(response, ensure_ascii=False))

if __name__ == "__main__":
    main()
