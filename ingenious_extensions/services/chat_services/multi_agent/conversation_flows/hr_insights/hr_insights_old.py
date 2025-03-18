import asyncio
from dataclasses import dataclass
import json
import os
from pathlib import Path
import random
import threading
import time
import re
from typing import Annotated, List
from autogen_core import (
    CancellationToken,
    AgentId,
    ClosureAgent,
    ClosureContext,
    DefaultSubscription,
    DefaultTopicId,
    MessageContext,
    RoutedAgent,
    SingleThreadedAgentRuntime,
    TopicId,
    TypeSubscription,
    default_subscription,
    message_handler,
    type_subscription,
    TRACE_LOGGER_NAME,
    EVENT_LOGGER_NAME,
)
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core.tools import FunctionTool

from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage, ChatMessage
from autogen_agentchat.base import Response
from jinja2 import Environment, FileSystemLoader
import jsonpickle
from ingenious.models.ag_agents import RelayAgent, RoutedAssistantAgent, RoutedResponseOutputAgent
from ingenious.utils.namespace_utils import get_path_from_namespace_with_fallback
from ingenious.services.chat_services.multi_agent.service import IConversationFlow
from ingenious.models.chat import ChatRequest, ChatResponse
from ingenious.models.agent import (
    AgentChat,
    Agent,
    AgentMessage,
    LLMUsageTracker,
    AgentChats,
)
import logging
from ingenious.models.message import Message as ChatHistoryMessage
# Custom class import from ingenious_extensions
from ingenious_extensions.models.agent import ProjectAgents
from ingenious_extensions.models.applicant import RootModel


def inject_criteria (template, key,injectValue):
    if not template:
        return template

    pattern = r'\$\$\$\s*' + re.escape(key) + r'\s*\$\$\$' 
    text = re.sub(pattern, injectValue, template,0, flags=re.IGNORECASE)
    return text

