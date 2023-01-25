# Protocol Constants
CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages
# In this dictionary we will have all the client and server command names
PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT",
    "logged_msg": "LOGGED",  # all the players that are online
    "get_question_msg": "GET_QUESTION",  # ask for question
    "send_answer_msg": "SEND_ANSWER",  # send the answer to the question
    "my_score_msg": "MY_SCORE",  # shows the score of the player
    "high_score_msg": "HIGHSCORE"  # shows the highest score in the server
}

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",  # response to logged message
    "logged_answer_msg": "LOGGED_ANSWER",  # response to logged message - all the players that are online
    'your_question_msg': 'YOUR_QUESTION',  # response to get_question message
    'correct_answer_msg': 'CORRECT_ANSWER',  # response to send_answer if it's correct
    'wrong_answer_msg': 'WRONG_ANSWER',  # response to send_answer if it's wrong
    'your_score_msg': 'YOUR_SCORE',  # response to my_score - sends the score
    'all_score_msg': 'ALL_SCORE',  # response to high_score - sends the table of users with the highest scores
    'error_msg': 'ERROR',  # error message that says the connection will be lost soon
    'no_question_msg': 'NO_QUESTION'  # response to get_question - END OF QUESTION
}  # ..  Add more commands if needed

# Other constants
ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    """
Gets command name (str) and data field (str) and creates a valid protocol message
    :return: Returns: str, or None if error occurred
    """

    if (cmd in PROTOCOL_CLIENT.values() or cmd in PROTOCOL_SERVER.values()) and len(data) <= 9999:
        if cmd == 'LOGIN' or cmd == 'SEND_ANSWER':
            return DELIMITER.join(['{message: <16}'.format(message=cmd), str(len(data)).zfill(4), data])
        else:
            return DELIMITER.join(['{message: <16}'.format(message=cmd), '0'.zfill(4), ''])


def parse_message(data):
    """
    Parses protocol message and returns command name and data field
    :return: cmd (str), data (str). If some error occured, returns None, None
    """
    cmd = None
    msg = None
    split_data = data.split(DELIMITER)
    if len(split_data) == 3 and \
            split_data[1].strip().isnumeric() and \
            len(split_data[0]) == 16 and \
            split_data[0].strip() in (list(PROTOCOL_CLIENT.values()) + list(PROTOCOL_SERVER.values())) and \
            len(split_data[1]) == 4 and \
            ((len(split_data[-1]) == 0 and len(split_data[1].lstrip('0')) == 0) or int(split_data[1].lstrip('0')) == len(split_data[2])):
        cmd = split_data[0].strip()
        msg = split_data[2]
    return cmd, msg


def split_data(string, num_hashtag):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    :return:list of fields if all ok. If some error occured, returns None
    """
    return string.split(DATA_DELIMITER, num_hashtag) if string.count(DATA_DELIMITER) == num_hashtag else None


def join_data(string):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter. 
    :return: string that looks like cell1#cell2#cell3
    """
    return DATA_DELIMITER.join(list(map(str, string)))