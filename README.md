# SMSenger Bridge

## Example

![Preview1](./images/woebot.jpg)
![Preview2](./images/cell.jpg)

## Prerequisites

- A Twilio account with a static 2-way SMS-enabled phone number (the Account SID and Auth token ready for you to use)
- A Facebook Messenger account

## Install instructions
I assume you know how to download/clone the repository.

First, create a virtualenv at the root of the project. (Optional)
```
cd /project/path/SMSenger-Bridge
virtualenv .
```

Activate the virtualenv (Optional)
```
./Scripts/activate
```

Install the requirements using pip
```
pip install -r requirements.txt
```

Duplicate the `.env.example` file and name it `.env`. Fill all the data in it with yours. _Note: TWILIO_TO_NUMBER is your own cellphone number, not the twilio one. Make sure it's a full number, including the + and country code_

Finally, run `main.py`
```
python main.py
```

## Setup
Once installed and running...

1. Open port 5000 in your firewall and add a port forward rule so it is accessible from the outside world
2. Go to your twilio SMS webhook (Phone Numbers => Manage Numbers => Active Numbers => your purchased number)
3. Paste your IP:port/sms link (looks like http://155.73.2.44:5000/sms) in the "A MESSAGE COMES IN" field

## How to use
Once twilio is setup...

All the messages you are sent through facebook messenger will be sent to you via SMS (note that you pay PER SMS in twilio and PER NUMBER)

If you want to talk to someone, send a message that looks like this: `@RECIPIENT NAME: Hello!`
the `@RECIPIENT NAME: ` part can be left out if you want to send a message to the same person many times in a row.

## Future of the project
For now, the next steps for the project are:

1. Make an "SMS Provider" interface for supporting more than twilio as a provider (medium priority)
2. Move the direct client accesses in the listeners to message queues and queue handlers (one for TO_SMS, one for TO_MESSENGER) (medium priority)
3. Find a more elegant way to put the API online than ngrok (low priority)
4. Find a cheaper SMS provider (with nice APIs available? that'd be rad. I think Amazon SNS supports SMS and is cheaper, might be useful to look into.) (high priority)
5. Add tests (medium priority)
6. Add CI (Circle CI maybe?) for automatic testing (low priority)
7. Support group chat (low priority)
8. Make the recipient search function cleverer (it sometimes picks strangers with similar names and does not prioritize messenger contacts over facebook contacts. It can also not search for messenger-only accounts) (high priority)