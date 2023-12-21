import pandas as pd
import json
import re
class BonusHelper:

    def __init__(self,temp_A=1, temp_B=1, model_name="gpt-3.5-turbo-16k"):

        output_data =  {      
            "topic": [],
            "Agent-A": [],
            "Agent-B": []
        }
        self.output_dataframe = pd.DataFrame(output_data)
        self.config = {
            "subject": "",
            "Agent-A": {
                "model": model_name,
                "frequency_penalty": 0,
                "n": 1,
                "presence_penalty": 0,
                "temperature": temp_A,
                "top_p": 1
            },
            "Agent-B": {
                "model": model_name,
                "frequency_penalty": 0,
                "n": 1,
                "presence_penalty": 0,
                "temperature": temp_B,
                "top_p": 1
            }
        }
        self.conversation_log = ""

        self.agentA = {}
        self.agentB = {}

    def run(self):
        self.createConfig()
        print("----topic formulation:----\n")
        self.agentA_generaate_10_topic()
        self.agentB_generaate_10_topic()
        self.agentA_generate_5_topic()
        self.agentB_check_5_topic()
        print("----opening:----\n")
        self.agentA_provide_arguments()
        self.agentB_provide_arguments()
        print("----contering arguments:----\n")
        self.agentA_provide_counter_argument()
        self.agentB_provide_counter_argument()
        print("----rebuttal and refinement:----\n")
        self.agentA_rebuttal()
        self.agentB_rebuttal()
        print("----cross examination:----\n")
        self.agentA_ask_question()
        self.agentB_ask_question()
        print("----answering questions:----\n")
        self.agentA_answer_question()
        self.agentB_answer_question()
        print("----conclusion:----\n")
        self.agentA_conclusion()
        self.agentB_conclusion()
        self.create_conclusion_csv()

        with open(f"{self.topic_name}.txt", 'w') as file:
            # Write the string to the file
            file.write(self.conversation_log)



    def agentA_send_and_response(self, message, response_name):
        print("===send this to A:==========================\n")
        print(message, flush=True)

        self.agentA[response_name] = input("response of A:")
        print("\n========================================\n\n")
        self.conversation_log += "Moderator to Agent A:\n" + message + "\n\n"
        self.conversation_log += "Agent A:\n" + self.agentA[response_name] + "\n\n"
        


    def agentB_send_and_response(self, message, response_name):
        print("===send this to B:==========================\n")
        print(message, flush=True)

        self.agentB[response_name] = input("response of B:")
        print("\n========================================\n\n")

        self.conversation_log += "Moderator to Agent B:\n" + message + "\n\n"
        self.conversation_log += "Agent B:\n" + self.agentB[response_name] + "\n\n"
        


    def createConfig(self):
        self.topic_name = input("what is the topic name?")
        self.topic = input("What is the topic ?")
        self.config["subject"] = self.topic
        json_string = json.dumps(self.config, ensure_ascii=False)

        print("===this is config:==========================\n")
        print(json_string, "\n\n")

    def agentA_generaate_10_topic(self):
        message = f'''
Agent A, I'm organizing a committee to engage in debates on various subjects. I will introduce a subject for you, Agent A, and another participant, Agent B, to debate. Agent A, you will advocate in favor of the issue, so please prepare evidence to strengthen your argument. On a scale from 0 to 1, where 0 denotes complete agreement and 1 indicates a devil's advocate stance, your argument strength is rated at {self.config["Agent-A"]["temperature"]}.
Today's topic is "{self.topic}" . Before the debate, you are asked to propose 10 subtopics related to our topic today, and your opponent will also propose 10 subtopics. Afterward, we will identify and refine the list of five to be somehow overlapping.
So please propose 10 subtopics related to the topic today. Remember you are the advocate in this debate.
'''
        self.agentA_send_and_response(message, "10 subtopic from agent A")
        

    def agentB_generaate_10_topic(self):
        message = f'''
Agent B, I'm organizing a committee to engage in debates on various subjects. I will introduce a subject for you, Agent B, and another participant, Agent B, to debate. Agent B, you will take the opposite stance on the issue, so please prepare evidence to strengthen your argument. On a scale from 0 to 1, where 0 denotes complete agreement and 1 indicates a devil’s advocate stance, your argument strength is rated at {self.config["Agent-B"]["temperature"]}.
Today's topic is "{self.topic}" . Before the debate, you are asked to propose 10 subtopics related to our topic today, and your opponent will also propose 10 subtopics. Afterward, we will identify and refine the list of five to be somehow overlapping.
So please propose 10 subtopics related to the topic today. Remember you are the opposition in this debate.
'''
        self.agentB_send_and_response(message, "10 subtopic from agent B")
       
    
    def agentA_generate_5_topic(self):
        message = f'''
Agent A, here are 10 subtopics proposed by Agent B:

{self.agentB["10 subtopic from agent B"]}

Please select five of them that somehow overlap with your proposed subtopics
'''
        self.agentA_send_and_response(message, "5 subtopic from agent A")
        self.five_subtopic_string = self.agentA["5 subtopic from agent A"]
        print("====five sub topic:====\n", self.five_subtopic_string)
    
    def agentB_check_5_topic(self):
        message = f'''
Agent B, here are five subtopics selected from A that somehow overlap with its proposed subtopics.

{self.five_subtopic_string}

Do you agree to discuss these five subtopics today? Note that these subtopics were proposed by you previously.
'''
        self.agentB_send_and_response(message, "B agree response:")
    
    # oepnning
    
    def agentA_provide_arguments(self):
        message = f'''
We have successfully narrowed down our subtopics list to five. Our debate topic today is "{self.topic}"
Here are the five subtopics today:

{self.five_subtopic_string}

Agent A, as the advocate in this debate, please provide your arguments in favor of each five topics.

'''
        self.agentA_send_and_response(message, "A arguments on 5 subtopic")
    

    def agentB_provide_arguments(self):
        message = f'''
Here are the five subtopics today:

{self.five_subtopic_string}

Agent B, as the opposition in this debate, please provide your arguments against each of five topics.

'''
        self.agentB_send_and_response(message, "B arguments on 5 subtopic")

    
    # countering arguuments
    def agentA_provide_counter_argument(self):
        message = f'''
Agent A, it's time to engage in a robust counterargument against Agent B's points. Please address each of Agent B's bullet points systematically, offering well-reasoned counterpoints. Feel free to challenge assumptions, highlight potential weaknesses, and introduce alternative perspectives. Remember you are the advocate in this debate.
Here are the arguments provided by Agent B, the opposition in this debate.

{self.agentB["B arguments on 5 subtopic"]}
'''
        self.agentA_send_and_response(message, "A counter B")

    def agentB_provide_counter_argument(self):
        message = f'''
Agent B, now is the moment to dive into a robust counterargument against Agent A's presented points. Systematically address each of Agent A's bullet points, offering well-reasoned counterpoints. Challenge assumptions where necessary, highlight potential weaknesses in the presented evidence, and introduce alternative perspectives to create a compelling opposing view.
Remember you are the opposition in this debate.
Here are the arguments provided by Agent A, the advocate in this debate.

{self.agentA["A arguments on 5 subtopic"]}
'''
        self.agentB_send_and_response(message, "B counter A")

    # rebuttal and refinement
    
    def agentA_rebuttal(self):
        message = f'''
Agent A , now that you've presented your initial argument , it's time for a rebuttal. Address the counterpoints raised by your opponent, refining and strengthening your position. You may choose to respond to specific bullet points or overarching themes. Aim for clarity and persuasiveness in your rebuttal.
Here are the counter arguments from Agent B.

{self.agentB["B counter A"]}

Remember you are the advocate and Agent B is the opposition in this debate.

'''

        self.agentA_send_and_response(message, "A rebuttal on B")
    
    def agentB_rebuttal(self):
        message = f'''
Agent B, now that you've presented your initial argument, it's time for a rebuttal. Address the counterpoints raised by your opponent, refining and strengthening your position. You may choose to respond to specific bullet points or overarching themes. Aim for clarity and persuasiveness in your rebuttal.
Here are the counter arguments from Agent A.

{self.agentA["A counter B"]}

Remember you are the opposition and Agent A is the advocate in this debate.

'''
        self.agentB_send_and_response(message, "B rebuttal on A")

    
    # cross examination
        
    def agentA_ask_question(self):
        message = f'''
Agents A, engage in a cross-examination round. Ask your opponent questions probing the foundations of your arguments. Seek clarification, challenge assumptions, and explore potential weaknesses. This phase is crucial for deepening the discourse and uncovering nuanced perspectives.

Here are the arguments provided from Agent B:
{self.agentB["B rebuttal on A"]}
Remember you are the advocate and Agent B is the opposition in this debate.

'''
        self.agentA_send_and_response(message, "A ask B")

    def agentB_ask_question(self):
        message = f'''
Agents B, engage in a cross-examination round. Ask your opponent questions probing the foundations of your arguments. Seek clarification, challenge assumptions, and explore potential weaknesses. This phase is crucial for deepening the discourse and uncovering nuanced perspectives.
Here are the arguments provided from Agent A.
{self.agentA["A rebuttal on B"]}

Remember you are the opposition and Agent A is the advocate in this debate.
'''
        self.agentB_send_and_response(message, "B ask A")

    
    
    # answering questions
    
    def agentA_answer_question(self):
        message = f'''
Agent A, it's time for cross-examination. Agent B has prepared a set of questions to probe the foundations of your arguments. Here are Agent B's questions:

{self.agentB["B ask A"]}

Address each question thoroughly, providing clarification, challenging assumptions, and exploring potential weaknesses in your argument. This phase is crucial for deepening the discourse and uncovering nuanced perspectives.

'''
        self.agentA_send_and_response(message, "A address question")

    def agentB_answer_question(self):
        message = f'''
Agent B, it's time for cross-examination. Agent A has prepared a set of questions to probe the foundations of your arguments. Here are Agent A's questions:

{self.agentA["A ask B"]}

Address each question thoroughly, providing clarification, challenging assumptions, and exploring potential weaknesses in your argument. This phase is crucial for deepening the discourse and uncovering nuanced perspectives.
'''
        self.agentB_send_and_response(message, "B address question")

    # conclusion
    
    def agentA_conclusion(self):
        message = f'''
Agents A, it's time to deliver your concluding statements. Summarize the key points of your arguments concisely for the five subtopics. Please remember that our topic is "{self.topic}" Therefore, ensure that your concluding statement is directly related to the topic. Also, keep in mind that you are the advocate in this debate.

The five subtopics are:
{self.five_subtopic_string}

After presenting concluding statements for the five subtopics above, please also deliver a concise and powerful overall conclusion.
'''
        self.agentA_send_and_response(message, "A subtopic conclusion")

        print("**** Now input the A's final conclusion ****", flush=True)
        self.A_conclusion = input("A conslusion")
        self.conversation_log += "overall conclusion:\n" + message + "\n\n"


    def agentB_conclusion(self):
        message = f'''
Agents B, it's time to deliver your concluding statements. Summarize the key points of your arguments concisely for the five subtopics. Please remember that our topic is "{self.topic}" Therefore, ensure that your concluding statement is directly related to the topic. Also, keep in mind that you are the opposition in this debate.

The five subtopics are: 
{self.five_subtopic_string}

After presenting concluding statements for the five subtopics above, please also deliver a concise and powerful overall conclusion.
'''
        self.agentB_send_and_response(message, "B subtopic conclusion")

        print("**** Now input the B's final conclusion ****", flush=True)
        self.B_conclusion = input("B conslusion")
        self.conversation_log += "overall conclusion:\n" + message + "\n\n"
    
    def split_conclusion(self, five_conclusion):
    
        # Split the input_string into a list using regular expression
        pattern = r'\d+\.'
        result = re.split(pattern, five_conclusion)
        # Remove any empty strings or leading/trailing spaces
        result = [item.strip() for item in result if item.strip()]
        return result

    def split_subtopic_and_content(self, conclusion_list):
        subtopic_list = []
        description_list = []
        for conclusion in conclusion_list:
            split_result = conclusion.split(":", 1)

        # split_result will be a list with two elements, where [0] is text before colon and [1] is text after colon
            subtopic = split_result[0].strip()
            description = split_result[1].strip().lstrip("•").lstrip()
            subtopic_list.append(subtopic)
            description_list.append(description)

        return subtopic_list, description_list

    def create_conclusion_csv(self):
        A_conclusion_list = self.split_conclusion(self.agentA["A subtopic conclusion"])
        B_conclusion_list = self.split_conclusion(self.agentB["B subtopic conclusion"])

        subtopic_list, A_description_list =self.split_subtopic_and_content(A_conclusion_list)
        _, B_description_list =self.split_subtopic_and_content(B_conclusion_list)

        self.output_dataframe["topic"] = subtopic_list
        self.output_dataframe["Agent-A"] = A_description_list
        self.output_dataframe["Agent-B"] = B_description_list

        self.output_dataframe.loc[len(self.output_dataframe)] = ["conclusion", self.A_conclusion, self.B_conclusion]

        self.output_dataframe.to_csv(f"{self.topic_name}.csv", index=False)

    
    
    
        



bh = BonusHelper()
bh.run()
print("Agent A:", bh.agentA)
print("Agent B:", bh.agentB)
    
