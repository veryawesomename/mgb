import random
easy = ["가", "나", "다", "라", "마", "바", "사", "아", "자", "차", "카", "타", "파","하"]
normal = ["미니게임", "키보드", "전사", "컴퓨터", "디스코드", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
hard = ["꿟", "깗", "껣", "낇", "꿃", "꼷", "끏", "뜳", "딻", "뗶", "띯", "똚", "뚦", "쑯", "쓟", "쌻", "쎩", "뿗", "뽌", "뿗", "뽏", "뢃", "뢟", "맇"]
def kg(lv):
    if lv == 1:
        r = random.randint(0, 13)
        enemy = easy[r]
        return enemy
        r = None
        enemy = None
    elif lv == 2:
        r = random.randint(0, 11)
        enemy = normal[r]
        return enemy
        r = None
        enemy = None
    elif lv == 3:
        text = None
        r = random.randint(0, 23)
        p = random.randint(1, 3)
        for i in range(0, int(p)):
            text += hard[r]
        return text
        r = None
        p = None
        text = None


