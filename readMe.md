
## **Project Description**  
**Feedbacker** is an AI-powered feedback system that classifies user reviews and sends personalized responses via email. It utilizes OpenAI’s GPT-4o for sentiment classification and generates appropriate feedback for positive and neutral reviews. If the review is negative, no response is generated, and an agent is notified. The system also integrates an email-sending functionality using Google SMTP.  

### **Features:**  
- **AI-Powered Sentiment Analysis**: Classifies reviews into positive, neutral, or negative.  
- **Dynamic Feedback Generation**: Generates personalized responses for positive and neutral reviews.  
- **Automated Email System**: Sends feedback emails using a configured SMTP server.  
- **Agent Notification**: If feedback is negative, a predefined message is sent to the support team.  

---

## Installation

### 1. Clone the repository
```sh
git clone https://github.com/yourusername/feedbacker.git
cd feedbacker
```

### 2. Install dependencies
```sh
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file and add your OPENAI_API_KEY and GOOGLE_APP_PASSWORD:
```env
GOOGLE_APP_PASSWORD=your_app_password
OPENAI_API_KEY=your_openai_api_key
```

### 4. Configure `config.yaml`
Modify `config.yaml` to set email settings and prompts. Update the sender email and the rest is optional.

## Usage

Run the application:
```sh
python app.py
```
Enter a review and receiver’s email when prompted.

## Configuration

Modify `config.yaml` to update prompts and email settings.

## License

This project is licensed under the MIT License.

## Author

Developed by [Shaukat Ali Khan](https://github.com/Shaukataliii)
```