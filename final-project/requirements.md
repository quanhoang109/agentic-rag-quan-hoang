# Final Project: Detailed Requirements

## Project Specifications

This document provides detailed technical specifications for your final project.

## Minimum Viable Product (MVP)

Your project must meet ALL of these minimum requirements:

### 1. Data Requirements

**Minimum Dataset Size:**
- At least 50 unique documents/entries
- Each entry should have meaningful content (not just titles)
- Data should be relevant to your chosen domain

**Data Format:**
- CSV, JSON, or structured text files
- Clean and well-formatted
- Include metadata when appropriate

**Data Quality:**
- No duplicate entries
- Properly encoded (UTF-8)
- Consistent formatting
- Cleaned of HTML/special characters

### 2. RAG Pipeline Requirements

**Embeddings:**
- Use OpenAI `text-embedding-3-small` or `text-embedding-3-large`
- Generate embeddings for all documents
- Store embeddings in ChromaDB

**Vector Database:**
- Use ChromaDB with PersistentClient
- Create appropriate collection(s)
- Store relevant metadata with embeddings
- Implement proper error handling

**Retrieval Function:**
- Accept query as input
- Generate query embedding
- Perform vector similarity search
- Return top 3-5 most relevant results
- Format results appropriately for agent

**Code Structure:**
```python
@function_tool
def your_rag_function(query: str) -> str:
    """
    Perform RAG search on your domain data.

    Args:
        query: User's search query

    Returns:
        Formatted search results
    """
    # 1. Generate query embedding
    # 2. Search vector database
    # 3. Format and return results
    pass
```

### 3. Agent Requirements

**Manager Agent:**
- Analyzes user intent
- Routes to appropriate specialized agent
- Must use handoff mechanism
- Clear instructions for routing logic

**Specialized Agents (minimum 2):**

**Agent 1 (RAG-based):**
- Uses your RAG function as a tool
- Processes retrieved information
- Generates natural language responses
- Must ALWAYS use tool before responding

**Agent 2 (Alternative functionality):**
- Different responsibility than Agent 1
- Can use RAG, external API, or computation
- Clear, distinct purpose

**Optional Agent 3+:**
- Additional specialized agents
- Each with unique responsibilities

**Agent Configuration Example:**
```python
from agents import Agent, function_tool, handoff

# Specialized agent
domain_agent = Agent(
    name="domain_expert",
    instructions=DOMAIN_INSTRUCTION,
    tools=[your_rag_function],
    model_settings=ModelSettings(tool_choice="required")
)

# Manager agent
manager_agent = Agent(
    name="manager",
    instructions=MANAGER_INSTRUCTION,
    handoffs=[domain_agent, other_agent]
)
```

### 4. API Server Requirements

**Framework:**
- Flask or FastAPI
- Must run on localhost

**Endpoints:**

**POST /chat (Required):**
```python
# Request format
{
    "message": "user query here",
    "thread_id": "unique-thread-id"
}

# Response format
{
    "role": "assistant",
    "content": "agent response here"
}
```

**Additional Endpoints (Optional):**
- GET /health - Health check
- POST /reset - Clear conversation history
- GET /threads - List active conversations

**Features:**
- Conversation history management per thread
- CORS enabled for frontend access
- Error handling with appropriate status codes
- Request validation
- Async agent execution

**Code Structure:**
```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio

app = Flask(__name__)
CORS(app)

conversation_history = {}

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        query = data.get("message", "")
        thread_id = data.get("thread_id", "default")

        # Validate input
        if not query:
            return jsonify({"error": "Message required"}), 400

        # Manage conversation history
        if thread_id not in conversation_history:
            conversation_history[thread_id] = []

        # Run agent
        new_input = conversation_history[thread_id] + [
            {"role": "user", "content": query}
        ]
        result = asyncio.run(Runner.run(manager_agent, new_input))

        # Update history
        conversation_history[thread_id] = new_input + [
            {"role": "assistant", "content": str(result.final_output)}
        ]

        return jsonify({
            "role": "assistant",
            "content": str(result.final_output)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
```

### 5. UI Requirements

**Framework:**
- Streamlit (recommended)
- Or custom React/Vue/HTML+JS

**Required Features:**
- Chat message display (user and assistant)
- Text input for queries
- Send button
- Message history
- New conversation button
- Thread ID display (can be hidden)

