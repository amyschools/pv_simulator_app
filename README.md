# PV Energy Meter Simulator

Steps for running:
1. Install RabbitMQ and start the server running. Since RabbitMQ was a requirement for the project, I will assume the
user has it installed and running.
2. Create a virtual environment with `python -m venv venv` and activate it with `source venv/bin/activate`
2. Install the dependency (pika, a RabbitMQ python client) with `pip install -r requirements.txt`
2. In a terminal window, run `python pv_simulator.py`. This will start the pv_simulator listening for messages.
3. In a new terminal window, run `python meter.py`. This will start the meter simulation sending continuous random
watt values between 0-9000 for the pv_simulator to receive. It will continue to send messages every 2 seconds for the
length of one day.
4. The watt measurement sent by the meter will be written into a csv file, along with a timestamp, the watt measurement
converted into kilowatts, and the sum of the powers (meter watts + PV kilowatts).
