from flask import Flask, request, render_template

app = Flask(__name__)

# 감정 데이터 (예시로 일부만 작성)
emotions_data = {
    "기쁨": {
        "keywords": ["행복", "환희", "기쁨", "즐거움"],
        "description": "기쁨은 우리 몸과 마음이 완전한 상태로 나아가는 감정입니다.",
        "solution": "기쁨을 지속하려면 주변과 나누고, 균형 잡힌 삶을 유지하세요."
    },
    # 추가 감정 데이터...
}

# 감정 분석 함수
def detect_emotion(user_input):
    matched_emotion = None
    max_matches = 0

    for emotion, data in emotions_data.items():
        match_count = sum(1 for keyword in data['keywords'] if keyword in user_input)
        if match_count > max_matches:
            max_matches = match_count
            matched_emotion = emotion

    return matched_emotion

@app.route('/', methods=['GET', 'POST'])
def home():
    emotion = None
    description = ""
    solution = ""

    if request.method == 'POST':
        user_input = request.form.get('user_input')
        emotion = detect_emotion(user_input)
        if emotion:
            description = emotions_data[emotion]["description"]
            solution = emotions_data[emotion]["solution"]

    return render_template('index.html', emotion=emotion, description=description, solution=solution)

if __name__ == '__main__':
    app.run(debug=True)
    
