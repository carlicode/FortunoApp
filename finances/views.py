from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import os
import logging
from dotenv import load_dotenv
from finances.models import Category  

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

logger = logging.getLogger(__name__)

# Leer el token desde las variables de entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Verificar que el token fue cargado correctamente
if not TELEGRAM_TOKEN:
    logger.error("El token de Telegram no está definido. Verifica el archivo .env.")
else:
    logger.info("Token de Telegram cargado correctamente.")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
print(f"Token loaded: {TELEGRAM_TOKEN}")

@csrf_exempt
def telegram_webhook(request):
    """Handles incoming webhook requests from Telegram."""
    if request.method == 'POST':
        try:
            # Parse the raw request body
            raw_body = request.body.decode('utf-8')
            logger.info(f"Raw body received: {raw_body}")
            body = json.loads(raw_body)

            # Extract chat_id and text from the message
            chat_id = body.get('message', {}).get('chat', {}).get('id')
            text = body.get('message', {}).get('text', '')

            if not chat_id:
                logger.error("Failed to retrieve chat_id")
                return JsonResponse({"error": "chat_id not found"}, status=400)

            # Route the commands to their handlers
            if text.startswith('/start'):
                handle_start(chat_id)
            elif text.startswith('/saldo'):
                handle_balance(chat_id)
            elif text.startswith('/ingreso'):
                handle_income(chat_id, text)
            elif text.startswith('/gasto'):
                handle_expense(chat_id, text)
            elif text.startswith('/categorias'):
                handle_categories(chat_id)
            else:
                send_message(chat_id, "Comando no reconocido. Usa /ayuda para ver los comandos disponibles.")

            return JsonResponse({"status": "ok"})
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    else:
        logger.warning("Invalid method on /webhook/")
        return JsonResponse({"error": "Invalid method"}, status=405)


def handle_start(chat_id):
    """Maneja el comando /start para dar la bienvenida al usuario y explicar las funciones del bot."""
    welcome_message = (
        "👋 ¡Bienvenido a FortunoBot!\n\n"
        "Aquí están los comandos que puedes usar:\n"
        "/saldo - Consulta tu saldo actual\n"
        "/ingreso [monto] [categoría] - Registra un ingreso (ej.: /ingreso 500 Sueldo)\n"
        "/gasto [monto] [categoría] - Registra un gasto (ej.: /gasto 100 Comida)\n"
        "/categorias - Lista todas las categorías disponibles\n\n"
        "¡Escribe cualquiera de estos comandos para comenzar! Si necesitas ayuda, usa /ayuda."
    )
    send_message(chat_id, welcome_message)

def send_message(chat_id, text):
    """Sends a message to a specific chat in Telegram."""
    payload = {
        'chat_id': chat_id,
        'text': text,
    }
    response = requests.post(TELEGRAM_API_URL + "/sendMessage", json=payload)
    logger.info(f"Attempting to send message to chat_id: {chat_id}")
    logger.info(f"Telegram response: {response.json()}")
    return response


# Additional command handlers
from finances.models import User, UserBalance, Transaction, Category

def handle_balance(chat_id):
    """Handles the /saldo command."""
    try:
        # Get or create the user's balance record
        user, _ = User.objects.get_or_create(telegram_id=chat_id)
        user_balance, _ = UserBalance.objects.get_or_create(user=user)
        
        send_message(chat_id, f"Tu saldo actual es: {user_balance.balance}")
    except Exception as e:
        logger.error(f"Error in handle_balance: {e}")
        send_message(chat_id, "Ocurrió un error al obtener tu saldo. Por favor, inténtalo de nuevo.")


def handle_income(chat_id, text):
    """Handles the /ingreso command."""
    try:
        _, amount, category_name = text.split()  # Expected format: /ingreso 100 Food
        amount = float(amount)

        # Get or create the user and their balance record
        user, _ = User.objects.get_or_create(telegram_id=chat_id)
        user_balance, _ = UserBalance.objects.get_or_create(user=user)

        # Get or create the category
        category, _ = Category.objects.get_or_create(name=category_name)

        # Create the transaction and update the balance
        Transaction.objects.create(user=user, category=category, type='ingreso', amount=amount)
        user_balance.balance += amount
        user_balance.save()

        send_message(chat_id, f"Ingreso de {amount} registrado en la categoría {category_name}. Nuevo saldo: {user_balance.balance}")
    except ValueError:
        send_message(chat_id, "Por favor, usa el formato: /ingreso [monto] [categoría].")
    except Exception as e:
        logger.error(f"Error in handle_income: {e}")
        send_message(chat_id, "Ocurrió un error al registrar el ingreso. Por favor, inténtalo de nuevo.")


def handle_expense(chat_id, text):
    """Handles the /gasto command."""
    try:
        _, amount, category_name = text.split()  # Expected format: /gasto 50 Transport
        amount = float(amount)

        # Get or create the user and their balance record
        user, _ = User.objects.get_or_create(telegram_id=chat_id)
        user_balance, _ = UserBalance.objects.get_or_create(user=user)

        # Get or create the category
        category, _ = Category.objects.get_or_create(name=category_name)

        # Create the transaction and update the balance
        Transaction.objects.create(user=user, category=category, type='gasto', amount=-amount)
        user_balance.balance -= amount
        user_balance.save()

        send_message(chat_id, f"Gasto de {amount} registrado en la categoría {category_name}. Nuevo saldo: {user_balance.balance}")
    except ValueError:
        send_message(chat_id, "Por favor, usa el formato: /gasto [monto] [categoría].")
    except Exception as e:
        logger.error(f"Error in handle_expense: {e}")
        send_message(chat_id, "Ocurrió un error al registrar el gasto. Por favor, inténtalo de nuevo.")


def handle_categories(chat_id):
    """Handles the /categorias command."""
    try:
        categories = Category.objects.all()
        if categories.exists():
            category_list = "\n".join([c.name for c in categories])
            send_message(chat_id, f"Categorías disponibles:\n{category_list}")
        else:
            send_message(chat_id, "No tienes categorías registradas.")
    except Exception as e:
        logger.error(f"Error in handle_categories: {e}")
        send_message(chat_id, "Ocurrió un error al listar las categorías. Por favor, inténtalo de nuevo.")
