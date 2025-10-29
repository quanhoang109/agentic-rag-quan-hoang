# Agentic RAG Learning Repository - Restructuring Plan

## Overview
Transform this repository into a comprehensive, hands-on learning resource for building Multi-Agent RAG (Retrieval-Augmented Generation) systems using OpenAI Agents SDK.

---

## Target Audience
- Intermediate Python developers
- ML/AI enthusiasts interested in agentic systems
- Engineers wanting to build production RAG applications
- Students learning about multi-agent architectures

---

## Learning Objectives
By completing this course, students will:
1. Understand RAG fundamentals and vector databases
2. Build single-agent RAG systems
3. Implement multi-agent orchestration
4. Integrate external data sources (CSV, Google Sheets)
5. Deploy production-ready API servers
6. Create interactive UI clients
7. Work with open-source LLM alternatives

---

## Repository Structure (Proposed)

```
agentic-rag/
├── README.md                          # Updated with learning path overview
├── plan.md                            # This file
├── requirements.txt                   # Dependencies
├── .env.example                       # Environment template
├── data/
│   └── hoanghamobile.csv             # Sample dataset
├── lessons/
│   ├── lesson-01-setup/
│   │   ├── README.md
│   │   ├── instructions.md
│   │   └── solution/
│   ├── lesson-02-embeddings/
│   │   ├── README.md
│   │   ├── instructions.md
│   │   ├── exercises/
│   │   └── solution/
│   ├── lesson-03-vector-database/
│   │   ├── README.md
│   │   ├── instructions.md
│   │   ├── exercises/
│   │   └── solution/
│   ├── lesson-04-basic-rag/
│   │   ├── README.md
│   │   ├── instructions.md
│   │   ├── exercises/
│   │   └── solution/
│   ├── lesson-05-single-agent/
│   │   ├── README.md
│   │   ├── instructions.md
│   │   ├── exercises/
│   │   └── solution/
│   ├── lesson-06-multi-agent/
│   │   ├── README.md
│   │   ├── instructions.md
│   │   ├── exercises/
│   │   └── solution/
│   ├── lesson-07-external-data/
│   │   ├── README.md
│   │   ├── instructions.md
│   │   ├── exercises/
│   │   └── solution/
│   ├── lesson-08-api-server/
│   │   ├── README.md
│   │   ├── instructions.md
│   │   ├── exercises/
│   │   └── solution/
│   ├── lesson-09-ui-client/
│   │   ├── README.md
│   │   ├── instructions.md
│   │   ├── exercises/
│   │   └── solution/
│   └── lesson-10-oss-models/
│       ├── README.md
│       ├── instructions.md
│       ├── exercises/
│       └── solution/
├── final-project/
│   ├── README.md
│   ├── requirements.md
│   ├── reference-solution/
│   │   ├── serve.py
│   │   ├── rag.py
│   │   ├── prompt.py
│   │   ├── setup.py
│   │   ├── client.py
│   │   └── oss_serve.py
│   └── starter-code/
└── docs/
    ├── architecture.md
    ├── best-practices.md
    ├── troubleshooting.md
    └── resources.md
```

---

## Detailed Lesson Breakdown

### **Lesson 1: Environment Setup & Prerequisites**

**Duration:** 30 minutes

**Learning Goals:**
- Understand project requirements
- Set up Python environment
- Configure OpenAI API keys
- Verify installation

**Topics Covered:**
- Python virtual environments
- Package management with pip
- Environment variables and .env files
- API key management best practices

**Hands-on Activities:**
1. Create virtual environment
2. Install dependencies from requirements.txt
3. Set up .env file with API keys
4. Run verification script

**Deliverables:**
- Working Python environment
- Configured API keys
- Installed dependencies verified

**Files to Create:**
- `lessons/lesson-01-setup/README.md` - Lesson overview
- `lessons/lesson-01-setup/instructions.md` - Step-by-step guide
- `lessons/lesson-01-setup/solution/verify.py` - Installation checker
- `lessons/lesson-01-setup/solution/.env.example` - Template

---

### **Lesson 2: Understanding Embeddings**

**Duration:** 1 hour

**Learning Goals:**
- Understand what embeddings are
- Learn vector representations of text
- Use OpenAI Embedding API
- Visualize embedding similarities

**Topics Covered:**
- Vector embeddings fundamentals
- text-embedding-3-small model
- Cosine similarity
- Semantic search basics

