## 프로젝트 설정
프로젝트 실행 전 루트 디렉토리에 `config.json` 파일을 생성하고 사용자 로컬 환경에 따라 아래 내용을 추가하십시오:

### 📝 config.json 작성 예시
<pre>
{
  "chrome_path": "C:/Program Files/Google/Chrome/Application/chrome.exe"
}</pre>

| 항목 | 설명 |
|:-----------|:------------|
| chrome_path | 사용자의 크롬 실행 파일 경로입니다.<br>Windows에서는 일반적으로 `C:/Program Files/Google/Chrome/Application/chrome.exe` 형태입니다.     |

💡 경로에 공백이 있는 경우에도 `"..."`로 감싸면 정상 작동합니다.

💡 크롬이 설치되어 있지 않거나 경로가 잘못되면 Selenium 실행 시 오류가 발생합니다.