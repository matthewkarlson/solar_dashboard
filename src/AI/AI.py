import autogen
import tempfile
import autogen.coding
import pandas as pd
from openai import OpenAI
import concurrent.futures
import AI.prompts as prompts

class AI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.temp_dir = tempfile.TemporaryDirectory()
        self.llm_config = {
            "model": "gpt-4o",
            "api_key": self.api_key
        }
        self.openAIClient = OpenAI(
            api_key=self.llm_config['api_key']
        )
    
    def initialise_context(self, contextData):
        dataframe_metadata = ""
        for data in contextData:
            df = pd.read_csv(data.path)
            dataframe_metadata = dataframe_metadata + prompts.DATAFRAME_METADATA_PROMPT.format(
                description=data.description,
                path = data.path,
                sample = df.sample(5).to_markdown()
            )
        
        self.coder = autogen.AssistantAgent(
            "code_writer_agent",
                system_message= prompts.CODE_WRITER_SYSTEM_MESSAGE.format(dataframe_metadata=dataframe_metadata),
                llm_config=self.llm_config,
        )
        self.executor = autogen.UserProxyAgent(
            name = "Code_Executor",
            system_message= "Executor, execute the code written by the Coder and report the result.",
            human_input_mode= "NEVER",

            code_execution_config={
                "executor": autogen.coding.DockerCommandLineCodeExecutor(
    image="agent-runner",  # Execute code using the given docker image name.
    timeout=10,  # Timeout for each code execution in seconds.
    work_dir=self.temp_dir.name,  # Use the temporary directory to store the code files.
)
            },
        )

        self.initializer = autogen.UserProxyAgent(
            name="Initializer",
            system_message="Initializer, initialize the context with the data provided.",
            llm_config=False,
        )

    def _state_transition(self,last_speaker, groupchat):
        messages = groupchat.messages

        if last_speaker is self.initializer:
            return self.coder
        elif last_speaker is self.coder:
            return self.executor
        elif last_speaker is self.executor:
            if messages[-1]["content"] == "exitcode: 1":
                return self.coder
            else:
                return None
    
    def answer_question(self, question):
        groupchat = autogen.GroupChat(
            agents=[self.initializer, self.coder, self.executor],
            messages=[],
            max_round=10,
            speaker_selection_method=self._state_transition,
        )
        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=self.llm_config)
        output = self.initializer.initiate_chat(
            manager,
            message = question
        )
        return output
    
    def answer_questions(self, questions):
        answers = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_question = {executor.submit(self.answer_question, question): question for question in questions}
            for future in concurrent.futures.as_completed(future_to_question):
                question = future_to_question[future]
                try:
                    answer = future.result()
                except Exception as exc:
                    answer=(f"Question {question} generated an exception: {exc}")
                answers.append(answer)
        return answers

    def create_summary(self, questions):
        answers = self.answer_questions(questions)
        prompt = prompts.SUMMARY_PROMPT_TEMPLATE.format(
            questions_and_answers = "\n".join([f"Q: {q}\nA: {a}" for q,a in zip(questions, answers)]),
            length_of_summary = "detailed and comprehensive, not excessive but enough to provide a clear and concise summary"
        )

        chat_completion = self.openAIClient.chat.completions.create(
            model = self.llm_config['model'],
            messages = [{"role": "user", "content":prompt}]
        )

        return chat_completion