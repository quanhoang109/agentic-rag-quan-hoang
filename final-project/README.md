# Final Project: Build Your Own Multi-Agent RAG System

## Overview

This capstone project will challenge you to apply everything you've learned throughout the 10 lessons to build a complete, production-ready multi-agent RAG system for a domain of your choice.

## Learning Objectives

By completing this project, you will demonstrate:
- Mastery of RAG pipeline implementation
- Multi-agent system design and orchestration
- API development and deployment
- UI/UX design for conversational interfaces
- Best practices in code organization and documentation

## Project Duration

**Estimated Time:** 4-6 hours (spread over multiple sessions)

## Prerequisites

You should have completed:
- ✅ Lesson 1: Environment Setup
- ✅ Lesson 2: Understanding Embeddings
- ✅ Lesson 3: Vector Database with ChromaDB
- ✅ Lesson 4: Building Basic RAG Pipeline
- ✅ Lesson 5: Single Agent with OpenAI Agents SDK
- ✅ Lesson 6: Multi-Agent Orchestration
- ✅ Lesson 7: External Data Integration
- ✅ Lesson 8: Building REST API Server
- ✅ Lesson 9: Interactive UI with Streamlit
- ✅ Lesson 10: Open Source Models with LiteLLM (optional)

## Project Requirements

### 1. Domain Selection

Choose a domain that interests you. Examples:

**E-commerce:**
- Product recommendations
- Customer support
- Order tracking

**Education:**
- Course recommendations
- Study materials search
- Q&A system

**Healthcare:**
- Symptom checker (informational only)
- Medical information retrieval
- Appointment scheduling

**Documentation:**
- Technical documentation search
- Code examples retrieval
- API reference assistant

**Custom Domain:**
- Your own creative idea!

### 2. System Components (Required)

Your system must include:

#### A. At Least 3 Specialized Agents
- **Manager Agent:** Routes requests to appropriate agents
- **Agent 1:** Handles primary domain queries (with RAG)
- **Agent 2:** Handles secondary domain queries
- **Agent 3+:** Additional specialized functionality

#### B. RAG Implementation
- Custom dataset (minimum 50 documents/entries)
- ChromaDB vector storage
- Proper document preprocessing
- Effective retrieval function

#### C. REST API Server
- Flask or FastAPI
- POST endpoint for chat
- Thread-based conversation management
- Error handling
- CORS support

#### D. Interactive UI
- Streamlit or React
- Chat interface
- Conversation history
- New conversation capability

#### E. Documentation
- README with setup instructions
- Architecture diagram
- API documentation
- Example queries

### 3. Optional Enhancements

Implement one or more of these for extra credit:

- ✨ Use OpenRouter for cost optimization
- ✨ Multi-modal support (images, files)
- ✨ Advanced prompt engineering
- ✨ Agent memory/context management
- ✨ Evaluation metrics and testing
- ✨ Docker deployment
- ✨ Authentication and user management
- ✨ Real-time streaming responses
- ✨ Voice input/output

## Evaluation Criteria

### Functionality (40 points)
- [ ] All agents work correctly (10 pts)
- [ ] RAG retrieval is accurate (10 pts)
- [ ] Proper agent routing/handoffs (10 pts)
- [ ] API handles requests correctly (5 pts)
- [ ] UI is functional and responsive (5 pts)

### Code Quality (30 points)
- [ ] Clean, organized code structure (10 pts)
- [ ] Proper error handling (5 pts)
- [ ] Type hints and documentation (5 pts)
- [ ] Follows best practices (5 pts)
- [ ] No security vulnerabilities (5 pts)

### Documentation (20 points)
- [ ] Clear README with setup instructions (8 pts)
- [ ] Architecture diagram or explanation (4 pts)
- [ ] API documentation (4 pts)
- [ ] Example usage/queries (4 pts)

### Creativity & Innovation (10 points)
- [ ] Unique use case or domain (5 pts)
- [ ] Additional features beyond requirements (5 pts)

**Total: 100 points**

**Grading Scale:**
- 90-100: Excellent
- 80-89: Good
- 70-79: Satisfactory
- 60-69: Needs Improvement
- Below 60: Incomplete

## Getting Started

### Step 1: Choose Your Domain

Think about:
- What interests you?
- What data can you access?
- What problems can you solve?
- What makes it unique?

### Step 2: Design Your System

Create a design document with:
- Domain description
- User personas
- Agent responsibilities
- Data sources
- Example conversations

### Step 3: Prepare Your Data

Collect and prepare your dataset:
- Minimum 50 documents/entries
- Clean and format data
- Create CSV or JSON format
- Plan metadata structure

### Step 4: Use Starter Code

Start from the templates in `starter-code/`:
- Basic project structure
- Template files for each component
- Configuration examples

### Step 5: Implement Components

Build in this order:
1. Data preprocessing
2. RAG pipeline
3. Individual agents
4. Manager agent
5. API server
6. UI client
7. Testing and refinement

### Step 6: Document Everything

As you build:
- Write clear comments
- Update README
- Document API endpoints
- Create usage examples