**Hands-on Activities:**
1. Generate embeddings for sample texts
2. Calculate similarity between embeddings
3. Visualize embedding space (2D projection)
4. Build simple semantic search

**Code Exercises:**
```python
# Exercise 1: Generate embeddings
def get_embedding(text: str) -> list[float]:
    # TODO: Implement using OpenAI API
    pass

# Exercise 2: Calculate similarity
def cosine_similarity(vec1, vec2):
    # TODO: Implement cosine similarity
    pass

# Exercise 3: Find most similar
def find_most_similar(query, documents):
    # TODO: Implement semantic search
    pass
```

**Deliverables:**
- Embedding generator function
- Similarity calculator
- Simple search implementation

**Files to Create:**
- `lessons/lesson-02-embeddings/README.md`
- `lessons/lesson-02-embeddings/instructions.md`
- `lessons/lesson-02-embeddings/exercises/embeddings_basics.py`
- `lessons/lesson-02-embeddings/solution/embeddings_complete.py`

---

### **Lesson 3: Vector Database with ChromaDB**

**Duration:** 1.5 hours

**Learning Goals:**
- Understand vector database concepts
- Set up ChromaDB
- Perform CRUD operations
- Implement vector search

**Topics Covered:**
- Vector database architecture
- ChromaDB persistent client
- Collections and metadata
- Vector search queries

**Hands-on Activities:**
1. Initialize ChromaDB client
2. Create collection with embeddings
3. Insert sample documents
4. Query with vector search
5. Update and delete operations

**Code Exercises:**
```python
# Exercise 1: Initialize ChromaDB
def setup_chromadb(path: str):
    # TODO: Create persistent client
    pass

# Exercise 2: Create collection
def create_collection(client, name: str):
    # TODO: Create or get collection
    pass

# Exercise 3: Insert documents
def insert_documents(collection, documents, embeddings, metadata):
    # TODO: Add documents to collection
    pass

# Exercise 4: Search
def search_similar(collection, query_embedding, n_results=3):
    # TODO: Implement vector search
    pass
```

**Deliverables:**
- ChromaDB setup script
- Document insertion pipeline
- Vector search function

**Files to Create:**
- `lessons/lesson-03-vector-database/README.md`
- `lessons/lesson-03-vector-database/instructions.md`
- `lessons/lesson-03-vector-database/exercises/chromadb_basics.py`
- `lessons/lesson-03-vector-database/solution/chromadb_complete.py`
- `lessons/lesson-03-vector-database/solution/sample_data.json`

---

### **Lesson 4: Building Basic RAG Pipeline**

**Duration:** 2 hours

**Learning Goals:**
- Understand RAG architecture
- Process and chunk documents
- Build retrieval pipeline
- Generate augmented responses

**Topics Covered:**
- RAG fundamentals (Retrieval, Augmentation, Generation)
- Document preprocessing
- Text chunking strategies
- Prompt engineering for RAG
- Context injection

**Hands-on Activities:**
1. Load and process CSV data
2. Create embeddings for documents
3. Store in vector database
4. Implement retrieval function
5. Build RAG query pipeline

**Code Exercises:**
```python
# Exercise 1: Data preprocessing
def preprocess_csv(filepath: str) -> pd.DataFrame:
    # TODO: Load and clean CSV
    pass

# Exercise 2: Create combined text
def create_document_text(row) -> str:
    # TODO: Combine fields into searchable text
    pass

# Exercise 3: RAG query
def rag_query(query: str, collection, llm_client) -> str:
    # TODO: Retrieve + Generate
    pass
```

**Deliverables:**
- Data preprocessing pipeline
- RAG query function
- Working end-to-end example

**Files to Create:**
- `lessons/lesson-04-basic-rag/README.md`
- `lessons/lesson-04-basic-rag/instructions.md`
- `lessons/lesson-04-basic-rag/exercises/rag_pipeline.py`
- `lessons/lesson-04-basic-rag/solution/rag_complete.py`
- `lessons/lesson-04-basic-rag/solution/setup_data.py`

---

### **Lesson 5: Single Agent with OpenAI Agents SDK**

**Duration:** 2 hours

**Learning Goals:**
- Introduction to OpenAI Agents SDK
- Create function tools
- Build single agent
- Implement agent with RAG tool

**Topics Covered:**
- OpenAI Agents SDK architecture
- Agent class and configuration
- Function tools decorator
- Agent instructions and prompts
- Runner for executing agents

