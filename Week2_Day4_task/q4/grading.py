def get_grade(avg):
    if avg >= 90:
        return 'A'
    elif 75 <= avg <= 89:
        return 'B'
    elif 60 <= avg <= 74:
        return 'C'
    elif 40 <= avg <= 59:
        return 'D'
    elif avg < 40:
        return 'F'