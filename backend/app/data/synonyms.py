# Synonyms for NLP Intent Recognition
from typing import Dict, List

SYNONYMS: Dict[str, List[str]] = {
    "attack": ["攻擊", "打", "斬", "砍", "刺", "射", "揍", "劈", "殺", "attack", "hit", "strike", "slash", "fight", "kill"],
    "defend": ["防禦", "防守", "格擋", "架勢", "defend", "block", "guard", "parry"],
    "observe": ["觀察", "查看", "察看", "檢視", "看", "調查", "四處看看", "四周", "周圍", "observe", "look", "examine", "inspect", "check", "view", "around"],
    "talk": ["說話", "對話", "交談", "問", "詢問", "talk", "speak", "chat", "ask", "inquire"],
    "pick": ["拾取", "撿", "拿", "拿起", "取得", "撿起", "收集", "獲得", "pick", "take", "get", "grab", "collect", "pickup"],
    "use": ["使用", "用", "喝", "吃", "服用", "use", "drink", "eat", "consume", "apply"],
    "move": ["前往", "走到", "去", "移動", "進入", "趕往", "move", "go", "walk", "travel", "enter", "goto"],
    "rest": ["休息", "睡覺", "療傷", "打坐", "冥想", "rest", "sleep", "heal", "meditate"],
    "escape": ["逃跑", "逃走", "逃離", "撤退", "退後", "escape", "flee", "run", "retreat"],
    "question": ["什麼", "為什麼", "怎麼", "如何", "哪裡", "誰", "when", "what", "why", "how", "where", "who"],
}
