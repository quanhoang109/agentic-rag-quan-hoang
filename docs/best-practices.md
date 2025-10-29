# Best Practices

## Code Organization

### Project Structure
```
agentic-rag/
├── serve.py          # API server entry point
├── rag.py            # RAG tools and functions
├── prompt.py         # Agent instructions
├── setup.py          # Data initialization
├── client.py         # UI client
└── .env              # Configuration (gitignored)
```

**Principles:**
- **Separation of Concerns:** Each file has a single responsibility
- **Modularity:** Functions and agents are reusable
- **Configuration:** External config via environment variables

### Code Style

Follow PEP 8 Python style guidelines:

```python
# Good: Clear function names, type hints
def get_embedding(text: str) -> list[float]:
    """Generate embedding for given text."""
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

# Bad: No type hints, unclear names
def ge(t):
    r = client.embeddings.create(input=t, model="text-embedding-3-small")
    return r.data[0].embedding
```

### Type Hints
Always use type hints for better code clarity:

```python
from typing import List, Dict, Any

@function_tool
def rag(query: str) -> str:
    """RAG tool with clear input/output types."""
    pass

def process_results(results: Dict[str, Any]) -> List[str]:
    """Process ChromaDB results."""
    pass
```

## Agent Design

### Instructions

**Do:**
- Be specific and clear about agent responsibilities
- Provide concrete examples
- Define decision criteria
- Enforce tool usage with "MUST ALWAYS use tool"

**Don't:**
- Make instructions too generic
- Leave behavior ambiguous
- Allow agents to skip tool calls

```python
# Good: Specific, with examples
PRODUCT_INSTRUCTION = """
You are a product assistant. You will receive product information from the user's query.

CRITICAL RULE: You MUST ALWAYS use the rag tool before responding.

Examples:
Question: Nokia 3210 4G có giá bao nhiêu?
Workflow: First call rag("Nokia 3210 4G giá"), then respond
Answer: Nokia 3210 4G có giá là 1,590,000 ₫.
"""

# Bad: Too generic
PRODUCT_INSTRUCTION = """
You help with products. Answer questions about products.
"""
```

### Tool Design

**Best Practices:**
1. **Single Responsibility:** Each tool does one thing well
2. **Error Handling:** Graceful failure with informative messages
3. **Logging:** Print debug information for troubleshooting
4. **Return Format:** Consistent, structured output

```python
@function_tool
def rag(query: str) -> str:
    """Product search tool with proper error handling."""
    try:
        print(f'----Product query: {query}')

        collection = chroma_client.get_collection(name=collection_name)
        query_embedding = get_embedding(query)

        # Normalize embedding
        query_embedding = query_embedding / np.linalg.norm(query_embedding)

        # Search
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=3
        )

        # Format results
        formatted = format_search_results(results)

        print(f'----Results: {formatted[:100]}...')
        return formatted

    except Exception as e:
        print(f'Error in RAG tool: {e}')
        return "Unable to retrieve product information at this time."
```

### Agent Configuration

```python
# Good: Clear configuration with appropriate settings
product_agent = Agent(
    name="product",  # Descriptive name
    instructions=PRODUCT_INSTRUCTION,  # Detailed instructions
    tools=[rag],  # Relevant tools only
    model_settings=ModelSettings(
        tool_choice="required"  # Force tool usage
    )
)

# With alternative models
product_agent = Agent(
    name="product",
    instructions=PRODUCT_INSTRUCTION,
    tools=[rag],
    model=custom_model,  # LitellmModel instance
    model_settings=ModelSettings(tool_choice="required")
)
```

## Error Handling

### API Server

```python
@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Validate input
        data = request.json
        query = data.get("message", "")
        thread_id = data.get("thread_id", "1")

        if not query:
            return jsonify({"error": "Missing query parameter"}), 400

        # Process request
        result = asyncio.run(Runner.run(manager_agent, new_input))

        return jsonify({
            "role": "assistant",
            "content": str(result.final_output)
        })

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            "error": f"Error processing request: {str(e)}"
        }), 500
```

### Tool Functions

```python
@function_tool
def shop_information_rag():
    """Google Sheets tool with error handling."""
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'credentials.json',
            scope
        )
        client = gspread.authorize(credentials)
        sheet = client.open_by_url(SHEET_URL).sheet1
        data = sheet.get_all_records()
        return data

    except FileNotFoundError:
        return "Error: Credentials file not found."
    except gspread.exceptions.APIError as e:
        return f"Error accessing Google Sheets: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
```

## Data Processing

### CSV/Data Loading

```python
# Good: Clean, documented data processing
def preprocess_csv(filepath: str) -> pd.DataFrame:
    """Load and preprocess product data."""
    df = pd.read_csv(filepath)

    # Remove empty rows
    df = df[df['information'].notna()]

    # Clean text fields
    df['information'] = df['information'].str.replace("<br>", " ")
    df['information'] = df['information'].str.replace("\n", " ")

    return df

def create_product_text(row) -> str:
    """Combine product fields into searchable text."""
    parts = []

    if row['title']:
        parts.append(row['title'])

    if row['current_price']:
        parts.append(f"có giá: {row['current_price']}")

    if row['color_options']:
        colors = ast.literal_eval(row['color_options'])
        parts.append(f"có màu sắc: {', '.join(colors)}")

    return " ".join(parts)
```

### Embedding Generation

```python
# Good: Batch processing for efficiency
def generate_embeddings_batch(texts: List[str], batch_size: int = 100) -> List[List[float]]:
    """Generate embeddings in batches to avoid rate limits."""
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        embeddings = [get_embedding(text) for text in batch]
        all_embeddings.extend(embeddings)

        # Rate limiting
        time.sleep(1)

    return all_embeddings
```