class ConversationFlow(IConversationFlow):
    async def get_conversation_response(
        self,
        chat_request: ChatRequest, # This needs to be an object that implements the IChatRequest model so you can extend this by creating a new model in the models folder
    ) -> ChatResponse:
        
        message = json.loads(chat_request.user_prompt)
        # event_type = chat_request.event_type
        # print(message)
        
        #  Get your agents and agent chats from your custom class in models folder
        project_agents = ProjectAgents()
        agents = project_agents.Get_Project_Agents(self._config)

        # Process your data payload using your custom data model class 
        # bike_sales_data = RootModel.model_validate(message)
        applicant_data = RootModel.model_validate(message)

        # Get the revision id and identifier from the message payload
        revision_id = message["revision_id"]
        identifier = message["identifier"]

        # Instantiate the logger and handler
        logger = logging.getLogger(EVENT_LOGGER_NAME)
        logger.setLevel(logging.INFO)

        llm_logger = LLMUsageTracker(
            agents=agents,
            config=self._config,
            chat_history_repository=self._chat_service.chat_history_repository,
            revision_id=revision_id,
            identifier=identifier,
            event_type="default"
        )

        logger.handlers = [llm_logger]

        # Note you can access llm models from the configuration array
        llm_config = self.Get_Models()[0]
        # Note the base IConversationFlow gives you a logger for logging purposes
        self._logger.debug("Starting Flow")

        # Load criteria content
        template_name = "applicant_criteria.jinja"
        criteria = await self.Get_Template(
                file_name=template_name, revision_id=revision_id
            )

        # Now add your system prompts to your agents from the prompt templates
        # Modify this if you want to modify the pattern used to correlate the agent name to the prompt template
        for agent in agents.get_agents():
            template_name = f"{agent.agent_name}_prompt.jinja"
            prompt = await self.Get_Template(
                file_name=template_name, revision_id=revision_id
            )
            agent.system_prompt = inject_criteria(prompt, "Criteria", criteria)    
            #agent.system_prompt = prompt.replace("$$$Criteria$$$", criteria)

        # Now construct your autogen conversation pattern the way you want
        # In this sample I'll first define my topic agents
        runtime = SingleThreadedAgentRuntime()

        async def register_research_agent(agent_name: str, tools: List[FunctionTool] = [], next_agent_topic: str = "user_proxy"):
            agent = agents.get_agent_by_name(agent_name=agent_name)
            reg_agent = await RoutedAssistantAgent.register(
                runtime=runtime,
                type=agent.agent_name,
                factory=lambda: RoutedAssistantAgent(agent=agent, data_identifier=identifier, next_agent_topic=next_agent_topic, tools=tools)
            )
            await runtime.add_subscription(
                TypeSubscription(topic_type=agent_name, agent_type=reg_agent.type)
            )

        await register_research_agent(agent_name="applicant_lookup_agent", next_agent_topic="user_proxy")
        await register_research_agent(agent_name="applicant_lookup_experience_score", next_agent_topic="user_proxy")
        await register_research_agent(agent_name="applicant_lookup_skill_score", next_agent_topic="user_proxy")
        # await register_research_agent(agent_name="fiscal_analysis_agent", next_agent_topic="user_proxy")
        # await register_research_agent(agent_name="bike_lookup_agent", tools=[bike_price_tool], next_agent_topic=None)

        user_proxy = await RelayAgent.register(
            runtime,
            "researcher",
            lambda: RelayAgent(
                agents.get_agent_by_name("user_proxy"),
                data_identifier=identifier,
                next_agent_topic="summary",
                number_of_messages_before_next_agent=3
            ),
        )
        await runtime.add_subscription(
                TypeSubscription(topic_type="user_proxy", agent_type=user_proxy.type)
            )

        # Optionally inject the chat history into the conversation flow so that you can avoid duplicate responses
        hist_itr = await self._chat_service.chat_history_repository.get_thread_messages(
            thread_id=chat_request.thread_id)

        hist_join = ['']
        for h in hist_itr:
            if h.role == "output":
                hist_join.append(h.content)                
        hist_str = '# Chat History \n\n' + '``` json\n\n " ' + json.dumps(hist_join)
        
        async def register_output_agent(agent_name: str, next_agent_topic: str = None):
            agent = agents.get_agent_by_name(agent_name=agent_name)
            summary = await RoutedResponseOutputAgent.register(
                runtime,
                agent.agent_name,
                lambda: RoutedResponseOutputAgent(
                    agent=agent,
                    data_identifier=identifier,
                    next_agent_topic=next_agent_topic,
                    additional_data=hist_str
                ),
            )
            await runtime.add_subscription(
                TypeSubscription(topic_type=agent_name, agent_type=summary.type)
            )

        await register_output_agent(agent_name="summary", next_agent_topic=None)

        results = []
        tasks = []

        runtime.start()

        initial_message: AgentMessage = AgentMessage(content=json.dumps(message))
        initial_message.content = "```json\n" + initial_message.content + "\n```"
        hr_agent_message: AgentMessage = AgentMessage(content=chat_request.user_prompt)
        await asyncio.gather(
            runtime.publish_message(
                initial_message,
                topic_id=TopicId(type="applicant_lookup_agent", source="default"),
            ),
            runtime.publish_message(
                initial_message,
                topic_id=TopicId(type="applicant_lookup_experience_score", source="default"),
            ),
            runtime.publish_message(
                initial_message,
                topic_id=TopicId(type="applicant_lookup_skill_score", source="default"),
            )
        )
        
        await runtime.stop_when_idle()

        # If you want to use the prompt tuner you need to write the responses to a file with the method provided in the logger
        await llm_logger.write_llm_responses_to_file(file_prefixes=[str(chat_request.user_id)])

        # Lastly return your chat response object
        chat_response = ChatResponse(
            thread_id=chat_request.thread_id,
            message_id=identifier,
            agent_response=jsonpickle.encode(unpicklable=False, value=llm_logger._queue),
            token_count=llm_logger.prompt_tokens,
            max_token_count=0,
            memory_summary=""
        )

        # summary_response: AgentChat = next(l for l in llm_logger._queue if l.chat_name == "summary")

        # message: ChatHistoryMessage = ChatHistoryMessage(
        #     user_id=chat_request.user_id,
        #     thread_id=chat_request.thread_id,
        #     message_id=identifier,
        #     role="output",
        #     # Get the item from the queue where chat_name = "summary"
        #     content=summary_response.chat_response.chat_message.content,
        #     content_filter_results=None,
        #     tool_calls=None,
        #     tool_call_id=None,
        #     tool_call_function=None
        # )

        # _ = await self._chat_service.chat_history_repository.add_message(message=message)

        return chat_response
