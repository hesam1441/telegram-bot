# Telegram Bot for Contact and Order Management

This project is a Telegram bot built using Python and the `python-telegram-bot` library. The bot allows users to send text-based contact requests, place orders, or retrieve a phone number for direct contact. It integrates with Gmail's SMTP server to send emails with user-submitted information.

## Features
- **Text Contact**: Users can submit their name, phone number, and message, which are sent via email.
- **Order Placement**: Users can place orders by providing their name, contact details, product name, and quantity, which are sent via email.
- **Phone Contact**: Displays a phone number for direct contact.
- **Cancel Operation**: Users can cancel ongoing conversations.
- **Multilingual Support**: The bot uses Persian (Farsi) for user interaction.

## Prerequisites
- Python 3.7+
- A Telegram account and a bot token from [BotFather](https://t.me/BotFather)
- A Gmail account with an App Password for SMTP access

## Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   Ensure you have the required packages listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` includes:
   - `python-telegram-bot==20.3`
   - `httpx`

4. **Configure Environment**
   Update the `bot.py` file with your credentials:
   - `BOT_TOKEN`: Your Telegram bot token from BotFather.
   - `EMAIL_ADDRESS`: Your Gmail email address.
   - `EMAIL_PASSWORD`: Your Gmail App Password (not your regular password; generate one from Gmail's security settings).
   - `RECEIVER_EMAIL`: The email address where contact and order details will be sent.

   **Note**: For security, consider using environment variables or a configuration file instead of hardcoding credentials.

## Usage

1. **Run the Bot**
   ```bash
   python bot.py
   ```

2. **Interact with the Bot**
   - Start the bot by sending `/start` in Telegram.
   - Choose from the main menu:
     - 📞 **تماس متنی** (Text Contact): Submit name, phone number, and message.
     - 🛒 **ثبت سفارش** (Place Order): Submit name, contact details, product, and quantity.
     - 📱 **تماس تلفنی** (Phone Contact): Get the manager's phone number.
   - Use `/cancel` to exit any ongoing conversation.

3. **Email Notifications**
   - Contact and order details are sent to the configured `RECEIVER_EMAIL` via Gmail's SMTP server.
   - Check the logs for email success or failure messages.

## Files
- `bot.py`: The main bot script implementing the Telegram bot logic and email functionality.
- `requirements.txt`: Lists the required Python packages.

## Notes
- Ensure your Gmail account has "2-Step Verification" enabled and generate an App Password for `EMAIL_PASSWORD`.
- The bot uses Persian (Farsi) for user interaction, as seen in the menu and prompts.
- Logs are generated with timestamps and error details for debugging.
- The bot uses `smtplib` for email functionality, which requires a secure SSL connection to Gmail's SMTP server (`smtp.gmail.com:465`).

## Troubleshooting
- **Bot Not Responding**: Verify the `BOT_TOKEN` and ensure the bot is added to your Telegram.
- **Email Errors**: Check the `EMAIL_ADDRESS` and `EMAIL_PASSWORD`. Ensure the App Password is correct and that Gmail's security settings allow less secure apps or App Passwords.
- **Dependency Issues**: Ensure all packages in `requirements.txt` are installed correctly.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details (if applicable).

## Contact
For issues or contributions, please open an issue or submit a pull request on the repository.