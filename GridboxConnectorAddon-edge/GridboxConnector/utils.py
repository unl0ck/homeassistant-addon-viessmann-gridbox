import json
import logging
import ast
import os
import re
class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        message = record.getMessage()
        try:
            # Versuche die Nachricht als Python-Dictionary zu parsen
            message_dict = ast.literal_eval(message)
            # Sensible Daten filtern, falls vorhanden
            sensitive_keys = ['username', 'password', 'id_token', 'access_token', 'client_id', 'token']
            for key in sensitive_keys:
                if key in message_dict:
                    message_dict[key] = '***'
            # Das modifizierte Dictionary zurück in einen String konvertieren
            record.msg = str(message_dict)
        except (ValueError, SyntaxError):
            logging.error(f"Error parsing message: {message}")
        except Exception as e:
            logging.error(f"Error filtering sensitive data: {e}")
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