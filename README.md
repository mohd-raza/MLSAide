# MLSAide Chatbot

MLSAide is a Streamlit-based chatbot designed to assist Microsoft Learn Student Ambassadors (MLSA) with program-related questions. Try out the [MLSAide](https://mlsaide.streamlit.app/)
chatbot to get answers to all your program-related questions as a Microsoft Learn Student Ambassador.
## Core Files and Their Function

### main.py

This file contains the Streamlit web application for the MLSAide chatbot. It sets up the user interface and manages the chat interaction. Key features include:

- Initializes the chat interface with a title, welcome message, and informative sidebar
- Manages the chat history using Streamlit's session state
- Handles user input through a chat input field
- Displays both user messages and bot responses in a chat-like format
- Uses a cached resource to initialize the answer generation function
- Calls the `get_answer_from_kb` function to generate responses based on user queries

### qdrant.py

This file is responsible for setting up and populating the knowledge base. It processes the source material and prepares it for efficient retrieval. Main functions include:

- `read_data_from_pdf()`: Extracts text content from a specified PDF file
- `get_text_chunks()`: Splits the extracted text into smaller, manageable chunks
- `get_embedding()`: Generates embeddings for text chunks using Azure OpenAI's embedding model
- Creates a Qdrant collection with appropriate vector configurations
- `insert_data()`: Uploads the embedded text chunks to the Qdrant collection
- The `main()` function orchestrates the entire process of reading, processing, and storing the data

### utils.py

This file contains utility functions for generating responses to user queries. It handles the integration between the user interface, the knowledge base, and the AI model. Key components include:

- Sets up connections to Azure OpenAI and Qdrant using environment variables
- `get_answer_from_kb` function:
  - Generates an embedding for the user's query
  - Searches the Qdrant database for relevant context based on the query embedding
  - Constructs a detailed prompt combining the query, retrieved context, and system instructions
  - Uses Azure OpenAI to generate a response based on this prompt
  - Applies rules and formatting to ensure appropriate and helpful responses

Together, these files create a system that ingests knowledge from a PDF, stores it in a vector database, and uses it to generate relevant and accurate responses to user queries about the Microsoft Learn Student Ambassadors program.

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI/ML**:
  - Azure OpenAI API for embeddings and text generation
  - Qdrant for vector similarity search
- **Data Processing**:
  - PyPDF2 for PDF text extraction
  - LangChain for text splitting
- **Other Libraries**:
  - python-dotenv for environment variable management
  - tqdm for progress bars in data processing

## Creator and Developer

MLSAide was created and developed by Mohammed Raza Syed, a Beta Microsoft Learn Student Ambassador who has been an active member of the MLSA INDIA community since 2023. This project was developed to assist fellow students and ambassadors with program-related queries as part of the Microsoft Learn Student Ambassadors program.
