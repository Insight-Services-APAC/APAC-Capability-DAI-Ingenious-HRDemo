from typing import List
from ingenious.models.agent import Agent, AgentChat, AgentChats, Agents, IProjectAgents
from pydantic import BaseModel
from ingenious.models.config import Config


class ProjectAgents(IProjectAgents):
    def Get_Project_Agents(self, config: Config) -> Agents:        
        local_agents = []
        local_agents.append(
            Agent(
                agent_name="criteria_formatting_agent",
                agent_model_name="gpt-4o",
                agent_display_name="criteria_formatting_agent",
                agent_description="A sample agent for hr.",
                agent_type="formatter",
                model=None,
                system_prompt=None,
                log_to_prompt_tuner=True,
                return_in_response=False
            )
        )
        local_agents.append(
            Agent(
                agent_name="payload_formatting_agent",
                agent_model_name="gpt-4o",
                agent_display_name="payload_formatting_agent",
                agent_description="A sample agent for hr.",
                agent_type="formatter",
                model=None,
                system_prompt=None,
                log_to_prompt_tuner=True,
                return_in_response=False
            )
        )
        local_agents.append(
            Agent(
                agent_name="applicant_lookup_agent",
                agent_model_name="gpt-4o",
                agent_display_name="applicant_lookup_agent",
                agent_description="A sample agent for hr.",
                agent_type="researcher",
                model=None,
                system_prompt=None,
                log_to_prompt_tuner=True,
                return_in_response=False
            )
        )
        local_agents.append(
            Agent(
                agent_name="applicant_lookup_experience_score",
                agent_model_name="gpt-4o",
                agent_display_name="applicant_lookup_experience_score",
                agent_description="A sample agent for hr.",
                agent_type="researcher",
                model=None,
                system_prompt=None,
                log_to_prompt_tuner=True,
                return_in_response=False
            )
        )
        local_agents.append(
            Agent(
                agent_name="applicant_lookup_skill_score",
                agent_model_name="gpt-4o",
                agent_display_name="applicant_lookup_skill_score",
                agent_description="A sample agent for hr.",
                agent_type="researcher",
                model=None,
                system_prompt=None,
                log_to_prompt_tuner=True,
                return_in_response=False
            )
        )
        local_agents.append(
            Agent(
                agent_name="summary",
                agent_model_name="gpt-4o",
                agent_display_name="Summarizer",
                agent_description="A sample agent.",
                agent_type="summary",
                model=None,
                system_prompt=None,
                log_to_prompt_tuner=True,
                return_in_response=True
            )
        )
        local_agents.append(
            Agent(
                agent_name="user_proxy_1",
                agent_model_name="gpt-4o",
                agent_display_name="user_proxy_1_agent",
                agent_description="A sample agent.",
                agent_type="user_proxy",
                model=None,
                system_prompt=None,
                log_to_prompt_tuner=False,
                return_in_response=False
            )
        ) 
        local_agents.append(
            Agent(
                agent_name="user_proxy_2",
                agent_model_name="gpt-4o",
                agent_display_name="user_proxy_2_agent",
                agent_description="A sample agent.",
                agent_type="user_proxy",
                model=None,
                system_prompt=None,
                log_to_prompt_tuner=False,
                return_in_response=False
            )
        )        

        return Agents(agents=local_agents, config=config)
