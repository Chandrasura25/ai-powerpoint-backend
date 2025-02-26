
## **Backend README.md**

```markdown
# AI-Powered PowerPoint Generator - Backend

This is the backend for the AI-Powered PowerPoint Generator. It is built using Python, FastAPI, and the `python-pptx` library. The backend accepts user input, generates a PowerPoint presentation using OpenAI, and returns the `.pptx` file for download.

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/ai-powerpoint-backend.git
   cd ai-powerpoint-backend
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up OpenAI API key**:
   - Create a `.env` file in the root directory:
     ```env
     OPENAI_API_KEY=your-openai-api-key
     ```
   - Replace `your-openai-api-key` with your actual OpenAI API key.

## Running the Backend

1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

2. The backend will be available at `http://localhost:8000`.

## API Endpoints

- **POST `/api/slide/generate-presentation`**:
  - Accepts JSON input:
    ```json
    {
      "topic": "Your Topic",
      "num_slides": 5,
      "layout": "Varied"
    }
    ```
  - Returns a `.pptx` file for download.

## Example Request

```bash
curl -X POST "http://localhost:8000/api/slide/generate-presentation" \
-H "Content-Type: application/json" \
-d '{"topic": "Future of AI", "num_slides": 5, "layout": "Varied"}'
```

## Dependencies

- `fastapi`
- `python-pptx`
- `openai`
- `uvicorn`
- `python-dotenv`

---

## License

This project is licensed under the MIT License.
```