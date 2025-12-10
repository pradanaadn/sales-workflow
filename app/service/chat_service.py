from langchain.chat_models import BaseChatModel
from langgraph.graph import StateGraph, END, START
# from langgraph.checkpoint.memory import InMemorySaver  
from langchain.messages import HumanMessage
from sqlalchemy.orm import Session
from app.schema.chat_state import ChatState
from app.schema.customer import CustomerSchema
from app.repository.find_customer import find_customer_by_telephone, create_customer

class ChatService:
    def __init__(self, chat_model: BaseChatModel, session: Session):
        self.chat_model = chat_model
        self.session = session
        self.agent = self.create_chat_graph()
        
    def create_chat_graph(self) -> StateGraph:
        graph = StateGraph(state_schema=ChatState)
        graph.add_node("check_user_exist", self.check_user_exist)
        graph.add_node("chat_node", self.chat)
        graph.add_node("initial_node", self.initial_response)
        graph.add_node("parse_customer_info", self.parse_customer_info)
        graph.add_edge(START, "check_user_exist")
        graph.add_conditional_edges(
            "check_user_exist",
            self.should_greet,
            {
                "greet": "initial_node",
                "chat": "chat_node",
                "parse_customer_info": "parse_customer_info",
            }
        )
        
        graph.add_edge("initial_node", END)
        graph.add_edge("parse_customer_info", END)        
        graph.add_edge("chat_node", END)
        # memory = InMemorySaver()
        return graph.compile()
    
    def check_user_exist(self, state: ChatState) -> bool:
        customer = find_customer_by_telephone(self.session, state.telephone_number)
        if customer:
            state.customer_info = CustomerSchema(
                name=customer.name,
                location=customer.location
            )
        return state
    
    def should_greet(self, state: ChatState) -> str:
        if not state.user_chat or state.user_chat.strip() == "":
            
            return "greet"
        
        if not state.is_known_customer():
            return "parse_customer_info"
        
        return "chat"
    
    def initial_response(self, state: ChatState) -> ChatState:
        if not state.is_known_customer():
            state.agent_response = "Hello! Dengan siapa saya berbicara?"
        if state.is_known_customer():
            state.agent_response = f"Hallo {state.customer_info.name}! Ada yang bisa saya bantu?"
        return state
    
    def chat(self, state: ChatState) -> ChatState:
        updated_state = self.chat_model.invoke([HumanMessage(content=state.user_chat)])
        state.agent_response = updated_state.content
        return state
    
    def parse_customer_info(self, state: ChatState) -> CustomerSchema | None:
        model_structured_output = self.chat_model.with_structured_output(CustomerSchema)
        customer_info = model_structured_output.invoke([HumanMessage(content=state.user_chat)])
        if not isinstance(customer_info, CustomerSchema):
            return state
    
        if customer_info.name:
            state.customer_info.name = customer_info.name
            state.agent_response = f"Hi {customer_info.name}, senang bertemu denganmu! Boleh saya tahu alamat untuk pengirimannya?"
        if customer_info.location:
            state.customer_info.location = customer_info.location
            state.agent_response = "Hi dengan siapa saya berbicara?"
            
        if customer_info.name and customer_info.location:
            create_customer(
                self.session,
                name=customer_info.name,
                location=customer_info.location,
                telephone=state.telephone_number
            )
            state.agent_response = f"Terima kasih {customer_info.name} sudah menghubungi kami! Bisa diceritakan lebih lanjut bagaimana saya bisa membantu Anda hari ini?"
        return state
    
    
from app.infra.llm import get_gemini_llm
from app.config import CONFIG
from app.container import Container


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


