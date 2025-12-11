from langchain.chat_models import BaseChatModel
from langgraph.graph import StateGraph, END, START
# from langgraph.checkpoint.memory import InMemorySaver  
from langchain.tools import tool
from langchain.agents import create_agent

from langchain.messages import HumanMessage
from sqlalchemy.orm import Session
from app.schema.chat_state import ChatState
from app.schema.customer import CustomerSchema
from app.repository.find_customer import find_customer_by_telephone, create_customer
from app.repository.stock_check import check_stock


def create_check_stock_tool(session: Session):
    @tool
    def check_stock_tool(product_name: str) -> str:
        """A tool to find list of stock of product

        Args:
            product_name (str): Query for product name

        Returns:
            str: Response, it might contain the list of product or not
        """
        stocks = check_stock(session, product_name)
        list_of_stocks = []
        if stocks:
            for stock in stocks:
                list_of_stocks.append(f"{stock.id}-{stock.product.name}-{stock.quantity}")
            stocks_str = "\n".join(list_of_stocks)
            response = f"Stok untuk produk {product_name} adalah sebagai berikut:\n {stocks_str}"
        else:
            response = f"Maaf, produk {product_name} tidak ditemukan dalam inventaris kami."
        return response
    return check_stock_tool


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
        tools = [create_check_stock_tool(self.session)]
        agent = create_agent(self.chat_model, tools, system_prompt="Anda adalah asisten layanan pelanggan yang ramah dan membantu. Anda dapat membantu pelanggan dengan pertanyaan mereka tentang produk dan layanan kami. Jika pelanggan menanyakan tentang ketersediaan produk, gunakan alat pemeriksaan stok untuk memberikan informasi yang akurat.")
        updated_state = agent.invoke(    {"messages": [{"role": "user", "content": state.user_chat}]},
)
        print(updated_state)
        state.agent_response = updated_state
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
    
    