**Hands-on Activities:**
1. Install openai-agents package
2. Create RAG function tool
3. Define agent instructions
4. Build product agent
5. Run queries through agent

**Code Exercises:**
```python
# Exercise 1: Create function tool
@function_tool
def product_search(query: str) -> str:
    # TODO: Implement RAG search
    pass

# Exercise 2: Create agent
def create_product_agent():
    # TODO: Configure agent with tools
    pass

# Exercise 3: Run agent
async def run_agent_query(agent, query: str):
    # TODO: Execute agent with Runner
    pass
```

**Deliverables:**
- RAG function tool
- Configured product agent
- Working agent execution

**Files to Create:**
- `lessons/lesson-05-single-agent/README.md`
- `lessons/lesson-05-single-agent/instructions.md`
- `lessons/lesson-05-single-agent/exercises/single_agent.py`
- `lessons/lesson-05-single-agent/solution/agent_complete.py`

---

### **Lesson 6: Multi-Agent Orchestration**

**Duration:** 3 hours

**Learning Goals:**
- Understand multi-agent architectures
- Implement agent handoffs
- Create manager agent
- Build specialized agents

**Topics Covered:**
- Multi-agent design patterns
- Agent handoffs and delegation
- Manager-worker pattern
- Handoff filters and input handling
- Agent communication

**Hands-on Activities:**
1. Create product agent (from Lesson 5)
2. Create shop information agent
3. Build manager agent with handoffs
4. Implement routing logic
5. Test multi-agent interactions

**Code Exercises:**
```python
# Exercise 1: Create specialized agents
def create_product_agent():
    # TODO: Product agent with RAG tool
    pass

def create_shop_agent():
    # TODO: Shop info agent
    pass

# Exercise 2: Manager agent
def create_manager_agent(product_agent, shop_agent):
    # TODO: Manager with handoffs
    pass

# Exercise 3: Custom input filter
def custom_input_filter(input_data: HandoffInputData) -> HandoffInputData:
    # TODO: Filter or modify handoff data
    pass
```

**Deliverables:**
- Three specialized agents
- Manager with routing logic
- Working multi-agent system

**Files to Create:**
- `lessons/lesson-06-multi-agent/README.md`
- `lessons/lesson-06-multi-agent/instructions.md`
- `lessons/lesson-06-multi-agent/exercises/multi_agent.py`
- `lessons/lesson-06-multi-agent/exercises/prompt_templates.py`
- `lessons/lesson-06-multi-agent/solution/agents_complete.py`
- `lessons/lesson-06-multi-agent/solution/prompts.py`

---

### **Lesson 7: External Data Integration**

**Duration:** 1.5 hours

**Learning Goals:**
- Connect to external data sources
- Google Sheets API integration
- Dynamic data retrieval
- Service account authentication

**Topics Covered:**
- Google Sheets API setup
- OAuth2 service accounts
- gspread library
- Dynamic vs static data
- Error handling for external APIs

**Hands-on Activities:**
1. Set up Google Cloud project
2. Create service account credentials
3. Share Google Sheet with service account
4. Implement sheet reading function
5. Create shop information tool

**Code Exercises:**
```python
# Exercise 1: Setup Google Sheets client
def setup_gsheet_client(credentials_path: str):
    # TODO: Authenticate and create client
    pass

# Exercise 2: Read sheet data
def get_sheet_data(sheet_url: str):
    # TODO: Fetch data from Google Sheets
    pass

# Exercise 3: Create tool
@function_tool
def shop_information_rag():
    # TODO: Implement Google Sheets RAG tool
    pass
```

**Deliverables:**
- Google Sheets integration
- Shop information tool
- Updated agent with new tool

**Files to Create:**
- `lessons/lesson-07-external-data/README.md`
- `lessons/lesson-07-external-data/instructions.md`
- `lessons/lesson-07-external-data/exercises/gsheet_integration.py`
- `lessons/lesson-07-external-data/solution/complete_integration.py`
- `lessons/lesson-07-external-data/solution/credentials_setup.md`

---

### **Lesson 8: Building REST API Server**

**Duration:** 2 hours

**Learning Goals:**
- Create Flask API server
- Implement chat endpoint
- Manage conversation threads
- Handle CORS and errors

**Topics Covered:**
- Flask web framework basics
- RESTful API design
- Request/response handling
- Conversation state management
- CORS configuration
- Error handling and validation
- Async/await with asyncio

