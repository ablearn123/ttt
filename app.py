import streamlit as st
import requests

class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json'
        }

        response = requests.post(self._host + '/testapp/v1/chat-completions/HCX-003',
                                 headers=headers, json=completion_request)
        return response.json()['result']['message']['content']

def main():
    st.title("CLOVA Studio 대화형 챗봇")

    # 세션 상태 초기화
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "너는 코드를 알려주는 챗봇이야"}
        ]

    # CompletionExecutor 인스턴스 생성
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiY5PSADQec5yX5HjbEYcaeqsIlHqbnkEn5xLl+5rGKfiF',
        api_key_primary_val='IAwokGLFVJw8kakhKBJBlmRRTJXxXNuTAW0JyMa3',
        request_id='f6d745dd-0ecb-4714-93b3-ef2d77644060'
    )

    # 대화 내용 표시
    for message in st.session_state.messages[1:]:  # 시스템 메시지 제외
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("질문을 입력하세요:"):
        # 사용자 메시지 추가 및 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # API 요청 데이터 준비
        request_data = {
            'messages': st.session_state.messages,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 256,
            'temperature': 0.5,
            'repeatPenalty': 5.0,
            'stopBefore': [],
            'includeAiFilters': True,
            'seed': 0
        }

        # 챗봇 응답 생성 중 표시
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("생각 중...")

            # API 호출 및 응답 처리
            full_response = completion_executor.execute(request_data)

            # 응답 메시지 추가 및 표시
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == '__main__':
    main()