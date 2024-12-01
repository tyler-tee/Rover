# Rover: Adoptable Pet Finder (Proof of Concept)

Rover is a proof-of-concept web application that demonstrates how to leverage OpenAI's natural language processing capabilities to facilitate pet adoption. By transforming natural language inputs into actionable parameters for the Petfinder API, Rover makes it easy to search for pets waiting for their forever homes.

The production version of this app is live at [lambdasandlapdogs.com/dogs/rover](https://www.lambdasandlapdogs.com/dogs/rover).

![rover_demo](https://github.com/user-attachments/assets/70458a19-a25f-41a3-9903-9bdbcef6d19e)

---

## Features

- **Natural Language Search**: Users can search for pets using queries like "Find me a golden retriever puppy in New York."
- **Dynamic Results**: Displays adoptable pets with details such as name, breed, age, and photos.
- **Simple Setup**: Designed as an example app for educational purposes, making it easy to deploy and experiment.

---

## Getting Started

### Prerequisites

- **Python** (>= 3.9 recommended)
- **OpenAI API Key**: Required to use OpenAI's API.
- **Petfinder API Key and Secret**: Needed to fetch data from the Petfinder API.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tyler-tee/Rover.git
   cd Rover
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure API keys:
   - Copy the `example_config.json` file from `/config` to `/config/config.json`.
   - Replace placeholder values in `config.json` with your API credentials:
     ```json
     {
       "OPENAI_API_KEY": "your_openai_api_key",
       "PETFINDER_API_KEY": "your_petfinder_api_key",
       "PETFINDER_API_SECRET": "your_petfinder_api_secret"
     }
     ```

4. Run the Flask application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://127.0.0.1:5000`.

---

## Project Structure

```plaintext
Rover/
├── app.py                  # Main Flask application
├── config/                 # Configuration files
│   ├── config.json         # API key configuration
│   └── example_config.json # Example configuration template
├── PetfinderClient/        # Petfinder API client implementation
├── static/                 # Static assets (CSS, JS, images)
├── templates/              # HTML templates for rendering pages
├── requirements.txt        # Python dependencies
└── .gitignore              # Files and directories to ignore in Git
```

---

## Usage

1. Open the web application in your browser.
2. Enter a natural language query, such as:
   - "Find me a Labrador puppy near Chicago."
3. Browse the results and view details about adoptable pets.

---

## API Integration

### OpenAI API

- **Purpose**: Parses natural language input to extract search parameters.
- **Endpoint**: OpenAI's completion or chat API.

### Petfinder API

- **Purpose**: Retrieves data on adoptable pets based on search parameters.
- **Endpoints Used**:
  - `/oauth2/token`: For authentication.
  - `/animals`: To fetch adoptable pet listings.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **OpenAI**: For enabling natural language processing.
- **Petfinder**: For their comprehensive API and database of adoptable pets.
