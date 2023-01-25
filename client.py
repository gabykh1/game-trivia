import socket
import chatlib

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


# HELPER SOCKET METHODS
def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    msg = chatlib.build_message(code, data)
    conn.send(msg.encode())


# Implement Code
def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """

    server_msg = conn.recv(1024).decode()
    cmd, data = chatlib.parse_message(server_msg)

    return cmd, data


def connect():  # connecting to the socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    return client_socket


def error_and_exit(error_msg):  # exit the loop when error is occurred
    print(error_msg)
    exit()


def build_send_recv_parse(conn, code, data=''):
    build_and_send_message(conn, code, data)
    data, msg_code = recv_message_and_parse(conn)
    return data, msg_code


def get_score(conn):
    data, msg_code = build_send_recv_parse(conn, 'MY_SCORE')
    return data, msg_code


def get_high_score(conn):
    data, msg_code = build_send_recv_parse(conn, 'HIGHSCORE')
    return data, msg_code


def play_question(conn):
    data, msg_code1 = build_send_recv_parse(conn, 'GET_QUESTION')
    if data == 'NO_QUESTIONS':
        print('oh my you run out of questions')
    id_question = msg_code1.split('#')[0]
    question = msg_code1.split('#')[2:]
    print('the question is: ', msg_code1.split('#')[1])
    counter = 1
    for question in question:
        print('{}.\t\t{}'.format(counter, question))
        counter += 1
    answer = 0
    while answer not in ['1', '2', '3', '4']:
        answer = input('choose your answer[1-4]: ')
    data, msg_code2 = build_send_recv_parse(conn, 'SEND_ANSWER', '#'.join((id_question, answer)))
    if data == 'WRONG_ANSWER':
        print("wrong :(, i'm sure you will succeed in the next question\n the write answer was", msg_code2)
    elif data == 'CORRECT_ANSWER':
        print('CORRECT <3, YOU ARE THE BEST!')

def get_logged_users(conn):
    data, msg_code = build_send_recv_parse(conn, 'LOGGED')
    print('logged users: {}'.format(msg_code))


def login(conn):
    """
    checks if the user have been successfully logged in, and if not the user starts again
    :param conn: the socket subject
    :return: nothing
    """
    while True:
        username = input("Please enter username: \n")
        password = input('Please enter password: \n')

        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], "#".join((username, password)))
        cmd, data = recv_message_and_parse(conn)

        if cmd != 'LOGIN_OK':
            error_and_exit('ERROR! login failed, try again :)')
        else:
            print("you've been successfully logged in")
            break


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT['logout_msg'], "")
    print('goodbye :)')


def main():
    socket = connect()
    login(socket)
    print("HI THERE! \nwhat would you like to do?\n"
          "p\t\tplay game\n"
          "s\t\tyour score\n"
          "h\t\tget high score\n"
          "l\t\tget logged users\n"
          "q\t\tquit")

    while True:
        choice = input('please enter your choice: ')
        if choice.lower() == 's' or choice == 'your score':
            print(get_score(socket)[0] + ' is ' + get_score(socket)[1])
        elif choice.lower() == 'h' or choice == 'high score':
            print(get_high_score(socket)[0] + ' is ' + get_high_score(socket)[1])
        elif choice.lower() == 'p' or choice == 'play game':
            play_question(socket)
        elif choice.lower() == 'l' or choice == 'logged users':
            get_logged_users(socket)
        elif choice.lower() == 'q' or choice == 'quit':
            break

    logout(socket)
    socket.close()


if __name__ == '__main__':
    main()


