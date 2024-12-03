import json
import logging
import ast
import os
class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        message = record.getMessage()
        try:
            literal_msg = ast.literal_eval(message)
            # Sensible Daten filtern, falls vorhanden
            if 'username' in literal_msg:
                literal_msg['username'] = '***'
            if 'password' in literal_msg:
                literal_msg['password'] = '***'
            if 'id_token' in literal_msg:
                literal_msg['id_token'] = '***'
            if 'access_token' in literal_msg:
                literal_msg['access_token'] = '***'
            if 'client_id' in literal_msg:
                literal_msg['client_id'] = '***'
            # Das modifizierte Dictionary zurück in einen String konvertieren
            record.msg = json.dumps(literal_msg)
        except Exception as e:
            # Wenn die Nachricht kein JSON ist, nichts tun
            logging.error(f"Error filtering sensitive data: {e}")
            pass
        return True

def get_bool_env(var, default=False):
    value = os.getenv(var, default)
    if isinstance(value, str):
        value = value.lower()
        if value in ["1", "true"]:
            return True
        if value in ["0", "false"]:
            return False
    return bool(value)