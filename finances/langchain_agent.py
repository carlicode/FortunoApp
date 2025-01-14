from langchain_openai import OpenAI
from langchain.agents import Tool, initialize_agent
from langchain.prompts import PromptTemplate
from finances.models import User, UserBalance, Transaction, Category
import os

openai_api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(temperature=0, openai_api_key=)

# Herramientas del agente
def consultar_saldo(chat_id):
    """Consulta el saldo actual de un usuario registrado en la base de datos."""
    try:
        user = User.objects.get(telegram_id=chat_id)
        user_balance = UserBalance.objects.get(user=user)
        return f"Tu saldo actual es: {user_balance.balance}"
    except User.DoesNotExist:
        return "No tienes un registro en nuestra base de datos. Usa /start para registrarte."

def registrar_ingreso(chat_id, monto, categoria):
    """Registra un ingreso para un usuario específico en una categoría."""
    try:
        user, _ = User.objects.get_or_create(telegram_id=chat_id)
        user_balance, _ = UserBalance.objects.get_or_create(user=user)
        category, _ = Category.objects.get_or_create(name=categoria)

        Transaction.objects.create(user=user, category=category, type="ingreso", amount=monto)
        user_balance.balance += float(monto)
        user_balance.save()

        return f"Ingreso de {monto} registrado en la categoría '{categoria}'. Nuevo saldo: {user_balance.balance}."
    except Exception as e:
        return f"Ocurrió un error: {str(e)}"

def dar_consejo_financiero(pregunta):
    """Usa LangChain para responder preguntas generales sobre finanzas personales."""
    prompt = PromptTemplate(
        input_variables=["pregunta"],
        template="Soy un asesor financiero experto. Responde a la consulta: {pregunta}"
    )
    chain = prompt | llm
    return chain.run(pregunta)

# Configurar herramientas
tools = [
    Tool(
        name="Consultar Saldo",
        func=lambda input_str: consultar_saldo(int(input_str)),
        description=(
            "Consulta el saldo actual de un usuario registrado en la base de datos. "
            "Proporciona el ID del usuario como entrada."
        ),
    ),
    Tool(
        name="Registrar Ingreso",
        func=lambda input_str: registrar_ingreso(*input_str.split(',')),
        description=(
            "Registra un ingreso para un usuario. Entrada esperada: 'chat_id,monto,categoria'."
        ),
    ),
    Tool(
        name="Dar Consejo Financiero",
        func=dar_consejo_financiero,
        description=(
            "Responde preguntas generales sobre finanzas personales. Ejemplo: "
            "'¿Cómo puedo ahorrar más dinero?'"
        ),
    ),
]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
