from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from app.core.config import settings


class LLMService:
    def __init__(self):
        if not settings.OPENAI_API_KEY or not settings.OPENAI_API_BASE_URL:
            raise ValueError("缺少必要的环境变量: OPENAI_API_KEY 或 OPENAI_API_BASE_URL")

        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.LLM_MODEL,
            base_url=settings.OPENAI_API_BASE_URL,
        )

        self.prompts = {
            "general": ChatPromptTemplate.from_template(
                "你是一个AI助手，请根据用户输入回答问题。用户输入：{input}"
            ),
            "product_analysis": ChatPromptTemplate.from_template(
                "你是一个产品分析专家，请分析以下产品信息并提供建议：{input}"
            ),
            "business_advice": ChatPromptTemplate.from_template(
                "你是一个商业顾问，请为以下业务问题提供专业建议：{input}"
            ),
        }

    async def get_response(self, user_input: str, prompt_type: str = "general") -> str:
        prompt = self.prompts.get(prompt_type, self.prompts["general"])
        chain = prompt | self.llm
        response = chain.invoke({"input": user_input})
        return response.content

    def get_available_prompts(self) -> list:
        return list(self.prompts.keys())


llm_service: LLMService | None = None
try:
    llm_service = LLMService()
except Exception as e:
    print(f"LLM服务初始化失败: {e}")
    llm_service = None


