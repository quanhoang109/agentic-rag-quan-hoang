# System Architecture

## Overview

This document describes the architecture of the Multi-Agent RAG (Retrieval-Augmented Generation) system for mobile shop sales assistance.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                   (Streamlit Chat Client)                    │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/REST
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       Flask API Server                       │
│                    (Conversation Handler)                    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Manager Agent                           │
│              (Request Analysis & Routing)                    │
└─────────────┬───────────────────────────┬───────────────────┘
              │                           │
              ▼                           ▼
    ┌─────────────────┐         ┌─────────────────────┐
    │  Product Agent  │         │ Shop Info Agent     │
    │   (RAG Tool)    │         │ (Google Sheets)     │
    └────────┬────────┘         └──────────┬──────────┘
             │                             │
             ▼                             ▼
    ┌─────────────────┐         ┌─────────────────────┐
    │   ChromaDB      │         │  Google Sheets API  │
    │ (Vector Store)  │         │  (Shop Information) │
    └─────────────────┘         └─────────────────────┘
```

## Components

### 1. User Interface (Streamlit)
**Purpose:** Interactive chat interface for users to communicate with the system

**Key Features:**
- Real-time chat messaging
- Conversation thread management
- Session state persistence
- Custom styling and avatars

**Files:** `client.py`

### 2. API Server (Flask)
**Purpose:** REST API endpoint for processing chat requests

**Key Features:**
- POST `/chat` endpoint
- Thread-based conversation history
- CORS support for cross-origin requests
- Error handling and validation
- Async agent execution

**Files:** `serve.py`, `oss_serve.py`

**Request/Response Format:**
```json
// Request
{
  "message": "Nokia 3210 4G có giá bao nhiêu?",
  "thread_id": "uuid-string"
}

// Response
{
  "role": "assistant",
  "content": "Nokia 3210 4G có giá là 1,590,000 ₫."
}
```

### 3. Manager Agent
**Purpose:** Orchestrates requests and routes to appropriate specialized agents

**Responsibilities:**
- Analyze user intent
- Determine which agent should handle the request
- Perform handoff to specialized agents
- Return final response

**Configuration:**
```python
Agent(
    name="manager",
    instructions=MANAGER_INSTRUCTION,
    handoffs=[product_agent, shop_information_agent]
)
```

**Files:** `prompt.py` (MANAGER_INSTRUCTION)

### 4. Product Agent
**Purpose:** Handles product-related queries using RAG

**Responsibilities:**
- Search product database via RAG tool
- Retrieve relevant product information
- Format responses with pricing, specs, colors, etc.

**Tools:**
- `rag()` - Vector search in ChromaDB

**Configuration:**
```python
Agent(
    name="product",
    instructions=PRODUCT_INSTRUCTION,
    tools=[rag]
)
```

**Files:** `prompt.py` (PRODUCT_INSTRUCTION), `rag.py`

### 5. Shop Information Agent
**Purpose:** Provides store details from Google Sheets

**Responsibilities:**
- Fetch shop information (hours, location, policies)
- Return up-to-date store data

**Tools:**
- `shop_information_rag()` - Google Sheets API

**Configuration:**
```python
Agent(
    name="shop_information",
    instructions=SHOP_INFORMATION_INSTRUCTION,
    tools=[shop_information_rag]
)
```

**Files:** `prompt.py` (SHOP_INFORMATION_INSTRUCTION), `rag.py`

## Data Flow

### Typical Query Flow

1. **User Input**
   - User types query in Streamlit UI
   - UI sends POST request to Flask API with message and thread_id

2. **API Processing**
   - Flask receives request
   - Loads conversation history for thread_id
   - Appends new user message

3. **Manager Analysis**
   - Manager agent receives conversation history
   - Analyzes user intent
   - Determines appropriate specialized agent

4. **Agent Handoff**
   - Manager performs handoff to specialized agent
   - Handoff includes conversation context

5. **Tool Execution**
   - Specialized agent calls appropriate tool
   - **Product Agent:** Queries ChromaDB vector database
   - **Shop Info Agent:** Fetches from Google Sheets

6. **Response Generation**
   - Tool returns relevant data
   - Agent generates natural language response
   - Response returned to Manager

7. **Response Delivery**
   - Manager returns final output
   - Flask appends to conversation history
   - Response sent to UI
   - UI displays message to user

## RAG Pipeline (Product Agent)

```
User Query: "Nokia 3210 4G có giá bao nhiêu?"
     │
     ▼