**Streamlit Example:**
```python
import streamlit as st
import requests
import uuid

# Initialize session state
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display title
st.title("Your Project Title")

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call API
    response = requests.post(
        "http://localhost:5001/chat",
        json={"message": prompt, "thread_id": st.session_state.thread_id}
    )

    # Add assistant message
    if response.status_code == 200:
        content = response.json()["content"]
        st.session_state.messages.append({"role": "assistant", "content": content})
        st.rerun()

# Sidebar
with st.sidebar:
    if st.button("New Conversation"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()
```

### 6. Documentation Requirements

**README.md Must Include:**

1. **Project Title and Description**
   - Clear, concise overview
   - What problem does it solve?

2. **Features**
   - List key features
   - What makes it unique?

3. **System Requirements**
   - Python version
   - Operating system compatibility

4. **Installation Instructions**
   ```bash
   # Step-by-step setup
   git clone ...
   cd project
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Configuration**
   - How to set up .env file
   - Required API keys
   - Any other configuration

6. **Data Setup**
   ```bash
   # How to initialize data
   python setup.py
   ```

7. **Running the Application**
   ```bash
   # Start API server
   python serve.py

   # In another terminal, start UI
   streamlit run client.py
   ```

8. **Usage Examples**
   - Example queries
   - Expected responses
   - Screenshots (optional)

9. **Project Structure**
   - File organization
   - Purpose of each file

10. **Agent Architecture**
    - Diagram or description
    - Agent responsibilities
    - Handoff flow

11. **API Documentation**
    - Endpoints
    - Request/response formats
    - Examples

12. **Known Issues / Limitations**
    - Any current bugs
    - Future improvements

13. **License**
    - MIT or your choice

**Additional Documentation (Optional but Recommended):**
- `docs/architecture.md` - Detailed system design
- `docs/api.md` - Complete API reference
- `CONTRIBUTING.md` - How others can contribute

### 7. Code Quality Requirements

**File Organization:**
```
your-project/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── setup.py           # Data initialization
├── rag.py             # RAG functions
├── prompt.py          # Agent instructions
├── serve.py           # API server
├── client.py          # UI client
├── data/
│   └── your_data.csv
└── tests/
    └── test_basic.py
```

**Code Standards:**

1. **Type Hints:**
```python
def get_embedding(text: str) -> list[float]:
    """Generate embedding for text."""
    pass

def search_database(query: str, limit: int = 3) -> list[dict]:
    """Search vector database."""
    pass
```

2. **Docstrings:**
```python
def process_query(query: str) -> str:
    """
    Process user query through RAG pipeline.

    Args:
        query: User's question or search query

    Returns:
        Formatted response with relevant information

    Raises:
        ValueError: If query is empty
        ConnectionError: If database unavailable
    """
    pass
```

3. **Error Handling:**
```python
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    return default_value
```

4. **Environment Variables:**
```python
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment")
```

5. **No Hardcoded Values:**
```python
# Bad
collection = client.get_collection("products")
API_URL = "http://localhost:5001"

# Good
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "products")
API_URL = os.getenv("API_URL", "http://localhost:5001")
```

### 8. Testing Requirements

**Minimum Tests:**

1. **Embedding Generation:**
```python
def test_embedding_generation():
    text = "test query"
    embedding = get_embedding(text)
    assert len(embedding) == 1536
    assert isinstance(embedding, list)
```

2. **Vector Search:**
```python
def test_vector_search():
    query = "sample query"
    results = rag(query)
    assert results is not None
    assert len(results) > 0
```

3. **API Endpoint:**
```python
def test_chat_endpoint():
    response = requests.post(
        "http://localhost:5001/chat",
        json={"message": "test", "thread_id": "test-1"}
    )
    assert response.status_code == 200
    assert "content" in response.json()
```

4. **Agent Execution:**
```python
def test_agent_response():
    result = asyncio.run(Runner.run(
        manager_agent,
        [{"role": "user", "content": "test query"}]
    ))
    assert result.final_output is not None
