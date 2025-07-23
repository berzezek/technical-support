from typing import List, Optional, Union, Dict
from pydantic import BaseModel


class ProcessDefinitionItemsField(BaseModel):
    """
    Fields for process definition items.
    """

    key: int
    name: str
    version: int
    bpmnProcessId: str
    tenantId: Optional[str] = None


class ProcessDefinitionItemSchema(BaseModel):
    """
    Schema for process definition search results.
    """

    items: List[ProcessDefinitionItemsField]
    sortValues: List[Union[str, int]]
    total: int


class ProcessDefinitionFilterFields(BaseModel):
    """
    Filter fields for search.
    """

    key: Optional[int] = None
    name: Optional[str] = None
    state: Optional[str] = None
    versionTag: Optional[str] = None
    bpmnProcessId: Optional[str] = None
    tenantId: Optional[str] = None


class ProcessDefinitionSearchFilterSchema(BaseModel):
    """
    Full schema for search query.
    """

    filter: Optional[ProcessDefinitionFilterFields] = None
    size: Optional[int] = None
    searchAfter: Optional[List[Dict[str, str]]] = None
    sort: Optional[List[Dict[str, str]]] = None


class ProcessInstanceFilterFields(BaseModel):
    """
    Filter fields for process instance search.
    """

    key: Optional[int] = None
    processVersion: Optional[int] = None
    processVersionTag: Optional[str] = None
    bpmnProcessId: Optional[str] = None
    parentKey: Optional[int] = None
    parentFlowNodeInstanceKey: Optional[int] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    state: Optional[str] = None
    incident: Optional[bool] = None
    processDefinitionKey: Optional[int] = None
    tenantId: Optional[str] = None


class ProcessInstanceSearchFilterSchema(BaseModel):
    """
    Full schema for process instance search query.
    """

    filter: Optional[ProcessInstanceFilterFields] = None
    size: Optional[int] = None
    searchAfter: Optional[List[Union[str, int]]] = None  # 🛠 исправлено
    sort: Optional[List[Dict[str, Union[str, int]]]] = None  # можно оставить так


class ProcessInstanceItemsField(BaseModel):
    key: int
    processVersion: int
    processVersionTag: Optional[str] = None
    bpmnProcessId: str
    parentKey: Optional[int] = None
    parentFlowNodeInstanceKey: Optional[int] = None
    startDate: str
    endDate: Optional[str] = None
    state: str
    incident: bool
    processDefinitionKey: int
    tenantId: Optional[str] = None


class ProcessInstanceSearchResponseSchema(BaseModel):
    items: List[ProcessInstanceItemsField]
    sortValues: List[Union[str, int]]
    total: int