┌─────────────────────────┐
│  Generate Query         │
│  Embedding              │
│  (OpenAI API)           │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  Vector Similarity      │
│  Search in ChromaDB     │
│  (Top 3 results)        │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  Extract Metadata       │
│  (product info)         │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  Return Context to      │
│  Agent for Generation   │
└──────────┬──────────────┘
           │
           ▼
Response: "Nokia 3210 4G có giá là 1,590,000 ₫."
```

## Database Schema

### ChromaDB Collection: "products"

**Structure:**
- **IDs:** UUID strings
- **Embeddings:** 1536-dimensional vectors (text-embedding-3-small)
- **Metadata:**
  - `information`: Combined text from all product fields

**Sample Metadata:**
```json
{
  "information": "Nokia 3210 4G Khuyến mại: Giảm 10% cho học sinh sinh viên... Màn hình 2.4 inch, Pin 1450mAh... có giá: 1,590,000 ₫ có màu sắc: Đen, Vàng"
}
```

### Google Sheets: Shop Information

**Fields (example):**
- Store location
- Opening hours
- Contact information
- Policies
- Services offered

## Multi-Agent Patterns

### 1. Manager-Worker Pattern
- **Manager:** Analyzes and routes requests
- **Workers:** Specialized agents for specific domains

### 2. Handoff Mechanism
```python
handoff(
    product_agent,
    input_filter=custom_input_filter
)
```

**Handoff Data:**
- `input_history`: Previous conversation
- `pre_handoff_items`: Messages before handoff
- `new_items`: New messages from handoff

### 3. Tool Execution Pattern
```python
@function_tool
def rag(query: str) -> str:
    # 1. Generate embedding
    # 2. Search vector database
    # 3. Return formatted results
    return search_result
```

## Alternative Models (OSS)

### LiteLLM Integration

The system supports multiple LLM providers via LiteLLM:

```python
# Example configurations
kimi = LitellmModel(
    model="openrouter/moonshot/kimi-k2-instruct",
    api_key=openrouter_key
)

product_agent = Agent(
    name="product",
    tools=[rag],
    model=kimi
)
```

**Benefits:**
- Cost optimization
- Reduced latency
- Provider redundancy

## Scalability Considerations

### Current Limitations
- In-memory conversation history (not persistent)
- Single-threaded Flask server
- No caching layer

### Recommended Improvements
1. **Persistent Storage:** Redis/PostgreSQL for conversation history
2. **Production Server:** Gunicorn/uWSGI with multiple workers
3. **Caching:** Redis for frequent queries
4. **Load Balancing:** Multiple API server instances
5. **Monitoring:** Logging and observability tools

## Security Considerations

1. **API Key Management**
   - Store in environment variables
   - Never commit to version control
   - Rotate regularly

2. **Input Validation**
   - Sanitize user inputs
   - Rate limiting on API endpoints

3. **Google Sheets Access**
   - Service account with minimal permissions
   - Credential file protection

4. **CORS Configuration**
   - Restrict allowed origins in production
   - Currently allows all origins (`*`)

## Performance Optimization

### Vector Search
- **Current:** Top 3 results
- **Optimization:** Adjust n_results based on query complexity

### Embedding Generation
- **Model:** text-embedding-3-small (cost-effective)
- **Alternative:** text-embedding-3-large (higher accuracy)

### Agent Execution
- **Async:** Uses `asyncio.run()` for non-blocking execution
- **Tracing:** Built-in trace functionality for debugging

## Extension Points

### Adding New Agents
1. Define new tool function with `@function_tool`
2. Create agent with appropriate instructions
3. Add to manager's handoff list

### Custom Data Sources
1. Implement new function tool
2. Handle authentication/connection
3. Return formatted data for agent

### UI Customization
- Modify Streamlit CSS
- Add new components
- Implement additional features (file upload, voice, etc.)
