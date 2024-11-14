import streamlit as st
from utils.llm_utils import generate_birthday_message
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Age group definitions
AGE_GROUPS = {
    "대학생 및 초기 사회 진출기": {
        "age_range": "20-25세",
        "characteristics": "대학 생활, 취업 준비기",
        "desired_message": "미래에 대한 불안감이 많기 때문에, 응원과 격려의 말"
    },
    "청년 직장인 및 결혼 준비기": {
        "age_range": "26-32세",
        "characteristics": "취업, 커리어 초기, 연애 및 결혼 준비",
        "desired_message": "커리어 초기와 연애 및 결혼 준비로 바쁜 시기라, 지지와 사랑의 메시지"
    },
    "결혼 및 가족 형성기": {
        "age_range": "33-39세",
        "characteristics": "결혼, 육아 시작, 커리어 발전기",
        "desired_message": "가족과 일에 대한 격려와 감사를 표현하는 말"
    },
    "자녀 양육 및 경력 성숙기": {
        "age_range": "40-49세",
        "characteristics": "자녀 교육, 커리어 안정화, 부모 부양 시작",
        "desired_message": "자녀 교육과 커리어 안정화 시기로, 노력에 대한 인정과 지지를 원하는 시기"
    },
    "중년 전환기": {
        "age_range": "50-58세",
        "characteristics": "자녀 독립 준비, 노후 준비 시작, 커리어 절정기",
        "desired_message": "가족과의 관계와 자신의 성취에 대한 인정"
    },
    "은퇴 준비 및 전환기": {
        "age_range": "59-64세",
        "characteristics": "은퇴 준비, 제2의 인생 설계, 손주 돌봄",
        "desired_message": "자신의 노고와 헌신에 대한 감사와 미래에 대한 긍정적인 메시지"
    },
    "노년기": {
        "age_range": "65-75세",
        "characteristics": "은퇴 생활, 건강 관리, 여가 활동",
        "desired_message": "그 동안의 고생을 인정하고, 앞으로의 건강과 행복을 기원하는 말"
    }
}

def create_message_with_progress():
    """Create message with progress bar"""
    progress_text = "메시지 생성 중..."
    my_bar = st.progress(0, text=progress_text)
    
    try:
        # Progress bar animation
        for percent_complete in range(0, 101, 20):
            time.sleep(0.1)  # Simulate processing time
            my_bar.progress(percent_complete, text=progress_text)
        
        # Generate message
        selected_info = AGE_GROUPS[st.session_state.selected_age_group]
        message = generate_birthday_message(
            age_group=st.session_state.selected_age_group,
            age_characteristics=selected_info['characteristics'],
            desired_message=selected_info['desired_message']
        )
        
        # Complete progress bar
        my_bar.progress(100, text="메시지 생성 완료!")
        time.sleep(0.5)  # Short pause to show completion
        my_bar.empty()  # Remove progress bar
        
        return message
        
    except Exception as e:
        my_bar.empty()
        raise e

# Page config
st.set_page_config(
    page_title="생일 메시지 생성기",
    page_icon="🎂",
    layout="centered"
)

# Title
st.title("🎂 AI 생일 메시지 생성기")
st.markdown("---")

# Initialize session state
if 'selected_age_group' not in st.session_state:
    st.session_state.selected_age_group = None
if 'generated_message' not in st.session_state:
    st.session_state.generated_message = None

# Age group selection using buttons in columns
st.subheader("연령대를 선택해주세요")
col1, col2 = st.columns(2)

# Create buttons for age groups
for idx, (age_group, info) in enumerate(AGE_GROUPS.items()):
    if idx % 2 == 0:
        if col1.button(f"{age_group}\n({info['age_range']})", key=f"btn_{idx}"):
            st.session_state.selected_age_group = age_group
            st.session_state.generated_message = None  # Reset previous message
    else:
        if col2.button(f"{age_group}\n({info['age_range']})", key=f"btn_{idx}"):
            st.session_state.selected_age_group = age_group
            st.session_state.generated_message = None  # Reset previous message

# Show selected age group info and generate message
if st.session_state.selected_age_group:
    st.markdown("---")
    selected_info = AGE_GROUPS[st.session_state.selected_age_group]
    st.info(f"📊 선택된 연령대: {st.session_state.selected_age_group} ({selected_info['age_range']})")
    
    if st.button("메시지 생성하기", key="generate"):
        try:
            message = create_message_with_progress()
            st.session_state.generated_message = message
            
        except Exception as e:
            st.error(f"메시지 생성 중 오류가 발생했습니다: {str(e)}")
    
    # Display generated message if available
    if st.session_state.generated_message:
        st.success("메시지가 생성되었습니다!")
        
        # Display full message
        with st.expander("전체 메시지", expanded=True):
            st.markdown(f"```{st.session_state.generated_message['full_message']}```")
        
        # Display message parts
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("제목"):
                st.write(st.session_state.generated_message['title'])
            with st.expander("본문"):
                st.write(st.session_state.generated_message['body'])
        with col2:
            with st.expander("가치 전달"):
                st.write(st.session_state.generated_message['sktvalue'])
            with st.expander("맺음말"):
                st.write(st.session_state.generated_message['closing'])
        
        # Copy button
        if st.button("메시지 복사하기", key="copy"):
            st.code(st.session_state.generated_message['full_message'])

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using OpenAI GPT")
