
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

    pattern = r'{{\s*' + re.escape(key) + r'\s*}}'
    template = re.sub(pattern, injectValue, template, flags=re.IGNORECASE)

    return template


fileName = "./ingenious_extensions/templates/prompts/applicant_criteria.jinja"
with open(f'{fileName}', 'r') as file:
    criteria = file.read()

fileName = "./ingenious_extensions/templates/prompts/applicant_lookup_agent_prompt.jinja"
with open(f'{fileName}', 'r') as file:
    system_prompt = file.read()

system_prompt = inject_criteria(system_prompt, "Criteria", criteria)

print(system_prompt)