## Security

### Environment Variables

```python
# Good: Proper environment variable handling
from dotenv import load_dotenv
import os

load_dotenv()

def require_env_key(key_name: str) -> str:
    """Get required environment variable or raise error."""
    value = os.getenv(key_name)
    if not value:
        raise EnvironmentError(f"{key_name} not found in environment variables")
    return value

# Usage
openai_key = require_env_key("OPENAI_API_KEY")
openrouter_key = require_env_key("OPENROUTER_API_KEY")
```

### Credentials Management

```bash
# .gitignore - Always exclude sensitive files
.env
*.json  # Service account credentials
db/     # Local database files
__pycache__/
*.pyc
```

### API Security

```python
# Production: Restrict CORS
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://yourdomain.com"])

# Add rate limiting
from flask_limiter import Limiter

limiter = Limiter(
    app=app,
    key_func=lambda: request.remote_addr,
    default_limits=["100 per hour"]
)

@app.route("/chat", methods=["POST"])
@limiter.limit("10 per minute")
def chat():
    # Your code here
    pass
```

## Testing

### Unit Tests

```python
import unittest
from rag import get_embedding, rag

class TestRAGFunctions(unittest.TestCase):

    def test_get_embedding(self):
        """Test embedding generation."""
        text = "Nokia 3210 4G"
        embedding = get_embedding(text)

        self.assertEqual(len(embedding), 1536)
        self.assertIsInstance(embedding, list)

    def test_rag_search(self):
        """Test RAG search functionality."""
        query = "Nokia 3210 4G giá"
        result = rag(query)

        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
```

### Integration Tests

```python
def test_agent_flow():
    """Test complete agent workflow."""
    query = "Nokia 3210 4G có giá bao nhiêu?"

    result = asyncio.run(Runner.run(
        manager_agent,
        [{"role": "user", "content": query}]
    ))

    assert result.final_output is not None
    assert "1,590,000" in result.final_output
```

### API Tests

```bash
# Test with curl
curl -X POST "http://localhost:5001/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Nokia 3210 4G có giá bao nhiêu?", "thread_id": "test-1"}'
```

## Performance

### Vector Search Optimization

```python
# Normalize embeddings for cosine similarity
query_embedding = query_embedding / np.linalg.norm(query_embedding)

# Adjust n_results based on needs
search_results = collection.query(
    query_embeddings=query_embedding,
    n_results=3  # Start with 3, adjust based on quality
)
```

### Conversation History

```python
# Limit history to prevent token overflow
MAX_HISTORY_LENGTH = 10

def manage_conversation(thread_id: str, new_message: dict):
    """Manage conversation history with limits."""
    if thread_id not in conversation_history:
        conversation_history[thread_id] = []

    history = conversation_history[thread_id]
    history.append(new_message)

    # Keep only recent messages
    if len(history) > MAX_HISTORY_LENGTH:
        conversation_history[thread_id] = history[-MAX_HISTORY_LENGTH:]
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_embedding_cached(text: str) -> tuple:
    """Cache embeddings for repeated queries."""
    embedding = get_embedding(text)
    return tuple(embedding)  # Lists aren't hashable
```

## Deployment

### Production Checklist

- [ ] Use production WSGI server (Gunicorn, uWSGI)
- [ ] Enable HTTPS
- [ ] Set up proper CORS restrictions
- [ ] Implement rate limiting
- [ ] Add logging and monitoring
- [ ] Use persistent storage for conversations
- [ ] Set up error alerting
- [ ] Configure auto-scaling
- [ ] Regular backup of ChromaDB

### Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ChromaDB persistence
VOLUME /app/db

EXPOSE 5001

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "serve:app"]
```

## Monitoring

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    logger.info(f"Received chat request: thread_id={thread_id}")
    # Your code
    logger.info(f"Response generated in {duration}s")
```

### Metrics

Track important metrics:
- Request latency
- Error rates
- Agent handoff patterns
- Tool usage frequency
- Token consumption

## Prompt Engineering

### Manager Instructions

```python
# Be explicit about routing logic
MANAGER_INSTRUCTION = """
CRITICAL RULE: You MUST ALWAYS delegate user queries to the appropriate agent.

DECISION CRITERIA:
- Product questions → Transfer to "product" agent
- Shop information → Transfer to "shop_information" agent

EXAMPLES:
User: "Nokia 3210 4G có giá bao nhiêu?"
Action: Transfer to product agent (price inquiry)
"""
```

### Worker Instructions

```python
# Force tool usage
PRODUCT_INSTRUCTION = """
CRITICAL RULE: You MUST ALWAYS use the rag tool before responding.

Your workflow:
1. ALWAYS call the rag tool first
2. Use the retrieved information
3. Format your response

Remember: ALWAYS search first, then respond.
"""
```

## Common Pitfalls

### 1. Agents Not Using Tools
**Problem:** Agent responds without calling tools
**Solution:** Use `tool_choice="required"` in ModelSettings

### 2. Poor Vector Search Results
**Problem:** Irrelevant results returned
**Solution:** Improve document chunking and metadata

### 3. Conversation Context Loss
**Problem:** Agents forget previous messages
**Solution:** Properly manage conversation history in handoffs

### 4. API Rate Limits
**Problem:** OpenAI API rate limit errors
**Solution:** Implement exponential backoff and caching

### 5. ChromaDB Persistence Issues
**Problem:** Data lost on restart
**Solution:** Use `PersistentClient` with proper path

```python
# Good: Persistent storage
chroma_client = chromadb.PersistentClient("db")

# Bad: In-memory only
chroma_client = chromadb.Client()
```
