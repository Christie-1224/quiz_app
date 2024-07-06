import pandas as pd
import os

df = pd.read_excel("./test.xlsx")
df.columns = ['总序号', '知识点', '题型', '题目', '选项A', '选项B', '选项C', '选项D', '答案', '出处','Unused']
df = df.drop(index=0).drop(columns='Unused')
df = df.reset_index(drop=True)
df.head()

questions = []
for i in range(len(df['总序号'])):
    example = dict()
    example['question']=str(df['总序号'][i])+'.'+df['题目'][i]
    example['options']=[df['选项A'][i],df['选项B'][i], df['选项C'][i], df['选项D'][i]]
    example['answer']=df['答案'][i]
    questions.append(example)


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QRadioButton, QButtonGroup,QHBoxLayout,QPushButton


class DoubleClickRadioButton(QRadioButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

    def mouseDoubleClickEvent(self, event):
        self.parent().check_answer(self)

class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.save_file = './quiz_state.txt'
        self.question_index = self.load_state()
        self.initUI()
        self.display_question()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Quiz Application')

        self.layout = QVBoxLayout()

        self.question_label = QLabel(self)
        self.question_label.setWordWrap(True)
        self.layout.addWidget(self.question_label)

        self.option_group = QButtonGroup(self)
        self.option_buttons = []
        self.result_labels = []
        for i in range(4):
            h_layout = QHBoxLayout()
            btn = DoubleClickRadioButton("", self)
            self.option_group.addButton(btn)
            self.option_buttons.append(btn)
            h_layout.addWidget(btn)
            
            result_label = QLabel(self)
            h_layout.addWidget(result_label)
            self.result_labels.append(result_label)

            self.layout.addLayout(h_layout)

        self.navigation_layout = QHBoxLayout()
        self.prev_button = QPushButton("上一题", self)
        self.prev_button.clicked.connect(self.prev_question)
        self.navigation_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("下一题", self)
        self.next_button.clicked.connect(self.next_question)
        self.navigation_layout.addWidget(self.next_button)

        self.layout.addLayout(self.navigation_layout)
        self.setLayout(self.layout)

    def display_question(self):
        if 0 <= self.question_index < len(questions):
            current_question = questions[self.question_index]
            self.question_label.setText(current_question["question"])

            for i, option in enumerate(current_question["options"]):
                self.option_buttons[i].setText(option)
                self.option_buttons[i].setChecked(False)
                self.result_labels[i].setText("")  # 重置结果标签

            self.prev_button.setEnabled(self.question_index > 0)
            self.next_button.setEnabled(self.question_index < len(questions) - 1)
        else:
            self.end_quiz()

    def check_answer(self, selected_button):
        selected_option = selected_button.text()
        current_question = questions[self.question_index]
        is_correct = selected_option[0] == current_question["answer"]

        for i, btn in enumerate(self.option_buttons):
            if btn == selected_button:
                if is_correct:
                    self.result_labels[i].setText("正确!")
                    self.result_labels[i].setStyleSheet("color: green;")
                else:
                    self.result_labels[i].setText(f"错误!")
                    self.result_labels[i].setStyleSheet("color: red;")
                break

    def prev_question(self):
        if self.question_index > 0:
            self.question_index -= 1
            self.save_state()
            self.display_question()

    def next_question(self):
        if self.question_index < len(questions) - 1:
            self.question_index += 1
            self.save_state()
            self.display_question()

    def end_quiz(self):
        self.question_label.setText("You have completed all questions!")
        for label in self.result_labels:
            label.setText("")
        self.save_state()

    def save_state(self):
        with open(self.save_file, 'w') as f:
            f.write(str(self.question_index))

    def load_state(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as f:
                return int(f.read())
        return 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    quiz = QuizApp()
    quiz.show()
    sys.exit(app.exec_())