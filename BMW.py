import os
import csv
import json

class FileManager:
    @staticmethod
    def check_files():
        print("Checking file...")
        if not os.path.exists("students.csv"):
            print("Error: students.csv not found. Please download the file from LMS.")
            return False
        print("File found: students.csv")
        
        print("Checking output folder...")
        if not os.path.exists("output"):
            os.makedirs("output")
            print("Output folder created: output/")
        else:
            print("Output folder already exists: output/")
        return True

class DataLoader:
    @staticmethod
    def load_data(filename):
        print("Loading data...")
        try:
            with open(filename, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                students = [row for row in reader]
            print(f"Total students: {len(students)}")
            return students
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found. Please check the filename.")
            return None
        except Exception as e:
            print(f"General error: {e}")
            return None

    @staticmethod
    def preview_data(students, n=5):
        if not students: return
        print(f"First {n} rows:-----------------------------")
        for row in students[:n]:
            print(f"{row['student_id']} | {row['age']} | {row['gender']} | "
                  f"{row['country']} | GPA: {row['GPA']}")
        print("-----------------------------------------------------------")

class DataAnalyser:
    def __init__(self, students):
        self.students = students

    def analyse_sleep_vs_gpa(self):
        print("Sleep vs GPA Analysis-----------------------------")
        low_sleep_gpas = []
        high_sleep_gpas = []

        for s in self.students:
            try:
                sleep = float(s['sleep_hours'])
                gpa = float(s['GPA'])
                
                if sleep < 6:
                    low_sleep_gpas.append(gpa)
                else:
                    high_sleep_gpas.append(gpa)
            except (ValueError, KeyError):
                print(f"Warning: could not convert value for student {s.get('student_id')} — skipping row.")
                continue

        avg_low = round(sum(low_sleep_gpas) / len(low_sleep_gpas), 2) if low_sleep_gpas else 0
        avg_high = round(sum(high_sleep_gpas) / len(high_sleep_gpas), 2) if high_sleep_gpas else 0
        diff = round(abs(avg_high - avg_low), 2)

        print(f"Students sleeping < 6 hours : {len(low_sleep_gpas)}")
        print(f"Average GPA (< 6 hours) : {avg_low}")
        print(f"Students sleeping >= 6 hours : {len(high_sleep_gpas)}")
        print(f"Average GPA (>= 6 hours) : {avg_high}")
        print(f"Difference in avg GPA : {diff}-----------------------------")

        return {
            "analysis": "Sleep vs GPA",
            "total_students": len(self.students),
            "low_sleep": {"students": len(low_sleep_gpas), "avg_gpa": avg_low},
            "high_sleep": {"students": len(high_sleep_gpas), "avg_gpa": avg_high},
            "gpa_difference": diff
        }

    def run_functional_tools(self):
        print("Lambda / Map / Filter-----------------------------")
        low_sleep = list(filter(lambda s: float(s['sleep_hours']) < 6, self.students))
        print(f"Students with sleep < 6 hrs : {len(low_sleep)}")
        
        gpa_values = list(map(lambda s: float(s['GPA']), self.students))
        print(f"GPA values (first 5) : {gpa_values[:5]}")
        
        stressed = list(filter(lambda s: float(s['mental_stress_level']) > 7, self.students))
        print(f"Students with stress > 7 : {len(stressed)}")
        print("-----------------------------")

class ResultSaver:
    @staticmethod
    def save_to_json(result, filename="output/result.json"):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4)
        
        print("==============================")
        print("ANALYSIS RESULT")
        print("==============================")
        print(f"Analysis : {result['analysis']}")
        print(f"Total students : {result['total_students']}-----------------------------")
        print(f"Sleep < 6 hours:\nStudents : {result['low_sleep']['students']}")
        print(f"Average GPA : {result['low_sleep']['avg_gpa']}")
        print(f"Sleep >= 6 hours:\nStudents : {result['high_sleep']['students']}")
        print(f"Average GPA : {result['high_sleep']['avg_gpa']}-----------------------------")
        print(f"GPA difference : {result['gpa_difference']}")
        print("==============================")
        print(f"Result saved to {filename}")

def main():
    if not FileManager.check_files():
        return

    loader = DataLoader()
    students = loader.load_data("students.csv")
    
    if students:
        loader.preview_data(students)
        
        analyser = DataAnalyser(students)
        results = analyser.analyse_sleep_vs_gpa()
        analyser.run_functional_tools()
        
        saver = ResultSaver()
        saver.save_to_json(results)

    print("\nTesting Error Handling with wrong file:")
    loader.load_data("wrong_file.csv")

if __name__ == "__main__":
    main()
