def structureData(doc):
    basics = ["name", "email", "phone", "url", "location", "language"]
    academics = ["courses", "education"]
    work = ["company", "position", "experience", "role"]
    expertise = ["skill", "project"]
    achievement = ["certification", "award", "publication"]
    data = {
        "basics": {
            "name": [],
            "email": [],
            "phone": [],
            "url": [],
            "location": [],
            "language": []
        },
        "academics": {
            "course": [],
            "education": []
        },
        "work": {
            "company": [],
            "position": [],
            "experience": [],
            "role": []
        },
        "expertise": {
            "skill": [],
            "project": []
        },
        "achievements": {
            "certification": [],
            "award": [],
            "publication": []
        }
    }
    for ent in doc.ents:
        if ent.label_ in basics:
            data["basics"][ent.label_].append(ent.text)
        if ent.label_ in academics:
            data["academics"][ent.label_].append(ent.text)
        if ent.label_ in work:
            data["work"][ent.label_].append(ent.text)
        if ent.label_ in expertise:
            data["expertise"][ent.label_].append(ent.text)
        if ent.label_ in achievement:
            data["achievements"][ent.label_].append(ent.text)
    return data
