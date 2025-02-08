import os
from dotenv import load_dotenv
import langchain
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnableBranch
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableBranch
from langchain.schema.output_parser import StrOutputParser
from typing import Tuple
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import utils


class FeedBacker:
    def __init__(self, config_path: str = 'config.yaml', show_logs: bool = False) -> None:
        self.config = utils.load_yaml_config(config_path)
        langchain.debug = show_logs
        self._set_things_up()

    def _set_things_up(self):
        self._prepare_templates()
        self._prepare_model()
        self._prepare_chain()

    def _prepare_templates(self) -> None:
        self.classification_template = ChatPromptTemplate.from_messages([
            ('system', self.config['classification_role']),
            ('human', self.config['fb_classification_prompt'])
        ])
        self.positive_fb_template = ChatPromptTemplate.from_messages([
            ('system', self.config['fb_generation_role']),
            ('human', self.config['positive_fb_prompt'])
        ])
        self.neutral_fb_template = ChatPromptTemplate.from_messages([
            ('system', self.config['fb_generation_role']),
            ('human', self.config['neutral_fb_prompt'])
        ])

    def _prepare_model(self) -> None:
        load_dotenv()
        self.model = ChatOpenAI(
            model='gpt-4o',
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2
        )

    def _prepare_chain(self) -> None:
        branches = RunnableBranch(
            (
                lambda x: 'positive' in x.lower(),
                self.positive_fb_template | self.model | StrOutputParser(),
            ),
            self.neutral_fb_template | self.model | StrOutputParser()
        )

        self.classification_chain = self.classification_template | self.model | StrOutputParser()
        self.chain = branches

    def get_feedback(self, review: str) -> Tuple[str, bool]:
        '''Returns (message, is_sentiment_negative). Message will be empty when sentiment is negative.
        '''
        sentiment = self.classification_chain.invoke({'review': review})
        if 'negative' in sentiment.lower():
            return ('', True)
        else:
            message = self.chain.invoke(sentiment)
            return(message, False)
    

class Mail:
    def __init__(self, config_path: str = 'config.yaml'):
        config = utils.load_yaml_config(config_path)
        self.sender_email = config['SENDER_EMAIL']
        self.customer_subject = config['CUSTOMER_SUBJECT']
        self.agent_subject = config['AGENT_SUBJECT']
        self.agent_message = config['AGENT_MESSAGE']
        self.app_password = os.getenv('GOOGLE_APP_PASSWORD')

    def send_email(self, mail_to: str, message: str, is_receiver_agent: bool = False) -> str:
        '''Sends mail using google smtp server. Uses predefined mail for the agent if he is the receiver.
        '''
        subject = self.agent_subject if is_receiver_agent else self.customer_subject
        message = self.agent_message if is_receiver_agent else message
        mail = self._prepare_mail(mail_to, subject, message)

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.sender_email, self.app_password)
                server.sendmail(self.sender_email, mail_to, mail.as_string())
            return f"Email sent successfully! \nIt was: \n{mail}"
        except Exception as e:
            return f"An error occured while sending mail. Error: {e}"

    def _prepare_mail(self, mail_to: str, subject: str, message: str) -> MIMEMultipart:
        mail = MIMEMultipart()
        mail["From"] = self.sender_email
        mail["To"] = mail_to
        mail["Subject"] = subject

        body = message
        mail.attach(MIMEText(body, "plain"))
        return mail
