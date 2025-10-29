# Troubleshooting Guide

## Common Issues and Solutions

### API Key Issues

#### Problem: `AuthenticationError: Invalid API key`
**Symptoms:**
```
openai.AuthenticationError: Invalid API key provided
```

**Solutions:**
1. Check `.env` file exists and has correct format:
```bash
OPENAI_API_KEY=sk-proj-...
OPENROUTER_API_KEY=sk-or-...
```

2. Verify environment is loaded:
```python
from dotenv import load_dotenv
load_dotenv()  # Must be called before using os.getenv()
```

3. Check API key is valid on provider dashboard
4. Ensure no extra spaces or quotes around keys in `.env`

#### Problem: `OPENAI_API_KEY not found in environment variables`
**Solution:**
```bash
# Check if .env file exists
ls -la .env

# If not, copy from example
cp .env.example .env

# Edit with your actual keys
nano .env
```

---

### ChromaDB Issues

#### Problem: `Collection not found`
**Symptoms:**
```
ValueError: Collection 'products' does not exist
```

**Solutions:**
1. Run setup script first:
```bash
python setup.py
```

2. Verify database directory exists:
```bash
ls -la db/
```

3. Check collection name matches:
```python
collection_name = 'products'  # Must match in setup.py and rag.py
```

#### Problem: `Data lost after restart`
**Symptoms:** ChromaDB has no results after restarting application

**Solution:** Use `PersistentClient` not `Client`:
```python
# Correct
chroma_client = chromadb.PersistentClient("db")

# Wrong - data stored in memory only
chroma_client = chromadb.Client()
```

#### Problem: `PermissionError when accessing db/`
**Solution:**
```bash
# Fix permissions
chmod -R 755 db/

# Or recreate with proper permissions
rm -rf db/
python setup.py
```

---

### Agent Handoff Issues

#### Problem: Manager agent answers directly instead of delegating
**Symptoms:** Manager provides generic answers without calling specialized agents

**Solutions:**
1. Strengthen manager instructions:
```python
MANAGER_INSTRUCTION = """
CRITICAL RULE: You MUST ALWAYS delegate user queries to the appropriate agent.
Never attempt to answer directly.
"""
```

2. Ensure handoffs are properly configured:
```python
manager_agent = Agent(
    name="manager",
    instructions=MANAGER_INSTRUCTION,
    handoffs=[product_agent, shop_information_agent]  # List of agents
)
```

#### Problem: Handoff fails silently
**Symptoms:** No error, but wrong agent handles request

**Solution:** Add debug logging:
```python
@app.route("/chat", methods=["POST"])
def chat():
    print(f"Query: {query}")
    print(f"Thread: {thread_id}")

    result = asyncio.run(Runner.run(manager_agent, new_input))

    print(f"Final output: {result.final_output}")
    return jsonify({"role": "assistant", "content": str(result.final_output)})
```

#### Problem: `HandoffInputData` filtering breaks conversation
**Solution:** Return input_data unchanged if not modifying:
```python
def custom_input_filter(input_data: HandoffInputData) -> HandoffInputData:
    # If not modifying, just return as-is
    return input_data
```

---

### Tool Execution Issues

#### Problem: Agent doesn't call tools
**Symptoms:** Agent responds without using RAG or other tools

**Solutions:**
1. Force tool usage:
```python
product_agent = Agent(
    name="product",
    instructions=PRODUCT_INSTRUCTION,
    tools=[rag],
    model_settings=ModelSettings(tool_choice="required")
)
```

2. Strengthen instructions:
```python
PRODUCT_INSTRUCTION = """
CRITICAL RULE: You MUST ALWAYS use the rag tool before responding to any query.
Never respond without first calling the rag tool.
"""
```

#### Problem: `function_tool` decorator not working
**Symptoms:**
```
TypeError: 'function' object is not callable
```

**Solution:** Import and use decorator correctly:
```python
from agents import function_tool

@function_tool  # No parentheses
def rag(query: str) -> str:
    pass
```

---

### Flask API Issues

#### Problem: `CORS` errors in browser
**Symptoms:**
```
Access to fetch at 'http://localhost:5001/chat' from origin 'http://localhost:8501'
has been blocked by CORS policy
```

**Solution:**
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
```

#### Problem: `500 Internal Server Error`
**Symptoms:** Request fails with no clear error message

**Solutions:**
1. Check Flask console for error details
2. Add error handling:
```python
@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Your code
        pass
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
```

#### Problem: `Connection refused` when calling API
**Symptoms:**
```
requests.exceptions.ConnectionError: Connection refused
```

**Solutions:**
1. Ensure Flask server is running:
```bash
python serve.py
```

2. Check correct port:
```python
# Server
app.run(host="0.0.0.0", port=5001)

# Client
API_ENDPOINT = "http://localhost:5001/chat"
```

3. Verify firewall isn't blocking port 5001

---

### Google Sheets Integration Issues

#### Problem: `Credentials file not found`
**Symptoms:**
```
FileNotFoundError: mles-class-12c1216b7303.json
```

**Solutions:**
1. Download service account JSON from Google Cloud Console
2. Place in project root directory
3. Update filename in code:
```python
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'your-credentials-file.json',  # Update this
    scope
)
```

#### Problem: `Permission denied` accessing Google Sheets
**Solutions:**
1. Share sheet with service account email:
   - Open Google Sheet
   - Click "Share"
   - Add service account email (found in JSON file)
   - Grant "Editor" permissions

2. Verify sheet URL is correct:
```python
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID').sheet1
```

#### Problem: `APIError: Quota exceeded`
**Solution:** Google Sheets API has rate limits:
```python
import time

