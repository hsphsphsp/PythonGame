def subject_grade(subject):
    mark = float(input("Input the mark of " + subject + ' : '))
    while mark > 100 and mark < 0:
        mark = float(input("The mark must be in between 0 and 100"))
    return mark

def grader(mark):
    if mark > 80:
        return 'A'
    elif mark > 60:
        return 'B'
    elif mark > 40:
        return 'C'
    elif mark > 20:
        return 'D'
    else:
        return 'F'

def grade_inform(subject):
    subject_grade = subject_grader(subject)
    print("The " + subject + " grade is : " + subject_grade)

calculus = subject_grade("Calculus")
linear_algebra = subject_grade("Linear Algebra")
python_programming = subject_grade("Python Programming")
philosophy = subject_grade("Philosophy")
english = subject_grade("English")

print("The Calculus grade is : " + grader(calculus))
print("The Linear Algebra grade is : " + grader(linear_algebra))
print("The Python Programming grade is : " + grader(python_programming))
print("The Philosophy grade is : " + grader(philosophy))
print("The English grade is : " + grader(english))
print("The average grade is : " + grader((calculus + linear_algebra + python_programming + philosophy + english) / 5))
