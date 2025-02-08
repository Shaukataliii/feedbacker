from backend import FeedBacker, Mail

app = FeedBacker(config_path='config.yaml', show_logs=False)
mailer = Mail(config_path='config.yaml')

if __name__ == '__main__':
    # Example usage
    review = input('Enter a review: ')
    mail_to = input('Enter receiver mail: ')

    feedback, is_sentiment_negative = app.get_feedback(review)
    
    response = mailer.send_email(mail_to=mail_to, message=feedback, is_receiver_agent=is_sentiment_negative)
    print(f'\nMailing Response: {response}')