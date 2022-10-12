class CourseSimple:
    def __init__(self, data: dict):
        content = data['content']
        self.personid = content['cpi']
        self.id = content['id']

        self.name = content['course']['data'][0]['name']

        pass

    def __str__(self):
        return self.name


class task:
    # 课程章节下的分支
    def __init__(self, data: dict):
        self.name = data['name']
        self.id = data['id']
        self.label = data['label']

    def __str__(self):
        return self.label + ' ' + self.name


class Knowledge:
    # 课程的章节
    def __init__(self, data: dict):
        self.name = data['name']
        self.id = data['id']
        self.label = data['label']
        self.card: list[task] = []

    def add_card(self, data: dict):
        self.card.append(task(data))

    def __str__(self):
        return self.label + ' ' + self.name


class Course:
    def __init__(self, data: dict):
        _course = data['data'][0]['course']['data'][0]
        _knowledge = _course['knowledge']['data']

        self.id = data['data'][0]['id']  # 课程id
        self.name = _course['name']
        self.teacher = _course['teacherfactor']

        self.knowledge: dict[int, Knowledge] = {i['id']: Knowledge(i) for i in _knowledge if i['status'] == 'open'}

        for i in _knowledge:
            if i['status'] == 'task':
                self.knowledge[i['parentnodeid']].add_card(i)

    def __str__(self):
        return self.name + ' - ' + self.teacher


class Card:
    def __init__(self,data:dict):
        self.knowledgeid=data['knowledgeid']



if __name__ == "__main__":
    from temp.clazz import test

    t = Course(test)
    print(t)
    print()
    for i in t.knowledge.items():
        print(i[1])
        for j in i[1].card:
            print(j)
        print()