**Hands-on Activities:**
1. Set up Flask application
2. Create /chat POST endpoint
3. Implement thread-based conversation history
4. Add error handling
5. Test with curl/Postman

**Code Exercises:**
```python
# Exercise 1: Create Flask app
def create_app():
    # TODO: Initialize Flask with CORS
    pass

# Exercise 2: Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    # TODO: Handle chat requests
    pass

# Exercise 3: Conversation history
conversation_history = {}

def manage_conversation(thread_id, new_message):
    # TODO: Manage thread history
    pass
```

**Deliverables:**
- Working Flask API server
- Chat endpoint with agents
- Conversation thread management

**Files to Create:**
- `lessons/lesson-08-api-server/README.md`
- `lessons/lesson-08-api-server/instructions.md`
- `lessons/lesson-08-api-server/exercises/flask_server.py`
- `lessons/lesson-08-api-server/solution/serve_complete.py`
- `lessons/lesson-08-api-server/solution/test_api.sh`

---

### **Lesson 9: Interactive UI with Streamlit**

**Duration:** 2 hours

**Learning Goals:**
- Build chat interface with Streamlit
- Manage UI state
- Connect to backend API
- Design conversational UX

**Topics Covered:**
- Streamlit framework basics
- Session state management
- Chat UI components
- API integration from frontend
- Custom CSS styling
- User experience design

**Hands-on Activities:**
1. Set up Streamlit app
2. Create chat message display
3. Implement input form
4. Connect to Flask backend
5. Add conversation threading
6. Style with custom CSS

**Code Exercises:**
```python
# Exercise 1: Initialize session state
def init_session_state():
    # TODO: Set up session variables
    pass

# Exercise 2: Display messages
def display_messages():
    # TODO: Render chat history
    pass

# Exercise 3: Send message
def send_message(user_input):
    # TODO: Call API and update UI
    pass
```

**Deliverables:**
- Streamlit chat interface
- Connected to backend API
- Styled conversation UI

**Files to Create:**
- `lessons/lesson-09-ui-client/README.md`
- `lessons/lesson-09-ui-client/instructions.md`
- `lessons/lesson-09-ui-client/exercises/streamlit_app.py`
- `lessons/lesson-09-ui-client/solution/client_complete.py`
- `lessons/lesson-09-ui-client/solution/custom_styles.md`

---

### **Lesson 10: Open Source Models with LiteLLM**

**Duration:** 2 hours

**Learning Goals:**
- Understand OSS LLM alternatives
- Use LiteLLM for model abstraction
- Integrate Together.ai and Groq
- Configure different models per agent

**Topics Covered:**
- Open source LLM landscape
- LiteLLM unified interface
- Together.ai (Kimi model)
- Groq (GPT-OSS models)
- Model selection strategies
- Cost optimization

**Hands-on Activities:**
1. Set up Together.ai and Groq API keys
2. Install litellm extension
3. Create LitellmModel instances
4. Configure agents with different models
5. Compare performance and costs

**Code Exercises:**
```python
# Exercise 1: Create LiteLLM model
def create_litellm_model(provider, model_name, api_key):
    # TODO: Initialize LitellmModel
    pass

# Exercise 2: Configure agents with OSS models
def create_oss_agents():
    # TODO: Create agents with different models
    pass

# Exercise 3: Model settings
def configure_model_settings():
    # TODO: Set tool_choice and other settings
    pass
```

**Deliverables:**
- Multi-provider model setup
- Agents using OSS models
- Performance comparison report

**Files to Create:**
- `lessons/lesson-10-oss-models/README.md`
- `lessons/lesson-10-oss-models/instructions.md`
- `lessons/lesson-10-oss-models/exercises/oss_integration.py`
- `lessons/lesson-10-oss-models/solution/oss_serve_complete.py`
- `lessons/lesson-10-oss-models/solution/model_comparison.md`

---

## Final Project

### **Capstone: Build Your Own Multi-Agent RAG System**

**Duration:** 4-6 hours

**Project Requirements:**
1. Choose a domain (e-commerce, customer service, documentation, etc.)
2. Design 3+ specialized agents
3. Implement RAG with custom dataset
4. Build REST API server
5. Create interactive UI
6. (Optional) Use OSS models
7. Write documentation

**Evaluation Criteria:**
- Functionality (40%)
  - All agents working correctly
  - RAG retrieval accuracy
  - Proper agent routing
- Code Quality (30%)
  - Clean, organized code
  - Error handling
  - Best practices
