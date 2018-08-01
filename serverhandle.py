from flask import Flask
from flask_ask import Ask, statement, question, session
from awshandle import EC2Manager

app = Flask(__name__)
ask = Ask(app, "/")

ec2_manager = EC2Manager()
server_name_list = ec2_manager.get_all_server_names()


@ask.launch
def server_handler_app():
    return question('Hi there !! I am your server manager. Currently you have %s active servers. '
                    'Would you like me to list them ?' % ec2_manager.get_active_instance_count())


@ask.intent('YesIntent')
def list_servers():
    return question('Following are the names of active servers. %s. Thats all. Would you like \
                    to do something else ?' % ','.join(ec2_manager.get_active_instance_names()))


@ask.intent('CountIntent')
def count_active_servers():
    return question('There are currently %s active servers.' % ec2_manager.get_active_instance_count())


@ask.intent('ListIntent')
def list_active_servers():
    return question('Following are the names of active servers. %s' % '\n'.join(ec2_manager.get_active_instance_names()))


@ask.intent('StartServerIntent', mapping={'server_name': 'server_name'})
def start_server(server_name):
    if server_name:
        server_name = server_name.lower()
    if server_name not in server_name_list:
        return question('%s is not available. Please try once more' % ec2_manager.get_active_instance_names())
    else:
        ec2_manager.start_server(server_name)
        return question('%s server is ready to serve' % ec2_manager.get_active_instance_names())


@ask.intent('StopServerIntent', mapping={'server_name': 'server_name'})
def stop_server(server_name):
    if server_name:
        server_name = server_name.lower()
    if server_name in server_name_list:
        return question('%s is not available. Please try once more' % ec2_manager.get_active_instance_names())
    else:
        ec2_manager.stop_server(server_name)
        return question('%s server has stopped' % ec2_manager.get_active_instance_names())

@ask.intent('MonitorIntent')
def monitor_server(server_name):
    if server_name:
        server_name = server_name.lower()
    if server_name in server_name_list:
        return question('%s is already being monitored' % ec2_manager.get_active_instance_names())
    else:
        ec2_manager.monitor_server(server_name)
        return question('%s server is ready to monitor' % ec2_manager.get_active_instance_names())


@ask.intent('UnmonitorIntent')
def unmonitor_server(server_name):
    print('+++++++++++++++++',server_name, '+++++++++++++++++++')
    if server_name:
        server_name = server_name.lower()
    if server_name in server_name_list:
        return question('%s is already unmonitored. Please try once more' % ec2_manager.get_active_instance_names())
    else:
        ec2_manager.unmonitor_server(server_name)
        return question('%s server is getting unmonitored' % ec2_manager.get_active_instance_names())

    
@ask.intent('AMAZON.CancelIntent')
def cancel_request():
    return statement('Always a pleasure working for you. Have a good day')

@ask.intent('AMAZON.StopIntent')
def stop_app():
    return statement('Always a pleasure working for you. Have a good day')
   

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5001,debug=True)