## Starter Code

The `starter-code/` directory contains:

```
starter-code/
├── README.md           # Starter project README template
├── requirements.txt    # Dependencies list
├── .env.example        # Environment variables template
├── setup.py            # Data loading template
├── rag.py              # RAG functions template
├── prompt.py           # Agent instructions template
├── serve.py            # API server template
├── client.py           # UI client template
└── data/
    └── sample_data.csv # Example data format
```

## Reference Solution

The `reference-solution/` directory contains the complete mobile shop assistant implementation as a working example. You can:
- Study the code structure
- Understand implementation patterns
- See best practices in action
- Use as inspiration (but don't copy!)

**Files in Reference Solution:**
- `serve.py` - Flask API with conversation management
- `rag.py` - RAG implementation with ChromaDB
- `prompt.py` - Agent instructions for all agents
- `setup.py` - Data preprocessing and loading
- `client.py` - Streamlit chat interface
- `oss_serve.py` - Alternative with open source models

## Submission Guidelines

### What to Submit

1. **Source Code**
   - All Python files
   - requirements.txt
   - .env.example (NOT .env!)
   - Data files or links to data

2. **Documentation**
   - README.md
   - Architecture diagram (can be text-based)
   - API documentation
   - Example queries

3. **Demo Video** (Optional)
   - 3-5 minute walkthrough
   - Show key features
   - Demonstrate conversations

### Submission Format

```
your-project-name/
├── README.md
├── requirements.txt
├── .env.example
├── setup.py
├── rag.py
├── prompt.py
├── serve.py
├── client.py
├── data/
│   └── your_data.csv
├── docs/
│   ├── architecture.md
│   └── api.md
└── tests/
    └── test_basic.py
```

### Submission Checklist

Before submitting, ensure:

- [ ] Code runs without errors
- [ ] All dependencies listed in requirements.txt
- [ ] .env.example provided (no real API keys!)
- [ ] README has clear setup instructions
- [ ] Data files included or accessible
- [ ] No sensitive information committed
- [ ] All features demonstrated
- [ ] Documentation is complete

## Example Projects

### Example 1: Restaurant Recommendation System

**Agents:**
- Manager: Routes queries
- Menu Agent: Searches menu items (RAG)
- Reservation Agent: Handles bookings (external API)
- Review Agent: Provides reviews and ratings (RAG)

**Data:**
- 100+ restaurant profiles
- Menus with descriptions
- Customer reviews
- Reservation availability

### Example 2: Tech Support Assistant

**Agents:**
- Manager: Triages issues
- Documentation Agent: Searches docs (RAG)
- Troubleshooting Agent: Guides through solutions (RAG)
- Ticket Agent: Creates support tickets (external system)

**Data:**
- Technical documentation
- Troubleshooting guides
- Common error codes
- Solution articles

### Example 3: Study Buddy

**Agents:**
- Manager: Routes learning queries
- Concept Agent: Explains concepts (RAG)
- Practice Agent: Generates quiz questions
- Progress Agent: Tracks learning progress (database)

**Data:**
- Educational content
- Practice problems
- Concept explanations
- Study guides

## Resources

### Helpful Links
- [OpenAI Agents SDK Examples](https://github.com/openai/openai-agents-sdk)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

### From This Course
- `docs/architecture.md` - System design patterns
- `docs/best-practices.md` - Coding guidelines
- `docs/troubleshooting.md` - Common issues
- `docs/resources.md` - Additional learning materials

## FAQ

**Q: Can I work in a team?**
A: This is typically an individual project, but check with your instructor.

**Q: Can I use the reference solution code?**
A: Use it for reference and understanding, but your implementation should be original.

**Q: What if I don't have enough data?**
A: You can generate synthetic data, use public datasets, or web scraping (with permission).

**Q: Can I use a different framework than Flask/Streamlit?**
A: Yes! As long as you meet the core requirements (API + UI).

**Q: How detailed should my documentation be?**
A: Detailed enough for someone to set up and run your project without asking questions.

**Q: Can I add features beyond requirements?**
A: Absolutely! Innovation is encouraged and earns extra points.

## Getting Help

If you're stuck:

1. **Review Lessons:** Go back to relevant lesson materials
2. **Check Docs:** Review `docs/` for guidance
3. **Reference Solution:** Study the working example
4. **Ask Questions:** Use discussions or office hours
5. **Debug Systematically:** Use the troubleshooting guide

## Timeline Suggestion

**Week 1:**
- Day 1-2: Choose domain, design system
- Day 3-4: Prepare data, build RAG pipeline
- Day 5-6: Implement agents
- Day 7: Testing and bug fixes

**Week 2:**
- Day 1-2: Build API server
- Day 3-4: Create UI
- Day 5-6: Documentation
- Day 7: Final testing and submission

## Good Luck!

This project is your opportunity to showcase what you've learned. Be creative, build something you're proud of, and most importantly, have fun!

Remember: The goal isn't perfection—it's demonstrating understanding and building something that works.

**Questions?** Check `requirements.md` for detailed specifications or ask in discussions.
