from flask import Flask, request, render_template

app = Flask(__name__)

# 감정 데이터 (예시로 일부만 작성)
emotions_data = {

    "비루함": {
         "keywords": ["슬픔", "비하", "습관", "더러움", "더럽", "추함", "추하"], 
         "description": "비루함이란 슬픔 때문에 자기에 대해 정당한 것 이하로 느끼는 것입니다. 습관화된 슬픔이 하나의 습관처럼 내면화될 때, 우리는 자신을 항상 비하하는 감정인 비루함에 젖어들게 됩니다.", 
         "solution": "사람이 비루해지는 것은 ‘내려놓지 못함’에 그 원인이 있습니다. 자존심을 내려놓지 못해 비열해지고, 인정 욕구를 내려놓지 못해 비겁해집니다. 비루함에서 벗어나기 위해서는 무언가를 내려놓을줄 알아야 합니다. 지속적인 애정과 칭찬이 있다면, 비루함은 조금씩 사라질 수 있습니다. 사랑은 비루함에서 우리를 구원할 수 있습니다." 
    }, 

    "자긍심": {
        "keywords":["고찰", "기쁨", "긍지", "보람", "자부심"], 
        "description": "자긍심이란 인간이 자기 자신과 자기의 활동 능력을 고찰하는 데서 생기는 기쁨입니다. 이는 스스로에게 긍지를 가지는 마음으로, 아주 사소한 것이라도 스스로 인정 해주고 긍정적인 사고를 할 수 있도록 하는 감정입니다.", 
        "solution": "누군가 나를 사랑한다는 사실 하나만으로 우리는 금방 자긍심을 회복할 수 있습니다. 우리가 얼마나 귀중한지를 알려주는 숭배자가 없다면, 자긍심을 갖기란 너무나 힘든 법입니다. 하지만, 미래에 대한 희망을 가지고 도전과 어려움 앞에서 용기를 내는 것이 중요합니다. 자신에게 자비를 베풀고 실수나 약점을 받아들임으로써 자존감을 해치지 않도록 노력하세요. 긍정적인 변화를 위한 의지를 다지고 작은 목표를 세워 실천해 나가다 보면 자신에 대한 자긍심이 점차 커질 것입니다." 
    }, 

    "경탄": { 
        "keywords": ["놀람", "무지", "일시", "감탄", "신기", "놀라"], 
        "description": "경탄이란 어떤 사물에 대한 관념으로, 이 특수한 관념은 다른 관념과는 아무런 연관이 없기 때문에 정신은 그 관념 안에서 확고하게 마뭅니다. 또한, 경탄은 무언가를 새롭게 접하면서 놀라움과 호기심을 느끼는 감정인데 일시적인 감정이므로 그 원인을 이해하기 전까지 계속될 수 있습니다.", 
        "solution": "일시적인 감정으로, 그 대상에 대해 깊이 이해하지 못한 상태에서 발생하는 것이 경탄이지만, 이성을 통해 그 상태를 극복할 수 있습니다. 경탄은 무지에서 기인한 감정이지만, 이 무지를 해결하지 위해 노력하고 지식을 쌓으면 경탄을 이겨내고 더 높은 차원의 이해와 지식에 도달할 수 있습니다. 경탄은 우리가 세상을 더 잘 이해하려는 동기를 부여할 수 있지만, 궁극적으로는 그 감정을 이성적으로 해소하여 균형 잡힌 시각을 갖는 것이 중요합니다." 
    },

    "경쟁심": { 
        "keywords": ["적대", "질투", "수동", "비교", "욕망", "욕구"],  
        "description": "경쟁심이란 타인이 어떤 사물에 대해 욕망을 가진다고 우리가 생각할 때, 우리 내면에 생기는 동일한 사물에 대한 욕망입니다. 경쟁심은 다른 사람들과 비교하여 자신의 상태나 위치를 향상시키려는 욕망에서 비롯됩니다. 또, 경쟁심은 다른 사람의 성공이나 성취를 보며 자신도 비슷한 성취를 이루고자 하는 감정이라고 할 수 있는데요, 이는 긍정적인 자극이 될 수 있지만, 지나치면 질투와 불안으로 이어질 위험이 있습니다.", 
        "solution": "경쟁심을 극복하기 위해서는 타인과의 비교를 멈추고 자신의 본성을 이해하며 이성적으로 살아가야 합니다. 또, 자신의 가치와 목표에 집중해야 합니다. 다른 사람과 비교하는 대신, 자신의 성장과 발전에 초점을 맞추고, 자발적이고 내적인 동기로 노력하려고 하는 것이 좋습니다." 
    },

    "야심": { 
        "keywords": ["욕망", "욕구", "소망", "질투", "경쟁심", "명예"], 
        "description": "야심은 타인이 나에게 부러워하는 시선을 보내주기를 바라는 사회적인 감정 중 하나로, 모든 감정을 키우며 강화하는 욕망입니다. 경쟁심은 다른 사람들과 비교하여 자신의 상태나 위치를 향상시키려는 욕망에서 비롯됩니다. 즉, 타인의 인정을 받고자 하는 강한 욕구를 의미합니다. 야심은 성취를 이루고자 하는 동기가 될 수 있지만, 지나치면 외부의 의존하게 되면서 불안과 스트레스를 유발할 수 있습니다.", 
        "solution": "야심은 적절히 통제해야만 합니다. 그럴 때에만 우리의 마음속에 다른 수많은 감정들도 자기 결을 따라 제대로 자라날 수 있고, 그러면 우리는 그만큼 더 행복에 다가갈 수 있습니다. 야심에 대응하는 가장 좋은 방법은 이성을 통해 자신의 본성을 깨닫고, 외부 평가에 휘둘리지 않으며, 내면의 자유와 자율적 삶을 추구하는 것입니다. 자기 자신에게 의미 있는 목표를 설정하고, 내면의 만족감을 추구하는 것이 좋습니다. 내적인 성취감을 찾으려 노력하면 야심이 균형 잡히고, 스스로에 대한 존중과 만족감이 높아질 것입니다." 
    }, 
    
    "사랑": { 
        "keywords": ["기쁨", "정성", "애정", "귀중", "소중", "즐겁", "즐거", "아낌"], 
        "description": "사랑이란 외부의 원인에 대한 생각을 수반하는 기쁨입니다. 이때 얻는 기쁨은 인간이 더욱 작은 완전성에서 더욱 큰 완전성으로 이행할 때 발생하는 감정입니다. 누군가를 만나 과거보다 더 완전한 인간이 되었다는 기쁨을 느낄 때, 사랑에 빠졌다고 할 수 있습니다.", 
        "solution": "사랑이 부족하다는 것은 우리가 어떤 대상이나 타인과의 연결을 충분히 느끼지 못하는 상태로, 이를 해결하기 위해서는 자기 인식, 긍정적인 상호작용 등이 필요합니다. " 
    }, 

    "대담함": { 
        "keywords": ["기쁨", "기쁘", "용기", "극복", "자신", "자율",], 
        "description": "대담함이란 동료가 맞서기 두려워하는 위험을 무릅쓰고 어떤 일을 하도록 자극되는 욕망입니다. 위기를 감내하려고 할 때, 용기와 대담함은 빛을 발합니다.", 
        "solution": "사랑이 죽으면 대담함이라는 감정, 온갖 불의와 억압에도 당당할 수 있었던 가장 인간적인 감정도 맥없이 사라지기 마련입니다. 사랑의 감정을 느낀다면 앞으로 발을 내딛을 수 있는 대담함을 얻을 수 있습니다. 또, 사랑의 대상에 대한 깊은 이해와 존중이 있을 때 사랑이 균형을 이루고 건강해질 수 있는데요, 이를 위해 상대방을 있는 그대로 받아들이고 함께 성장할 수 있는 사랑을 키워 나가려 노력하는 것이 중요합니다." 
    }, 

    "탐욕": {
        "keywords": ["욕심", "파괴", "욕망", "이기", "무절제"], 
        "description": "탐욕이란 부에 대한 무절제한 욕망이자 사랑입니다. 밑도 끝도 없이 치명적으로 중독적인 욕망인 탐욕에는 중용이 있을 수 없습니다. 탐욕은 의부의 자극에 의해 통제되지 못한 감정으로, 인간을 이성적 삶에서 멀어지게 만들고, 결국 자신에게도 해가 될 수 있는 선택을 하게 만듭니다.", 
        "solution": "자신의 욕망이 어떤 원인에서 비롯되는지를 이해하고, 그 욕망이 진정으로 필요한 것인지 자문해 보세요. 탐욕을 억제하기 위해서는 돈을 목적의 자리가 아니라 수단의 자리로 만들어야 합니다. 즉, 최적생계비를 계산하고, 그것을 삶에 관철해야 합니다." 
    },

    "반감": {
        "keywords": ["반대", "거부", "반발", "반의", "슬픔"], 
        "description": "반감이란 우연적으로 슬픔의 원인인 어떤 사물의 관념을 동반하는 슬픔입니다. 누군가와 함께 있을 때 슬픔을 느낀다면, 우리는 그 사람을 미워하게 되고, 이는 필연적으로 느끼게 되는 감정입니다. 하지만, 반감을 이와 달리 어떤 사람을 보았을 때, 과거에 미워했던 사람이 떠올라 슬픈 감정이 드는 우연적인 감정입니다. 반감은 과거의 상처나 실망에 대한 반응으로 나타나며, 종종 분노와 같은 강한 감정을 동반합니다.", 
        "solution": "반감에 쉽게 사로잡히는 사람은 과거 망령에 사로잡혀 살아가는 사람이라고 할 수 있습니다. 반감을 줄이기 위해서는 과거에 사로잡혀 있어서는 안됩니다. 또, 반감을 줄이기 위해 이해와 용서를 통해 감정을 처리하세요. 반감의 원인을 알아보고 상대방의 입장에서 상황을 바라보며, 감정을 표현할 수 있는 방법을 찾아보는 것도 좋습니다." 
    }, 
    
    "대담함": {
        "keywords": ["기쁨", "기쁘", "용기", "극복", "자신", "자율"],  
        "description": "대담함이란 동료가 맞서기 두려워하는 위험을 무릅쓰고 어떤 일을 하도록 자극되는 욕망입니다. 위기를 감내하려고 할 때, 용기와 대담함은 빛을 발합니다. 대담함은 때로는 중요한 성취를 이끌어낼 수 있지만, 이성적 판단 없이 지나치게 무모해질 경우 예상치 못한 위험이나 실패로 이어질 수도 있습니다.", 
        "solution": "사랑이 죽으면 대담함이라는 감정, 온갖 불의와 억압에도 당당할 수 있었던 가장 인간적인 감정도 맥없이 사라지기 마련입니다. 사랑의 감정을 느낀다면 앞으로 발을 내딛을 수 있는 대담함을 얻을 수 있습니다. 또, 대담함을 얻으려면 작은 도전부터 시작해 점차 자신감을 쌓고, 실패를 배움의 기회로 여기는 태도를 갖는 것이 중요합니다. 과거 성공 경험을 떠올려 자신감을 키우는 것도 도움이 될 것입니다." 
    }, 

    "박애": {
        "keywords": ["친절", "희생", "가난", "사랑", "공감", "행복"],  
        "description": "박애란 우리가 불쌍하게 생각하는 사람에게 친절하려고 하는 욕망입니다. 자신이 가진 전부를 내어줄 수 있을 때 박애라는 감정은 빛을 발하게 됩니다. 박애의 주체는 동시에 비참한 신세로 전락하게 되겠지만, 동시에 제대로 사랑했다는 행복감을 만끽하게 될 것입니다. ‘자발적인 가난’, 이것이 바로 박애가 드러나는 행동 양식입니다. 박애는 다른 사람의 고통을 이해하고 그들을 돕고자 하는 마음에서 출발합니다.", 
        "solution": "한 번이라도 비참한 삶을 경험했던 사람이 박애의 감정을 갖기 더 용이한 법입니다. 따라서 내 삶이 가장 비참해질 때, 인생이 바닥까지 떨어질 때, 그만큼 모든 사람을 품어줄 수 있는 역량을 기르고 있는 것인지도 모릅니다. 좌절하지 말고 그 바닥을 차고 올라오는 데 성공한다면 우리는 마침내 박애의 감수성을 배울 수 있습니다. 평소에 작은 도움을 실천하고, 이타적인 가치관을 발전시키며, 타인과의 관계를 소중히 여긴다면 박애의 감수성을 더 키울 수 있을 것입니다." 
    }, 

    "연민": {
        "keywords": ["공감", "도움", "이해", "인식", "가련", "해악", "비극", "불행"], 
        "description": "연민이란 자신과 비슷하다고 상상하는 타인에게 일어난 해악의 관념을 동반하는 슬픔입니다. 연민은 타인의 고통에 공감하고 도움을 주고자 하는 마음에서 비롯됩니다. 불행히도 연민은 결코 사랑으로 바뀔 수 없습니다. 연민을 계속 품고 있으려는 사람은 상대방이 계속 불행하기를 기도해야 할 것이며, 따라서 연민의 감정은 비극으로 끝날 수밖에 없는 것입니다.", 
        "solution": "연민이라는 것은 양날을 가졌습니다. 연민을 잘 다루지 못하겠으면 거기서 손을 떼고, 특히 마음을 떼야 합니다. 단, 연민을 잘 다룰 수 있다면 자기 자신을 돌보면서 타인의 문제를 너무 깊게 개인적으로 받아들이지 않도록 경계를 설정하고, 행동으로 연민을 표현하세요." 
    }, 

    "회한": {
        "keywords": ["슬픔", "한탄", "깨달음", "뉘우침", "고통", "후회"],
        "description": "회한이란 희망에 어긋나게 일어난 과거 사물의 관념을 동반하는 슬픔입니다. 회한의 감정에 대한 좋은 비유는 ‘엎질러서는 안되는 물동이를 엎질렀다는 슬픈 느낌’입니다. 무기력과 비겁의 경험을 배경으로 회한은 꽃핍니다. 다시 말해, 회한은 과거의 행동이나 결정에 대해 후회하며 느끼는 부정적인 감정이라고 할 수 있는데요, 이는 자신이 저지른 실수에 대한 자책으로 나타납니다. 회한에 빠진 사람은 아직 성숙하지 못하고 용기가 부족한 사람이라고 할 수 있습니다. 회한을 겪으면 과거에 매몰되어 현재를 제대로 살지 못할 수 있습니다.", 
        "solution": "회한이라는 슬픈 감정을 떨칠 수 있는 가장 좋은 방법은, 나중에 회한이 없도록 지금 과감하게 선택하고 당당하게 실천하는 것입니다.  감정을 인정하고 실수에서 배우며, 현재에 집중하기를 바랍니다." 
    }, 

    "당황": {
        "keywords": ["두려", "두렵", "당황", "당혹", "놀람", "혼란", "불안"], 
        "description": "당황이란 인간을 무감각하게 만들거나 동요하게 만들어 악을 피할 수 없도록 만드는 두려움입니다. 한마디로 내가 누구인지 모르겠다는 느낌, 혹은 나 자신을 믿지 못할 것 같다는 느낌이 바로 당황이라는 감정의 정체입니다. 당황을 느끼면 무기력함이나 불확실성을 느낄 수 있고, 종종 의사결정 능력을 저하시킬 수도 있습니다.", 
        "solution": "당황이라는 것이 나쁜 것만은 아닙니다. 당황의 감정을 통해 우리는 진정한 자신을 찾을 수 있고, 가면의 욕망과 맨얼굴의 욕망이 내면에서 충돌할 때도 무조건 맨얼굴의 욕망, 즉 내가 이런 사람이었나 하고 경이롭게 생각하는 욕망이 이길 수밖에 없기 때문입니다. 그래도, 당황을 해결하고 싶다면 이성적인 사고와 감정 조절을 통해 상황을 명확히 파악하고, 상황을 분석한 후 우선순위를 정하세요." 
    }, 

    "경멸": {
        "keywords": ["멸시", "업신여김", "부정", "비난", "혐오", "분노"],  
        "description": "경멸이란 정신이 어떤 사물의 현존에 의하여 그 사물 자체 안에 있는 것보다 오히려 그 사물 자체 안에 없는 것을 상상하게끔 움직여질 정도로 정신을 거의 동요시키지 못하는 어떤 사물에 대한 상상입니다. 누군가를 앞에 두고서 다른 사람을 생각하는 것, 혹은 다른 사람을 생각하려고 하는 것이 바로 경멸입니다. 경멸은 종종 자아를 높이거나 상대방을 깎아내리는 방식으로 나타나며, 인간 관계를 악화시키고 갈등을 초래할 수 있습니다. 경멸의 감정은 종종 두려움이나 불안의 반응으로 나타나기도 합니다.", 
        "solution": "경멸하는 대상과 함께 있지 않으면, 모든 문제는 저절로 해결됩니다. 대상과 함께 있어야 한다면, 상대방의 입장에서 생각해 보는 태도를 가지고, 긍정적인 관계를 구축해 보세요. 또한, 경멸당하지 않으려면 내게서 슬픔을 느끼는 사람을 쿨하게 보내 주는 방법밖에 없습니다. " 
    }, 

    "잔혹함": {
        "keywords": ["잔인", "가혹", "무자비", "고통", "해악"], 
        "description": "잔혹함이나 잔인함이란 우리가 사랑하거나 가엽게 여기는 자에게 해악을 가하게끔 우리를 자극하는 욕망입니다. 배신의 피를 혼자만 묻히고 있는 것이 싫어, 상대방도 사랑을 배신하는 피를 흘리도록 강요하는 것이 잔혹함이라는 감정의 실체라고 할 수 있습니다. 잔혹함은 타인을 무시하거나 고통을 즐기는 감정으로 나타날 수 있으며, 인간관계에 심각한 해를 끼칠 수도 있습니다. 잔혹함은 종종 감정의 억압이나 개인의 고통을 외부로 표출하는 방식으로 나타납니다.", 
        "solution": "소중하게 여기는 대상에게 해악을 가하지 않도록, 자신의 욕망을 조절할 수 있도록 노력해야 합니다. 또, 자신의 감정을 인식하고 타인의 고통에 대한 공감 능력을 키워보세요. 잔혹함 감정이 지속된다면 상담이나 치료를 통해 감정을 처리하고 이해하는 것이 도움이 될 수 있습니다." 
    }, 

    "욕망": {
        "keywords": ["본질", "충동", "이익", "탐험", "야심", "야망", "욕구"], 
        "description": "욕망이란 인간의 본질이 주어진 감정에 따라 어떤 것을 행할 수 있도록 결정되는 한에서 인간의 본질 자체입니다. 욕망은 자신의 의식을 동반하는 충동이고, 충동은 인간의 본질이 자신의 유지에 이익이 되는 것을 행할 수 있도록 결정되는 한에서 인간의 본질 자체입니다. 출발의 설렘이 있다면, 과거 우리의 욕망은 나만의 욕망이었다는 것을 확인할 수 있습니다. 하지만, 완성의 허무함이 있다면, 과거 우리의 욕망은 불행히도 타인의 욕망을 반복했던 것임이 밝혀집니다.", 
        "solution": "‘자신의 감정에 충실하기’ 이것이야말로 우리가 자신의 욕망을 긍정하고 복원하는 유일한 방법입니다. 욕망을 해결하기 위해서는 자기 인식과 조절을 통해 욕망을 균형 있게 다루는 것도 도움이 됩니다. 절제를 연습하고 현재에 집중해 보세요." 
    }, 

    "동경": {
        "keywords": ["씁쓸", "쓸쓸", "과거", "추억", "소유", "회상", "그립"],  
        "description": "동경이란, 지금은 결코 소유할 수 없는 무언가를 소유하려는 욕망 또는 충동입니다. 가장 최고였던 순간을 꿈꾸지만, 그 이면에는 이미 자신이 전성기를 지났다는 씁쓸한 자각이 깔려 있습니다. 또한, 단순한 욕망 뿐만이 아니라 가장 최고였던 순간을 되찾고자 하는 깊은 열망과 상실감의 감정이 혼합된 상태이기도 합니다.", 
        "solution": "동경이라는 감정을 극복하기 위해서는, 무엇보다도 현재에 충실해야 합니다. 현재의 삶에 직면할 때만, 새로운 삶의 절정에 이를 수 있기 때문입니다. 또한, 이성을 통해 과거의 순간이 아닌 내가 누구인가를 이해하고, 내적 평온을 추구하며 동경을 긍정적으로 승화할 수 있습니다." 
    }, 

    "멸시": {
        "keywords": ["미움", "무시", "무가치", "이별", "모멸", "상처", "분노", "편견"], 
        "description": "멸시란 미움 때문에 어떤 사람에 대해 정당한 것 이하로 느끼는 것입니다. 예를 들어, 사랑에 빠졌던 남녀가 이별하기 직전 상대를 미워하고 무가치한 사람으로 여기게 되는 것이 멸시의 사례입니다. 이는 주로 실망, 상처, 또는 배신감에서 비롯되며, 대상의 본질적인 가치를 부정함으로써 상대와의 관계를 무시하려고 하는 심리적 방어 기제로 작용하기도 합니다.", 
        "solution": "멸시는 관계에 대한 책임을 지고 단호히 청산할 때 극복할 수 있습니다. 멸시는 미움의 원인을 상대에게서 찾으려고 하고, 관계를 먼저 끊어 주기를 바라면서 시작되기 때문입니다.  또한, 상대방에 대한 내적 이해와 감정적 거리두기를 통해 극복할 수 있습니다. 스스로의 감정을 객관화하고 상대의 가치와 본질을 인정하려는 노력이 필요합니다. 이를 통해 자신도 감정의 소모에서 벗어나 평온함을 되찾을 수 있습니다." 
    }, 

    "절망": {
        "keywords": ["버려", "좌절", "실망", "기대", "절망", "비극"], 
        "description": "절망이란,의심의 원인이 제거된 미래 또는 과거 사물의 관념에서 생기는 슬픔입니다. 공포에서 절망이 생깁니다. 무시무시한 결과가 예측되는 일에 대해, 그러한 일이 오지 않을 거라고 스스로를 위로하다가 그 결과에 직면하게 될 때, 절망이 우리에게 다가옵니다.", 
        "solution": "절망에 빠지지 않기 위해서는 비관론적 사고가 필요합니다. 항상 최악의 경우를 염두에 둔다면, 미래에 대한 기대도 그만큼 줄어들기 때문입니다. 또한, 작은 목표를 설정하여 하나하나 해결하거나, 현재의 순간에 집중하는 것을 통해 절망이라는 감정에서 벗어날 수 있습니다. " 
    }, 

    "음주욕": {
        "keywords": ["음주", "우울", "잿빛", "욕망", "무기력", "패배", "불운", "비참"], 
        "description": "음주욕이란 술에 대한 지나친 욕망이자 사랑입니다. 현재 삶에 대한 무기력과 패배 의식 때문에, 비참한 현실을 잊고 과거의 좋았던 시절을 떠올리며 술에 빠지게 됩니다. 마약 중독도 같은 맥락에서 발생합니다.", 
        "solution": "자기 이해를 통해 현실을 직시하고, 이성으로 감정을 통제하려고 할 때 음주에서 빠져나올 수 있습니다. 또한, 현재에 집중할 수 있는 새로운 삶의 의미와 목적을 발견하여 의미 있는 목적을 가지고 삶을 살아갈 수 있도록 해야 합니다." 
    }, 

    "과대평가": {
        "keywords": ["숭배", "행복", "사랑", "비범", "주인공", "빠짐", "과함", "상상"], 
        "description": "과대평가는 특정 사람에 대한 사랑이나 강한 애착 때문에 그 사람의 가치를 실제보다 높게 평가하는 감정적 상태입니다. 이는 상대방의 결점이나 한계를 지나치게 긍정적으로 바라보는 경향을 동반하며, 그 사람을 이상화하는 착각을 불러일으키기도 합니다. 과대평가는 관계 초기나 깊은 애정을 느낄 때 자주 발생하며, 이를 통해 자신이 느끼는 애정을 정당화하려는 무의식적 욕구에서 비롯됩니다.", 
        "solution": "과대평가를 극복하는 법은, 상대의 강점과 약점을 객관적으로 분석하여 균형 잡힌 시각을 유지하는 것입니다. 또한, 상대방에게 기대는 감정을 되짚어보고 자신의 가치를 발견하려고 노력하는 것이 중요합니다. 서로의 차이점을 인정하며 불완전함 속에서도 사랑의 의미를 찾는 연습이 필요합니다. 마지막으로, 자신의 감정에 대해 솔직하게 반성하고, 상대에 대한 과도한 이상화를 줄여가는 것이 중요합니다. 다만, 상대방을 전혀 과대평가하지 않는다면 그것은 정말로 사랑하는 것이 아니기 때문에, 이를 부정적인 감정으로 바라봐서는 안됩니다." 
    }, 

    "호의": {
        "keywords": ["결핍", "연인의 친구", "애인의 친구", "친구의 친구", "타인", "친절", "정당화", "성욕"], 
        "description": "호의란 타인에게 친절을 베푼 사람에 대한 사랑입니다. 내가 사랑하거나 좋아하는 사람에게 친절을 베푸는 사람을 보았을 때, 호감이 생기는 것은 당연한 본능입니다. 하지만, 호의는 친구에 대한 사랑이기에 편한 상태로 다가갈 수 있으며, 애인과 소원해질 때 애인을 배제한 친구와의 사랑으로 이어질 수 있기 때문에, 호의를 경계적인 시선에서 바라봐야 합니다.", 
        "solution": "자신의 애인을 친구에게 소개시켜 주거나, 셋이 함께하는 멍청한 짓은 저지르지 말아야 합니다. 또한, 호의가 애인과의 관계에 부정적인 영향을 미치지 않도록, 자신의 감정을 명확히 하고 경계를 설정하는 것이 중요합니다. 또한, 친구와 애인의 관계를 명확히 분리하고, 서로 간의 신뢰를 쌓는 방법으로 건강한 관계를 유지하는 것이 필요합니다." 
    }, 

    "환희": {
        "keywords": ["감격", "희망", "소망", "실현", "기대", "선물", "기쁨", "충만", "놀라"], 
        "description": "환희란 우리가 희망했던 것보다 더 좋게 된 과거 사물의 관념을 동반하는 기쁨입니다. 무언가를 희망했지만, 그 희망했던 것보다 사태가 더 좋게 펼쳐지면 우리는 환희라는 감정에 둘러싸이게 됩니다. 하지만 환희를 자주 겪는다면, 본인에게 큰 기대를 하지 않는 소심한 사람일 확률이 높기 때문에, 환희는 그다지 좋은 감정이 아닐지도 모릅니다.", 
        "solution": "할 일에 적극적으로 나서고, 자주적으로 행동하는 것이 좋은 방법이 될 것입니다. 환희가 지나치게 느껴지면 가까운 사람이나 신뢰할 수 있는 사람과 대화하면서 감정을 나눠 보세요. 지나친 환희가 혼자 느낄 때는 강렬하게 다가오지만, 누군가와 나누고 의견을 들으면 감정을 객관적으로 다룰 수 있게 됩니다." 
    }, 

    "영광": {
        "keywords": ["칭찬", "영웅", "찬양", "칭송", "희소", "성공", "성취", "기여", "칭송"], 
        "description": "영광은 우리가 타인이 칭찬할 거라고 상상하는 우리 자신의 어떤 행동의 관념을 동반하는 기쁨입니다. 내가 한 영웅적이고 희소한 행동으로 인해 타인의 칭찬을 들었을 때, 우리가 느끼는 감정이 영광입니다.", 
        "solution": "이는 어쩌면 다른 사람에게 당할 멸시나 경멸에 대한 원초적인 두려움에 의해 발생하여 타인을 경쟁상대로만 생각하는 것이기 때문에, 치욕을 감내하고 사랑과 유대의 가치를 상기하며 타인과 공존해야 합니다. 외부의 기대나 평가보다는, 스스로 만족할 수 있는 기준을 설정해 보세요. 자신의 가치와 목표에 맞춘 기준을 가지면, 외부의 압박감을 줄이고 더 안정적인 마음을 가질 수 있습니다." 
    }, 

    "감사": {
        "keywords": ["사랑", "친절", "욕망", "노력", "열정", "마무리",], 
        "description": "감사는 사랑의 감정을 가지고 우리에게 친절을 베푼 사람에게 친절하고자 하는 욕망 또는 사랑의 노력입니다. 감사에는 사랑이라는 감정이 함축되어 있지만, 아이러니하게도 감사의 말을 전하면서 사랑이 마무리되기도 합니다. 이는 지금까지 행복했지만, 더 이상 사랑을 감당하기 힘들다는 반증이기도 하며, 자신의 나약함에 대한 대가이기도 합니다.", 
        "solution": "감사 자체는 자연스러운 감정이기 때문에 받아들이되, 나약해져서 모든 관계를 끝내려고 하지 않도록 노력해야 합니다. 외부의 기대나 평가보다는, 스스로 만족할 수 있는 기준을 설정해 보세요. 자신의 가치와 목표에 맞춘 기준을 가지면, 외부의 압박감을 줄이고 더 안정적인 마음을 가질 수 있습니다." 
    }, 

    "겸손": {
        "keywords": ["절망", "무력", "무기력", "무능", "약함", "고찰", "겸손", "슬픔"], 
        "description": "겸손이란 인간이 자기의 무능과 약함을 고찰하는 데서 생기는 슬픔입니다. 자신이 자랑하던 돈의 무기력함을 자랑하거나, 한 사람 앞에서 사랑이 무기력함을 보여주는 것이 겸손입니다. 겸손은 자신의 능력이나 성취를 과장하거나 내세우지 않고, 다른 사람을 존중하며 자신을 낮추는 태도입니다. 겸손은 자신이 부족하거나 가치가 없다고 여기는 것이 아니라, 자신의 강점과 약점을 균형 있게 인식하고 다른 사람에게 배우려는 마음가짐을 포함합니다.", 
        "solution": "겸손은 사람을 성숙하게 하지만, 심한 겸손은 자신이 할 수 있는 것마저 할 수 없다고 절망하는 것이기 때문에, 자만심과 절망의 균형을 찾아 어른이 되려고 노력해야 합니다. 오히려 자신의 능력을 지나치게 낮추거나 과소평가하는 경우가 있습니다. 이는 겸손이 아니라 자신감 부족으로 이어질 수 있습니다. 성취한 것을 객관적으로 인정하되, 이를 자랑하거나 과장하지 않는 균형을 찾는 것이 중요합니다." 
    }, 

    "분노": {
        "keywords": ["연대", "해악", "미움", "불행", "유사", "화", "공감", "동료", "유대"],  
        "description": "분노는 타인에게 해악을 끼친 어떤 사람에 대한 미움입니다. 특히, 스스로와 유사한 대상에게 불행을 준 사람에 대해 더 크게 분노를 느낍니다. 분노는 연대 의식 혹은 유대감이 있는 사람만이 가질 수 있으며, 해악을 끼치는 강자에 대해 저항할 수 있는 수단이 됩니다.", 
        "solution": "약자의 입장이라면 연대를 통해 분노를 만들어야 합니다." 
    }, 

    "질투": {
        "keywords": ["타인", "의식", "불행", "시기", "미움", "견제", "관심"], 
        "description": "질투란 타인의 행복을 슬퍼하고 반대로 타인의 불행을 기뻐하도록 인간을 자극하는 한에서의 미움입니다. 질투는 타인에 대한 불신과 자기 자신에 대한 불안에서 발생하며, 스스로가 주인공이 되고 싶은 감정에서 비롯됩니다.", 
        "solution": "한 번 질투가 발생하면 감정을 이전으로 되돌릴 수는 없기 때문에, 특별히 주의하고 또 주의해야 합니다. 분노를 억누르기보다는 건강하게 표현하는 것이 중요합니다. 기분을 정중하게 표현하거나, 상대방과 대화하면서 자신의 감정을 설명해 보세요. 예를 들어 “난 이 부분이 힘들어” 또는 “이 상황에서 화가 났어”라고 말하는 것이 좋습니다." 
    }, 

    "적의": {
        "keywords": ["미움", "혐오", "우울", "슬픔", "슬프", "욕망",],
        "description": "적의란 우리들이 미워하는 사람에게 해악을 가하게끔 우리들을 자극하는 욕망입니다. 적의는 미움에서 더 나아가, 구체적인 해악을 가하려는 의지가 있기 때문에 위험합니다. 적의는 종종 두려움이나 오해, 혹은 과거의 상처에서 비롯되며, 때로는 방어적인 반응으로 나타납니다.", 
        "solution": "적의를 해결하기 위해서는 자신의 감정을 이해하고 긍정적인 관계를 형성하는 것이 좋습니다. 적의의 원인을 분석하고 상황을 이성적으로 바라보며, 공감을 키워보세요. 상대방을 해치려고 할 때 실패하면 엄청난 결핍을, 성공하면 엄청난 성취감을 느끼기 때문에, 주변에 적의를 가진 사람이 있다면 하루속히 피하는 것이 좋습니다. " 
    }, 

    "조롱": {
        "keywords": ["불행", "비웃음", "희열", "미움", "기쁨", "묘함"],  
        "description": "조롱이란 우리가 경멸하는 것이 우리가 미워하는 사물 안에 있다고 생각할 때 발생하는 기쁨입니다. 조롱은 타인을 낮추거나 웃음거리로 삼기 위해 그 사람의 약점이나 실수를 부각시키는 부정적인 태도라고 할 수 있는데요, 이는 다른 사람에게 상처를 주고, 관계를 악화시키며, 타인의 자존감을 떨어뜨릴 수 있습니다. 미움과 기쁨이 교차하는 감정으로, 예를 들어, 미워하는 사람에게서 불합리와 위선을 발견했을 때 기뻐하게 되는 것이 있습니다.", 
        "solution": "조롱은 기쁨을 느끼게는 하지만, 병적인 감정이기 때문에 미워하는 사람과 같이 있지 않도록 하여 발생하지 않도록 해야 합니다. 조롱을 해결하기 위해서는 자신의 감정을 성찰하고 상대방의 입장에서 생각하며 공감을 연습하고, 존중과 배려를 바탕으로 긍정적인 관계를 유지하려는 노력을 통해 더 나은 인간관계를 형성하려고 해보세요." 
    }, 

    "욕정": {
        "keywords": ["욕망", "성욕", "성교", "발정", "사랑"],  
        "description": "욕정은 성교에 대한 욕망이나 성교에 대한 사랑입니다. 적당한 경우나 그렇지 않은 경우에도 모두 욕정이라고 불리며, 종족 보존의 차원에서 머무르는 추한 것이 아니라 삶의 힘을 유지하거나 증진시키는 대상으로 여겨질 수도 있습니다. 욕정은 자연스러운 인간의 감정이지만, 지나칠 경우 타인에 대한 존중을 해칠 수 있으며, 관계에 부정적인 영향을 미칠 수도 있습니다.", 
        "solution": "욕정을 사랑의 완성이나 결실로 여겨서는 안되며, 사랑이 시작되는 한 가지 계기로 바라봐야 합니다. 욕정을 해결하기 위해 욕망을 조절하고 자기 성찰을 통해 감정을 균형 있게 다루어 보세요." 
    }, 

    "탐식": {
        "keywords": ["식욕", "탐욕", "음식", "다이어트", "공허", "허기", "좌절"],  
        "description": "탐식이란 먹는 것에 대한 지나친 욕망이자 사랑입니다. 이는 타인을 무시하고 음식에 몰입하도록 만들며, 상대방에게 모욕감을 느끼게 합니다. 탐식은 신체 건강뿐만 아니라 정신적, 감정적 웰빙에도 부정적인 영향을 미칠 수 있으며, 이는 스트레스, 불안, 우울 등의 감정에서 비롯될 수도 있습니다.", 
        "solution": "과하게 탐식에 빠지면 동물로 전락하며, 반면에 식욕을 제거하려고 해서는 안됩니다. 그 사이에서 적당히 중용을 유지할 수 있도록 노력해야 합니다. 또한, 자기 인식과 건강한 식습관을 통해 조절하는 것이 중요합니다. 천천히 먹는 습관을 기르고 건강한 음식 선택을 우선시하며, 정서적 식사 습관을 길러보세요." 
    }, 

    "두려움": {
        "keywords": ["미래", "과거", "슬픔", "두렵", "두려", "무섭", "무서", "불확실", "가벼움", "공황"], 
        "description": "두려움이란 우리가 그 결과에 대해 어느정도 의심하는 미래 또는 과거 사물의 관념에서 생기는 비연속적인 슬픔입니다. 미래에 대한 두려움, 그것은 과거 불행에 대한 기억과 짝을 이루는 감정일 수밖에 없습니다.  이 감정은 개인의 안전을 지키기 위해 진화한 생존 메커니즘으로, 위험을 감지하고 회피하도록 돕습니다. 두려움은 우리 내면에서 탄생하여 우리의 비전을 지배하게 됩니다. 인간은 과거를 통해 미래를 꿈꾸는 동물이기에 미래를 장밋빛으로, 혹은 잿빛으로 꿈꾸게 될 수도 있습니다.", 
        "solution": "가장 중요한 것은 가벼움을 확보하는 것입니다. 모든 것들은 잠시 내 곁에 있을 뿐이라는 것을 안다면, 미래에 대한 두려움의 감정은 그만큼 줄어들 것입니다. 두려움을 완전히 없애기보다는, 이를 조절하고 건강하게 받아들이는 것이 중요합니다. " 
    }, 

    "동정": {
        "keywords": ["동일시", "사랑", "기쁨", "기뻐", "타인", "선의"], 
        "description": "동정이란 타인의 행복을 기뻐하고 또 반대로 타인의 불행을 슬퍼하도록 인간을 자극하는 한에서의 사랑입니다. 동정에는 묘한 동일시를 전제로 합니다. 동정은 그 사람의 입장에서 직접적인 감정이나 경험을 완전히 이해하지는 못하지만, 상대방이 처한 상황에 대한 공감에서 비롯됩니다. 동정하는 사람이나 받는 사람이나 비슷한 신분이나 지위에 있어야만 합니다. 연민에는 묘한 우월감이 전제되어 있기에 차이가 있습니다.", 
        "solution": "아무나 동정해서는 안됩니다. 명문대 친구를 지방대 친구가 동정했다가는 위로는 커녕 모욕을 받았다고 느끼며 예상치 못한 반발을 초래할 수도 있기 때문입니다. 동정이 아닌 진정한 지지를 제공하려면 상대가 원하는 반응을 이해하고 상황에 맞는 방식으로 다가가는 것이 중요합니다. 때로는 단순한 경청이, 때로는 실질적인 도움이나 조언이 필요할 수 있습니다." 
    }, 

     "공손": {
        "keywords": ["온건", "배려", "욕망", "공손", "웃사람",], 
        "description": "공손함이나 온건함은 사람들의 마음에 드는 일을 하고 그렇지 않은 일은 하지 않으려는 욕망입니다. 표면적으로 타인을 배려하는 공동체 의식이 있는 것처럼 보이지만, 그 이면에는 타인들 혹은 공동체에 대한 공포가 드리우고 있는 짙은 그늘이 있음을을 보아야만 합니다. 상대방에게 불쾌감을 주지 않으려는 마음에서 비롯된 행동과 말투로, 예의와 배려를 기본으로 합니다. 공손함은 단순히 겉으로만 보여주는 예의가 아니라, 상대방을 존중하는 진심 어린 마음에서 나오는 행동입니다.", 
        "solution": "죽을 때까지 타인의 욕망을 따르는 데에 성공한다면, 그는 폐인이 될 것입니다. 공손한 사람을 주의하세요. 공손함의 근본은 상대방을 존중하는 마음에서 나옵니다. 타인의 입장을 이해하려고 노력하고, 그들의 시간, 노력, 감정을 존중하는 태도를 갖추면 자연스럽게 공손한 행동이 따라옵니다." 
    }, 
   
    "미움": {
        "keywords": ["슬픔", "살해", "자살", "의지", "타인", "원망", "증오", "혐오", "불호"], 
        "description": "미움이란 외적 원인의 관념을 동반하는 슬픔입니다. 미움이라는 관계는 반드시 서로 헤어져야만 하는, 둘 중 하나가 이 세상을 떠나야 끝날 수 있는 저주받은 관계입니다. 미움이란 감정은 상대방을 죽이거나 자살하는 것으로 우리를 내몰게 됩니다. 살아야겠다는 의지를 감소시켜서 우리를 고사목처럼 만들어 버리는 감정입니다.", 
        "solution": "미움이라는 감정은 둘 중 하나가 세상에서 사라져야 끝날 수 있는 감정입니다. 따라서, 이를 자연스레 받아들이되 미움이라는 감정에 잠식되지 않도록 해야 합니다. 미움의 감정을 억누르기보다는, 먼저 그 감정이 왜 생겼는지 솔직하게 인식하고 수용하는 것이 중요합니다. 미움을 느끼는 자신의 감정을 부정하지 않고 받아들이는 것이 첫걸음입니다." 
    }, 

    "후회": {
        "keywords": ["자유", "의지", "불행", "후회", "미련", "불운", "선택", "자유", "결단", "슬픔"], 
        "description": "후회란 우리가 정신의 자유로운 결단으로 했다고 믿는 어떤 행위에 대한 관념을 수반하는 슬픔입니다. 자신의 모든 불행을 직접적으로 초래할 수 있는, 일종의 전지전능한 힘을 가지고 있다고 믿을 때에만, 후회라는 감정에 사로잡히게 됩니다. 불운을 자기가 초래했다고 믿는, 선택에서 절대적으로 자유로웠다 믿는 것은 착각이자 오만입니다. 후회는 강한 자의식을 가진 사람에게 자주 찾아오는 감정입니다.", 
        "solution": "이론적으로는 어떤 행위가 자신의 자유로운 결단에서 이루어진 것이 아니라는 점을 알게된다면, 비로소 후회라는 슬픈 감정에게서 벗어날 수 있습니다. 한번 후회에 사로잡히면, 여간 떨쳐내기 쉽지 않습니다. 후회는 유아적인 감정입니다. 자기 뜻대로 되지 않는 것, 즉 타자의 타자성을 받아들여야 조금씩 후회에서 벗어날 수 있습니다." 
    }, 

    "끌림": {
        "keywords": ["우연", "기쁨", "타자", "만남", "상태", "행복"],  
        "description": "끌림이란 우연에 의해 기쁨이 원인이 될 수도 있는 그 어떤 사물의 관념을 수반하는 기쁨입니다. 타자로부터 유래한 기쁨은 꽃을 만개할 수도, 아닐 수도 있습니다. 전자는 사랑, 후자는 끌림입니다. 둘을 구분하는 결정적인 계기는 ‘우연’인데, 타자와의 만남에서 유래하는 기쁨이 필연적이라면 사랑, 우연적이라면 끌림입니다. 우연적인 기쁨은 반드시 어떤 사람이 아닌, 나의 상태에 의해 결정되는 것입니다.", 
        "solution": "끌림을 사랑으로 착각하지 않으려면, 우리의 삶이 사랑에 허기질 정도로 불행한 상태는 아닌지 스스로 점검해 봐야 합니다. 우리의 삶이 어느정도 행복하도록 스스로를 배려해야 한다는 것입니다. 끌림이 지나치게 커질 경우, 감정적 거리를 두는 것이 도움이 됩니다. 감정에 휘둘리기보다는 일시적으로 거리를 두고 차분히 생각해보는 것이 좋습니다. 만약 그 사람과 계속해서 자주 접촉할 상황이라면 일정 부분 물리적 거리를 유지하는 것도 한 방법입니다." 
    }, 

    "치욕": {
        "keywords": ["비난", "슬픔", "치욕", "부끄러움", "자의식"],  
        "description": "치욕이란 우리가 타인에게 비난받는다고 생각되는 어떤 행동의 관념을 동반하는 슬픔입니다. 타인이 자신의 어떤 행동을 비난한다고 생각할 때, 우리 내면에 발생하는 슬픈 감정입니다. 남들 앞에서 큰 실수를 하거나 타인에게 모욕당하는 상황에서 느끼는 경우가 많습니다.", 
        "soulution": "타인이 실제로 비난하지 않을 수도 있습니다. 중요한 건 우리가 어떻게 생각하냐입니다. 사람마다 역린(그 사람에게 하지 말아야 할 표현이나 행동)은 전혀 다릅니다. 좋은 인간관계를 꿈꾸는 사람이라면 만나고 있는 사람의 역린을 먼저 파악해야 합니다." 
    }, 

    "겁": {
        "keywords": ["욕망", "불행", "공포", "실패", "미래", "떨림", "긴장", "위축", "회피", "소심"],  
        "description": "겁남은 동료가 감히 맞서는 위험을 두려워하여 자기의 욕망이 방해당하는 것입니다. 미래에 벌어질 수 있는 가장 불행한 일에 대한 공포, 이것이 바로 겁의 정체입니다. 겁이 많은 사람은 실패를 두려워하는 사람입니다. 위협적이거나 불확실한 상황에서 느끼는 두려움이나 불안감을 의미합니다. 겁은 신체적, 정신적 위험을 예상하거나 실제로 마주할 때 본능적으로 생기는 감정으로, 우리를 위험에서 보호하려는 생존 본능과 연관되어 있습니다.", 
        "solution": "겁이라는 감정에서 빠져나오는 유일한 방법은 현재 자신의 욕망에 몰입하고 그것을 관철시키려는 자세 이외에 다른 방법은 없습니다. 더 강한 욕망의 대상을 만나려고 노력해야 합니다. 웬만한 욕망의 대상으로는 항상 미래의 실패가 떠오를 수 밖에 없기 때문입니다. " 
    }, 

    "확신": {
        "keywords": ["의심", "미래", "과거", "기쁨", "확신"], 
        "description": "확신은 의심의 원인이 제거된 미래 또는 과거 사물의 관념에서 생기는 기쁨입니다. 확신은 의심이 없다면 발생할 수도 없습니다. 의심을 일으킬만한 원인이 사라져야만 확신의 기쁨이 찾아오기 때문입니다. 의심의 크기와 확신이 가져다 주는 기쁨의 크기는 비례합니다. 그렇지만 확신에는 의심을 품었던 흉터가 그대로 남아있을 수밖에 없습니다. 언제든 상처는 다시 드러날 수도 있고, 확신이 저 멀리 물러나고 의심이 그 자리를 차지할 수도 있습니다. 확신과 의심은 동시에 존재합니다.", 
        "solution": "확신과 의심에서 벗어나기 위해서는 할 수 있는 모든 일을 한 후에, 그 결과가 좋지 않다면 쿨하게 포기하세요. 결정이 실패할 경우 최악의 \ 상황을 미리 상상해보고 그것을 어떻게 해결할지 계획해보세요. 이 과정을 통해 걱정이 줄어들고 마음의 준비가 되어 확신을 높일 수 있습니다." 
    }, 

    "희망": {
        "keywords": ["기쁨", "불확실", "희망", "미래", "의심", "양면", "기대", "떨림"], 
        "description": "희망은 우리들이 그 결과에 대하여 어느 정도 의심하는 미래나 과거의 사물의 관념에서 생기는 불확실한 기쁨입니다. 희망이란 감정 뒤에는 우리의 삶을 뒤죽박죽으로 만들 수 있는 힘이 숨겨져 있습니다. 불확실성이 크면 클수록 우리의 숨통을 조여올 것입니다. 그렇지만 불확실성을 제거할 수는 없습니다. 그렇다면 희망 또한 사라지기 때문입니다다", 
        "solution": "희망은 어른보다는 어린아이들이 더 많이 품습니다. 불확실성보다 기쁨에 주목하기 때문입니다. 조그마한 희망부터 조금씩 마음을 채워가세요. 큰 목표가 힘들어 보일 때, 작은 목표부터 세워 하나씩 성취해 보세요. 작은 성공을 통해 자신감을 얻고, 희망을 유지하는 데 도움이 됩니다." 
    }, 

    "오만": {
        "keywords": ["자신감", "비극", "자만", "오만", "지식", "전지전능", "탐구", "최고"], 
        "description": "오만이란 자신에 대한 사랑 때문에 자신을 정당한 것 이상으로 느끼는 것입니다. 오만이란 감정은 어떤 것에 대해 항상 전지전능하다는 자신감에서 싹트는 법입니다. 오만은 항상 비극으로 끝나기 마련입니다. 누구보다 잘 안다고 생각하는 바로 그것이 자신의 전지전능을 비웃기라도 하는 것처럼 오만한 사람을 파멸로 이끌기 때문입니다. 오만이 생기는 순간, 무언가를 알려고 하지 않기에 그것을 사랑하지 않는 것과 다르지 않습니다. 그러니 한때는 사랑받았던 그것이 이제 우리에게 복수를 하게 됩니다.", 
        "solution": "오만이라는 감정에 잠식되지 않기 위해서는, 스스로에 대한 객관적인 판단이 필요합니다. 스스로가 전지전능하다는 착각을 하지 않도록 주의해야 합니다. 주변 사람들에게 피드백을 요청하고, 이를 열린 마음으로 수용하세요. 타인이 자신의 행동에 대해 어떻게 느끼는지를 알면, 오만한 태도를 인식하고 개선할 수 있습니다" 
    }, 

    "소심함": {
        "keywords": ["악", "두려움", "두렵", "두려", "걱정", "욕망", "충격", "미래"], 
        "description": "소심함은 우리들이 두려워하는 큰 악을 더 작은 악으로 피하려는 욕망입니다. 소심함과 대담함은 인간이 가질 수 없는 양극단의 감정이라고 할 수 있습니다. 결과가 뜻대로 되지 않을까 두려워하면 매사에 소심하게 되고, 자신의 뜻대로 될 것이라 확신하게 된다면 모든 일에 대담하게 됩니다. 두 감정 모두 극단적일 수 있습니다.", 
        "solution": "그러나 소심함에는 미래가 뜻대로 되지 않을 때, 소심한 사람은 그다지 충격을 받지 않는다는 미덕이 있기도 합니다. 미래에 대한 균형잡힌 시선을 갖기 위해서 대담함 또한 지닐 필요가 있습니다. 결과가 뜻대로 되지 않을 때, 쿨한 자세를 갖도록 하세요." 
    }, 

    "쾌감": {
        "keywords": ["정신", "신체", "동시", "기쁨", "유쾌", "행복"], 
        "description": "정신과 신체에 동시에 관계되는 기쁨의 정서를 쾌감이나 유쾌함이라고 합니다. 몸과 마음이 모두 기쁨으로 충만할 때는 그리 자주 찾아오는 경험은 아닙니다.  이는 보통 신체적, 정신적 자극에 의해 느껴지며, 기쁨, 만족감, 또는 편안함과 같은 긍정적인 감정 상태로 나타납니다. 쾌감은 사람에게 동기 부여가 되기도 하며, 반복하고 싶은 경험을 만들기도 합니다.", 
        "solution": "우리는 자신의 몸이 어느 때에 행복을 느끼는지, 어느 때에 불행을 느끼는지 계속 응시해야만 합니다. 아무리 정신으로 '이럴 때 나는 틀림없이 행복할 거야'라고 생각해도 직접 몸으로 겪는 기쁨을 느끼지 못한다면, 우리는 결코 행복할 수 없습니다." 
    }, 

    "슬픔": {
        "keywords": ["완전", "슬픔", "훼손", "타자", "우울", "암울"], 
        "description": "슬픔은 인간이 더 큰 완전성에서 더 작은 완전성으로 이행하는 것입니다. 당연히 우리는 덜 완전해지는 느낌에서 벗어나려고 노력할 것입니다. 슬픔은 타자를 만나서 삶의 충만함이 훼손된다고 느낄 때의 감정입니다. 원치않는 타자와의 관계가 지속되면 우리는 슬픔이라는 감정에 지배됩니다.", 
        "solution": "이렇게 슬픔을 느낄 때, 우리에게 상대적으로 더 잘해주는 타자가 등장하면, 우리는 너무나도 쉽게 기쁨의 감정에 빠져들게 됩니다. 슬픔을 주는 대상이라면 단연코 그것을 제거하거나 그것을 떠나야만 합니다. 변덕이나 변심을 얘기하는 사회적 평판에 대해서는 철저하게 쿨해질 필요가 있습니다."
    }, 

    "수치심": {
        "keywords": ["슬픔", "억제", "수치", "공포", "타인", "시선", "반성", "부끄"],  
        "description": "수치심에 대해 이야기 하기 위해서는 치욕에 대해 알아야 합니다. 치욕이란 우리가 부끄러워하는 행위에 수반되는 슬픔입니다. 반면, 수치심이란 치욕에 대한 공포나 소심함이고 추한 행위를 지 않도록 인간을 억제하는 것입니다. 우리가 다른 사람으로부터 비난받는다고 생각되는 자신의 어떤 행동에 대한 관념을 동반하는 슬픔이기도 합니다. 수치심은 앞으로 치욕을 당하면 어쩌나 하는 공포감이나 소심함으로 드러나기 때문에 중요한 감정입니다. 수치심을 느낄 때 타인의 시선을 느낄 뿐만 아니라 동시에 자신의 행동 또한 강하게 반성합니다. 수치심은 자긍심과 자존감을 위해 중요합니다", 
        "solution": "수치심은 추한 행동을 하지 않기 위해, 인간에게 어느 정도는 꼭 필요합니다. 다만 너무 과하게 느껴 행동에 제약을 받지 않도록 견제해야 합니다.  적당한 수준의 성취를 인정하는 것이 중요합니다." 
    }, 

    "복수심": {
        "keywords": ["미움", "해악", "똑같음", "복수", "자괴", "욕망", "보복", "분노", "자극"], 
        "description": "복수심은 미움의 정서로 우리에게 해악을 가한 사람에게 똑같은 미움으로 해악을 가하게끔 우리를 자극하는 욕망입니다. 타인에게 해악을 가하기 위해서는, 자신의 마음을 딱딱한 얼음처럼 만들어 놓는 것이 좋습니다. 일반적으로 분노와 억울함이 결합되어 발생하는 감정으로, 상대에게 자신이 느꼈던 고통을 되돌려 주고자 하는 마음입니다. 복수심은 일시적으로 분노를 해소하는 듯 보일 수 있지만, 종종 더 큰 갈등과 부정적인 결과를 초래할 수 있어 신중하게 다룰 필요가 있습니다.", 
        "solution": " 약자가 복수를 포기하는 순간, 자신이 강자에게 복수할 수 조차 없는 존재라는 자괴감에서 벗어나게 됩니다. 사랑이든 복수든 사실 오직 자유로운 자, 혹은 강자만이 누릴 수 있는 욕망이라는 사실을 잊어서는 안됩니다."
    }
    
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
