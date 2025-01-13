# Gmail Email Reader and Vector Storage System

This project retrieves emails from Gmail, extracts and cleans the email content, and stores the email data as vector embeddings using `Chroma` for retrieval. The cleaned email content is also saved locally as text files.

## Features
- Connects to Gmail API to read emails.
- Extracts plain text and cleans content using `Ollama` LLM for formatting.
- Saves cleaned emails to local text files.
- Embeds cleaned content and saves it to a `Chroma` vector store for semantic retrieval.

---

## Prerequisites

### Libraries and APIs
Ensure you have the following dependencies installed:

- `google-api-python-client`
- `google-auth`
- `google-auth-oauthlib`
- `google-auth-httplib2`
- `langchain`
- `chroma` (VectorStore)
- `ollama`
- `bs4` (BeautifulSoup)

Install dependencies using pip:
```bash
pip install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2 beautifulsoup4 langchain chromadb ollama
```

### Credentials Setup
1. **Enable Gmail API:** Go to the [Google Cloud Console](https://console.cloud.google.com/) and enable the Gmail API.
2. **Download OAuth2 credentials:** Create credentials for an OAuth 2.0 client and download the JSON file (e.g., `client_secret.json`).
3. **Place the credentials JSON file** at the path specified in `cred_path`.

---

## File Structure
```
.
├── main.py            # Main Python script for execution
├── transform.py       # Contains content cleaning and parsing functions
├── data.py            # Contains email extraction functions
├── chroma.py          # Contains vector store embedding functions
├── config.py          # Configuration file for constants
├── vectorstore_email_db/  # Directory to store Chroma database
├── emails_txt/        # Directory to store local text files of emails
└── token.json         # Stores access and refresh tokens
```

---

## Configuration

- `SCOPES`: Defines the Gmail API access scope.
- `output_dir`: Directory path for storing email text files.
- `cred_path`: Path to the OAuth 2.0 credentials JSON.

---

## Running the Application

### Steps:
1. Modify `config.py` to set the correct `cred_path`, `SCOPES`, and `output_dir`.
2. Run the main script:
   ```bash
   python main.py
   ```
3. Authenticate via the URL if prompted (for first-time runs).
4. The program will fetch inbox emails (default `maxResults` can be modified in `read_emails_from_google_api`).

---

## Explanation of Functions

### `download_creds(creds)`
- Handles the OAuth2 authentication flow.
- Refreshes expired credentials or runs a local server for login.

### `read_emails_from_google_api(maxResults)`
- Initializes Gmail API credentials and builds the service.
- Retrieves a list of inbox emails.
- Calls `obtain_email_details` from `data.py` to extract subject, sender, and body.
- Calls `parse_content` (from `transform.py`) to clean the content.
- Calls `clean_content_with_ollama` (from `transform.py`) to further refine text using LLM.
- Saves cleaned emails to `output_dir` as text files.
- Converts each cleaned email into a `Document` object for embedding.
- Calls `store_to_chroma` (from `chroma.py`) to store embeddings in `Chroma`.

### `obtain_email_details(service, message_id)` (from `data.py`)
- Fetches email details (subject, sender, and content) using Gmail API.
- Decodes both plain text and HTML body content.

### `parse_content(content)` (from `transform.py`)
- Parses HTML content and extracts plain text using `BeautifulSoup`.
- Removes extra whitespace and special characters.

### `clean_content_with_ollama(content)` (from `transform.py`)
- Uses `Ollama` LLM to clean text (removes disclaimers, signatures, etc.).

### `store_to_chroma(emails_list)` (from `chroma.py`)
- Splits cleaned text into smaller chunks.
- Converts chunks into vector embeddings using `langchain`.
- Saves the embeddings in a persistent `Chroma` database.

---

## Sample Output

Each email saved to `emails_txt/` directory as:
```
email_{message_id}_original.txt
email_{message_id}.txt
```
Contents of each file:
```
Subject: [Email Subject]
Sender: [Sender Email]
Content:
[Cleaned Email Content]
```

---

## Example Query
Perform retrieval using the Chroma vector store:
```python
retriever = vectorstore.as_retriever(k=4)
print(retriever.invoke("What's on sale at skincare store"))
```
Returns relevant emails related to the query.

---

## Notes
- Ensure correct file path for `client_secret.json`.
- You can modify the query to fetch specific emails (e.g., unread emails).
- Adjust the chunk size and overlap in `RecursiveCharacterTextSplitter` as needed.

---

## Enhancements
- Add error logging for better debugging.
- Implement retry mechanisms for API rate limits.
- Extend to support attachments parsing.

---

## License
This project is licensed under the MIT License.

---

## Contributing
Feel free to submit issues or pull requests for improvements.

---

## References
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Google Cloud Authentication Guide](https://cloud.google.com/docs/authentication/getting-started)
- [LangChain Documentation](https://docs.langchain.com/)

