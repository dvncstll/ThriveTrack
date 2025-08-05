def evaluate_burnout(data):
    hours = int(data['work_hours'])
    breaks = int(data['breaks_taken'])

    if hours > 50 and breaks < 2:
        return {"risk": "High", "suggestion": "Schedule 1:1 wellness check"}
    elif hours > 40:
        return {"risk": "Medium", "suggestion": "Encourage more breaks"}
    else:
        return {"risk": "Low", "suggestion": "No action needed"}