- Documentation (20%)
  - Clear README
  - API documentation
  - Setup instructions
- Creativity (10%)
  - Unique use case
  - Additional features

**Starter Code Provided:**
- Basic project structure
- Template files
- Sample dataset format

**Reference Solution:**
- Complete implementation (current codebase)
- Best practices documentation
- Deployment guide

**Files to Create:**
- `final-project/README.md` - Project overview
- `final-project/requirements.md` - Detailed requirements
- `final-project/starter-code/` - Template files
- `final-project/reference-solution/` - Current codebase moved here
- `final-project/evaluation-rubric.md` - Grading criteria

---

## Supporting Documentation

### **docs/architecture.md**
- Multi-agent system architecture
- RAG pipeline flow diagrams
- Data flow between components
- Design patterns and best practices

### **docs/best-practices.md**
- Code organization
- Error handling strategies
- Testing approaches
- Security considerations
- Performance optimization

### **docs/troubleshooting.md**
- Common errors and solutions
- API key issues
- ChromaDB persistence problems
- Agent handoff debugging
- CORS and networking issues

### **docs/resources.md**
- OpenAI Agents SDK documentation
- ChromaDB documentation
- LiteLLM documentation
- Research papers on RAG
- Community resources

---

## Implementation Steps

### Phase 1: Repository Restructure (Week 1)
1. Create new folder structure
2. Move existing code to `final-project/reference-solution/`
3. Update main README.md with learning path
4. Create .env.example template

### Phase 2: Lessons 1-5 (Week 2-3)
1. Write lesson content (README + instructions)
2. Create exercises with TODOs
3. Implement solution code
4. Test all exercises
5. Add quiz/checkpoint questions

### Phase 3: Lessons 6-10 (Week 4-5)
1. Write lesson content (README + instructions)
2. Create exercises with TODOs
3. Implement solution code
4. Test all exercises
5. Add quiz/checkpoint questions

### Phase 4: Final Project & Docs (Week 6)
1. Create final project requirements
2. Build starter code templates
3. Write supporting documentation
4. Create troubleshooting guide
5. Add resources and references

### Phase 5: Testing & Refinement (Week 7)
1. User testing with beta learners
2. Collect feedback
3. Refine instructions
4. Fix bugs and issues
5. Add FAQ section

---

## Success Metrics

### Learning Outcomes
- 90%+ of students complete Lessons 1-5
- 70%+ complete all 10 lessons
- 50%+ complete final project
- Average project score > 75%

### Code Quality
- All solutions run without errors
- Comprehensive error handling
- Well-documented code
- Follow Python best practices

### Student Feedback
- Clear instructions (>4/5 rating)
- Appropriate difficulty progression
- Helpful examples and exercises
- Good documentation

---

## Additional Features to Consider

### Advanced Topics (Optional Lessons)
- **Lesson 11:** Advanced prompt engineering
- **Lesson 12:** Agent memory and context management
- **Lesson 13:** Testing and evaluation metrics
- **Lesson 14:** Production deployment (Docker, cloud)
- **Lesson 15:** Monitoring and observability

### Interactive Elements
- Jupyter notebooks for exploratory lessons
- Video walkthroughs (screencasts)
- Interactive quizzes
- Code challenges/competitions
- Community forum/Discord

### Assessment Tools
- Automated testing for exercises
- Code quality checker
- Project submission system
- Peer review guidelines

---

## Timeline

| Week | Tasks | Deliverables |
|------|-------|--------------|
| 1 | Repository restructure | New folder structure, updated README |
| 2-3 | Lessons 1-5 | Complete lessons with exercises |
| 4-5 | Lessons 6-10 | Complete lessons with exercises |
| 6 | Final project & docs | Project template, documentation |
| 7 | Testing & refinement | Polished learning materials |
| 8 | Launch | Published repository |

---

## Maintenance Plan

### Regular Updates
- Monthly: Update dependencies
- Quarterly: Refresh with new SDK features
- Bi-annually: Major content review

### Community Engagement
- Issue tracking for learner questions
- Pull requests for improvements
- Discussion forum
- Office hours/Q&A sessions

---

## Conclusion

This restructuring plan transforms the current codebase into a comprehensive, progressive learning resource. By breaking down complex concepts into digestible lessons with hands-on exercises, students will gain practical experience building production-ready agentic RAG systems.

The modular structure allows students to learn at their own pace while the final project ensures they can synthesize all concepts into a complete application.
