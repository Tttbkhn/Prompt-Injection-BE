# Prompt-Injection-BE
Backend for AI Prompt Injection Project. Responsible for the API, Integrations

### Steps to Set Up the Ollama Environment

#### 1. **Download and Install Ollama Environment To Run Smollm Model**
   - Ollama provides a local environment where you can run models like `smollm` directly on your machine. To install Ollama, follow these steps:

   - **For macOS**:
     1. Open your terminal and run the following command to install the Ollama environment:
        ```bash
        brew install ollama
        ```

   - **For Windows**:
     1. Go to the [Ollama download page](https://ollama.com) and download the installer for Windows.
     2. Follow the on-screen instructions to install the Ollama environment.

#### 2. **Pull the `smollm` Model**
   - Once you have the Ollama environment installed, you can pull the `smollm` model to your local environment.
   - Run the following command to download the `smollm` model:
     ```bash
     ollama pull smollm
     ```

   - This will download the `smollm` model locally, and it will be ready to be used in your Python code.

#### 3. **Run the `smollm` Model**
   - After pulling the `smollm` model, you can now run it.
   - In the terminal, run the following command to start the `smollm` model:
     ```bash
     ollama run smollm
     ```

   - This will launch the `smollm` model, and it will be ready to accept queries.

#### 4. **Run Your Python Code**
   - After downloading the `smollm` model and running it, you can now execute your Python script.

   - In the same terminal or a new terminal window, navigate to the directory where your Python script is located and run:
     ```bash
     python smollm.py
     ```

   - When prompted, you can input your query, and the `smollm` model will respond via the Ollama environment.

### Full Instructions Example:

1. **Install Ollama**:
   ```bash
   brew install ollama  # For macOS
   ```

2. **Pull the `smollm` model**:
   ```bash
   ollama pull smollm
   ```

3. **Run the `smollm` model**:
   ```bash
   ollama run smollm
   ```

4. **Run your Python script**:
   ```bash
   python smollm.py
   ```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---