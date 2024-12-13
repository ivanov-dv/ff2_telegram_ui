from config import BACKEND_URL, BACKEND_TOKEN, AUTH_HEADERS
from utils.backend_client import BackendClient

client = BackendClient(BACKEND_URL, BACKEND_TOKEN, AUTH_HEADERS)