def shop_information_rag():
    try:
        data = sheet.get_all_records()
        return data
    except gspread.exceptions.APIError as e:
        if 'Quota exceeded' in str(e):
            time.sleep(60)  # Wait and retry
            return shop_information_rag()
        raise
```

---

### Streamlit UI Issues

#### Problem: `ModuleNotFoundError: No module named 'streamlit'`
**Solution:**
```bash
pip install streamlit
```

#### Problem: Session state not persisting
**Solution:** Initialize properly:
```python
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
```

#### Problem: `experimental_rerun` deprecated warning
**Solution:** Use new method:
```python
# Old
st.experimental_rerun()

# New
st.rerun()
```

#### Problem: UI not updating after sending message
**Solution:** Ensure form clears and rerenders:
```python
with st.form(key="chat_form", clear_on_submit=True):
    st.text_input("Your message:", key="user_input")
    st.form_submit_button("Send", on_click=send_message)
```

---

### Embedding Issues

#### Problem: `Invalid dimensions` for embeddings
**Symptoms:**
```
ValueError: Embedding dimension mismatch
```

**Solutions:**
1. Ensure consistent model:
```python
# Always use same model for embedding
def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"  # Don't change mid-project
    )
    return response.data[0].embedding
```

2. If changing models, recreate ChromaDB collection:
```bash
rm -rf db/
python setup.py  # Regenerate with new model
```

#### Problem: Poor search results
**Solutions:**
1. Improve document preprocessing:
```python
# Clean text before embedding
text = text.replace("<br>", " ").replace("\n", " ")
text = " ".join(text.split())  # Normalize whitespace
```

2. Normalize embeddings for cosine similarity:
```python
import numpy as np

query_embedding = get_embedding(query)
query_embedding = query_embedding / np.linalg.norm(query_embedding)
```

3. Adjust number of results:
```python
results = collection.query(
    query_embeddings=query_embedding,
    n_results=5  # Increase from 3
)
```

---

### OpenRouter / LiteLLM Issues

#### Problem: `Model not found` with OpenRouter
**Solution:** Check model name format:
```python
# Correct format for OpenRouter
model = LitellmModel(
    model="openrouter/provider/model-name",
    api_key=openrouter_key
)

# Examples:
# "openrouter/anthropic/claude-3-sonnet"
# "openrouter/openai/gpt-4"
```

#### Problem: `API key invalid` for alternative providers
**Solutions:**
1. Check `.env` has correct keys:
```bash
OPENROUTER_API_KEY=sk-or-v1-...
```

2. Verify key on provider dashboard

3. Pass key explicitly if needed:
```python
model = LitellmModel(
    model="openrouter/anthropic/claude-3-sonnet",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
```

---

### Data Processing Issues

#### Problem: `ast.literal_eval` fails on color_options
**Symptoms:**
```
ValueError: malformed node or string
```

**Solution:** Handle invalid data:
```python
import ast

try:
    colors = ast.literal_eval(row['color_options'])
except (ValueError, SyntaxError):
    colors = []  # Default to empty list
```

#### Problem: CSV encoding errors
**Symptoms:**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte
```

**Solution:**
```python
df = pd.read_csv("./hoanghamobile.csv", encoding='utf-8-sig')
# Or try: encoding='latin-1' if utf-8 fails
```

---

### Async/Await Issues

#### Problem: `asyncio.run() cannot be called from running event loop`
**Symptoms:** Error when running in Jupyter or async context

**Solution:**
```python
# In sync context (Flask)
result = asyncio.run(Runner.run(manager_agent, new_input))

# In async context (Jupyter, async functions)
result = await Runner.run(manager_agent, new_input)
```

---

### Debugging Tips

#### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Print Agent Trace
```python
with trace(workflow_name="Debug", group_id="test"):
    result = asyncio.run(Runner.run(manager_agent, new_input))
    print(result)  # Includes full trace
```

#### Check ChromaDB Contents
```python
collection = chroma_client.get_collection(name="products")
print(f"Collection count: {collection.count()}")

# Get sample
results = collection.get(limit=5)
print(results)
```

#### Test Embedding Generation
```python
text = "Nokia 3210 4G"
embedding = get_embedding(text)
print(f"Embedding length: {len(embedding)}")
print(f"First 5 values: {embedding[:5]}")
```

#### Test API Directly
```bash
# Test with curl
curl -X POST "http://localhost:5001/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "test", "thread_id": "debug-1"}' \
     -v  # Verbose mode for debugging
```

---

## Getting Help

If you're still stuck after trying these solutions:

1. **Check Error Messages:** Read the full error traceback
2. **Search Issues:** Look for similar problems in project issues
3. **Minimal Example:** Create minimal reproducible example
4. **Ask for Help:** Include:
   - Error message (full traceback)
   - Code snippet
   - What you've tried
   - Python version and OS

### Useful Commands

```bash
# Check Python version
python --version

# List installed packages
pip list

# Check if services are running
ps aux | grep python

# Check port usage
lsof -i :5001

# Recreate environment
rm -rf venv/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
