from __future__ import annotations
from abc import ABC, abstractmethod


class PromptBuilder(ABC):
    @abstractmethod
    def build_prompt(self, **kargs) -> dict:
        pass


class SystemPromptBuilder(PromptBuilder) :
    def build_prompt(self, **kargs) -> dict:
        """
            Generates a structured prompt with components.

            Args: A dictionary with the following keys-
                role (str): A valid role system/user.
                context (str): Background information or additional details to aid in the task.
                input_data (str): The specific input data for the task.

            Returns:
                dict: A dictionary containing the structured prompt components.
            """
        role=kargs.get('role', None)
        context=kargs.get("context", None)
        input_data=kargs.get("input_data", None)

        print("Running System Prompt builder.")
        
        prompt = {}

        for _key in kargs:
            value = kargs.get(_key, None)
            if value is not None:
                prompt.update({_key:value})

        return prompt 


class UserPromptBuilder(PromptBuilder):
    def build_prompt(self, **kargs) -> dict:
        """

            Generates a structured prompt with components.

            Args: A dictionary with the following keys-
                role (str): A valid role system/user.
                context (str): Background information or additional details to aid in the task.
                input_data (str): The specific input data for the task.

            Returns:
                dict: A dictionary containing the structured prompt components.
            """
        role=kargs.get('role', None)
        context=kargs.get("context", None)
        input_data=kargs.get("input_data", None)

        print("Running User Prompt builder.")
        
        prompt = {}

        for _key in kargs:
            value = kargs.get(_key, None)
            if value is not None:
                prompt.update({_key:value})

        return prompt 


class PromptFactory(ABC):
    @abstractmethod
    def create_prompt_builder(self) -> PromptBuilder:
        pass

class SystemPrompt(PromptFactory):
    def create_prompt_builder(self) -> PromptBuilder:
        return SystemPromptBuilder()

class UserPrompt(PromptFactory):
    def create_prompt_builder(self) -> PromptBuilder:
        return UserPromptBuilder()



if __name__ == "__main__":
    spf = SystemPrompt()
    print(spf.create_prompt_builder().build_prompt())

    upf = UserPrompt()
    print(upf.create_prompt_builder().build_prompt())