```

## Optional Enhancements

### Advanced Features (Choose 1+)

**1. OpenRouter Integration:**
- Use alternative models via OpenRouter
- Implement model fallback strategy
- Compare costs and performance

**2. Streaming Responses:**
- Real-time token streaming
- Update UI as response generates
- Better user experience

**3. Multi-modal Support:**
- Accept images as input
- Process PDFs or documents
- Return visual responses

**4. Advanced Context Management:**
- Summarize long conversations
- Maintain context across sessions
- Implement memory mechanisms

**5. Evaluation Metrics:**
- Measure retrieval accuracy
- Track response quality
- A/B test different approaches

**6. Deployment:**
- Docker containerization
- Deploy to cloud (Railway, Render, etc.)
- CI/CD pipeline

**7. Authentication:**
- User accounts
- API key management
- Rate limiting per user

**8. Analytics:**
- Track usage patterns
- Monitor performance
- Generate reports

## Evaluation Rubric (Detailed)

### Functionality (40 points)

**Agents (10 points):**
- Manager routes correctly (3 pts)
- Specialized agents respond appropriately (4 pts)
- Handoffs work smoothly (3 pts)

**RAG (10 points):**
- Retrieves relevant documents (4 pts)
- Embeddings generated correctly (2 pts)
- Results formatted well (2 pts)
- Handles edge cases (2 pts)

**Agent Routing (10 points):**
- Correct agent selected (5 pts)
- Handles ambiguous queries (3 pts)
- Fallback behavior (2 pts)

**API (5 points):**
- Endpoints work correctly (2 pts)
- Error handling (2 pts)
- Response format correct (1 pt)

**UI (5 points):**
- Chat interface functional (2 pts)
- Message display correct (1 pt)
- Input handling works (1 pt)
- New conversation works (1 pt)

### Code Quality (30 points)

**Organization (10 points):**
- Clear file structure (3 pts)
- Logical separation of concerns (3 pts)
- Consistent naming (2 pts)
- No code duplication (2 pts)

**Error Handling (5 points):**
- Try-except blocks used appropriately (2 pts)
- Meaningful error messages (2 pts)
- Graceful degradation (1 pt)

**Documentation (5 points):**
- Type hints present (2 pts)
- Docstrings for functions (2 pts)
- Inline comments where needed (1 pt)

**Best Practices (5 points):**
- Environment variables used (2 pts)
- No hardcoded secrets (2 pts)
- Follows Python conventions (1 pt)

**Security (5 points):**
- API keys not exposed (2 pts)
- Input validation (2 pts)
- CORS configured appropriately (1 pt)

### Documentation (20 points)

**README (8 points):**
- Clear description (2 pts)
- Complete setup instructions (3 pts)
- Usage examples (2 pts)
- Well-formatted (1 pt)

**Architecture (4 points):**
- System design explained (2 pts)
- Agent roles clear (2 pts)

**API Docs (4 points):**
- Endpoints documented (2 pts)
- Examples provided (2 pts)

**Examples (4 points):**
- Sample queries (2 pts)
- Expected outputs (2 pts)

### Creativity (10 points)

**Domain Choice (5 points):**
- Unique or interesting domain (2 pts)
- Well-defined use case (2 pts)
- Practical application (1 pt)

**Additional Features (5 points):**
- Beyond minimum requirements (3 pts)
- Innovative approach (2 pts)

## Submission Checklist

Before submitting, verify:

### Code
- [ ] All Python files included
- [ ] requirements.txt complete
- [ ] .env.example provided
- [ ] .gitignore includes .env and credentials
- [ ] No syntax errors
- [ ] Code runs without errors

### Data
- [ ] Data files included or downloadable
- [ ] setup.py creates database successfully
- [ ] Minimum 50 documents/entries
- [ ] Data is clean and formatted

### Functionality
- [ ] API server starts successfully
- [ ] UI client connects to API
- [ ] Agents respond appropriately
- [ ] RAG retrieval works
- [ ] Conversation history maintained

### Documentation
- [ ] README complete and clear
- [ ] Installation instructions tested
- [ ] Architecture explained
- [ ] API documented
- [ ] Example queries provided

### Quality
- [ ] Code follows best practices
- [ ] Error handling implemented
- [ ] Type hints included
- [ ] Docstrings present
- [ ] No security issues

### Testing
- [ ] Basic tests written
- [ ] All tests pass
- [ ] Manual testing completed

## Getting Help

If requirements are unclear:
- Review lesson materials
- Check reference solution
- Ask in discussions
- Office hours available

Good luck building your multi-agent RAG system! 🚀
