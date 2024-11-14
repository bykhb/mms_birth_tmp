from langchain_openai import ChatOpenAI
import json
import logging
import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_llm() -> ChatOpenAI:
    """Initialize and return LLM instance"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    return ChatOpenAI(
        # model = 'azure/openai/gpt-4o-2024-05-13'
        model = 'anthropic/claude-3-5-sonnet-20240620'
        ,temperature = 0.8 # 여러가지 단어들 나오게 하는거
        ,frequency_penalty = 1.5 # 같은 말 반복 못하게
        ,max_tokens = 4096 # claude는 max_tokens 지정해야 제대로 돌아감
        ,timeout = None
        # ,max_retries = 2
        ,api_key = "sk-gapk-1tQCB4O2KnH5GG68DeUKfjAKQ-vJ9kc9"
        ,base_url = "https://api.platform.a15t.com/v1"
)


def generate_birthday_message(age_group: str, age_characteristics: str, desired_message: str) -> Dict[str, Any]:
    """Generate birthday message using LLM"""
    logger.info(f"Generating message for age group: {age_group}")
    
    try:
        llm = get_llm()
        
        messages = [
            {"role": "system", "content": "You are an AI assistant that creates personalized birthday messages in Korean."},
            {"role": "user", "content": f"""
            다음 정보를 바탕으로 생일 축하 MMS 메시지를 작성해주세요:
            
            연령대: {age_group}
            특성: {age_characteristics}
            메시지 톤: {desired_message}
            
            다음 형식으로 작성해주세요:
            1. 제목: 생일 축하 인사 (한 줄)
            2. 본문: 연령대에 맞는 공감 메시지 (2-3문장)
            3. SK텔레콤 가치: 연결, 사랑, 전달의 가치를 담은 메시지 (1-2문장)
            4. 맺음말: 마무리 인사 (한 줄)
            
            지침:
            - 전체 500자 이내
            - 공손하고 따뜻한 톤 유지
            - '당신' 대신 '고객님' 사용
            - 감동적이고 감성적인 표현 사용
            """}
        ]
        
        logger.info("Sending request to OpenAI")
        response = llm.invoke(messages)
        logger.info("Received response from OpenAI")
        
        # Split response into sections
        content = response.content
        sections = content.split('\n\n')
        
        # Extract message parts
        result = {
            "title": sections[0] if len(sections) > 0 else "생일을 축하드립니다",
            "body": sections[1] if len(sections) > 1 else "",
            "sktvalue": sections[2] if len(sections) > 2 else "SK텔레콤은 언제나 고객님과 함께하겠습니다.",
            "closing": sections[3] if len(sections) > 3 else "행복한 하루 보내세요."
        }
        
        # Combine into full message
        result["full_message"] = "\n\n".join([
            result["title"],
            result["body"],
            result["sktvalue"],
            result["closing"]
        ])
        
        logger.info("Successfully generated message")
        return result
        
    except Exception as e:
        logger.error(f"Error generating message: {str(e)}")
        raise 