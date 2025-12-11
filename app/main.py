from sqlalchemy.orm import Session
from app.db import create_db_and_tables
from app.infra.llm import get_gemini_llm
from app.config import CONFIG
from app.container import Container
from app.service.chat_service import ChatService

create_db_and_tables()



container = Container()
container.wire(modules=[__name__])
session: Session = container.session()


llm = get_gemini_llm(CONFIG.gemini_key)
chat_service = ChatService(chat_model=llm, session=container.session())
agent = chat_service.agent
# initial_state = ChatState(
#     telephone_number="+1234567890",
#     user_chat="Hello, I need help with my order."
# )
# config = {"configurable": {"thread_id": "abc123"}}

# final_state = chat_service.agent.invoke(initial_state, config=config)
container.shutdown_resources()


