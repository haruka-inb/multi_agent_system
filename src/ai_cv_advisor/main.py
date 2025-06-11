from crew import CareerSupportCrew
    
def run():

    pdf_path = './data/sample_cv.pdf'

    cv_crew = CareerSupportCrew(inputs=pdf_path)
    cv_crew.crew().kickoff(inputs={'pdf_path': pdf_path})
    
if __name__ == '__main__':
    run()